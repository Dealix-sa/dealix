"""Approvals must survive a restart, and both backends must stay in step.

The approval queue was process-memory only. ``get_default_approval_store``
unconditionally built the in-memory store, so every deploy or restart discarded
pending approvals — a founder who approved a batch before a deploy would find an
empty queue afterwards with no way to tell whether the work went out. A durable
``PostgresApprovalStore`` existed but had no caller.

It also could not simply be switched on. It implemented a subset of the
in-memory contract, and production code calls the missing parts:
``bulk_approve`` (api/routers/approval_center.py), ``expire_overdue`` and
``clear``. Swapping the backend without porting them would have raised
AttributeError at runtime, in the approval path, in production.

So the first test here is the parity test. It is the one that would have caught
that, and it keeps catching it as either store grows.
"""

from __future__ import annotations

import inspect
from datetime import UTC, datetime, timedelta

import pytest

from auto_client_acquisition.approval_center.approval_store import (
    ApprovalStore,
    describe_default_backend,
    get_default_approval_store,
    reset_default_approval_store,
    resolve_backend_name,
)
from auto_client_acquisition.approval_center.postgres_store import PostgresApprovalStore
from auto_client_acquisition.approval_center.schemas import ApprovalRequest


def _public_methods(cls: type) -> set[str]:
    return {
        name
        for name, member in inspect.getmembers(cls, callable)
        if not name.startswith("_") and getattr(member, "__qualname__", "").startswith(cls.__name__)
    }


def _request(approval_id: str, **overrides) -> ApprovalRequest:
    payload = {
        "approval_id": approval_id,
        "object_type": "outreach_draft",
        "object_id": "obj_sample",
        "action_type": "send_email",
        "action_mode": "approval_required",
        "summary_en": "Draft to a sample company",
        "summary_ar": "مسودة إلى شركة نموذجية",
        "proof_impact": "leadops:sample",
    }
    payload.update(overrides)
    return ApprovalRequest(**payload)


@pytest.fixture
def pg_store(tmp_path):
    """A Postgres-shaped store backed by a real file, so it survives reopening."""
    return PostgresApprovalStore(database_url=f"sqlite:///{tmp_path/'approvals.db'}")


# ── Parity: the bug that made the cutover unsafe ────────────────────────────


def test_both_backends_expose_the_same_public_contract():
    """Neither store may drift ahead of the other.

    Callers resolve the backend at runtime, so any method on one and not the
    other is an AttributeError waiting for a config change to trigger it.
    """
    memory_only = _public_methods(ApprovalStore) - _public_methods(PostgresApprovalStore)
    postgres_only = _public_methods(PostgresApprovalStore) - _public_methods(ApprovalStore)

    assert not memory_only, f"PostgresApprovalStore is missing: {sorted(memory_only)}"
    assert not postgres_only, f"ApprovalStore is missing: {sorted(postgres_only)}"


@pytest.mark.parametrize(
    "method", ["bulk_approve", "expire_overdue", "clear", "create_with_founder_rules"]
)
def test_methods_used_in_production_exist_on_postgres_store(method):
    """These four are called from api/routers and were absent before."""
    assert hasattr(PostgresApprovalStore, method)


# ── Durability: the actual point ────────────────────────────────────────────


def test_pending_approvals_survive_a_store_restart(tmp_path):
    """Reopening against the same database must show the same queue."""
    db = f"sqlite:///{tmp_path/'approvals.db'}"

    first = PostgresApprovalStore(database_url=db)
    first.create(_request("apr_survives_1"))
    first.create(_request("apr_survives_2"))
    assert len(first.list_pending()) == 2

    # A new instance against the same file is what a redeploy looks like.
    second = PostgresApprovalStore(database_url=db)

    assert {r.approval_id for r in second.list_pending()} == {
        "apr_survives_1",
        "apr_survives_2",
    }


