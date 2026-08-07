"""Canonical Company Brain facade over existing Dealix builders."""
from __future__ import annotations

from auto_client_acquisition.company_brain.brain import build_company_brain
from auto_client_acquisition.company_brain_v6 import BuildRequest, build_company_brain_v6
from dealix.company_intelligence.contracts import (
    CanonicalCompanyBrain,
    CompanyBrainSource,
    ProvenanceRef,
)


def build_internal_company_brain(*, tenant_id: str = "dealix") -> CanonicalCompanyBrain:
    """Normalize the existing defensive Dealix snapshot.

    Existing builder semantics remain unchanged: no LLM, no network, and
    failing component signals degrade rather than crash the full snapshot.
    """
    brain = build_company_brain()
    return CanonicalCompanyBrain(
        tenant_id=tenant_id,
        company_handle=brain.company_name.lower(),
        source=CompanyBrainSource.INTERNAL_SNAPSHOT,
        generated_at=brain.generated_at,
        mission=brain.mission_en,
        current_priorities=list(brain.current_priorities),
        health_overall=brain.health_overall,
        guardrails=dict(brain.guardrails),
        provenance=[
            ProvenanceRef(
                source_type=CompanyBrainSource.INTERNAL_SNAPSHOT,
                source_id="auto_client_acquisition.company_brain.brain",
                tenant_id=tenant_id,
                observed_at=brain.generated_at,
            )
        ],
    )


def build_customer_company_brain(
    request: BuildRequest,
    *,
    tenant_id: str,
) -> CanonicalCompanyBrain:
    """Normalize the existing per-customer V6 Company Brain.

    The V6 builder remains responsible for forbidden-channel enforcement,
    service matching, risk computation, and next-best-action selection.
    """
    brain = build_company_brain_v6(request)
    evidence_ids = brain.evidence_ids or [f"req:{brain.company_handle}"]
    return CanonicalCompanyBrain(
        tenant_id=tenant_id,
        company_handle=brain.company_handle,
        source=CompanyBrainSource.CUSTOMER_V6,
        generated_at=brain.generated_at,
        sector=brain.sector,
        region=brain.region,
        offer=brain.offer,
        ideal_customer_profile=brain.icp,
        tone_preference=brain.tone_preference,
        language_preference=brain.language_preference,
        pain_points=list(brain.pain_points),
        allowed_channels=list(brain.allowed_channels),
        blocked_channels=list(brain.blocked_channels),
        next_best_action=brain.next_best_action,
        risk_profile=dict(brain.risk_profile),
        provenance=[
            ProvenanceRef(
                source_type=CompanyBrainSource.CUSTOMER_V6,
                source_id=evidence_id,
                tenant_id=tenant_id,
                observed_at=brain.generated_at,
            )
            for evidence_id in evidence_ids
        ],
    )
