from __future__ import annotations

import asyncio
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.routers import company_targeting
from api.routers.company_targeting import router
from api.security.auth_deps import get_current_user
from db.models_company_targeting import (
    AgentCapabilityEvaluationRecord,
    CommercialCampaignItemRecord,
    CommercialCampaignPlanRecord,
    CompanyDirectoryEntryRecord,
)


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_status_and_benchmark() -> None:
    client = _client()
    status = client.get("/api/v1/company-targeting/status")
    benchmark = client.get("/api/v1/company-targeting/capability-benchmark")
    assert status.status_code == 200
    assert status.json()["external_send"] is False
    assert benchmark.status_code == 200
    assert benchmark.json()["count"] >= 12


def test_capability_eval_blocks_unsafe_send() -> None:
    client = _client()
    response = client.post(
        "/api/v1/company-targeting/evaluate-capability",
        json={
            "capability": "sales",
            "output": {
                "facts": ["fact"],
                "source_refs": [],
                "channel_policy": {
                    "channel": "whatsapp",
                    "consent_verified": False,
                    "opt_out_checked": False,
                    "external_send": True,
                },
            },
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["production_eligible"] is False
    assert "live_external_send_requested" in body["evaluation"]["critical_failures"]


def test_negotiation_endpoint_requires_approval_for_discount() -> None:
    client = _client()
    response = client.post(
        "/api/v1/company-targeting/negotiate",
        json={
            "account_name": "شركة اختبار",
            "offer_id": "growth_engine_os",
            "customer_problem": "ضعف المبيعات",
            "list_price_sar": 25000,
            "approved_floor_sar": 22500,
            "requested_discount_pct": 15,
            "evidence_refs": ["ev_001"],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["external_commitment"] is False
    assert body["plan"]["approval_required"] is True


def test_company_directory_endpoints_require_an_authenticated_tenant() -> None:
    client = _client()
    response = client.get("/api/v1/company-targeting/summary")
    assert response.status_code == 401
    assert response.json()["detail"].startswith("Missing or invalid Authorization")


def test_summary_uses_authenticated_tenant_not_request_input(
    tmp_path,
    monkeypatch,
) -> None:
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'targeting.db'}")
    sessions = async_sessionmaker(engine, expire_on_commit=False)

    async def seed() -> None:
        async with engine.begin() as connection:
            await connection.run_sync(CompanyDirectoryEntryRecord.__table__.create)
        async with sessions() as session:
            for tenant_id in ("tenant_a", "tenant_b"):
                session.add(
                    CompanyDirectoryEntryRecord(
                        id=f"{tenant_id}_entry",
                        tenant_id=tenant_id,
                        import_id=f"{tenant_id}_import",
                        company_name=f"Company {tenant_id}",
                        normalized_name=f"company {tenant_id}",
                        source_sheet="data",
                        source_row_number=2,
                        source_fingerprint=f"fingerprint_{tenant_id}",
                        priority="P1_RESEARCH",
                        recommended_offer_id="free_mini_diagnostic",
                        value_angle_ar="اختبار",
                        suppression_reasons_json=["consent_not_proven"],
                    )
                )
            await session.commit()

    asyncio.run(seed())
    monkeypatch.setattr(company_targeting, "async_session_factory", lambda: sessions)
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        tenant_id="tenant_a"
    )
    client = TestClient(app)
    response = client.get(
        "/api/v1/company-targeting/summary",
        params={"tenant_id": "tenant_b"},
    )
    assert response.status_code == 200
    assert response.json()["tenant_id"] == "tenant_a"
    assert response.json()["total_companies"] == 1
    asyncio.run(engine.dispose())


def test_evaluation_and_campaign_preview_are_persisted_without_external_send(
    tmp_path,
    monkeypatch,
) -> None:
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'evidence.db'}")
    sessions = async_sessionmaker(engine, expire_on_commit=False)

    async def seed() -> None:
        async with engine.begin() as connection:
            for table in (
                CompanyDirectoryEntryRecord.__table__,
                AgentCapabilityEvaluationRecord.__table__,
                CommercialCampaignPlanRecord.__table__,
                CommercialCampaignItemRecord.__table__,
            ):
                await connection.run_sync(table.create)
        async with sessions() as session:
            session.add(
                CompanyDirectoryEntryRecord(
                    id="tenant_a_entry",
                    tenant_id="tenant_a",
                    import_id="tenant_a_import",
                    company_name="شركة اختبار",
                    normalized_name="شركة اختبار",
                    city="الرياض",
                    activity="مقاولات",
                    source_sheet="data",
                    source_row_number=2,
                    source_fingerprint="fingerprint_a",
                    research_priority_score=90,
                    priority="P1_RESEARCH",
                    recommended_offer_id="executive_command_center_7500",
                    value_angle_ar="وضوح المشاريع والمخاطر والتحصيل",
                    suppression_reasons_json=["consent_not_proven"],
                )
            )
            await session.commit()

    asyncio.run(seed())
    monkeypatch.setattr(company_targeting, "async_session_factory", lambda: sessions)
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        tenant_id="tenant_a"
    )
    client = TestClient(app)
    evaluation_response = client.post(
        "/api/v1/company-targeting/evaluation-runs",
        json={
            "agent_name": "sales_agent",
            "scenario_id": "sales_discovery_ar_01",
            "capability": "sales_discovery",
            "output": {
                "facts": ["fact_without_source"],
                "source_refs": [],
                "channel_policy": {
                    "channel": "research_only",
                    "opt_out_checked": True,
                    "external_send": False,
                },
            },
        },
    )
    assert evaluation_response.status_code == 200
    assert evaluation_response.json()["production_eligible"] is False

    campaign_response = client.post(
        "/api/v1/company-targeting/campaign/preview",
        json={
            "campaign_name": "cohort_0",
            "offer_id": "executive_command_center_7500",
            "max_items": 10,
        },
    )
    assert campaign_response.status_code == 200
    campaign = campaign_response.json()
    assert campaign["external_side_effect"] is False
    assert campaign["plan"]["external_actions_performed"] == 0
    assert campaign["plan"]["research_only_count"] == 1

    async def counts() -> tuple[int, int, int]:
        async with sessions() as session:
            return (
                len((await session.execute(
                    select(AgentCapabilityEvaluationRecord)
                )).scalars().all()),
                len((await session.execute(
                    select(CommercialCampaignPlanRecord)
                )).scalars().all()),
                len((await session.execute(
                    select(CommercialCampaignItemRecord)
                )).scalars().all()),
            )

    assert asyncio.run(counts()) == (1, 1, 1)
    asyncio.run(engine.dispose())