def test_approval_decision_survives_a_restart(tmp_path):
    db = f"sqlite:///{tmp_path/'approvals.db'}"

    first = PostgresApprovalStore(database_url=db)
    first.create(_request("apr_decided"))
    first.approve("apr_decided", who="founder")

    second = PostgresApprovalStore(database_url=db)
    restored = second.get("apr_decided")

    assert restored is not None
    assert restored.status == "approved"
    assert any(e["action"] == "approve" for e in restored.edit_history)


def test_in_memory_store_loses_everything_on_restart():
    """Pins why this work was needed, so nobody 'simplifies' back to it."""
    first = ApprovalStore()
    first.create(_request("apr_lost"))
    assert len(first.list_pending()) == 1

    assert ApprovalStore().list_pending() == []


# ── Ported behaviour matches the reference implementation ───────────────────


def test_bulk_approve_by_prefix_matches_memory_semantics(pg_store):
    pg_store.create(_request("apr_a", proof_impact="leadops:one"))
    pg_store.create(_request("apr_b", proof_impact="leadops:two"))
    pg_store.create(_request("apr_c", proof_impact="other:three"))

    result = pg_store.bulk_approve(who="founder", proof_impact_prefix="leadops:")

    assert sorted(result["approved"]) == ["apr_a", "apr_b"]
    assert pg_store.get("apr_c").status == "pending"


def test_bulk_approve_refuses_without_a_selector(pg_store):
    """Approving everything by default is the wrong default for this queue."""
    pg_store.create(_request("apr_unselected"))

    result = pg_store.bulk_approve(who="founder")

    assert result["approved"] == []
    assert "required" in result["reason"]
    assert pg_store.get("apr_unselected").status == "pending"


def test_bulk_approve_persists_across_restart(tmp_path):
    db = f"sqlite:///{tmp_path/'approvals.db'}"
    first = PostgresApprovalStore(database_url=db)
    first.create(_request("apr_bulk", proof_impact="leadops:x"))
    first.bulk_approve(who="founder", proof_impact_prefix="leadops:")

    assert PostgresApprovalStore(database_url=db).get("apr_bulk").status == "approved"


def test_expire_overdue_flips_only_past_expiry(pg_store):
    past = datetime.now(UTC) - timedelta(hours=1)
    future = datetime.now(UTC) + timedelta(hours=1)
    pg_store.create(_request("apr_old", expires_at=past))
    pg_store.create(_request("apr_fresh", expires_at=future))

    assert pg_store.expire_overdue() == 1
    assert pg_store.get("apr_old").status == "expired"
    assert pg_store.get("apr_fresh").status == "pending"


def test_clear_empties_the_store(pg_store):
    pg_store.create(_request("apr_clear"))

    pg_store.clear()

    assert pg_store.list_pending() == []


# ── Backend selection ───────────────────────────────────────────────────────


