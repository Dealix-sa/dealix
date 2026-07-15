"""Objection handler — returns structured responses from the objection bank."""

from __future__ import annotations

from typing import Any

from dealix.conversation_engine import company_brain


def handle_objection(objection_id: str) -> dict[str, Any] | None:
    for ob in company_brain.objections():
        if ob.get("id") == objection_id:
            return _shape(ob)
    return None


def handle_by_trigger(trigger_text: str) -> dict[str, Any] | None:
    text = (trigger_text or "").strip()
    for ob in company_brain.objections():
        if ob.get("trigger_ar", "") and ob["trigger_ar"] in text:
            return _shape(ob)
    return None


def all_objection_responses() -> list[dict[str, Any]]:
    return [_shape(ob) for ob in company_brain.objections()]


def relevant_objections(target: dict[str, Any], offer: dict[str, Any]) -> list[dict[str, Any]]:
    """Objections most likely to surface for this target/offer.

    Always includes price, proof, and the two trust objections (send-on-behalf,
    data-permissions) because those are the recurring Dealix trust questions.
    """
    always = {"price_high", "prove_value", "send_on_our_behalf", "data_permissions"}
    picks = [ob for ob in company_brain.objections() if ob.get("id") in always]
    if offer.get("id") == "b2g_readiness_sprint":
        extra = company_brain.objections()
        for ob in extra:
            if ob.get("id") == "guarantee_results":
                picks.append(ob)
    return [_shape(ob) for ob in picks]


def _shape(ob: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": ob.get("id", ""),
        "trigger_ar": ob.get("trigger_ar", ""),
        "understanding_ar": ob.get("understanding_ar", ""),
        "short_ar": ob.get("short_ar", ""),
        "detailed_ar": ob.get("detailed_ar", ""),
        "followup_question_ar": ob.get("followup_question_ar", ""),
        "negotiation_move": ob.get("negotiation_move", ""),
        "proof_needed": ob.get("proof_needed", ""),
        "risk_flags": ["draft_only", "no_guarantee"],
    }
