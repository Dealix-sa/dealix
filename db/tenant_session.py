"""Transaction-scoped tenant binding for PostgreSQL row-level security.

Every policy in :mod:`db.rls_policies` reads ``app.tenant_id``. RLS must stay
inactive until request code can bind that setting inside the same transaction
as its queries; otherwise every protected query sees no rows.

This module provides that prerequisite only. It does not enable any policy.
"""

from __future__ import annotations

import re
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import async_session_factory

TENANT_SETTING = "app.tenant_id"
_SAFE_TENANT_ID = re.compile(r"[A-Za-z0-9_-]{1,64}")
_SET_TENANT = text("SELECT set_config(:setting, :tenant_id, true)")
_GET_TENANT = text("SELECT current_setting(:setting, true)")


class UnsafeTenantIdentifier(ValueError):
    """Raised when a tenant identifier is outside the canonical ID grammar."""


def assert_safe_tenant_id(tenant_id: str) -> str:
    """Return a canonical tenant ID or fail before a session is touched."""
    if not isinstance(tenant_id, str) or _SAFE_TENANT_ID.fullmatch(tenant_id) is None:
        raise UnsafeTenantIdentifier(
            f"refusing tenant id {tenant_id!r}: must match "
            f"{_SAFE_TENANT_ID.pattern}"
        )
    return tenant_id


async def bind_tenant(session: AsyncSession, tenant_id: str) -> None:
    """Bind ``tenant_id`` to ``session`` for its current transaction.

    ``set_config(..., true)`` is PostgreSQL's parameterizable equivalent of
    ``SET LOCAL``. The third argument scopes the value to the transaction, so
    a pooled connection cannot carry one tenant into the next request.
    """
    safe = assert_safe_tenant_id(tenant_id)
    await session.execute(
        _SET_TENANT,
        {"setting": TENANT_SETTING, "tenant_id": safe},
    )


async def current_bound_tenant(session: AsyncSession) -> str | None:
    """Return the transaction's bound tenant, or ``None`` when it is unset."""
    result = await session.execute(
        _GET_TENANT,
        {"setting": TENANT_SETTING},
    )
    value = result.scalar()
    return str(value) if value else None


async def tenant_session(tenant_id: str) -> AsyncGenerator[AsyncSession, None]:
    """FastAPI yield dependency for a session already bound to ``tenant_id``.

    Keep this function as an undecorated async generator. Decorating it with
    ``asynccontextmanager`` would make FastAPI inject the context-manager
    wrapper instead of entering the generator and yielding ``AsyncSession``.
    """
    safe = assert_safe_tenant_id(tenant_id)
    async with async_session_factory()() as session:
        try:
            await bind_tenant(session, safe)
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
