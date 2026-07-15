"""Pipeline orchestrator for the Launch Conversation & Negotiation Engine.

Runs the full internal, draft-only flow:
  safety guard -> company brain -> target scoring -> offer matching ->
  message generation -> objection handling -> negotiation planning ->
  proof building -> approval queue -> follow-up planning -> learning loop.

Never sends anything. Returns a single JSON-serializable payload.
"""

from __future__ import annotations

import datetime as _dt
from typing import Any

from dealix.conversation_engine import (
    approval_policy,
    company_brain,
    followup_planner,
    learning_loop,
    message_generator,
    negotiation_planner,
    offer_matcher,
    proof_builder,
    safety_guard,
    target_profile,
)


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def run(
    *,
    limit: int = 25,
    mode: str = "draft-only",
    env: dict[str, str] | None = None,
    targets: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    safety = safety_guard.evaluate_environment(env)

    payload: dict[str, Any] = {
        "generated_at": _now(),
        "mode": mode,
        "founder_email": company_brain.founder_email(),
        "safety": safety.as_dict(),
        "opportunities": [],
        "approval_queue": [],
        "negotiation_playbooks": [],
        "proof_packs": [],
        "followups": [],
        "email_drafts": [],
        "whatsapp_drafts": [],
    }

    if not safety.safe:
        payload["verdict"] = safety.verdict
        payload["highest_leverage_action"] = (
            "Disable all send/auto flags and set OUTBOUND_MODE=draft_only, then re-run."
        )
        payload["learning"] = learning_loop.reflect(payload)
        payload["summary"] = _summary(payload)
        return payload

    raw_targets = targets if targets is not None else company_brain.seed_targets()
    scored = target_profile.score_targets(raw_targets)[: max(0, limit)]

    approval_index = 1
    for scored_target in scored:
        match = offer_matcher.match_offer(scored_target)
        offer = match.get("primary_offer", {})
        channels_drafts = message_generator.build_all_channels(scored_target, offer)
        plan = negotiation_planner.build_plan(scored_target, match)
        proof = proof_builder.build_proof_pack(scored_target, match)
        approvals = approval_policy.build_approval_items(
            scored_target, match, channels_drafts, approval_index
        )
        approval_index += len(approvals)
        followups = followup_planner.build_followups(scored_target, channels_drafts)

        opportunity = dict(scored_target)
        opportunity["offer_match"] = {
            "primary_offer_id": match.get("primary_offer_id"),
            "match_score": match.get("match_score"),
            "rationale_ar": match.get("rationale_ar"),
        }
        opportunity["channels"] = channels_drafts
        payload["opportunities"].append(opportunity)
        payload["approval_queue"].extend(approvals)
        payload["negotiation_playbooks"].append(plan)
        payload["proof_packs"].append({"company": scored_target.get("company"), **proof})
        payload["followups"].extend(followups)

        email = channels_drafts.get("email", {})
        whatsapp = channels_drafts.get("whatsapp", {})
        payload["email_drafts"].append(
            {"company": scored_target.get("company"), "contact_name": scored_target.get("contact_name"), **email}
        )
        payload["whatsapp_drafts"].append(
            {"company": scored_target.get("company"), "contact_name": scored_target.get("contact_name"), **whatsapp}
        )

    payload["verdict"] = safety.verdict
    top = payload["opportunities"][0] if payload["opportunities"] else None
    payload["highest_leverage_action"] = (
        f"مراجعة واعتماد drafts لأعلى فرصة: {top['company']}"
        if top
        else "لا توجد فرص — أضف بيانات warm-list حقيقية."
    )
    payload["learning"] = learning_loop.reflect(payload)
    payload["summary"] = _summary(payload)
    return payload


def _summary(payload: dict[str, Any]) -> dict[str, Any]:
    approvals = payload.get("approval_queue", [])
    return {
        "opportunities": len(payload.get("opportunities", [])),
        "approval_items": len(approvals),
        "email_drafts": len(payload.get("email_drafts", [])),
        "whatsapp_drafts": len(payload.get("whatsapp_drafts", [])),
        "negotiation_playbooks": len(payload.get("negotiation_playbooks", [])),
        "proof_packs": len(payload.get("proof_packs", [])),
        "followups": len(payload.get("followups", [])),
        "all_external_require_approval": all(
            item.get("approval_required") for item in approvals
        ),
        "live_send": False,
    }
