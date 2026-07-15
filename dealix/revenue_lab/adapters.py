"""Adapters from existing Dealix company targeting into Revenue Lab signals."""

from __future__ import annotations

from dealix.company_os.company_directory import DirectoryCandidate

from .models import CompanySignal, EvidenceReference


def signal_from_directory_candidate(
    candidate: DirectoryCandidate,
    *,
    tenant_id: str,
    evidence_ref: str,
    observed_at: str,
    permission: str = "research_only",
    decision_maker_role: str = "unknown — research required",
) -> CompanySignal:
    """Enrich a governed directory candidate without inferring contact consent."""
    relationship = candidate.relationship_status
    if relationship not in {
        "customer",
        "prospect",
        "strategic_partner",
        "referral_partner",
        "channel_distributor",
        "implementation_partner",
        "technology_partner",
        "co_marketing_partner",
        "service_exchange",
        "supplier",
        "investor",
        "government_stakeholder",
    }:
        relationship = "prospect"
    return CompanySignal(
        tenant_id=tenant_id,
        account_id=candidate.id,
        company_name=candidate.company_name,
        sector=candidate.activity or "unknown",
        company_size="unknown",
        department="sales",
        relationship=relationship,
        permission=permission,
        decision_maker_role=decision_maker_role,
        offer_match=candidate.recommended_offer_id,
        why_now=(
            f"Research priority {candidate.research_priority_score:.1f}/100 from the "
            "governed company-directory scorer; validate before outreach."
        ),
        value_exchange=candidate.value_angle_ar,
        pain_hypotheses=(candidate.value_angle_ar,),
        unknowns=(
            "decision owner",
            "current systems and process",
            "client-sourced baseline",
            "lawful contact permission",
        ),
        evidence=(
            EvidenceReference(
                source_ref=evidence_ref,
                source_type="company_directory_import",
                observed_at=observed_at,
                title=f"Directory source for {candidate.company_name}",
                quality="internal",
            ),
        ),
        strategic_fit=max(0, min(100, round(candidate.fit_score))),
        urgency=max(0, min(100, round(candidate.research_priority_score))),
        demo=False,
    )


__all__ = ["signal_from_directory_candidate"]
