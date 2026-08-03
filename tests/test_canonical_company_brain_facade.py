from __future__ import annotations

from auto_client_acquisition.company_brain_v6 import BuildRequest
from auto_client_acquisition.company_brain_v6.schemas import FORBIDDEN_CHANNELS
from dealix.company_intelligence import (
    CompanyBrainSource,
    build_customer_company_brain,
    build_internal_company_brain,
)


def test_internal_snapshot_normalizes_without_network_contract() -> None:
    brain = build_internal_company_brain(tenant_id="dealix")

    assert brain.tenant_id == "dealix"
    assert brain.source is CompanyBrainSource.INTERNAL_SNAPSHOT
    assert brain.company_handle == "dealix"
    assert brain.provenance[0].tenant_id == "dealix"
    assert brain.guardrails["approval_required_for_external_actions"] is True


def test_customer_v6_preserves_forbidden_channel_enforcement() -> None:
    brain = build_customer_company_brain(
        BuildRequest(
            company_handle="acme-ksa",
            sector="b2b_saas",
            allowed_channels=["email", "cold_whatsapp", "linkedin_automation"],
            blocked_channels=[],
            pain_points=["manual follow-up"],
        ),
        tenant_id="tenant-acme",
    )

    assert brain.source is CompanyBrainSource.CUSTOMER_V6
    assert brain.tenant_id == "tenant-acme"
    assert brain.company_handle == "acme-ksa"
    assert brain.allowed_channels == ["email"]
    assert set(FORBIDDEN_CHANNELS) <= set(brain.blocked_channels)
    assert brain.pain_points == ["manual follow-up"]
    assert brain.next_best_action


def test_customer_provenance_is_tenant_scoped() -> None:
    brain = build_customer_company_brain(
        BuildRequest(company_handle="proof-co"),
        tenant_id="tenant-proof",
    )

    assert brain.provenance
    assert all(ref.tenant_id == "tenant-proof" for ref in brain.provenance)
    assert all(ref.source_type is CompanyBrainSource.CUSTOMER_V6 for ref in brain.provenance)


def test_contract_rejects_empty_tenant_id() -> None:
    request = BuildRequest(company_handle="invalid-tenant")

    try:
        build_customer_company_brain(request, tenant_id="")
    except ValueError as exc:
        assert "tenant_id" in str(exc)
    else:
        raise AssertionError("empty tenant_id must be rejected")


def test_company_brain_router_serves_canonical_facade() -> None:
    """The API router must route the canonical view through the facade,
    not redefine CompanyBrain truth independently (consolidation map
    docs/company/COMPANY_INTELLIGENCE_CONSOLIDATION_MAP_2026-07-31.md)."""
    from fastapi.testclient import TestClient

    from api.main import create_app

    client = TestClient(create_app())

    resp = client.get("/api/v1/company-brain/canonical")
    assert resp.status_code == 200
    body = resp.json()

    expected = build_internal_company_brain(tenant_id="dealix").model_dump(mode="json")
    volatile_fields = {"generated_at", "provenance"}
    assert {k: v for k, v in body.items() if k not in volatile_fields} == {
        k: v for k, v in expected.items() if k not in volatile_fields
    }
    assert body["source"] == CompanyBrainSource.INTERNAL_SNAPSHOT.value
    assert body["tenant_id"] == "dealix"
    assert body["guardrails"]["approval_required_for_external_actions"] is True
