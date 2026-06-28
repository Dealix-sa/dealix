#!/usr/bin/env python3
"""Generate Dealix commercial go-live pack from safe local data.

No network, no email, no WhatsApp, no external sends.
"""
from __future__ import annotations

import csv
import json
from datetime import UTC, date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "reports" / "commercial"
LEDGER_DIR = ROOT / "ledgers"

DEFAULT_PRODUCTS = [
    {
        "product": "Revenue Command Room OS",
        "wedge": "متابعات وعروض ضائعة",
        "first_offer": "7-Day Revenue Command Room Sprint",
        "price_range_sar": "5,000–12,000",
        "proof": "follow-up queue + CEO daily report + command room",
    },
    {
        "product": "Company Brain OS",
        "wedge": "قرارات إدارية غير واضحة",
        "first_offer": "14-Day Company Brain Sprint",
        "price_range_sar": "15,000–35,000",
        "proof": "daily decision + future radar + 30-day action plan",
    },
    {
        "product": "WhatsApp / Inbox Follow-up OS",
        "wedge": "واتساب وإيميل خارج القياس",
        "first_offer": "Follow-up Recovery Sprint",
        "price_range_sar": "3,000–9,000",
        "proof": "categorized conversations + reviewed reply drafts",
    },
    {
        "product": "AI Trust & Compliance OS",
        "wedge": "استخدام AI بدون سياسة",
        "first_offer": "AI Trust Setup Sprint",
        "price_range_sar": "5,000–15,000",
        "proof": "AI policy + approval gates + data handling SOP",
    },
]

DEFAULT_TARGETS = [
    {"sector": "clinics", "city": "Riyadh", "pain": "missed bookings and follow-ups", "offer": "Follow-up OS"},
    {"sector": "real estate", "city": "Riyadh", "pain": "lead leakage after first inquiry", "offer": "Revenue Command Room OS"},
    {"sector": "logistics", "city": "Riyadh/Jeddah", "pain": "proposal follow-up and B2B pipeline visibility", "offer": "Revenue Command Room OS"},
    {"sector": "training centers", "city": "Saudi Arabia", "pain": "registration follow-up and cohort sales", "offer": "WhatsApp / Inbox Follow-up OS"},
    {"sector": "marketing agencies", "city": "Saudi Arabia", "pain": "internal ops + client reporting", "offer": "Client Delivery OS"},
]


def ensure_ledgers() -> None:
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    prospects = LEDGER_DIR / "commercial_targets_template.csv"
    if not prospects.exists():
        with prospects.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "company_name",
                    "sector",
                    "city",
                    "website",
                    "source_url",
                    "verification_status",
                    "owner_decision",
                    "pain_hypothesis",
                    "recommended_product",
                    "next_action",
                ],
            )
            writer.writeheader()
            writer.writerow(
                {
                    "company_name": "Sample Clinic",
                    "sector": "clinics",
                    "city": "Riyadh",
                    "website": "https://example.com",
                    "source_url": "https://example.com/contact",
                    "verification_status": "ready_for_review",
                    "owner_decision": "review",
                    "pain_hypothesis": "booking follow-ups may be delayed",
                    "recommended_product": "WhatsApp / Inbox Follow-up OS",
                    "next_action": "manual review before outreach",
                }
            )


def build_markdown() -> str:
    today = date.today().isoformat()
    lines = [
        f"# Dealix Commercial Go-Live Pack — {today}",
        "",
        "## Executive verdict",
        "",
        "Dealix is ready for founder-led manual commercial execution when safety flags remain disabled, targets are verified, and drafts are reviewed by the founder before any external action.",
        "",
        "## Safety posture",
        "",
        "- Live outbound: disabled by default.",
        "- Email: drafts/review only unless future controlled-live PR enables it.",
        "- WhatsApp: draft-only unless opt-in + approved template + explicit controlled-live gates exist.",
        "- SMS: disabled.",
        "- Claims: no fake ROI, no fake clients, no guaranteed revenue.",
        "",
        "## Products to sell first",
        "",
        "| Product | Wedge | First offer | Price range SAR | Proof |",
        "|---|---|---|---:|---|",
    ]
    for p in DEFAULT_PRODUCTS:
        lines.append(f"| {p['product']} | {p['wedge']} | {p['first_offer']} | {p['price_range_sar']} | {p['proof']} |")
    lines += [
        "",
        "## First target sectors",
        "",
        "| Sector | City | Pain hypothesis | Offer |",
        "|---|---|---|---|",
    ]
    for t in DEFAULT_TARGETS:
        lines.append(f"| {t['sector']} | {t['city']} | {t['pain']} | {t['offer']} |")
    lines += [
        "",
        "## Founder actions today",
        "",
        "1. Pick one product wedge only: Revenue Command Room or Follow-up OS.",
        "2. Research 20 companies manually and record `source_url`.",
        "3. Approve 5–10 high-quality manual outreach drafts.",
        "4. Book discovery calls; do not sell a huge system on first touch.",
        "5. For every reply, log status, objection, next action, and proof needed.",
        "",
        "## Acceptance gates before sending",
        "",
        "- `source_url` exists.",
        "- `verification_status` is `ready_for_review` or `approved_to_send`.",
        "- `owner_decision` is `send` or `call`.",
        "- Email includes opt-out wording.",
        "- WhatsApp is not used unless opt-in exists.",
        "- No guaranteed ROI or fake social proof.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ensure_ledgers()
    md = build_markdown()
    (REPORT_DIR / "latest.md").write_text(md, encoding="utf-8")
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "ready_for_founder_manual_execution",
        "products": DEFAULT_PRODUCTS,
        "target_sectors": DEFAULT_TARGETS,
        "safety": {
            "external_send_enabled": False,
            "email_send_enabled": False,
            "whatsapp_send_enabled": False,
            "whatsapp_allow_live_send": False,
            "sms_send_enabled": False,
            "outbound_mode": "draft_only",
        },
    }
    (REPORT_DIR / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("COMMERCIAL_PACK_GENERATED=reports/commercial/latest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
