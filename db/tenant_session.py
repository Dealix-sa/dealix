"""Bind a request's tenant to its database session.

``db/rls_policies.py`` defines row-level security for 30+ tables, and every
policy is written as::

    tenant_id = current_setting('app.tenant_id', true)

Nothing in the repository ever set that variable. That is not a partial
implementation — it is a loaded gun. In Postgres, ``current_setting(..., true)``
returns NULL when the setting is absent, and ``tenant_id = NULL`` is never true,
so applying those policies today would make **every query against those tables
return zero rows**. Not a leak: a total, silent outage across leads, deals,
contacts, invoices, users and proof events.

So session binding has to exist and be proven before RLS can be switched on.
This module is that prerequisite.

``SET LOCAL`` is deliberate. It scopes the setting to the current transaction,
so a pooled connection cannot carry one tenant's identity into the next
request's checkout — which, with RLS live, is exactly how one company would end
up reading another's rows.
"""

from __future__ import annotations

import re
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import async_session_factory

#: The GUC every RLS policy in db/rls_policies.py reads.
TENANT_SETTING = "app.tenant_id"

#: Tenant identifiers are interpolated into a SET LOCAL statement, because
#: Postgres does not accept a bind parameter there. That makes validation the
#: security boundary rather than a tidiness check: anything outside this
#: character set is refused instead of escaped.
_SAFE_TENANT_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


class UnsafeTenantIdentifier(ValueError):
    """Raised when a tenant id could not be safely bound to a session."""


def assert_safe_tenant_id(tenant_id: str) -> str:
    """Validate a tenant id for interpolation into ``SET LOCAL``."""
    if not isinstance(tenant_id, str) or not _SAFE_TENANT_ID.match(tenant_id):
        raise UnsafeTenantIdentifier(
            f"refusing to bind tenant id {tenant_id!r}: must match "
            f"{_SAFE_TENANT_ID.pattern}"
        )
    return tenant_id


async def bind_tenant(session: AsyncSession, tenant_id: str) -> None:
    """Scope ``session`` to ``tenant_id`` for the current transaction.

    Must be called before the first query on a session whose tables carry RLS,
    otherwise the policies evaluate against NULL and the session sees nothing.
    """
    safe = assert_safe_tenant_id(tenant_id)
    await session.execute(text(f"SET LOCAL {TENANT_SETTING} = '{safe}'"))


async def current_bound_tenant(session: AsyncSession) -> str | None:
    """Return the tenant currently bound, or ``None``. Intended for assertions."""
    result = await session.execute(
        text(f"SELECT current_setting('{TENANT_SETTING}', true)")
    )
    value = result.scalar()
    return value or None


@asynccontextmanager
async def tenant_session(tenant_id: str) -> AsyncGenerator[AsyncSession, None]:
    """A session already scoped to ``tenant_id``.

    Mirrors ``db.session.get_session`` so callers can swap one for the other,
    with the binding issued inside the transaction that will run the queries.
    """
    assert_safe_tenant_id(tenant_id)
    async with async_session_factory()() as session:
        try:
            await bind_tenant(session, tenant_id)
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
