#!/usr/bin/env python3
"""Dealix Self-Operating Company OS runner.

This runner creates a realistic, approval-first operating cycle for Dealix.
It automates internal thinking, prioritisation, queue generation, draft planning,
proof logging, and commercial execution reports. It intentionally does not send,
publish, charge, merge, deploy, or mutate production.

Usage:
    python scripts/commercial/run_self_operating_company_os.py --mode draft-only --limit 50
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "reports" / "self_operating_company_os"
DATA_ROOT = ROOT / "data" / "self_operating_company_os"

FORBIDDEN_ENV_FLAGS = {
    "EXTERNAL_SEND_ENABLED": "true",
    "AUTO_WHATSAPP_ENABLED": "true",
    "AUTO_LINKEDIN_ENABLED": "true",
    "AUTO_PAYMENT_CAPTURE_ENABLED": "true",
    "AUTO_MERGE_ENABLED": "true",
    "PRODUCTION_MUTATION_ENABLED": "true",
}

PLAYBOOKS = [
    {
        "name": "production_trust",
        "goal": "Clear production, Railway, smoke, and security blockers before commercial scaling.",
        "priority": 100,
        "safe_actions": [
            "review PR #872 production-smoke API-key alignment",
            "review PR #858 Railway config foundation",
            "summarise failed or cancelled CI gates",
            "prepare next maintainer action",
        ],
        "approval_required_for": ["merge PR", "production config change", "secret update"],
        "kpi": "Production Smoke green on main and Railway config drift prevented.",
    },
    {
        "name": "first_paid_client",
        "goal": "Close the first 499 SAR Revenue Proof Sprint through manual payment and proof-pack delivery.",
        "priority": 95,
        "safe_actions": [
            "prepare 499 SAR offer brief",
            "prepare manual close checklist",
            "prepare payment evidence object",
            "prepare proof-pack delivery checklist",
        ],
        "approval_required_for": ["send offer", "send invoice", "mark payment received"],
        "kpi": "One confirmed payment received and proof pack delivered.",
    },
    {
        "name": "grand_targeting",
        "goal": "Build a ranked acquisition queue from safe sources and generate approval-ready drafts.",
        "priority": 90,
        "safe_actions": [
            "rank targets by fit, urgency, access, proof, and payment likelihood",
            "match each target to one offer",
            "generate draft-only outreach and follow-up actions",
            "route all external actions to approval queue",
        ],
        "approval_required_for": ["email", "WhatsApp", "LinkedIn", "phone", "meeting booking"],
        "kpi": "Top 10 reviewed targets and at least 3 founder-approved next actions.",
    },
    {
        "name": "market_access",
        "goal": "Target foreign companies and local Saudi companies with Market Access and Revenue Command offers.",
        "priority": 85,
        "safe_actions": [
            "identify foreign-market-entry candidates",
            "identify local B2B growth candidates",
            "create one-page Saudi opportunity snapshot drafts",
            "prepare partner/distributor desk recommendations",
        ],
        "approval_required_for": ["external outreach", "partner introduction", "commercial proposal"],
        "kpi": "Five high-fit market access opportunities ready for founder review.",
    },
    {
        "name": "content_and_proof",
        "goal": "Turn daily work into trust assets: proof packs, LinkedIn drafts, case notes, and SEO report drafts.",
        "priority": 80,
        "safe_actions": [
            "generate LinkedIn draft from proof evidence",
            "generate weekly proof-pack outline",
            "generate Saudi market insight draft",
            "generate one short founder update draft",
        ],
        "approval_required_for": ["publish post", "publish case study", "use client name"],
        "kpi": "Three proof-based content drafts and one proof-pack outline.",
    },
    {
        "name": "learning_loop",
        "goal": "Update priorities from replies, no-replies, meetings, invoices, payments, and proof-pack delivery.",
        "priority": 75,
        "safe_actions": [
            "record outcome placeholders",
            "adjust score rules",
            "identify repeated objections",
            "recommend tomorrow's highest-leverage action",
        ],
        "approval_required_for": ["change pricing", "change public promise", "change production workflow"],
        "kpi": "Tomorrow's plan reflects today's evidence.",
    },
]

OFFER_LADDER = [
    {"name": "Revenue Proof Sprint", "price": "499 SAR", "best_for": "first paid proof and quick manual close"},
    {"name": "Market Access Snapshot", "price": "499-1,500 SAR", "best_for": "foreign or Saudi market validation"},
    {"name": "Revenue Leak Diagnostic", "price": "4,999 SAR", "best_for": "companies with clear follow-up leakage"},
    {"name": "Saudi Market Entry Sprint", "price": "8,000-20,000 SAR", "best_for": "foreign B2B companies testing KSA"},
    {"name": "B2G Readiness Sprint", "price": "10,000-50,000 SAR", "best_for": "enterprise/B2G readiness without access claims"},
    {"name": "Revenue Command Room", "price": "monthly retainer", "best_for": "ongoing sales operations and proof packs"},
]

SEED_TARGETS = [
    {
        "company_name": "Warm inbound prospect",
        "target_type": "inbound",
        "sector": "Saudi B2B services",
        "pain_hypothesis": "Follow-up and proposal leakage after customer inquiries.",
        "source": "manual/warm",
        "urgency": 90,
        "accessibility": 85,
        "value": 70,
        "risk": 15,
    },
    {
        "company_name": "Local clinic or training center",
        "target_type": "local_b2b",
        "sector": "healthcare/training",
        "pain_hypothesis": "WhatsApp and call leads are not consistently followed up.",
        "source": "manual list",
        "urgency": 80,
        "accessibility": 75,
        "value": 65,
        "risk": 20,
    },
    {
        "company_name": "Foreign B2B SaaS entering KSA",
        "target_type": "foreign_market_entry",
        "sector": "software",
        "pain_hypothesis": "Needs Saudi market access, partner mapping, Arabic pitch, and first pilots.",
        "source": "approved public research",
        "urgency": 75,
        "accessibility": 60,
        "value": 90,
        "risk": 30,
    },
    {
        "company_name": "Saudi supplier seeking B2G readiness",
        "target_type": "b2g_readiness",
        "sector": "services/supply",
        "pain_hypothesis": "Needs capability statement, proposal readiness, and partner mapping.",
        "source": "manual/referral",
        "urgency": 70,
        "accessibility": 60,
        "value": 85,
        "risk": 35,
    },
]

@dataclass
class ActionItem:
    id: str
    playbook: str
    action: str
    owner: str
    status: str
    approval_required: bool
    risk_level: str

@dataclass
class TargetCard:
    id: str
    company_name: str
    target_type: str
    sector: str
    pain_hypothesis: str
    offer_fit: str
    score: int
    risk_level: str
    recommended_channel: str
    next_action: str
    approval_status: str


def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def date_stamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def ensure_dirs() -> None:
    for path in [OUT_ROOT / "daily", OUT_ROOT / "actions", OUT_ROOT / "approvals", OUT_ROOT / "targets", OUT_ROOT / "proof", OUT_ROOT / "content", DATA_ROOT]:
        path.mkdir(parents=True, exist_ok=True)


def env_tripwire() -> List[str]:
    violations = []
    for key, bad_value in FORBIDDEN_ENV_FLAGS.items():
        if os.getenv(key, "").strip().lower() == bad_value:
            violations.append(f"{key}={bad_value}")
    return violations


def load_targets() -> List[Dict[str, Any]]:
    path = DATA_ROOT / "targets.json"
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    return SEED_TARGETS


def pick_offer(target: Dict[str, Any]) -> str:
    target_type = target.get("target_type", "")
    if target_type == "foreign_market_entry":
        return "Market Access Snapshot"
    if target_type == "b2g_readiness":
        return "B2G Readiness Sprint"
    if target.get("urgency", 0) >= 85:
        return "Revenue Proof Sprint"
    return "Revenue Leak Diagnostic"


def score_target(target: Dict[str, Any]) -> int:
    urgency = int(target.get("urgency", 50))
    accessibility = int(target.get("accessibility", 50))
    value = int(target.get("value", 50))
    risk = int(target.get("risk", 30))
    proof_bonus = 10 if target.get("source") in {"manual/warm", "manual/referral"} else 0
    score = round((urgency * 0.30) + (accessibility * 0.25) + (value * 0.30) + proof_bonus - (risk * 0.15))
    return max(0, min(100, score))


def risk_level(score: int, target: Dict[str, Any]) -> str:
    risk = int(target.get("risk", 30))
    if risk >= 40:
        return "medium"
    if score >= 80:
        return "low"
    return "review"


def build_target_cards(limit: int) -> List[TargetCard]:
    cards: List[TargetCard] = []
    for idx, target in enumerate(load_targets()[:limit], start=1):
        score = score_target(target)
        offer = pick_offer(target)
        channel = "manual founder review"
        if target.get("target_type") == "inbound":
            channel = "reply to warm inbound only after approval"
        elif target.get("target_type") == "foreign_market_entry":
            channel = "LinkedIn/email draft for approval"
        cards.append(
            TargetCard(
                id=f"TGT-{idx:04d}",
                company_name=str(target.get("company_name", "Unknown target")),
                target_type=str(target.get("target_type", "unknown")),
                sector=str(target.get("sector", "unknown")),
                pain_hypothesis=str(target.get("pain_hypothesis", "needs discovery")),
                offer_fit=offer,
                score=score,
                risk_level=risk_level(score, target),
                recommended_channel=channel,
                next_action=f"Prepare founder-approved draft for {offer}",
                approval_status="pending_founder_review",
            )
        )
    return sorted(cards, key=lambda card: card.score, reverse=True)


def build_actions() -> List[ActionItem]:
    actions: List[ActionItem] = []
    counter = 1
    for playbook in sorted(PLAYBOOKS, key=lambda p: p["priority"], reverse=True):
        for action in playbook["safe_actions"][:3]:
            actions.append(
                ActionItem(
                    id=f"ACT-{counter:04d}",
                    playbook=playbook["name"],
                    action=action,
                    owner="Dealix OS",
                    status="queued_internal",
                    approval_required=False,
                    risk_level="low",
                )
            )
            counter += 1
    return actions


def build_approval_queue(cards: Iterable[TargetCard]) -> List[Dict[str, Any]]:
    queue: List[Dict[str, Any]] = []
    for card in cards:
        queue.append(
            {
                "target_id": card.id,
                "company_name": card.company_name,
                "action_type": "external_follow_up_draft",
                "channel": card.recommended_channel,
                "draft_text": build_draft(card),
                "risk_flags": ["external_action_requires_founder_approval", "no_auto_send"],
                "proof_to_attach": "Use only real proof pack or public Dealix docs; do not invent client proof.",
                "status": "pending_founder_approval",
            }
        )
    return queue


def build_draft(card: TargetCard) -> str:
    if card.target_type == "foreign_market_entry":
        return (
            f"Hi [Name], I am based in Riyadh and help B2B companies test Saudi market opportunities through a practical Dealix {card.offer_fit}. "
            f"For {card.company_name}, the likely opportunity is: {card.pain_hypothesis}. "
            "Would it be useful if I send a one-page Saudi opportunity snapshot?"
        )
    return (
        f"السلام عليكم [الاسم]، أشتغل على Dealix لمساعدة الشركات على ترتيب الفرص والمتابعة. "
        f"بالنسبة لـ {card.company_name}، الفرضية عندنا: {card.pain_hypothesis}. "
        f"أقترح نبدأ بـ {card.offer_fit} بشكل صغير وواضح، مع تقرير وإثبات عمل. هل يناسب أرسل لك صفحة مختصرة؟"
    )


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_daily_report(cards: List[TargetCard], actions: List[ActionItem], approvals: List[Dict[str, Any]], tripwire: List[str]) -> Path:
    today = date_stamp()
    path = OUT_ROOT / "daily" / f"{today}.md"
    lines = [
        f"# Dealix Self-Operating Company OS — {today}",
        "",
        "## Verdict",
        "SAFE_TO_RUN_INTERNAL_DRAFT_ONLY" if not tripwire else "HALTED_BY_ENV_TRIPWIRE",
        "",
        "## Operating rule",
        "Automate internal intelligence, scoring, drafting, proof logging, and reporting. Require founder approval for every external action.",
        "",
        "## Top commercial targets",
    ]
    for card in cards[:10]:
        lines.append(f"- **{card.id} — {card.company_name}** | score {card.score} | offer: {card.offer_fit} | next: {card.next_action}")
    lines.extend(["", "## Top internal actions"])
    for action in actions[:12]:
        lines.append(f"- **{action.id}** [{action.playbook}] {action.action}")
    lines.extend(["", "## Pending approval queue"])
    for item in approvals[:10]:
        lines.append(f"- **{item['target_id']}** {item['action_type']} via {item['channel']} — {item['status']}")
    lines.extend([
        "",
        "## Revenue focus",
        "1. Finish production trust: #872 then #858.",
        "2. Close first 499 SAR Revenue Proof Sprint through #873 manual payment + proof pack path.",
        "3. Use #871/#874 queues to pick the best founder-reviewed targets.",
        "4. Let #869 repeat the loop after payment/proof path is stable.",
        "",
        "## Forbidden actions",
        "- No cold WhatsApp.",
        "- No automated external sending.",
        "- No fake proof.",
        "- No guaranteed revenue claims.",
        "- No payment/revenue status before confirmed payment.",
        "- No production mutation or PR merge without explicit approval.",
    ])
    if tripwire:
        lines.extend(["", "## Tripwire violations", *[f"- {v}" for v in tripwire]])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def verify_outputs() -> Dict[str, Any]:
    today = date_stamp()
    required = [
        OUT_ROOT / "daily" / f"{today}.md",
        OUT_ROOT / "actions" / f"{today}.json",
        OUT_ROOT / "approvals" / f"{today}.json",
        OUT_ROOT / "targets" / f"{today}.json",
        OUT_ROOT / "proof" / f"{today}.json",
        OUT_ROOT / "content" / f"{today}.md",
    ]
    missing = [str(path) for path in required if not path.exists()]
    return {"ok": not missing, "missing": missing}


def write_content_queue(cards: List[TargetCard]) -> Path:
    today = date_stamp()
    path = OUT_ROOT / "content" / f"{today}.md"
    ideas = [
        "LinkedIn draft: Why Saudi B2B companies lose money in follow-up before they lose it in sales.",
        "Market insight draft: How foreign B2B companies should test Saudi demand before hiring or opening full operations.",
        "Founder update draft: Building Dealix as an approval-first revenue operating system, not a spam bot.",
    ]
    lines = [f"# Content queue — {today}", "", "All posts are drafts. Do not publish without founder approval.", ""]
    for idea in ideas:
        lines.append(f"- {idea}")
    lines.extend(["", "## Target-derived angles"])
    for card in cards[:5]:
        lines.append(f"- {card.sector}: {card.pain_hypothesis} -> {card.offer_fit}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    ensure_dirs()
    today = date_stamp()
    tripwire = env_tripwire()

    cards = build_target_cards(args.limit)
    actions = build_actions()
    approvals = build_approval_queue(cards)

    proof_log = {
        "generated_at": utc_stamp(),
        "mode": args.mode,
        "tripwire_violations": tripwire,
        "proof_rule": "append-only evidence; no revenue before payment_received; no closed_won before proof_pack_delivered",
        "safe_actions_count": len(actions),
        "target_count": len(cards),
        "approval_count": len(approvals),
    }

    write_json(OUT_ROOT / "targets" / f"{today}.json", [asdict(card) for card in cards])
    write_json(OUT_ROOT / "actions" / f"{today}.json", [asdict(action) for action in actions])
    write_json(OUT_ROOT / "approvals" / f"{today}.json", approvals)
    write_json(OUT_ROOT / "proof" / f"{today}.json", proof_log)
    write_content_queue(cards)
    report = write_daily_report(cards, actions, approvals, tripwire)
    verification = verify_outputs()

    summary = {
        "ok": verification["ok"] and not tripwire,
        "mode": args.mode,
        "daily_report": str(report.relative_to(ROOT)),
        "targets": len(cards),
        "actions": len(actions),
        "approvals": len(approvals),
        "missing": verification["missing"],
        "tripwire_violations": tripwire,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
