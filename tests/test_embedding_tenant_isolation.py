"""Indexing a conversation must not overwrite another tenant's embedding.

``EmbeddingService.index_conversation`` upserts into
``conversation_embeddings``. The lookup filtered on ``conversation_id`` alone:

    select(ConversationEmbeddingRecord).where(
        ConversationEmbeddingRecord.conversation_id == conversation_id
    )

``conversation_id`` is not unique on that table, so several tenants can hold a
row for one conversation — and the unscoped lookup returned whichever tenant
indexed it first, then overwrote that row's ``embedding_json`` in place while
leaving its ``tenant_id`` untouched. Nothing in the row afterwards shows that
another tenant wrote it.

It is reachable, not theoretical: ``conversation_id`` arrives from a
background-job payload the caller supplies
(``core/queue/tasks.py:_run_embedding_index``), so one tenant naming another's
conversation poisons that tenant's semantic memory.

``index_account`` is deliberately *not* scoped the same way — see
``test_account_embeddings_are_intentionally_global`` at the bottom for why the
two differ, so a future reader does not "fix" the asymmetry into a bug.
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from db.models import Base, ConversationEmbeddingRecord

TENANT_A = "tenant_attacker"
TENANT_B = "tenant_victim"
CONVERSATION = "conv_shared_id"


@pytest_asyncio.fixture
async def session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        # Only the table under test, matching the other *_tenant_isolation
        # suites. Creating the whole metadata works in isolation but fails
        # once any other test has imported a model with a PostgreSQL-only
        # column type — SQLite cannot render JSONB — which makes the failure
        # depend on collection order rather than on this code.
        await conn.run_sync(
            Base.metadata.create_all,
            tables=[ConversationEmbeddingRecord.__table__],
        )
    factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with factory() as sess:
        yield sess
    await engine.dispose()


@pytest.fixture
def service(monkeypatch):
    """EmbeddingService with a deterministic, offline embedder."""
    from core.memory.embedding_service import EmbeddingService

    svc = EmbeddingService()

    async def _fake_embed(text: str):
        # Distinct, recognisable vectors per caller so an overwrite is visible.
        return [float(len(text))] * 4

    monkeypatch.setattr(svc, "embed", _fake_embed)
    return svc


async def _rows(session) -> list[ConversationEmbeddingRecord]:
    result = await session.execute(
        select(ConversationEmbeddingRecord).where(
            ConversationEmbeddingRecord.conversation_id == CONVERSATION
        )
    )
    return list(result.scalars().all())


@pytest.mark.asyncio
async def test_second_tenant_does_not_overwrite_the_first(service, session):
    """The defect: tenant A's index call rewrote tenant B's vector."""
    await service.index_conversation(
        conversation_id=CONVERSATION, text="victim", tenant_id=TENANT_B, session=session
    )
    await session.commit()

    victim_before = (await _rows(session))[0]
    original_vector = list(victim_before.embedding_json)

    await service.index_conversation(
        conversation_id=CONVERSATION,
        text="attacker-supplied text that is a different length",
        tenant_id=TENANT_A,
        session=session,
    )
    await session.commit()

    rows = {row.tenant_id: row for row in await _rows(session)}

    assert TENANT_B in rows, "the victim's row disappeared"
    assert rows[TENANT_B].embedding_json == original_vector, (
        "another tenant's index call overwrote the victim's embedding"
    )
    assert TENANT_A in rows, "the second tenant got no row of its own"
    assert rows[TENANT_A].embedding_json != original_vector


@pytest.mark.asyncio
async def test_a_tenant_still_updates_its_own_row_in_place(service, session):
    """Scoping must not turn every re-index into a duplicate row."""
    await service.index_conversation(
        conversation_id=CONVERSATION, text="first", tenant_id=TENANT_B, session=session
    )
    await session.commit()
    await service.index_conversation(
        conversation_id=CONVERSATION,
        text="second pass, longer text",
        tenant_id=TENANT_B,
        session=session,
    )
    await session.commit()

    rows = await _rows(session)

    assert len(rows) == 1, f"re-indexing duplicated the row: {len(rows)} rows"
    assert rows[0].embedding_json == [float(len("second pass, longer text"))] * 4


@pytest.mark.asyncio
async def test_a_tenantless_caller_cannot_reach_a_tenant_row(service, session):
    """``tenant_id=None`` must match NULL, not match everything."""
    await service.index_conversation(
        conversation_id=CONVERSATION, text="victim", tenant_id=TENANT_B, session=session
    )
    await session.commit()
    original = list((await _rows(session))[0].embedding_json)

    await service.index_conversation(
        conversation_id=CONVERSATION,
        text="anonymous caller with different length",
        tenant_id=None,
        session=session,
    )
    await session.commit()

    rows = {row.tenant_id: row for row in await _rows(session)}

    assert rows[TENANT_B].embedding_json == original, (
        "a tenant-less caller reached a tenant-owned row"
    )
    assert None in rows


@pytest.mark.asyncio
async def test_different_conversations_stay_separate(service, session):
    await service.index_conversation(
        conversation_id="conv_one", text="one", tenant_id=TENANT_B, session=session
    )
    await service.index_conversation(
        conversation_id="conv_two", text="two", tenant_id=TENANT_B, session=session
    )
    await session.commit()

    result = await session.execute(select(ConversationEmbeddingRecord))
    assert len({row.conversation_id for row in result.scalars().all()}) == 2


def test_account_embeddings_are_intentionally_global():
    """Pins why ``index_account`` is not scoped, so nobody "fixes" it into a bug.

    ``account_embeddings.account_id`` is unique, so one row exists per account
    platform-wide, and ``accounts`` carries no ``tenant_id`` at all — the
    entity is global and ``tenant_id`` on the embedding is provenance, not
    ownership. Adding a tenant predicate to that upsert would make a second
    tenant's call miss the row and violate the unique constraint, raising an
    IntegrityError inside a worker.

    If either fact changes, this test fails and the asymmetry must be
    revisited rather than silently inherited.
    """
    from db.models import AccountEmbeddingRecord, AccountRecord, ConversationRecord

    assert AccountEmbeddingRecord.__table__.columns["account_id"].unique is True
    assert "tenant_id" not in AccountRecord.__table__.columns
    assert "tenant_id" not in ConversationRecord.__table__.columns
    assert ConversationEmbeddingRecord.__table__.columns["conversation_id"].unique is not True
