#!/usr/bin/env python3
"""Dealix Client Company Operating OS runner.

This runner models the full daily company-service layer for a client:
- understand company profile,
- produce department tasks,
- recommend targets and reasons,
- generate negotiation strategy,
- produce approval cards for WhatsApp/email/dashboard,
- prepare drafts and proof logs.

It is intentionally approval-first. External sending is represented as approval cards;
this runner does not send messages, charge payments, or mutate production systems.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "reports" / "client_company_operating_os"
DATA_ROOT = ROOT / "data" / "client_company_operating_os"


@dataclass
class DepartmentMission:
    department: str
    daily_goal: str
    target_type: str
    why_it_matters: str
    recommended_action: str
    negotiation_strategy: str
    approval_prompt: str


@dataclass
class ApprovalCard:
    id: str
    department: str
    action_type: str
    target: str
    why: str
    benefit: str
    draft: str
    negotiation_strategy: str
    allowed_employee_replies: List[str]
    approval_required: bool
    external_send_enabled: bool


DEFAULT_COMPANY_PROFILE: Dict[str, Any] = {
    "company_name": "Example Client Company",
    "business_model": "B2B services",
    "target_customers": ["SMEs", "enterprise buyers", "strategic partners"],
    "active_departments": ["sales", "support", "marketing", "partnerships", "management"],
    "main_offer": "service/product sold to business customers",
    "current_channels": ["email", "WhatsApp", "website", "referrals", "LinkedIn"],
    "approval_owner": "assigned employee or founder",
    "risk_policy": "approval-first external actions",
}


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def ensure_dirs() -> None:
    for sub in ["daily", "approval_cards", "department_missions", "whatsapp_bot", "proof", "negotiation", "targets"]:
        (OUT_ROOT / sub).mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)


def load_company_profile() -> Dict[str, Any]:
    path = DATA_ROOT / "company_profile.json"
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return {**DEFAULT_COMPANY_PROFILE, **data}
        except json.JSONDecodeError:
            pass
    return DEFAULT_COMPANY_PROFILE


def build_department_missions(profile: Dict[str, Any]) -> List[DepartmentMission]:
    name = profile["company_name"]
    return [
        DepartmentMission(
            department="sales",
            daily_goal="Recover and progress revenue opportunities.",
            target_type="warm lead, stalled proposal, high-fit prospect",
            why_it_matters="Sales leakage usually happens after the first interest signal, not before it.",
            recommended_action="Rank top follow-ups, draft messages, prepare call script, and ask employee approval.",
            negotiation_strategy="Start with a small proof step, reduce risk, show operational value, then upsell.",
            approval_prompt=f"Approve contacting the top sales target for {name}?",
        ),
        DepartmentMission(
            department="support",
            daily_goal="Protect customer satisfaction and detect churn risks.",
            target_type="open ticket, repeated complaint, delayed response, high-value client",
            why_it_matters="Support conversations reveal product gaps, upsell chances, and retention risk.",
            recommended_action="Summarize issues, draft response, flag urgent cases, and recommend escalation.",
            negotiation_strategy="Acknowledge the pain, offer a clear next step, and avoid overpromising.",
            approval_prompt=f"Approve the support response draft for {name}?",
        ),
        DepartmentMission(
            department="marketing",
            daily_goal="Turn market intelligence and proof into content and campaigns.",
            target_type="sector pain, proof pack, customer objection, market event",
            why_it_matters="Content should come from real customer signals, not generic posting.",
            recommended_action="Generate post drafts, campaign angles, and proof-backed messaging.",
            negotiation_strategy="Position the company around a concrete pain and proof, not broad claims.",
            approval_prompt=f"Approve today's marketing draft for {name}?",
        ),
        DepartmentMission(
            department="partnerships",
            daily_goal="Find strategic partners that can multiply distribution or credibility.",
            target_type="complementary company, channel partner, platform, local distributor",
            why_it_matters="Partnerships can create leverage beyond one-by-one sales.",
            recommended_action="Map mutual value, draft partnership intro, and prepare meeting objective.",
            negotiation_strategy="Lead with mutual value, pilot scope, shared upside, and low-risk next step.",
            approval_prompt=f"Approve partnership outreach draft for {name}?",
        ),
        DepartmentMission(
            department="management",
            daily_goal="Give the owner a command-room view of work, risk, and money.",
            target_type="internal decision, blocked task, revenue risk, approval queue",
            why_it_matters="Owners need decisions, not dashboards full of noise.",
            recommended_action="Summarize today, top risks, top opportunities, approvals, and proof.",
            negotiation_strategy="Separate urgent from important; ask for one decision at a time.",
            approval_prompt=f"Review today's owner brief for {name}?",
        ),
    ]


def build_approval_cards(missions: List[DepartmentMission], profile: Dict[str, Any]) -> List[ApprovalCard]:
    company = profile["company_name"]
    cards: List[ApprovalCard] = []
    for idx, mission in enumerate(missions, start=1):
        target = f"{mission.target_type} for {company}"
        draft = (
            f"Department: {mission.department}\n"
            f"Target: {target}\n"
            f"Reason: {mission.why_it_matters}\n"
            f"Suggested action: {mission.recommended_action}\n"
            f"Negotiation: {mission.negotiation_strategy}"
        )
        if mission.department == "sales":
            draft = (
                "السلام عليكم [الاسم]، لاحظنا أن لديكم فرصة لتحسين المتابعة وتحويل الاهتمام إلى خطوات أوضح. "
                "نقترح نبدأ بخطوة صغيرة تثبت القيمة: ترتيب الفرص الحالية، تجهيز رسائل المتابعة، وتسليم Proof Pack واضح. "
                "هل يناسب نحدد مكالمة قصيرة؟"
            )
        elif mission.department == "partnerships":
            draft = (
                "السلام عليكم [الاسم]، نرى احتمال شراكة بيننا لأن خدماتنا تكمل بعضها وتقدر تفتح فرص توزيع أو قيمة مشتركة. "
                "أقترح اجتماع قصير نحدد فيه نطاق Pilot صغير وفائدة متبادلة واضحة."
            )
        elif mission.department == "support":
            draft = (
                "شكرًا لتوضيح المشكلة. فهمنا أن التحدي الأساسي هو [المشكلة]. "
                "الخطوة المقترحة: [حل واضح] خلال [مدة]. سنحدثك بالنتيجة ونوثق ما تم."
            )
        cards.append(
            ApprovalCard(
                id=f"APP-{idx:04d}",
                department=mission.department,
                action_type="approve_edit_reject_or_explain",
                target=target,
                why=mission.why_it_matters,
                benefit=mission.daily_goal,
                draft=draft,
                negotiation_strategy=mission.negotiation_strategy,
                allowed_employee_replies=["approve", "edit", "reject", "explain", "better_draft", "negotiation", "schedule_follow_up", "mark_done"],
                approval_required=True,
                external_send_enabled=False,
            )
        )
    return cards


def build_whatsapp_bot_spec(cards: List[ApprovalCard]) -> Dict[str, Any]:
    return {
        "purpose": "Employee command interface for approving, editing, rejecting, and understanding Dealix actions.",
        "default_external_send_enabled": False,
        "commands": {
            "اليوم": "Show top department actions and approvals.",
            "ليش": "Explain why an action is recommended.",
            "فايدة": "Explain expected business value.",
            "تفاوض": "Generate negotiation strategy.",
            "عدل": "Ask for a revised draft.",
            "وافق": "Approve an action for controlled execution.",
            "ارفض": "Reject an action and capture reason.",
            "اثبات": "Show proof/evidence linked to the action.",
        },
        "sample_cards": [asdict(card) for card in cards[:3]],
    }


def build_daily_report(profile: Dict[str, Any], missions: List[DepartmentMission], cards: List[ApprovalCard]) -> Path:
    d = today()
    path = OUT_ROOT / "daily" / f"{d}.md"
    lines = [
        f"# Dealix Client Company Operating OS - {profile['company_name']} - {d}",
        "",
        "## Operating verdict",
        "DRAFT_ONLY_APPROVAL_FIRST",
        "",
        "## What the system is doing today",
        "The system is preparing cross-department work for sales, support, marketing, partnerships, and management. Every external action is routed to employee approval before execution.",
        "",
        "## Department missions",
    ]
    for mission in missions:
        lines.extend([
            f"### {mission.department}",
            f"- Goal: {mission.daily_goal}",
            f"- Target type: {mission.target_type}",
            f"- Why: {mission.why_it_matters}",
            f"- Action: {mission.recommended_action}",
            f"- Negotiation: {mission.negotiation_strategy}",
            "",
        ])
    lines.extend(["## Employee approval cards", ""])
    for card in cards:
        lines.extend([
            f"### {card.id} - {card.department}",
            f"- Target: {card.target}",
            f"- Why: {card.why}",
            f"- Benefit: {card.benefit}",
            f"- External send enabled: {card.external_send_enabled}",
            f"- Replies: {', '.join(card.allowed_employee_replies)}",
            "",
        ])
    lines.extend([
        "## Proof rule",
        "No claim, closed-won status, client name, or revenue number should be used without evidence.",
        "",
        "## Next build step",
        "Connect this approval-card model to Gmail drafts, CRM rows, WhatsApp command bot, and controlled-live senders in separate gated PRs.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    args = parser.parse_args()

    ensure_dirs()
    profile = load_company_profile()
    missions = build_department_missions(profile)
    cards = build_approval_cards(missions, profile)
    whatsapp_spec = build_whatsapp_bot_spec(cards)
    report = build_daily_report(profile, missions, cards)
    d = today()

    write_json(OUT_ROOT / "department_missions" / f"{d}.json", [asdict(mission) for mission in missions])
    write_json(OUT_ROOT / "approval_cards" / f"{d}.json", [asdict(card) for card in cards])
    write_json(OUT_ROOT / "whatsapp_bot" / f"{d}.json", whatsapp_spec)
    write_json(OUT_ROOT / "proof" / f"{d}.json", {
        "generated_at": now(),
        "mode": args.mode,
        "external_send_enabled": False,
        "approval_required": True,
        "proof_rule": "No claim or outcome without evidence.",
    })

    summary = {
        "ok": True,
        "mode": args.mode,
        "generated_at": now(),
        "company_name": profile["company_name"],
        "daily_report": str(report.relative_to(ROOT)),
        "department_missions": len(missions),
        "approval_cards": len(cards),
        "whatsapp_command_interface_ready": True,
        "external_send_enabled": False,
    }
    write_json(OUT_ROOT / "targets" / f"{d}.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
