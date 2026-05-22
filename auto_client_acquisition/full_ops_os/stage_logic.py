"""Stage business logic for the Full Ops Sales System (stages 1-8).

Each handler turns the lead + accumulated state into a deterministic
output. ``metrics`` is audit-safe (labels, scores, counts — never PII or
free text); ``state`` is the full output, kept only in the run's
in-memory metadata. All 12 stages are wired: 1-8 sales pipeline, 9-12
delivery / proof / expansion / learning.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.adoption_os.adoption_score import (
    AdoptionDimensions,
    adoption_band,
    adoption_score,
)
from auto_client_acquisition.capital_os.asset_types import CapitalAssetType
from auto_client_acquisition.full_ops_os.pain import extract_pain
from auto_client_acquisition.full_ops_os.stages import Stage
from auto_client_acquisition.proof_architecture_os.proof_score import (
    EnterpriseProofDimensions,
    enterprise_proof_score,
    proof_score_band,
)
from auto_client_acquisition.revenue_os.scoring import score_account_row
from auto_client_acquisition.sales_os.qualification import qualify


@dataclass(frozen=True, slots=True)
class StageOutput:
    """Result of running one stage's business logic."""

    metrics: dict[str, Any] = field(default_factory=dict)
    state: dict[str, Any] = field(default_factory=dict)


Lead = dict[str, Any]
RunState = dict[str, Any]
StageHandler = Callable[[Lead, RunState], StageOutput]


def _h_signal_intake(lead: Lead, state: RunState) -> StageOutput:
    required = ("company_name", "source")
    missing = [k for k in required if not str(lead.get(k, "")).strip()]
    accepted = not missing
    return StageOutput(
        metrics={"accepted": accepted, "missing_fields": missing},
        state={"accepted": accepted, "missing_fields": missing},
    )


def _h_enrichment(lead: Lead, state: RunState) -> StageOutput:
    useful = ("sector", "city", "employee_count", "notes",
              "relationship_status", "request_text")
    present = [k for k in useful if str(lead.get(k, "")).strip()]
    coverage = round(len(present) / len(useful), 3)
    return StageOutput(
        metrics={
            "coverage": coverage,
            "present_count": len(present),
            "missing": [k for k in useful if k not in present],
        },
        state={"coverage": coverage, "present": present},
    )


def _h_scoring(lead: Lead, state: RunState) -> StageOutput:
    result = score_account_row(lead)
    return StageOutput(
        metrics={
            "score": result["score"],
            "reasons": result["reasons"],
            "risks": result["risks"],
        },
        state=result,
    )


def _h_pain(lead: Lead, state: RunState) -> StageOutput:
    result = extract_pain(str(lead.get("request_text", "")))
    payload = result.to_dict()
    return StageOutput(metrics=payload, state=payload)


def _h_qualification(lead: Lead, state: RunState) -> StageOutput:
    score = int(state.get(Stage.SCORING.name, {}).get("score", 0))
    pain_clear = bool(state.get(Stage.PAIN_EXTRACTION.name, {}).get("pain_clear", False))
    result = qualify(
        pain_clear=pain_clear,
        owner_present=bool(lead.get("owner_present", False)),
        data_available=bool(lead.get("data_available", False)),
        accepts_governance=bool(lead.get("accepts_governance", True)),
        has_budget=bool(lead.get("has_budget", False)),
        wants_safe_methods=bool(lead.get("wants_safe_methods", True)),
        proof_path_visible=score >= 50,
        retainer_path_visible=bool(lead.get("retainer_interest", False)),
        raw_request_text=str(lead.get("request_text", "")),
        sector=str(lead.get("sector", "")),
        city=str(lead.get("city", "")),
    )
    payload = result.to_dict()
    return StageOutput(
        metrics={
            "decision": payload["decision"],
            "score": payload["score"],
            "recommended_offer": payload["recommended_offer"],
            "reasons": payload["reasons"],
            "doctrine_violations": payload["doctrine_violations"],
        },
        state=payload,
    )


def _h_prioritization(lead: Lead, state: RunState) -> StageOutput:
    score = int(state.get(Stage.SCORING.name, {}).get("score", 0))
    decision = str(state.get(Stage.QUALIFICATION.name, {}).get("decision", ""))
    if decision in ("accept", "reframe") and score >= 70:
        priority = "P1"
    elif score >= 45 and decision not in ("reject", "refer_out"):
        priority = "P2"
    else:
        priority = "P3"
    return StageOutput(
        metrics={"priority": priority, "score": score, "decision": decision},
        state={"priority": priority},
    )


def _h_draft(lead: Lead, state: RunState) -> StageOutput:
    qual = state.get(Stage.QUALIFICATION.name, {})
    decision = str(qual.get("decision", ""))
    offer = str(qual.get("recommended_offer", "next_step")).replace("_", " ")
    company = str(lead.get("company_name", "")).strip() or "—"
    body_en = (
        f"Hi — regarding {company}: after a quick review, the next step we'd "
        f"suggest is {offer}. Would a short call work?"
    )
    body_ar = (
        f"مرحباً — بخصوص {company}: بعد مراجعة سريعة، الخطوة التالية المقترحة "
        f"هي {offer}. هل تناسبكم مكالمة قصيرة؟"
    )
    draft = {
        "subject": f"Dealix — next step for {company}",
        "body_ar": body_ar,
        "body_en": body_en,
    }
    return StageOutput(
        metrics={
            "draft_generated": True,
            "draft_chars": len(body_ar) + len(body_en),
            "for_decision": decision,
        },
        state={"draft": draft},
    )


