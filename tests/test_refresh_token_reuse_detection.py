"""Replaying a rotated refresh token must end every session, not just fail.

`/api/v1/auth/refresh` already rotated: the presented token is revoked and a
new one issued. What it did not do is notice a *replay*. The lookup filtered
on `revoked_at IS NULL`, so an already-rotated token and a token that never
existed collapsed into the same 401 — throwing away the only signal that a
token had been stolen.

Rejecting the replay alone is not enough, and it punishes the wrong party.
Rotation means exactly one token is live at a time, so whoever refreshes first
keeps the session:

* **thief refreshes first** — the thief holds a live token, and the real
  user's next refresh 401s. The victim is logged out; the attacker is not.
* **user refreshes first** — the thief's replay 401s, but the user's session
  continues and nobody learns the token leaked.

Revoking the whole family on reuse makes both cases safe: either party
replaying the old token ends both sessions and forces re-authentication, which
the attacker cannot do and the legitimate user can. This is the standard
rotation-with-reuse-detection behaviour from the OAuth 2.0 security BCP.

Runs against in-memory SQLite with the auth dependencies pointed at it, so no
PostgreSQL is needed.
"""

from __future__ import annotations

import uuid

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from db.models import Base, RefreshTokenRecord, RoleRecord, TenantRecord, UserRecord

TENANT = "tnt_reuse"
PASSWORD = "correct-horse-battery"


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all,
            tables=[
                TenantRecord.__table__,
                RoleRecord.__table__,
                UserRecord.__table__,
                RefreshTokenRecord.__table__,
            ],
        )
    factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with factory() as session:
        yield session
    await engine.dispose()


@pytest_asyncio.fixture
async def user(db_session):
    from api.routers.auth import _hash_password

    tenant = TenantRecord(id=TENANT, name="Reuse Co", slug="reuse-co")
    record = UserRecord(
        id=f"usr_{uuid.uuid4().hex[:12]}",
        tenant_id=TENANT,
        email="victim@example.com",
        name="Victim",
        hashed_password=_hash_password(PASSWORD),
        is_active=True,
    )
    db_session.add_all([tenant, record])
    await db_session.commit()
    return record


@pytest_asyncio.fixture
async def client(db_session, monkeypatch):
    from api.main import app
    from db.session import get_db

    monkeypatch.setenv("API_KEYS", "")

    async def _transactional_db():
        # Match db.session:get_db exactly: a raised HTTPException rolls back.
        # This catches security writes that were only flushed before the 401.
        try:
            yield db_session
            await db_session.commit()
        except Exception:
            await db_session.rollback()
            raise

    app.dependency_overrides[get_db] = _transactional_db
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac
    finally:
        app.dependency_overrides.clear()


async def _login(client) -> dict:
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "victim@example.com", "password": PASSWORD},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()


async def _refresh(client, token: str):
    return await client.post("/api/v1/auth/refresh", json={"refresh_token": token})


async def _live_token_count(session, user_id: str) -> int:
    result = await session.execute(
        select(RefreshTokenRecord).where(
            RefreshTokenRecord.user_id == user_id,
            RefreshTokenRecord.revoked_at.is_(None),
        )
    )
    return len(list(result.scalars().all()))


# ── Rotation still works ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_a_normal_refresh_rotates(client, user):
    first = await _login(client)
    rotated = await _refresh(client, first["refresh_token"])

    assert rotated.status_code == 200, rotated.text
    assert rotated.json()["refresh_token"] != first["refresh_token"]


@pytest.mark.asyncio
async def test_the_new_token_works(client, user):
    first = await _login(client)
    second = (await _refresh(client, first["refresh_token"])).json()

    third = await _refresh(client, second["refresh_token"])

    assert third.status_code == 200, third.text


# ── Reuse detection ───────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_replaying_a_rotated_token_is_refused(client, user):
    first = await _login(client)
    await _refresh(client, first["refresh_token"])

    replay = await _refresh(client, first["refresh_token"])

    assert replay.status_code == 401


@pytest.mark.asyncio
async def test_reuse_revokes_every_session(client, user, db_session):
    """The defect: only the replayed token died, so the thief kept theirs."""
    user_id = user.id
    first = await _login(client)
    await _refresh(client, first["refresh_token"])
    assert await _live_token_count(db_session, user_id) == 1

    await _refresh(client, first["refresh_token"])  # the replay

    assert await _live_token_count(db_session, user_id) == 0, (
        "a live session survived a detected token reuse"
    )


@pytest.mark.asyncio
async def test_the_token_the_thief_obtained_stops_working(client, user):
    """Thief refreshes first, victim replays — the thief must not survive.

    This is the case the plain 401 got backwards: without family revocation
    the attacker keeps a live session and the victim is the one locked out.
    """
    stolen = (await _login(client))["refresh_token"]
    thief_token = (await _refresh(client, stolen)).json()["refresh_token"]

    victim_replay = await _refresh(client, stolen)
    assert victim_replay.status_code == 401

    thief_retry = await _refresh(client, thief_token)
    assert thief_retry.status_code == 401, "the thief's session outlived the detection"


@pytest.mark.asyncio
async def test_the_response_says_why(client, user):
    first = await _login(client)
    await _refresh(client, first["refresh_token"])

    replay = await _refresh(client, first["refresh_token"])

    assert "reuse" in replay.json()["detail"].lower()


@pytest.mark.asyncio
async def test_reuse_does_not_touch_another_users_sessions(client, user, db_session):
    """Family revocation must stop at the user it belongs to."""
    from api.routers.auth import _hash_password

    other = UserRecord(
        id=f"usr_{uuid.uuid4().hex[:12]}",
        tenant_id=TENANT,
        email="bystander@example.com",
        name="Bystander",
        hashed_password=_hash_password(PASSWORD),
        is_active=True,
    )
    db_session.add(other)
    await db_session.commit()
    other_id = other.id

    bystander = await client.post(
        "/api/v1/auth/login",
        json={"email": "bystander@example.com", "password": PASSWORD},
    )
    assert bystander.status_code == 200, bystander.text

    first = await _login(client)
    await _refresh(client, first["refresh_token"])
    await _refresh(client, first["refresh_token"])  # trigger detection

    assert await _live_token_count(db_session, other_id) == 1, (
        "another user's session was revoked by an unrelated reuse"
    )
    still_valid = await _refresh(client, bystander.json()["refresh_token"])
    assert still_valid.status_code == 200


# ── An unknown token is still just unknown ────────────────────────────────


@pytest.mark.asyncio
async def test_a_forged_token_does_not_revoke_anything(client, user, db_session):
    """Otherwise anyone could log a user out by posting garbage."""
    user_id = user.id
    await _login(client)
    assert await _live_token_count(db_session, user_id) == 1

    from api.security.jwt import create_refresh_token

    unknown = create_refresh_token(user_id=user.id, tenant_id=TENANT)
    resp = await _refresh(client, unknown)

    assert resp.status_code == 401
    assert await _live_token_count(db_session, user_id) == 1, (
        "a token that was never issued revoked a live session"
    )
