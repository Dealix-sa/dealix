"""Proof-of-value builder — assembles a proof pack that never claims fake results.

Validates every proof pack against the forbidden-claims list so no guaranteed
revenue / ROI language can slip through.
"""

from __future__ import annotations

from typing import Any

from dealix.conversation_engine import company_brain


def build_proof_pack(target: dict[str, Any], match: dict[str, Any]) -> dict[str, Any]:
    offer = match.get("primary_offer", {})
    rules = company_brain.proof_rules()

    pack = {
        "pain_hypothesis": target.get("pain_hypothesis_ar", ""),
        "evidence_source": target.get("source", "hypothesis"),
        "opportunity_score": target.get("score", 0),
        "offer_match": offer.get("name_en") or offer.get("id") or "",
        "draft_message": (
            "See channel drafts (email/whatsapp) in the approval queue."
        ),
        "expected_outcome": (
            "نتوقع اكتشاف نقاط تسرب في المتابعة وفرص مؤهلة إضافية — والهدف قياس التحسن."
        ),
        "what_we_will_measure": offer.get("measure_ar", rules.get("allowed_measures", [])),
        "what_client_provides": [
            "عينة leads/محادثات (10 كافية للبداية)",
            "توضيح نظام المتابعة الحالي",
            "اعتماد المؤسس قبل أي إرسال",
        ],
        "what_dealix_delivers": offer.get("deliverables_ar", []),
        "next_approval_needed": "اعتماد المؤسس على drafts قبل أي تواصل خارجي.",
    }

    violations = validate_proof_pack(pack)
    pack["safe"] = not violations
    pack["violations"] = violations
    return pack


def validate_proof_pack(pack: dict[str, Any]) -> list[str]:
    """Return a list of forbidden-claim violations (empty = clean)."""
    forbidden = [c.lower() for c in company_brain.proof_rules().get("forbidden_claims", [])]
    blob = " ".join(str(v).lower() for v in _flatten(pack))
    violations = []
    for claim in forbidden:
        if claim and claim in blob:
            violations.append(f"forbidden_claim:{claim}")
    return violations


def _flatten(value: Any) -> list[str]:
    out: list[str] = []
    if isinstance(value, dict):
        for v in value.values():
            out.extend(_flatten(v))
    elif isinstance(value, (list, tuple)):
        for v in value:
            out.extend(_flatten(v))
    else:
        out.append(str(value))
    return out
