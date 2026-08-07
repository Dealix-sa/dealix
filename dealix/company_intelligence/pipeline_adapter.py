"""Fail-closed adapter from revenue pipeline Lead to canonical Opportunity.

Bridges ``auto_client_acquisition.revenue_pipeline.lead.Lead`` into
``CanonicalOpportunity`` without escalating authority. The operational Lead
carries pipeline stage, commitment, and payment evidence; this adapter
normalises it into the canonical shape the rest of the Company Intelligence
execution spine expects.

Key constraints:
  - Pipeline stages map to canonical ``OpportunityStage`` via an explicit
    mapping table. Unknown stages fail-closed to ``RESEARCH``.
  - ``external_action_allowed`` is always ``False``.
  - ``approval_required`` is always ``True``.
  - ``score`` is derived from stage progression and evidence fields.
  - The adapter never assumes consent or authorization beyond what the
    pipeline lead explicitly carries.
"""
from __future__ import annotations

from typing import Any

from dealix.company_intelligence.execution_contracts import (
    CanonicalOpportunity,
    OpportunityStage,
)

# ---------------------------------------------------------------------------
# Stage mapping
# ---------------------------------------------------------------------------

_STAGE_MAP: dict[str, OpportunityStage] = {
    # Early stages → RESEARCH
    "warm_intro_selected": OpportunityStage.RESEARCH,
    "message_drafted": OpportunityStage.RESEARCH,
    # Outreach → QUALIFY
    "founder_sent_manually": OpportunityStage.QUALIFY,
    "replied": OpportunityStage.QUALIFY,
    # Discovery → APPROVAL
    "diagnostic_requested": OpportunityStage.APPROVAL,
    "diagnostic_delivered": OpportunityStage.APPROVAL,
    # Offer → CONVERSATION
    "pilot_offered": OpportunityStage.CONVERSATION,
    # Commitment → PILOT
    "commitment_received": OpportunityStage.PILOT,
    # Payment → PROOF
    "payment_received": OpportunityStage.PROOF,
    # Delivery → COMMERCIAL
    "delivery_started": OpportunityStage.COMMERCIAL,
    "delivered": OpportunityStage.COMMERCIAL,
    "proof_pack_delivered": OpportunityStage.COMMERCIAL,
    # Post-delivery → WON or LOST
    "upsell_offered": OpportunityStage.WON,
    "closed_won": OpportunityStage.WON,
    "closed_lost": OpportunityStage.LOST,
}


def _resolve_stage(raw_stage: str) -> OpportunityStage:
    """Map a pipeline stage string to a canonical OpportunityStage.

    Unknown stages fail-closed to ``RESEARCH``.
    """
    return _STAGE_MAP.get(raw_stage.lower().strip(), OpportunityStage.RESEARCH)


def _compute_score(
    *,
    stage: OpportunityStage,
    has_commitment: bool,
    has_payment: bool,
) -> int:
    """Derive an opportunity score (0–100) from stage + evidence.

    The score is a simple heuristic:
      - Base score from stage position in the pipeline
      - Bonus for commitment evidence (+10)
      - Bonus for payment evidence (+15)
      - Capped at 100
    """
    stage_scores: dict[OpportunityStage, int] = {
        OpportunityStage.RESEARCH: 10,
        OpportunityStage.QUALIFY: 20,
        OpportunityStage.APPROVAL: 35,
        OpportunityStage.CONVERSATION: 45,
        OpportunityStage.PILOT: 60,
        OpportunityStage.PROOF: 75,
        OpportunityStage.COMMERCIAL: 85,
        OpportunityStage.WON: 100,
        OpportunityStage.LOST: 0,
        OpportunityStage.PARKED: 5,
    }
    base = stage_scores.get(stage, 10)
    bonus = 0
    if has_commitment:
        bonus += 10
    if has_payment:
        bonus += 15
    return min(100, base + bonus)


