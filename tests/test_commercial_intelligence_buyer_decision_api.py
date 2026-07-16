from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from api.routers import commercial_intelligence as router_module
from api.routers.commercial_intelligence import BuyerDecisionPlanBody
from db.models_commercial_intelligence import (
    CommercialOpportunityRecord,
    DepartmentObjectiveRecord,
    StrategicRelationshipRecord,
)


class _ScalarResult:
    def __init__(self, records: list[object]) -> None:
        self.records = records

    def scalars(self) -> "_ScalarResult":
        return self

    def all(self) -> list[object]:
        return self.records


class _Session:
    def __init__(self) -> None:
        now = datetime.now(UTC)
        self.opportunity = SimpleNamespace(
            id="opp_1",
            tenant_id="tenant-a",
            status="active",
            department_objective_id="obj_1",
            relationship_id="rel_1",
            source_signal_ids_json=["sig_1"],
            company_name="شركة اختبار",
            title="فرص بلا خطوة تالية",
            offer_id="revenue_proof_sprint",
            proof_target="توثيق خط الأساس والقرار",
            score=78,
            evidence_level="l3_first_party",
        )
        self.objective = SimpleNamespace(
            id="obj_1",
            tenant_id="tenant-a",
            objective="توحيد رؤية الفرص",
            metric="verified_next_action_rate",
        )
        self.relationship = SimpleNamespace(
            id="rel_1",
            tenant_id="tenant-a",
            permission_state="consented",
        )
        self.signal = SimpleNamespace(
            id="sig_1",
            tenant_id="tenant-a",
            account_id="account-1",
            source_id="source_1",
            claim="أكد العميل وجود فرص بلا خطوة تالية.",
            signal_type="verified_operating_problem",
            evidence_ref="evidence://discovery/1",
            evidence_level="l3_first_party",
            confidence=90,
            observed_at=now,
            expires_at=now + timedelta(days=30),
            payload_json={},
        )
        self.source = SimpleNamespace(
            id="source_1",
            policy_status="approved",
            active=True,
        )
        self.execute_calls = 0

    async def __aenter__(self) -> "_Session":
        return self

    async def __aexit__(self, *_: object) -> None:
        return None

    async def get(self, model: type[object], record_id: str) -> object | None:
        lookup = {
            (CommercialOpportunityRecord, "opp_1"): self.opportunity,
            (DepartmentObjectiveRecord, "obj_1"): self.objective,
            (StrategicRelationshipRecord, "rel_1"): self.relationship,
        }
        return lookup.get((model, record_id))

    async def execute(self, _: object) -> _ScalarResult:
        self.execute_calls += 1
        return _ScalarResult([self.signal] if self.execute_calls == 1 else [self.source])


@pytest.mark.asyncio
async def test_buyer_decision_endpoint_is_tenant_scoped_and_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _Session()
    monkeypatch.setattr(router_module, "async_session_factory", lambda: lambda: session)

    result = await router_module.build_opportunity_buyer_decision_plan(
        "opp_1",
        BuyerDecisionPlanBody(
            known_objections=["عندي Odoo", "أعطني خصم 30%"],
            requested_discount_pct=30,
        ),
        current_user={"tenant_id": "tenant-a"},
    )

    assert result["opportunity_id"] == "opp_1"
    assert result["truth_map"][0]["disposition"] == "customer_context"
    assert result["offer_architecture"]["price_sar"] is None
    assert result["price_included"] is False
    assert result["external_action_allowed"] is False
    assert result["external_commitment_made"] is False
    assert any(item["id"] == "approve_commercial_exception" for item in result["approval_queue"])
