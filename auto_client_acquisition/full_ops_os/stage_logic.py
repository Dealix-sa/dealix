"""Stage business logic for the Full Ops Sales System (stages 1-8).

Each handler turns the lead + accumulated state into a deterministic
output. ``metrics`` is audit-safe (labels, scores, counts — never PII or
free text); ``state`` is the full output, kept only in the run's
in-memory metadata. Stages 9-12 are stubbed here and wired in Wave 21.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.full_ops_os.pain import extract_pain
from auto_client_acquisition.full_ops_os.stages import Stage
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


def _h_stub(lead: Lead, state: RunState) -> StageOutput:
    # Stages 9-12 — delivery, proof, expansion, learning — wired in Wave 21.
    return StageOutput(metrics={"pending_wave": 21}, state={})


STAGE_HANDLERS: dict[Stage, StageHandler] = {
    Stage.SIGNAL_INTAKE: _h_signal_intake,
    Stage.ENRICHMENT: _h_enrichment,
    Stage.SCORING: _h_scoring,
    Stage.PAIN_EXTRACTION: _h_pain,
    Stage.QUALIFICATION: _h_qualification,
    Stage.PRIORITIZATION: _h_prioritization,
    Stage.DRAFT_GENERATION: _h_draft,
    Stage.APPROVAL_GATE: _h_approval_gate,
    Stage.DELIVERY: _h_stub,
    Stage.PROOF: _h_stub,
    Stage.EXPANSION: _h_stub,
    Stage.LEARNING: _h_stub,
}


def run_stage_logic(stage: Stage, lead: Lead, state: RunState) -> StageOutput:
    """Run the business logic for a stage."""
    return STAGE_HANDLERS[stage](lead, state)


__all__ = ["StageOutput", "STAGE_HANDLERS", "run_stage_logic"]