def test_backend_defaults_to_memory_without_a_database(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("APPROVAL_STORE_BACKEND", raising=False)

    assert resolve_backend_name() == "in_memory"


def test_backend_prefers_postgres_when_a_database_is_configured(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://user@host/db")
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("APPROVAL_STORE_BACKEND", raising=False)

    assert resolve_backend_name() == "postgres"


def test_test_environment_stays_in_memory_even_with_a_database(monkeypatch):
    """Otherwise the shared sqlite file leaks approvals between tests."""
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./shared.db")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.delenv("APPROVAL_STORE_BACKEND", raising=False)

    assert resolve_backend_name() == "in_memory"


def test_explicit_postgres_overrides_the_test_environment_default(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./shared.db")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("APPROVAL_STORE_BACKEND", "postgres")

    assert resolve_backend_name() == "postgres"


def test_explicit_memory_setting_overrides_a_configured_database(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://user@host/db")
    monkeypatch.setenv("APPROVAL_STORE_BACKEND", "memory")

    assert resolve_backend_name() == "in_memory"


def test_default_store_uses_durable_backend_for_a_real_database(monkeypatch, tmp_path):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path/'live.db'}")
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("APPROVAL_STORE_BACKEND", raising=False)
    reset_default_approval_store()
    try:
        assert describe_default_backend() == "postgres"
    finally:
        reset_default_approval_store()


def test_default_store_falls_back_to_memory_when_postgres_is_unreachable(monkeypatch):
    """Availability over durability — but the degradation must be reported."""
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg2://nobody@127.0.0.1:1/none")
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("APPROVAL_STORE_BACKEND", raising=False)
    reset_default_approval_store()

    def explode(*_args, **_kwargs):
        raise RuntimeError("database unreachable")

    monkeypatch.setattr(
        "auto_client_acquisition.approval_center.postgres_store.PostgresApprovalStore.__init__",
        explode,
    )
    try:
        assert describe_default_backend() == "in_memory"
        assert isinstance(get_default_approval_store(), ApprovalStore)
    finally:
        reset_default_approval_store()


def test_async_database_urls_are_converted_to_a_sync_driver():
    """The app runs asyncpg/aiosqlite; this store is synchronous."""
    from auto_client_acquisition.approval_center.approval_store import _sync_database_url

    assert _sync_database_url("postgresql+asyncpg://u@h/d") == "postgresql+psycopg://u@h/d"
    assert _sync_database_url("sqlite+aiosqlite:///./x.db") == "sqlite:///./x.db"


@pytest.mark.parametrize(
    "raw",
    [
        "postgresql+asyncpg://u:p@h:5432/d",
        "postgresql://u:p@h:5432/d",
        "postgres://u:p@h:5432/d",
        "postgresql+psycopg://u:p@h:5432/d",
    ],
)
def test_converted_url_actually_builds_an_engine(raw):
    """The test that was missing, and the reason the first fix did nothing.

    Asserting the converted *string* looks right proves nothing: the original
    implementation emitted ``postgresql+psycopg2://`` while this repository
    installs psycopg 3 (``psycopg[binary]`` in requirements.txt). create_engine
    raised ModuleNotFoundError, the broad except in get_default_approval_store
    swallowed it, and the store silently returned to memory — so the durability
    fix was inert in production while every string assertion passed.

    This builds a real engine with the drivers actually installed. It does not
    connect, so no database is required.
    """
    from sqlalchemy import create_engine

    from auto_client_acquisition.approval_center.approval_store import _sync_database_url

    engine = create_engine(_sync_database_url(raw), future=True)

    assert engine.dialect.driver == "psycopg", (
        f"{raw} resolved to driver {engine.dialect.driver!r}; this repo installs "
        "psycopg 3 only, so anything else fails at create_engine time."
    )


def test_psycopg2_is_not_installed_so_must_never_be_emitted():
    """Pins the fact that made the original conversion wrong."""
    import importlib.util

    from auto_client_acquisition.approval_center.approval_store import (
        SYNC_POSTGRES_DRIVER,
        _sync_database_url,
    )

    assert importlib.util.find_spec("psycopg2") is None, (
        "psycopg2 is now installed — re-evaluate SYNC_POSTGRES_DRIVER."
    )
    assert SYNC_POSTGRES_DRIVER == "postgresql+psycopg"
    assert "psycopg2" not in _sync_database_url("postgresql+asyncpg://u@h/d")


def test_production_with_a_real_database_url_selects_the_durable_backend(
    monkeypatch, tmp_path
):
    """End-to-end: the factory must not quietly land on memory.

    This is the assertion the earlier work lacked — it checked which backend was
    *intended*, never which one was *constructed*.
    """
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path/'prod.db'}")
    monkeypatch.delenv("APPROVAL_STORE_BACKEND", raising=False)
    reset_default_approval_store()
    try:
        store = get_default_approval_store()
        assert type(store).__name__ == "PostgresApprovalStore", (
            "factory fell back to memory — approvals would not survive restart"
        )
    finally:
        reset_default_approval_store()
