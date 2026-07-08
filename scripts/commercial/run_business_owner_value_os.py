#!/usr/bin/env python3
"""Dealix Business Owner Value OS.

This runner turns Dealix from a collection of automation ideas into a business-owner
value engine: it translates each product capability into a measurable outcome,
controlled action queue, owner-facing report, and proof requirement.

It does not send external messages or perform live changes. It prepares a controlled
outbound queue that can later be executed only by an approved live-sender PR and
explicit founder approval.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "reports" / "business_owner_value_os"


@dataclass
class ValueModule:
    name: str
    owner_pain: str
    dealix_capability: str
    measurable_value: str
    proof_required: str
    first_offer: str
    risk_control: str


@dataclass
class ControlledOutboundAction:
    id: str
    audience: str
    channel: str
    purpose: str
    draft: str
    approval_required: bool
    live_send_allowed_now: bool
    safety_reason: str


VALUE_MODULES: List[ValueModule] = [
    ValueModule(
        name="Revenue Follow-up Recovery",
        owner_pain="Leads arrive through WhatsApp, calls, website forms, or referrals, then get lost or followed up too late.",
        dealix_capability="Central queue that ranks follow-ups, drafts replies, and shows next action.",
        measurable_value="More replies, fewer lost inquiries, faster follow-up, and visible daily pipeline.",
        proof_required="Before/after follow-up queue, list of reviewed leads, drafts created, actions approved, replies received.",
        first_offer="Revenue Proof Sprint - 499 SAR",
        risk_control="No auto-send; founder/client approves all outbound actions.",
    ),
    ValueModule(
        name="Owner Command Room",
        owner_pain="The owner does not know what happened today, who needs follow-up, what is blocked, or where money is leaking.",
        dealix_capability="Daily owner brief with top opportunities, risks, pending approvals, and proof evidence.",
        measurable_value="Clear operating rhythm and fewer missed commercial decisions.",
        proof_required="Daily report, action queue, approval queue, proof log, and weekly summary.",
        first_offer="Revenue Leak Diagnostic - 4,999 SAR",
        risk_control="Reports are internal until the owner approves sharing.",
    ),
    ValueModule(
        name="Market Access Desk",
        owner_pain="A foreign or local company wants to enter a market but does not know which customers, partners, or message to start with.",
        dealix_capability="Market access snapshot, target scoring, partner mapping, Arabic/English drafts, and proof-backed action plan.",
        measurable_value="Lower expansion risk and faster first pilot conversation.",
        proof_required="Target list, scorecard, source notes, one-page snapshot, approved drafts.",
        first_offer="Market Access Snapshot - 499-1,500 SAR",
        risk_control="No government-access claims; no scraped/bought lists; all sources documented.",
    ),
    ValueModule(
        name="B2G Readiness",
        owner_pain="The company wants enterprise/government opportunities but lacks capability statement, proposal discipline, and partner readiness.",
        dealix_capability="B2G readiness checklist, capability statement draft, partner map, proposal requirements summary.",
        measurable_value="Better readiness for qualified opportunities without risky claims.",
        proof_required="Checklist, gap report, capability statement draft, partner shortlist.",
        first_offer="B2G Readiness Sprint - 10k-50k SAR",
        risk_control="No promises of awards, influence, or special access.",
    ),
    ValueModule(
        name="Proof Pack Delivery",
        owner_pain="The owner cannot easily see what was delivered, what changed, or what value was created.",
        dealix_capability="Proof pack that documents inputs, actions, decisions, outputs, and measurable evidence.",
        measurable_value="Trust, retention, renewal, and upsell evidence.",
        proof_required="Append-only evidence trail with payment and delivery status.",
        first_offer="Included in every paid sprint.",
        risk_control="No fake proof and no client names without permission.",
    ),
]


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def ensure_dirs() -> None:
    for sub in ["daily", "value_modules", "controlled_outbound", "owner_briefs"]:
        (OUT_ROOT / sub).mkdir(parents=True, exist_ok=True)


def build_controlled_outbound_queue() -> List[ControlledOutboundAction]:
    return [
        ControlledOutboundAction(
            id="OUT-0001",
            audience="Warm inbound / referral lead",
            channel="email_or_linkedin_manual",
            purpose="Offer 499 SAR Revenue Proof Sprint",
            draft="السلام عليكم [الاسم]، عندي تجربة صغيرة من Dealix تساعدكم تشوفون وين تضيع فرص المتابعة خلال فترة قصيرة، مع تقرير واضح و Proof Pack. نبدأ بـ 499 ريال فقط كاختبار عملي. هل يناسب أرسل لك صفحة مختصرة؟",
            approval_required=True,
            live_send_allowed_now=False,
            safety_reason="External sending requires founder approval and a separate controlled-live sender implementation.",
        ),
        ControlledOutboundAction(
            id="OUT-0002",
            audience="Local B2B owner",
            channel="email_or_linkedin_manual",
            purpose="Diagnose revenue/follow-up leakage",
            draft="السلام عليكم [الاسم]، Dealix يساعد صاحب العمل يعرف يوميًا: من يحتاج متابعة؟ أين تضيع الفرص؟ ماذا نرسل؟ وما الدليل على العمل المنجز؟ أقدر أرسل لك نموذج صفحة واحدة يوضح الفكرة على شركتكم؟",
            approval_required=True,
            live_send_allowed_now=False,
            safety_reason="Manual/warm context only; no cold WhatsApp or mass automation.",
        ),
        ControlledOutboundAction(
            id="OUT-0003",
            audience="Foreign B2B company considering Saudi",
            channel="email_or_linkedin_manual",
            purpose="Market Access Snapshot",
            draft="Hi [Name], I help B2B companies test Saudi market opportunities through a practical Dealix Market Access Snapshot: target accounts, partner hypotheses, localized positioning, and next-step recommendations. Would it be useful if I send a one-page snapshot for [Company]?",
            approval_required=True,
            live_send_allowed_now=False,
            safety_reason="No auto-send and no scraped contact lists; founder approval required.",
        ),
    ]


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_owner_brief(modules: List[ValueModule], outbound: List[ControlledOutboundAction]) -> Path:
    d = today()
    path = OUT_ROOT / "owner_briefs" / f"{d}.md"
    lines = [
        f"# Dealix Business Owner Value Brief - {d}",
        "",
        "## What Dealix sells to a business owner",
        "Dealix is an AI operating system that helps the owner stop losing opportunities after interest appears. It turns inquiries, follow-ups, proposals, and proof into a daily operating rhythm.",
        "",
        "## Core owner value",
        "1. Know what happened today.",
        "2. Know who needs follow-up.",
        "3. Know what to send next.",
        "4. Know where revenue is leaking.",
        "5. Get proof of work before paying for bigger automation.",
        "",
        "## Value modules",
    ]
    for module in modules:
        lines.extend([
            f"### {module.name}",
            f"- Owner pain: {module.owner_pain}",
            f"- Dealix capability: {module.dealix_capability}",
            f"- Measurable value: {module.measurable_value}",
            f"- First offer: {module.first_offer}",
            f"- Proof required: {module.proof_required}",
            f"- Risk control: {module.risk_control}",
            "",
        ])
    lines.extend(["## Controlled outbound queue", ""])
    for item in outbound:
        lines.extend([
            f"### {item.id} - {item.purpose}",
            f"- Audience: {item.audience}",
            f"- Channel: {item.channel}",
            f"- Approval required: {item.approval_required}",
            f"- Live send allowed now: {item.live_send_allowed_now}",
            f"- Safety: {item.safety_reason}",
            "",
        ])
    lines.extend([
        "## Next commercial move",
        "Use the 499 SAR Revenue Proof Sprint for the first paid proof, then upsell to Revenue Leak Diagnostic or Revenue Command Room based on evidence.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    args = parser.parse_args()

    ensure_dirs()
    d = today()
    outbound = build_controlled_outbound_queue()

    write_json(OUT_ROOT / "value_modules" / f"{d}.json", [asdict(module) for module in VALUE_MODULES])
    write_json(OUT_ROOT / "controlled_outbound" / f"{d}.json", [asdict(item) for item in outbound])
    brief = write_owner_brief(VALUE_MODULES, outbound)

    summary: Dict[str, Any] = {
        "ok": True,
        "mode": args.mode,
        "generated_at": now(),
        "owner_brief": str(brief.relative_to(ROOT)),
        "value_modules": len(VALUE_MODULES),
        "controlled_outbound_items": len(outbound),
        "live_send_enabled": False,
        "external_actions_require_approval": True,
    }
    write_json(OUT_ROOT / "daily" / f"{d}.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
