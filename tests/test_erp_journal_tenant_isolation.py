"""A journal entry must not move another tenant's general-ledger balance.

``ERPService.create_journal_entry(tenant_id, data)`` stamps ``tenant_id`` on
the entry and on every line — and then updated the account balance like this:

    account = await self.session.get(GLAccountRecord, line["account_id"])
    if account:
        account.current_balance += line["debit"] - line["credit"]

``account_id`` comes straight from the caller's payload, so an entry naming
another tenant's GL account silently moved that tenant's balance. Of every
place a cross-tenant write can land, accounting records are the worst: least
likely to be noticed, hardest to unwind.

``tenant_id`` was already a parameter of the function — the guard was simply
missing, not unavailable.

Scope note: ``api/routers/erp/finance.py`` is **not mounted**, so this was not
reachable over HTTP when it was fixed. It is a landmine rather than an open
door, and the guard belongs with the write rather than with whoever mounts
the router later. The gate now flags this shape (``session.get`` by id with no
following ``tenant_id`` check), which is how it was found.
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from db.models import Base
from db.models_erp import GLAccountRecord, JournalEntryLineRecord, JournalEntryRecord

TENANT_A = "tnt_poster"
TENANT_B = "tnt_victim"


@pytest_asyncio.fixture
async def session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all,
            tables=[
                GLAccountRecord.__table__,
                JournalEntryRecord.__table__,
                JournalEntryLineRecord.__table__,
            ],
        )
    factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with factory() as sess:
        yield sess
    await engine.dispose()


@pytest_asyncio.fixture
async def accounts(session):
    own = GLAccountRecord(
        id="gl_own",
        tenant_id=TENANT_A,
        account_code="1000",
        account_name="Cash",
        account_type="asset",
        current_balance=0.0,
        is_active=True,
    )
    victim = GLAccountRecord(
        id="gl_victim",
        tenant_id=TENANT_B,
        account_code="1000",
        account_name="Victim Cash",
        account_type="asset",
        current_balance=100_000.0,
        is_active=True,
    )
    session.add_all([own, victim])
    await session.commit()
    return {"own": own, "victim": victim}


def _entry(account_id: str, debit: float = 5000.0) -> dict:
    return {
        "description": "test entry",
        "lines": [{"account_id": account_id, "debit": debit, "credit": 0.0}],
    }


@pytest.mark.asyncio
async def test_posting_against_another_tenants_account_is_refused(session, accounts):
    """The defect: this silently altered the victim's ledger balance."""
    from dealix.erp.service import ERPService

    svc = ERPService(session)

    with pytest.raises(ValueError):
        await svc.create_journal_entry(TENANT_A, _entry("gl_victim"))

    await session.rollback()
    victim = await session.get(GLAccountRecord, "gl_victim")
    assert victim.current_balance == 100_000.0, (
        "another tenant's general-ledger balance was moved"
    )


@pytest.mark.asyncio
async def test_posting_against_an_unknown_account_is_refused(session, accounts):
    from dealix.erp.service import ERPService

    svc = ERPService(session)

    with pytest.raises(ValueError):
        await svc.create_journal_entry(TENANT_A, _entry("gl_does_not_exist"))


@pytest.mark.asyncio
async def test_posting_against_your_own_account_still_works(session, accounts):
    """The guard must not break ordinary bookkeeping."""
    from dealix.erp.service import ERPService

    svc = ERPService(session)

    entry = await svc.create_journal_entry(TENANT_A, _entry("gl_own", debit=250.0))
    await session.commit()

    assert entry.tenant_id == TENANT_A
    own = await session.get(GLAccountRecord, "gl_own")
    assert own.current_balance == 250.0


@pytest.mark.asyncio
async def test_a_foreign_line_rejects_the_whole_entry(session, accounts):
    """A journal entry is atomic — a partial post is worse than no post.

    Skipping only the offending line would leave debits and credits
    unbalanced, which is a harder problem than a refused entry.
    """
    from dealix.erp.service import ERPService

    svc = ERPService(session)
    mixed = {
        "description": "one own line, one foreign line",
        "lines": [
            {"account_id": "gl_own", "debit": 100.0, "credit": 0.0},
            {"account_id": "gl_victim", "debit": 0.0, "credit": 100.0},
        ],
    }

    with pytest.raises(ValueError):
        await svc.create_journal_entry(TENANT_A, mixed)

    await session.rollback()
    victim = await session.get(GLAccountRecord, "gl_victim")
    assert victim.current_balance == 100_000.0