def _derive_next_action(stage: OpportunityStage) -> str:
    """Derive next action from canonical stage."""
    actions: dict[OpportunityStage, str] = {
        OpportunityStage.RESEARCH: "research_and_qualify",
        OpportunityStage.QUALIFY: "send_intro_message",
        OpportunityStage.APPROVAL: "deliver_diagnostic",
        OpportunityStage.CONVERSATION: "present_pilot_offer",
        OpportunityStage.PILOT: "collect_payment_evidence",
        OpportunityStage.PROOF: "start_delivery",
        OpportunityStage.COMMERCIAL: "assemble_proof_pack",
        OpportunityStage.WON: "explore_upsell",
        OpportunityStage.LOST: "review_and_learn",
        OpportunityStage.PARKED: "re_evaluate_fit",
    }
    return actions.get(stage, "review_manually")


def _derive_proof_target(stage: OpportunityStage) -> str:
    """Derive proof target from canonical stage."""
    targets: dict[OpportunityStage, str] = {
        OpportunityStage.RESEARCH: "icp_fit_assessment",
        OpportunityStage.QUALIFY: "reply_received",
        OpportunityStage.APPROVAL: "diagnostic_completion",
        OpportunityStage.CONVERSATION: "pilot_commitment",
        OpportunityStage.PILOT: "payment_confirmed",
        OpportunityStage.PROOF: "delivery_evidence",
        OpportunityStage.COMMERCIAL: "proof_pack_delivered",
        OpportunityStage.WON: "renewal_or_upsell",
        OpportunityStage.LOST: "loss_reason_documented",
        OpportunityStage.PARKED: "re_engagement_criteria",
    }
    return targets.get(stage, "manual_review")


def normalize_pipeline_lead(
    lead: Any,
    *,
    tenant_id: str,
    company_id: str,
    offer_id: str,
) -> CanonicalOpportunity:
    """Normalize a revenue pipeline ``Lead`` into a ``CanonicalOpportunity``.

    Parameters
    ----------
    lead:
        A ``Lead`` or any duck-typed object with ``id``, ``stage``,
        optionally ``sector``, ``region``, ``commitment_evidence``,
        ``payment_evidence``, ``expected_amount_sar``, ``slot_id``.
    tenant_id:
        The tenant scope for the resulting canonical opportunity.
    company_id:
        The canonical company_id this opportunity belongs to.
    offer_id:
        The canonical offer_id this opportunity is for.
    """
    lead_id = str(getattr(lead, "id", "") or "").strip()
    if not lead_id:
        raise ValueError("lead must have a non-empty id")

    raw_stage = str(getattr(lead, "stage", "warm_intro_selected") or "warm_intro_selected").strip()
    stage = _resolve_stage(raw_stage)

    commitment_evidence = str(getattr(lead, "commitment_evidence", "") or "").strip()
    payment_evidence = str(getattr(lead, "payment_evidence", "") or "").strip()

    has_commitment = bool(commitment_evidence)
    has_payment = bool(payment_evidence)

    score = _compute_score(
        stage=stage,
        has_commitment=has_commitment,
        has_payment=has_payment,
    )

    # Build score reasons
    score_reasons: dict[str, Any] = {
        "pipeline_stage": raw_stage,
        "canonical_stage": stage.value,
        "has_commitment_evidence": has_commitment,
        "has_payment_evidence": has_payment,
    }

    # Blockers
    blockers: list[str] = []
    if stage == OpportunityStage.LOST:
        blockers.append("deal_lost")
    if stage == OpportunityStage.PARKED:
        blockers.append("deal_parked")

    # Confidence band
    confidence_band = "low"
    if has_payment:
        confidence_band = "high"
    elif has_commitment or stage.value in ("conversation", "pilot", "proof", "commercial"):
        confidence_band = "medium"

    next_action = _derive_next_action(stage)
    proof_target = _derive_proof_target(stage)

    return CanonicalOpportunity(
        tenant_id=tenant_id,
        opportunity_id=f"opp_{lead_id}",
        company_id=company_id,
        company_name="",
        offer_id=offer_id,
        stage=stage,
        score=score,
        score_reasons=score_reasons,
        confidence_band=confidence_band,
        blockers=blockers,
        next_action=next_action,
        proof_target=proof_target,
        approval_required=True,
        external_action_allowed=False,
    )
