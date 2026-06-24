#!/usr/bin/env python3
"""Generate a safe daily targeting plan for Dealix.

This creates a plan only. It does not fetch targets and does not contact anyone.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "reports" / "commercial"

SECTOR_WEDGES = [
    {
        "sector": "clinics",
        "search_goal": 20,
        "pain_hypothesis": "booking and patient follow-up delays",
        "offer": "WhatsApp / Inbox Follow-up OS",
        "first_message_angle": "ترتيب المتابعات بدون تغيير أنظمتكم الحالية",
    },
    {
        "sector": "real_estate",
        "search_goal": 20,
        "pain_hypothesis": "lead leakage after first inquiry",
        "offer": "Revenue Command Room OS",
        "first_message_angle": "توضيح العملاء الساخنين والمتابعات المتأخرة يوميا",
    },
    {
        "sector": "logistics",
        "search_goal": 15,
        "pain_hypothesis": "B2B proposals need structured follow-up",
        "offer": "Revenue Command Room OS",
        "first_message_angle": "غرفة قيادة للعروض والمتابعات والفرص",
    },
    {
        "sector": "training_centers",
        "search_goal": 15,
        "pain_hypothesis": "registrations and cohort sales need follow-up discipline",
        "offer": "Follow-up Recovery Sprint",
        "first_message_angle": "تحويل الاستفسارات إلى queue متابعة قابلة للقياس",
    },
    {
        "sector": "marketing_agencies",
        "search_goal": 15,
        "pain_hypothesis": "client delivery and reporting needs repeatable operating system",
        "offer": "Client Delivery OS",
        "first_message_angle": "تسليم عملاء أوضح وproof pack أسبوعي",
    },
    {
        "sector": "b2b_services",
        "search_goal": 15,
        "pain_hypothesis": "pipeline visibility and proposal follow-up are unclear",
        "offer": "Revenue Command Room OS",
        "first_message_angle": "أول 10 إجراءات اليوم من pipeline واحد واضح",
    },
]


def build_markdown() -> str:
    today = date.today().isoformat()
    lines = [
        f"# Dealix Daily Targeting Plan — {today}",
        "",
        "## Operating rule",
        "",
        "Research 100 companies. Verify 40. Draft 25. Manually approve 10-15. Do not automate live sending.",
        "",
        "## Sector allocation",
        "",
        "| Sector | Research goal | Pain hypothesis | Offer | Message angle |",
        "|---|---:|---|---|---|",
    ]
    for item in SECTOR_WEDGES:
        lines.append(
            f"| {item['sector']} | {item['search_goal']} | {item['pain_hypothesis']} | {item['offer']} | {item['first_message_angle']} |"
        )
    lines += [
        "",
        "## Manual approval checklist",
        "",
        "- source_url exists",
        "- verification_status is ready_for_review or approved_to_send",
        "- owner_decision is review before send",
        "- no guaranteed revenue claim",
        "- no fake customer proof",
        "- opt-out wording exists for email",
        "- WhatsApp requires opt-in",
        "",
        "## Founder execution block",
        "",
        "1. Research the first 30 targets before writing any message.",
        "2. Pick 10 best-fit targets only.",
        "3. Write one pain-specific draft per company.",
        "4. Send manually only after review.",
        "5. Log every reply, objection, and next action.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "plan_only_no_contact",
        "research_total": sum(item["search_goal"] for item in SECTOR_WEDGES),
        "sector_wedges": SECTOR_WEDGES,
        "manual_send_limit": "10-15 after founder review",
    }
    (OUT_DIR / "daily_targeting_plan.md").write_text(build_markdown(), encoding="utf-8")
    (OUT_DIR / "daily_targeting_plan.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("TARGETING_PLAN_GENERATED=reports/commercial/daily_targeting_plan.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
