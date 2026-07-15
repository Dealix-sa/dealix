from __future__ import annotations

from auto_client_acquisition.full_ops import get_default_queue
from auto_client_acquisition.service_catalog.registry import SERVICE_IDS
from dealix.company_os.workload_router import (
    CompanyWorkloadRequest,
    capability_map,
    route_company_workload,
)


def _request(**overrides) -> CompanyWorkloadRequest:
    values = {
        "tenant_id": "tenant_a",
        "customer_id": "customer_001",
        "title": "رفع المبيعات والتسويق وأتمتة العمليات",
        "description": "نحتاج pipeline وحملات وتقليل العمل اليدوي",
        "evidence_ids": ("ev_baseline_001",),
    }
    values.update(overrides)
    return CompanyWorkloadRequest(**values)


def test_capability_map_covers_company_and_uses_canonical_offerings() -> None:
    capabilities = capability_map()
    assert len(capabilities) == 16
    assert {c["domain"] for c in capabilities} >= {
        "executive_strategy", "sales", "marketing_brand", "operations",
        "finance", "compliance_risk", "people_ops", "product",
    }
    mapped_services = {
        service_id
        for capability in capabilities
        for service_id in capability["service_ids"]
    }
    assert mapped_services <= SERVICE_IDS


def test_routes_cross_function_work_to_existing_catalog() -> None:
    route = route_company_workload(_request())
    domains = {route.primary_domain, *route.supporting_domains}
    assert {"sales", "marketing_brand", "operations"} <= domains
    assert "growth_engine_os" in route.recommended_service_ids
    assert "operations_automation_os" in route.recommended_service_ids
    assert route.autonomy_level == "L3_INTERNAL_EXECUTE"
    assert route.action_mode == "draft_only"
    assert len(route.execution_plan) == 7


def test_high_impact_finance_decision_is_escalated_to_owner() -> None:
    route = route_company_workload(
        _request(
            title="اعتماد خصم واسترداد دفعة لعميل",
            description="نحتاج قرار سعر وعقد جديد",
            external_action_requested=True,
            requested_channel="email",
        )
    )
    assert route.primary_domain == "finance"
    assert route.risk_level in ("high", "critical")
    assert route.action_mode == "approval_required"
    assert route.queue_status == "needs_approval"
    assert route.human_decision is not None
    assert route.human_decision["owner_role"] == "finance_owner"


def test_cold_whatsapp_and_linkedin_automation_are_blocked() -> None:
    whatsapp = route_company_workload(
        _request(
            external_action_requested=True,
            requested_channel="whatsapp",
            recipient_opted_in=None,
        )
    )
    linkedin = route_company_workload(
        _request(
            external_action_requested=True,
            requested_channel="linkedin",
        )
    )
    assert whatsapp.action_mode == "blocked"
    assert "whatsapp_opt_in_not_proven" in whatsapp.risk_flags
    assert linkedin.action_mode == "blocked"
    assert "linkedin_automation_disallowed" in linkedin.risk_flags


def test_opted_in_whatsapp_is_drafted_but_not_sent() -> None:
    route = route_company_workload(
        _request(
            external_action_requested=True,
            requested_channel="whatsapp_business",
            recipient_opted_in=True,
        )
    )
    assert route.action_mode == "approval_required"
    assert route.queue_status == "needs_approval"
    assert route.autonomy_level == "L2_DRAFT"


def test_contact_values_are_redacted_before_queue_storage() -> None:
    route = route_company_workload(
        _request(
            title="تواصل مع ahmed@example.com",
            description="رقمه +966 55 123 4567 ونحتاج عرض مبيعات",
        )
    )
    item = route.to_work_item()
    assert route.pii_redacted is True
    assert "ahmed@example.com" not in item.title_ar
    assert "+966" not in item.description_ar
    assert "possible_pii_redacted" in item.risk_flags


def test_queue_insert_is_idempotent_and_tenant_isolated() -> None:
    queue = get_default_queue()
    queue.clear()
    route_a = route_company_workload(_request(tenant_id="tenant_a"))
    route_b = route_company_workload(_request(tenant_id="tenant_b"))
    queue.add(route_a.to_work_item())
    queue.add(route_a.to_work_item())
    queue.add(route_b.to_work_item())
    assert len(queue.list_all(tenant_id="tenant_a")) == 1
    assert len(queue.list_all(tenant_id="tenant_b")) == 1
    queue.clear()
