"""Engagement engine — the living, multi-channel commercial loop.

Given a set of accounts and (optionally) ongoing conversations and inbound
events, the engine uses the brain to decide the next best action per account,
opens or advances conversations on the recommended channel, prepares the exact
draft payloads, and produces a prioritised, unified action plan for the
command room.

It is the connective tissue that makes the system feel *alive* — one brain,
many channels, one worklist — while remaining draft-only and fail-closed.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

from app.commercial import conversation as convo
from app.commercial import icp_scoring, lead_sourcing
from app.commercial.engagement_schemas import OutboundPayload
from app.commercial.reasoning import CommercialBrain, get_brain
from app.commercial.safety import is_safe_default_environment, safe_defaults

# Motion → preferred channel order. WhatsApp only when opt-in exists.
_CHANNEL_PREFERENCE = ("email", "whatsapp", "linkedin_manual", "phone")


@dataclass
class EngagementResult:
    generated_at: str = ""
    accounts: list[Any] = field(default_factory=list)
    conversations: list[dict[str, Any]] = field(default_factory=list)
    payloads: list[dict[str, Any]] = field(default_factory=list)
    action_plan: list[dict[str, Any]] = field(default_factory=list)
    safety_ok: bool = True
    safety_violations: list[str] = field(default_factory=list)
    safety_posture: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "summary": {
                "accounts": len(self.accounts),
                "conversations": len(self.conversations),
                "payloads": len(self.payloads),
                "actions": len(self.action_plan),
                "safety_posture": self.safety_posture,
            },
            "action_plan": self.action_plan,
            "conversations": self.conversations,
            "payloads": self.payloads,
            "safety_ok": self.safety_ok,
            "safety_violations": self.safety_violations,
        }


def _choose_channel(account: Any) -> str:
    opt_in = bool(_g(account, "whatsapp_opt_in", False))
    has_email = bool(_g(account, "public_email")) and not _g(account, "email_opt_out", False)
    if has_email:
        return "email"
    if _g(account, "whatsapp") and opt_in:
        return "whatsapp"
    if _g(account, "linkedin_url"):
        return "linkedin_manual"
    if _g(account, "phone"):
        return "phone"
    return "email"


def run_engagement(
    account_records: list[Mapping[str, Any]],
    *,
    inbound_by_account: Mapping[str, list[Mapping[str, Any]]] | None = None,
    icp_rules: Mapping[str, Any] | None = None,
    client_rules: Mapping[str, Any] | None = None,
    brain: CommercialBrain | None = None,
    enforce_safe_defaults: bool = True,
) -> EngagementResult:
    """Run one pass of the living engagement loop."""
    inbound_by_account = inbound_by_account or {}
    brain = brain or get_brain()
    result = EngagementResult(
        generated_at=datetime.now(UTC).isoformat(),
        safety_posture=safe_defaults(),
    )

    if enforce_safe_defaults and not is_safe_default_environment():
        result.safety_ok = False
        posture = safe_defaults()
        result.safety_violations = [
            f"{k}={v}" for k, v in posture.items() if (k == "outbound_mode" and v != "draft_only") or (k != "outbound_mode" and v)
        ]
        return result

    accounts = lead_sourcing.load_accounts(account_records)
    for acc in accounts:
        icp_scoring.apply_score(acc, icp_rules)
    result.accounts = accounts

    for acc in accounts:
        motion = (_g(acc, "recommended_motion") or "sales_prospecting").strip() or "sales_prospecting"
        channel = _choose_channel(acc)

        conversation, payload = convo.start_conversation(
            acc, motion=motion, channel=channel, brain=brain, client_rules=client_rules
        )

        # Replay any provided inbound events through the engine.
        for event in inbound_by_account.get(_g(acc, "account_id"), []):
            text = str(event.get("text", ""))
            button_intent = event.get("button_intent")
            payload = convo.handle_inbound(
                conversation, inbound_text=text, account=acc, brain=brain,
                button_intent=button_intent, client_rules=client_rules,
            )

        rec = payload.safety.get("recommendation", {})
        result.conversations.append(conversation.to_dict())
        result.payloads.append(payload.to_dict())
        result.action_plan.append(
            {
                "account_id": _g(acc, "account_id"),
                "company": _g(acc, "company_name"),
                "conversation_id": conversation.conversation_id,
                "channel": channel,
                "motion": motion,
                "stage": conversation.stage,
                "recommended_action": rec.get("recommended_action", conversation.next_action),
                "priority": rec.get("priority", 3),
                "confidence": rec.get("confidence", 0.0),
                "rationale": rec.get("rationale", []),
                "risk_level": conversation.risk_level,
                "requires_approval": True,
                "send_status": payload.send_status,
                "safe_to_send_now": bool(payload.safety.get("allowed", False)),
            }
        )

    # Prioritise the action plan (1 = highest), then by confidence desc.
    result.action_plan.sort(key=lambda a: (a.get("priority", 3), -a.get("confidence", 0.0)))
    return result


def write_engagement_report(result: EngagementResult, out_dir: str | Path) -> dict[str, str]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "latest.json"
    md_path = out / "latest.md"
    json_path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_engagement_markdown(result), encoding="utf-8")
    return {"json": str(json_path), "md": str(md_path)}


def render_engagement_markdown(result: EngagementResult) -> str:
    p = result.safety_posture
    lines = [
        "# Dealix Commercial Growth OS — Living Engagement Room",
        "",
        f"_Generated: {result.generated_at}_",
        "",
        "## Safety posture (fail-closed)",
        "",
        f"- Outbound mode: **{p.get('outbound_mode')}**",
        f"- External send: **{p.get('external_send_enabled')}** · "
        f"Email: **{p.get('email_send_enabled')}** · "
        f"WhatsApp live: **{p.get('whatsapp_allow_live_send')}**",
        "",
        "## Summary",
        "",
        f"- Accounts: {len(result.accounts)}",
        f"- Conversations: {len(result.conversations)}",
        f"- Prepared payloads (drafts): {len(result.payloads)}",
        f"- Actions in plan: {len(result.action_plan)}",
        "",
        "## Prioritised next best actions",
        "",
    ]
    if result.action_plan:
        for i, a in enumerate(result.action_plan, 1):
            lines.append(
                f"{i}. **P{a['priority']}** [{a['channel']}/{a['motion']}] "
                f"{a['company']} → `{a['recommended_action']}` "
                f"(conf {a['confidence']:.0%}, risk {a['risk_level']}, "
                f"safe_to_send_now={a['safe_to_send_now']})"
            )
            if a.get("rationale"):
                lines.append(f"   - why: {' '.join(a['rationale'])}")
    else:
        lines.append("- None")
    lines += [
        "",
        "> Every action above is a **draft** prepared by the brain. Nothing has "
        "been sent on any channel; live transmission requires the safety gates "
        "and explicit approval.",
        "",
    ]
    return "\n".join(lines)


def _g(obj: Any, key: str, default: Any = "") -> Any:
    if isinstance(obj, Mapping):
        return obj.get(key, default)
    return getattr(obj, key, default)
