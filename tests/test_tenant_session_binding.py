"""RLS cannot be switched on until the tenant is bound to the session.

``db/rls_policies.py`` writes every policy as
``tenant_id = current_setting('app.tenant_id', true)``, and nothing in the
repository set that variable. Applying those policies in that state would not
have leaked data — it would have hidden all of it. ``current_setting(..., true)``
returns NULL when unset, ``tenant_id = NULL`` is never true, so every query
against leads, deals, contacts, invoices, users and proof events would return
zero rows. A silent, total outage.

These tests pin the prerequisite: the binding works, it is transaction-scoped so
a pooled connection cannot carry one tenant into another request, and a tenant
id that could break out of the ``SET LOCAL`` statement is refused rather than
escaped.

Postgres-specific behaviour is exercised against Postgres and skipped elsewhere;
the validation tests are engine-independent and always run.
"""

from __future__ import annotations

import os

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from db.tenant_session import (
    TENANT_SETTING,
    UnsafeTenantIdentifier,
    assert_safe_tenant_id,
    bind_tenant,
    current_bound_tenant,
)

pytestmark = pytest.mark.asyncio

POSTGRES_URL = os.getenv("TEST_POSTGRES_URL", "")
requires_postgres = pytest.mark.skipif(
    not POSTGRES_URL,
    reason="TEST_POSTGRES_URL not set — SET LOCAL/current_setting are Postgres-only",
)


# ── Validation: the security boundary ───────────────────────────────────────


@pytest.mark.parametrize(
    "tenant_id", ["acme", "acme_real_estate", "tenant-123", "acme--beta", "A" * 64]
)
async def test_accepts_ordinary_tenant_identifiers(tenant_id):
    """Hyphens are allowed, including a doubled one.

    ``--`` starts a comment in SQL but not inside a quoted literal, and the
    quote is the boundary the regex actually protects: only ``'`` can end the
    string early, and that is rejected below. Excluding hyphens instead would
    ban legitimate identifiers like ``tenant-123`` for no security gain.
    """
    assert assert_safe_tenant_id(tenant_id) == tenant_id


@pytest.mark.parametrize(
    "tenant_id",
    [
        "acme'; SET app.tenant_id = 'other",  # break out of the statement
        "acme' OR '1'='1",
        "acme; DROP TABLE leads",
        "",
        "A" * 65,
        "acme space",
        "tenant\nid",
        "acme\\",  # trailing backslash — escape-handling edge
    ],
)
async def test_rejects_identifiers_that_could_break_out_of_set_local(tenant_id):
    """Postgres takes no bind parameter in SET LOCAL, so validation is the guard.

    If any of these were interpolated instead of refused, a caller controlling
    the tenant id could rebind the session to another tenant — which, with RLS
    live, is a cross-tenant read.
    """
    with pytest.raises(UnsafeTenantIdentifier):
        assert_safe_tenant_id(tenant_id)


async def test_non_string_identifiers_are_refused():
    for value in (None, 123, ["acme"], {"tenant": "acme"}):
        with pytest.raises(UnsafeTenantIdentifier):
            assert_safe_tenant_id(value)  # type: ignore[arg-type]


async def test_bind_tenant_refuses_before_touching_the_session():
    """A rejected id must never reach the database at all."""

    class ExplodingSession:
        async def execute(self, *_args, **_kwargs):
            raise AssertionError("unsafe tenant id reached the database")

    with pytest.raises(UnsafeTenantIdentifier):
        await bind_tenant(ExplodingSession(), "acme'; DROP TABLE leads")  # type: ignore[arg-type]


# ── Behaviour against a real Postgres ───────────────────────────────────────


@requires_postgres
async def test_binding_sets_the_variable_rls_policies_read():
    engine = create_async_engine(POSTGRES_URL, future=True)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            assert await current_bound_tenant(session) is None

            await bind_tenant(session, "acme")

            assert await current_bound_tenant(session) == "acme"
    finally:
        await engine.dispose()


@requires_postgres
async def test_binding_does_not_survive_the_transaction():
    """SET LOCAL, not SET.

    With a connection pool, a plain SET would leave one tenant's identity on the
    connection for whoever checks it out next — the exact mechanism by which one
    company would read another's rows once RLS is live.
    """
    engine = create_async_engine(POSTGRES_URL, future=True)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            await bind_tenant(session, "acme")
            await session.commit()

            assert await current_bound_tenant(session) is None, (
                "tenant survived the transaction — a pooled connection would "
                "carry it into the next request"
            )
    finally:
        await engine.dispose()


@requires_postgres
async def test_unset_tenant_makes_an_rls_predicate_match_nothing():
    """Demonstrates why RLS must not ship before binding does.

    This is the failure mode in miniature: with no tenant bound, the predicate
    every policy uses evaluates to NULL, so it selects no rows.
    """
    engine = create_async_engine(POSTGRES_URL, future=True)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with factory() as session:
            result = await session.execute(
                text(
                    "SELECT ('acme' = current_setting(:setting, true)) IS NOT TRUE"
                ),
                {"setting": TENANT_SETTING},
            )
            assert result.scalar() is True, (
                "predicate matched with no tenant bound — the outage this "
                "guards against would not reproduce"
            )
    finally:
        await engine.dispose()
