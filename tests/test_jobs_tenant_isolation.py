"""Cross-tenant isolation contract for the background-jobs endpoints.

`api/routers/jobs.py` is mounted in the running app. Before this guard it
returned any job by ID with no authentication and no tenant filter, and
listed jobs for whatever tenant the caller named. A job record carries
``input_payload`` and ``output_payload`` — the lead record being scored,
the drafted proposal, the outreach batch — so reading another tenant's
job meant reading their business content.

Enqueue endpoints also took the owning tenant from the request body, so a
job could be filed under another tenant.
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.routers import jobs
from api.security.auth_deps import get_current_user
from db.models import Base, BackgroundJobRecord
from db.session import get_db

ATTACKER_TENANT = "tenant_a"
VICTIM_TENANT = "tenant_b"
VICTIM_JOB = "job_of_b"
VICTIM_SECRET = "victim-proposal-draft-contents"


class _User:
    def __init__(self, tenant_id: str, system_role: str = "user") -> None:
        self.id = f"user_of_{tenant_id}"
        self.tenant_id = tenant_id
        self.system_role = system_role


@pytest_asyncio.fixture
async def session_factory():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all, tables=[BackgroundJobRecord.__table__]
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        session.add(
            BackgroundJobRecord(
                id=VICTIM_JOB,
                tenant_id=VICTIM_TENANT,
                job_type="proposal_draft",
                status="succeeded",
                input_payload={"deal_id": "deal_of_b"},
                output_payload={"draft": VICTIM_SECRET},
            )
        )
        await session.commit()
    yield factory
    await engine.dispose()


def _build_client(session_factory, user: _User) -> AsyncClient:
    async def override_db():
        async with session_factory() as session:
            yield session
            await session.commit()

    app = FastAPI()
    app.include_router(jobs.router)
    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_user] = lambda: user
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.mark.asyncio
async def test_status_does_not_leak_another_tenants_job(session_factory):
    async with _build_client(session_factory, _User(ATTACKER_TENANT)) as client:
        response = await client.get(f"/jobs/{VICTIM_JOB}")

    assert response.status_code == 404
    assert VICTIM_SECRET not in response.text


@pytest.mark.asyncio
async def test_status_serves_the_owning_tenant(session_factory):
    async with _build_client(session_factory, _User(VICTIM_TENANT)) as client:
        response = await client.get(f"/jobs/{VICTIM_JOB}")

    assert response.status_code == 200
    assert response.json()["output_payload"]["draft"] == VICTIM_SECRET


@pytest.mark.asyncio
async def test_listing_cannot_target_another_tenant(session_factory):
    async with _build_client(session_factory, _User(ATTACKER_TENANT)) as client:
        response = await client.get("/jobs/", params={"tenant_id": VICTIM_TENANT})

    assert response.status_code == 403
    assert VICTIM_SECRET not in response.text


@pytest.mark.asyncio
async def test_listing_defaults_to_the_callers_tenant(session_factory):
    async with _build_client(session_factory, _User(ATTACKER_TENANT)) as client:
        response = await client.get("/jobs/")

    assert response.status_code == 200
    assert response.json() == []


def test_job_routes_require_authentication():
    protected = {
        ("GET", "/jobs/{job_id}"),
        ("GET", "/jobs/{job_id}/stream"),
        ("GET", "/jobs/"),
        ("POST", "/jobs"),
        ("POST", "/jobs/lead-score"),
        ("POST", "/jobs/proposal-draft"),
        ("POST", "/jobs/outreach-batch"),
    }
    found = {}
    for route in jobs.router.routes:
        for method in route.methods:
            found[(method, route.path)] = {
                dep.call for dep in route.dependant.dependencies
            }

    for key in protected:
        assert key in found, f"route missing from the router: {key}"
        assert get_current_user in found[key], f"{key[0]} {key[1]} is unauthenticated"
