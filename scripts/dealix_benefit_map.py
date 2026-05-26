from __future__ import annotations

import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports" / "readiness"


BENEFITS = [
    {
        "rank": 1,
        "area": "Revenue",
        "files": [
            "scripts/build_manual_send_queue.py",
            "scripts/triage_reply.py",
            "scripts/proposal_from_lead.py",
            "scripts/payment_request.py",
            "scripts/revenue_ledger.py",
        ],
        "why": "These move a prospect from message to proposal to payment.",
        "next_action": "Send 10 messages and update lead status after each one.",
    },
    {
        "rank": 2,
        "area": "Founder Focus",
        "files": [
            "scripts/hermes_founder_brief.py",
            "scripts/hermes_opportunity_radar.py",
            "scripts/hermes_score.py",
            "scripts/hermes_weekly_review.py",
        ],
        "why": "These reduce distraction and show the next best action.",
        "next_action": "Open the newest reports/founder/sami-command-brief file.",
    },
    {
        "rank": 3,
        "area": "Trust + Safety",
        "files": [
            "scripts/score_local_output.py",
            "scripts/local_generate_score_check.py",
            "scripts/ledger_guard.py",
            "scripts/hermes_trust_pack.py",
        ],
        "why": "These prevent unsafe claims, weak messages, and corrupted ledgers.",
        "next_action": "Run quality + governance before any external message.",
    },
    {
        "rank": 4,
        "area": "Delivery + Proof",
        "files": [
            "scripts/new_client_intake.py",
            "scripts/delivery_tracker.py",
            "scripts/generate_ai_trust_report.py",
            "scripts/proof_from_lead.py",
            "scripts/retainer_offer.py",
        ],
        "why": "These turn paid work into proof assets and retainer offers.",
        "next_action": "Use complete_delivery only after real delivery is done.",
    },
    {
        "rank": 5,
        "area": "Distribution",
        "files": [
            "scripts/hermes_partner_os.py",
            "scripts/hermes_partner_pack.py",
            "scripts/hermes_case_study.py",
            "scripts/hermes_productization_gate.py",
        ],
        "why": "These create partner leverage and prevent building SaaS too early.",
        "next_action": "Send 3 partner intros after your first 10 customer messages.",
    },
]


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Dealix/Hermes Benefit Map",
        "",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "This report ranks the files by direct business value right now.",
        "",
        "| Rank | Area | Why it matters | Next action |",
        "|---:|---|---|---|",
    ]

    for b in BENEFITS:
        lines.append(f"| {b['rank']} | {b['area']} | {b['why']} | {b['next_action']} |")

    for b in BENEFITS:
        lines += [
            "",
            f"## {b['rank']}. {b['area']}",
            "",
            f"**Why:** {b['why']}",
            "",
            "**Critical files:**",
            "",
        ]
        for f in b["files"]:
            exists = (ROOT / f).exists()
            lines.append(f"- `{f}` — {'OK' if exists else 'MISSING'}")
        lines += [
            "",
            f"**Next action:** {b['next_action']}",
        ]

    lines += [
        "",
        "## CEO Rule",
        "",
        "If an activity does not move Lead → Reply → Proposal → Payment → Delivery → Proof → Retainer, it belongs in backlog.",
    ]

    out = REPORTS / f"benefit-map-{time.strftime('%Y%m%d-%H%M%S')}.md"
    out.write_text("\n".join(lines), encoding="utf-8")

    print(f"DEALIX_BENEFIT_MAP={out}")
    print("DEALIX_BENEFIT_MAP=PASS")


if __name__ == "__main__":
    main()
