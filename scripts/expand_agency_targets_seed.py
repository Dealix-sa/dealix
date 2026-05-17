#!/usr/bin/env python3
"""Ensure agency_accounts_seed.csv has at least 80 strategic rows (idempotent)."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.paths import AGENCY_TARGETS_CSV
from dealix.commercial_ops.targeting_csv import TARGET_FIELDS

MIN_ROWS = 80

_PROFILES: list[tuple[str, str, str, str, str]] = [
    ("agency_wedge", "العميل يسأل عن ROI بعد الحملة", "linkedin_manual", "A", "ten_lead_audit"),
    ("agency_wedge", "لا proof أسبوعي للعميل", "email_warm", "A", "agency_proof_pack"),
    ("direct_b2b", "متابعة أولى بطيئة", "email_warm", "B", "governed_diagnostic"),
    ("saas", "توسع AI بدون حوكمة", "linkedin_manual", "D", "executive_diagnostic"),
    ("crm_partner", "تنفيذ CRM قبل التشخيص", "email_warm", "C", "diagnostic_layer"),
    ("consulting_firm", "عملاء يطلبون أتمتة بلا أدلة", "email_warm", "A", "agency_proof_pack"),
    ("hospitality", "استفسارات MICE بلا owner", "phone_task", "B", "ten_lead_audit"),
    ("real_estate_developer", "جودة leads inbound", "email_warm", "B", "ten_lead_audit"),
    ("agency_partner", "co-sell عميل واحد", "partner_intro", "A", "partner_sprint"),
    ("marketing_agency", "ضغط inbound", "linkedin_manual", "A", "ten_lead_audit"),
    ("executive_governance", "مخاطر توسع AI", "partner_intro", "D", "executive_diagnostic"),
]


def _existing_companies(rows: list[dict[str, str]]) -> set[str]:
    return {(r.get("company") or "").strip().lower() for r in rows}


def _append_rows(rows: list[dict[str, str]], *, need: int) -> list[dict[str, str]]:
    companies = _existing_companies(rows)
    n = len(rows)
    slot = n + 1
    statuses = ["not_contacted", "message_drafted", "sent_manual", "replied", "meeting_booked"]
    priorities = ["high", "medium", "low"]
    channels_extra = ["inbound", "phone_task"]
    added = 0
    while len(rows) < MIN_ROWS and added < need + 20:
        seg, pain, channel, motion, offer = _PROFILES[(slot - 1) % len(_PROFILES)]
        if slot % 5 == 0:
            channel = channels_extra[slot % len(channels_extra)]
        company = f"هدف استراتيجي {slot}"
        key = company.lower()
        if key in companies:
            slot += 1
            continue
        rows.append(
            {
                "company": company,
                "contact": "REPLACE:contact",
                "segment": seg,
                "pain_hypothesis": pain,
                "channel": channel,
                "motion": motion,
                "offer_id": offer,
                "status": statuses[slot % len(statuses)],
                "next_action": "مسودة — موافقة قبل الإرسال",
                "next_action_date": "",
                "priority": priorities[slot % len(priorities)],
                "notes": f"seed strategic slot {slot}",
            }
        )
        companies.add(key)
        slot += 1
        added += 1
    return rows


def main() -> int:
    path = AGENCY_TARGETS_CSV
    if not path.is_file():
        print(f"FAIL: missing {path}")
        return 1
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    before = len(rows)
    if before >= MIN_ROWS:
        print(f"OK: rows={before} (already >= {MIN_ROWS})")
        return 0
    rows = _append_rows(rows, need=MIN_ROWS - before)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=TARGET_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"OK: expanded {before} -> {len(rows)} rows at {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
