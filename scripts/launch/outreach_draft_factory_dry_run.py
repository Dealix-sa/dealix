"""Dry-run: generate 3 sample outreach drafts for different channels.

Usage:
    python scripts/launch/outreach_draft_factory_dry_run.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dealix.launch_os.outreach_factory import TrustPreflightError, build_draft

SAMPLE_REQUESTS = [
    {
        "label": "Email — Revenue Leak Audit for Automotive",
        "account": {
            "account_id": "riyadh_motors_01",
            "account_name": "Riyadh Motors Group",
            "contact_name": "Ahmed Al-Otaibi",
            "sector": "automotive",
        },
        "offer_id": "REVENUE_LEAK_AUDIT",
        "channel": "email",
    },
    {
        "label": "LinkedIn Manual — Sales Command Center for Real Estate",
        "account": {
            "account_id": "golden_realty_02",
            "account_name": "Golden Realty Co",
            "contact_name": "Sara Al-Rashidi",
            "sector": "real_estate",
        },
        "offer_id": "SALES_COMMAND_CENTER",
        "channel": "linkedin_manual",
    },
    {
        "label": "Phone Script — WhatsApp Follow-Up OS for Clinics",
        "account": {
            "account_id": "clinic_care_03",
            "account_name": "Clinic Care Network",
            "contact_name": "Dr. Khalid",
            "sector": "healthcare_clinics",
        },
        "offer_id": "WHATSAPP_FOLLOWUP_OS",
        "channel": "phone",
    },
]


def main() -> None:
    print("=" * 65)
    print("DEALIX — Outreach Draft Factory Dry Run (3 Channels)")
    print("مصنع مسودات التواصل — 3 قنوات")
    print("=" * 65)

    for req in SAMPLE_REQUESTS:
        print(f"\n--- {req['label']} ---")
        try:
            draft = build_draft(
                account=req["account"],
                offer_id=req["offer_id"],
                channel=req["channel"],
            )
            print(f"  Draft ID:          {draft.id}")
            print(f"  Channel:           {draft.channel}")
            print(f"  Persona:           {draft.persona_id}")
            print(f"  Requires Approval: {draft.requires_approval}")
            print(f"  Trust Warnings:    {draft.trust_score}")
            print(f"  Subject (EN):      {draft.subject_en or '(no subject)'}")
            print(f"  Subject (AR):      {draft.subject_ar or '(no subject)'}")
            print(f"  Body preview (EN): {draft.body_en[:120].strip()}...")
            print(f"  Body preview (AR): {draft.body_ar[:120].strip()}...")
            print(f"  CTA (AR):          {draft.cta_ar}")
        except TrustPreflightError as exc:
            print(f"  [BLOCKED] {exc}")

    print("\n" + "=" * 65)


if __name__ == "__main__":
    main()
