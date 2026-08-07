"""RLS stays inactive until PostgreSQL tenant binding is proven."""

from __future__ import annotations

import ast
import inspect
import os
from contextlib import asynccontextmanager
from pathlib import Path

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.sql.elements import TextClause

from db.rls_policies import RLS_POLICIES
from db.tenant_session import (
    TENANT_SETTING,
    UnsafeTenantIdentifier,
    assert_safe_tenant_id,
    bind_tenant,
    current_bound_tenant,
    tenant_session,
)

POSTGRES_URL = os.getenv("TEST_POSTGRES_URL", "")
requires_postgres = pytest.mark.skipif(
    not POSTGRES_URL,
    reason="TEST_POSTGRES_URL is required for PostgreSQL SET LOCAL semantics",
)


@pytest.mark.parametrize(
    "tenant_id",
    ["acme", "acme_real_estate", "tenant-123", "acme--beta", "A" * 64],
)
def test_accepts_canonical_tenant_identifiers(tenant_id):
    assert assert_safe_tenant_id(tenant_id) == tenant_id


@pytest.mark.parametrize(
    "tenant_id",
    [
        "acme'; SET app.tenant_id = 'other",
        "acme' OR '1'='1",
        "acme; DROP TABLE leads",
        "",
        "A" * 65,
        "acme space",
        "tenant\nid",
        "acme\\",
    ],
)
def test_rejects_noncanonical_tenant_identifiers(tenant_id):
    with pytest.raises(UnsafeTenantIdentifier):
        assert_safe_tenant_id(tenant_id)


@pytest.mark.parametrize("tenant_id", [None, 123, ["acme"], {"tenant": "acme"}])
def test_rejects_non_string_tenant_identifiers(tenant_id):
    with pytest.raises(UnsafeTenantIdentifier):
        assert_safe_tenant_id(tenant_id)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_rejected_id_never_touches_the_database():
    class _ExplodingSession:
        async def execute(self, *_args, **_kwargs):
            raise AssertionError("unsafe tenant identifier reached the database")

    with pytest.raises(UnsafeTenantIdentifier):
        await bind_tenant(
            _ExplodingSession(),  # type: ignore[arg-type]
            "acme'; DROP TABLE leads",
        )


@pytest.mark.asyncio
async def test_binding_uses_parameters_not_sql_interpolation():
    class _CaptureSession:
        statement = ""
        params: dict[str, str] = {}

        async def execute(self, statement, params):
            self.statement = str(statement)
            self.params = params

    session = _CaptureSession()
    await bind_tenant(session, "tenant-123")  # type: ignore[arg-type]

    assert "tenant-123" not in session.statement
    assert session.params == {
        "setting": TENANT_SETTING,
        "tenant_id": "tenant-123",
    }
    assert "set_config" in session.statement


def test_every_declared_rls_policy_reads_the_canonical_setting():
    assert len(RLS_POLICIES) >= 30
    assert all(TENANT_SETTING in expression for expression in RLS_POLICIES.values())


def test_application_runtime_does_not_apply_rls():
    """Activating RLS remains a separate reviewed migration and release gate."""
    repo = Path(__file__).resolve().parents[1]
    callers: list[str] = []
    paths = list((repo / "api").rglob("*.py")) + [repo / "db" / "session.py"]
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            called = getattr(node.func, "id", getattr(node.func, "attr", None))
            if called == "apply_rls":
                callers.append(path.relative_to(repo).as_posix())

    assert callers == []


def test_tenant_session_is_a_fastapi_yield_dependency():
    """FastAPI only enters undecorated async-generator dependencies."""
    assert inspect.isasyncgenfunction(tenant_session)


@pytest.mark.asyncio
async def test_rls_admin_helpers_use_sqlalchemy_executable_clauses(monkeypatch):
    """SQLAlchemy 2 refuses raw SQL strings before they reach PostgreSQL."""
    from db import rls_policies

    statements: list[TextClause] = []

    class _Result:
        @staticmethod
        def scalar_one_or_none():
            return True

    class _Session:
        async def execute(self, statement, params=None):
            statements.append(statement)
            return _Result()

    @asynccontextmanager
    async def _session():
        yield _Session()

    monkeypatch.setattr(rls_policies, "get_session", _session)
    monkeypatch.setattr(
        rls_policies,
        "RLS_POLICIES",
        {"leads": f"tenant_id = current_setting('{TENANT_SETTING}', true)"},
    )

    await rls_policies.apply_rls()
    await rls_policies.disable_rls("leads")
    status = await rls_policies.verify_rls()

    assert status["enabled"] == ["leads"]
    assert statements
    assert all(isinstance(statement, TextClause) for statement in statements)


@requires_postgres
@pytest.mark.asyncio
async def test_binding_sets_the_setting_read_by_rls():
    engine = create_async_engine(POSTGRES_URL)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            assert await current_bound_tenant(session) is None
            await bind_tenant(session, "acme")
            assert await current_bound_tenant(session) == "acme"
    finally:
        await engine.dispose()


@requires_postgres
@pytest.mark.asyncio
async def test_binding_does_not_survive_transaction_commit():
    engine = create_async_engine(POSTGRES_URL)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            await bind_tenant(session, "acme")
            await session.commit()
            assert await current_bound_tenant(session) is None
    finally:
        await engine.dispose()


@requires_postgres
@pytest.mark.asyncio
async def test_unset_tenant_makes_policy_predicate_match_nothing():
    engine = create_async_engine(POSTGRES_URL)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            result = await session.execute(
                text(
                    "SELECT "
                    "('acme' = current_setting(:setting, true)) IS NOT TRUE"
                ),
                {"setting": TENANT_SETTING},
            )
            assert result.scalar() is True
    finally:
        await engine.dispose()