def _h_approval_gate(lead: Lead, state: RunState) -> StageOutput:
    draft = state.get(Stage.DRAFT_GENERATION.name, {}).get("draft")
    return StageOutput(
        metrics={"gated": True, "has_draft": bool(draft)},
        state={"gated": True, "draft": draft},
    )


def _h_delivery(lead: Lead, state: RunState) -> StageOutput:
    draft = state.get(Stage.DRAFT_GENERATION.name, {}).get("draft")
    decision = str(state.get(Stage.QUALIFICATION.name, {}).get("decision", ""))
    return StageOutput(
        metrics={
            "stages_completed": len(state),
            "draft_ready": bool(draft),
            "decision": decision,
        },
        state={"delivery_ready": bool(draft), "decision": decision},
    )


def _h_proof(lead: Lead, state: RunState) -> StageOutput:
    score = int(state.get(Stage.SCORING.name, {}).get("score", 0))
    coverage = float(state.get(Stage.ENRICHMENT.name, {}).get("coverage", 0.0))
    qual = state.get(Stage.QUALIFICATION.name, {})
    decision = str(qual.get("decision", ""))
    no_violations = not qual.get("doctrine_violations")
    pain_count = int(state.get(Stage.PAIN_EXTRACTION.name, {}).get("signal_count", 0))
    intake_ok = bool(state.get(Stage.SIGNAL_INTAKE.name, {}).get("accepted", False))
    dims = EnterpriseProofDimensions(
        metric_clarity=score,
        source_clarity=90 if intake_ok else 40,
        evidence_quality=int(coverage * 100),
        governance_confidence=90 if no_violations else 20,
        business_relevance=85 if decision in ("accept", "reframe") else 45,
        before_after_comparison=min(100, pain_count * 30),
        retainer_linkage=80 if decision == "accept" else 40,
        limitations_honesty=80,
    )
    proof = enterprise_proof_score(dims)
    band = proof_score_band(proof)
    return StageOutput(
        metrics={
            "proof_score": proof,
            "proof_band": band,
            "proof_pack_ready": proof >= 70,
        },
        state={"proof_score": proof, "proof_band": band},
    )


def _h_expansion(lead: Lead, state: RunState) -> StageOutput:
    proof = int(state.get(Stage.PROOF.name, {}).get("proof_score", 0))
    score = int(state.get(Stage.SCORING.name, {}).get("score", 0))
    coverage = float(state.get(Stage.ENRICHMENT.name, {}).get("coverage", 0.0))
    decision = str(state.get(Stage.QUALIFICATION.name, {}).get("decision", ""))
    dims = AdoptionDimensions(
        executive_sponsor=80 if lead.get("owner_present") else 30,
        workflow_owner=80 if lead.get("owner_present") else 30,
        data_readiness=int(coverage * 100),
        user_engagement=score,
        approval_completion=70,
        proof_visibility=proof,
        monthly_cadence=70 if lead.get("retainer_interest") else 30,
        expansion_pull=85 if decision == "accept" else 40,
    )
    adopt = adoption_score(dims)
    band = adoption_band(adopt)
    retainer_ready = band in ("scale_account", "retainer_ready")
    return StageOutput(
        metrics={
            "adoption_score": adopt,
            "adoption_band": band,
            "retainer_ready": retainer_ready,
        },
        state={
            "adoption_score": adopt,
            "adoption_band": band,
            "retainer_ready": retainer_ready,
        },
    )


def _h_learning(lead: Lead, state: RunState) -> StageOutput:
    signals = list(state.get(Stage.PAIN_EXTRACTION.name, {}).get("signals", []))
    proof_band = str(state.get(Stage.PROOF.name, {}).get("proof_band", ""))
    decision = str(state.get(Stage.QUALIFICATION.name, {}).get("decision", ""))
    if proof_band == "case_candidate":
        asset = CapitalAssetType.PROOF_EXAMPLE.value
    elif decision == "accept":
        asset = CapitalAssetType.DRAFT_TEMPLATE.value
    else:
        asset = CapitalAssetType.SECTOR_INSIGHT.value
    return StageOutput(
        metrics={
            "friction_signals": signals,
            "capital_asset_candidate": asset,
            "learning_captured": True,
        },
        state={"capital_asset_candidate": asset},
    )


STAGE_HANDLERS: dict[Stage, StageHandler] = {
    Stage.SIGNAL_INTAKE: _h_signal_intake,
    Stage.ENRICHMENT: _h_enrichment,
    Stage.SCORING: _h_scoring,
    Stage.PAIN_EXTRACTION: _h_pain,
    Stage.QUALIFICATION: _h_qualification,
    Stage.PRIORITIZATION: _h_prioritization,
    Stage.DRAFT_GENERATION: _h_draft,
    Stage.APPROVAL_GATE: _h_approval_gate,
    Stage.DELIVERY: _h_delivery,
    Stage.PROOF: _h_proof,
    Stage.EXPANSION: _h_expansion,
    Stage.LEARNING: _h_learning,
}


def run_stage_logic(stage: Stage, lead: Lead, state: RunState) -> StageOutput:
    """Run the business logic for a stage."""
    return STAGE_HANDLERS[stage](lead, state)


__all__ = ["StageOutput", "STAGE_HANDLERS", "run_stage_logic"]
