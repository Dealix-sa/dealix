"""Dry-run: run 3 sample drafts through trust preflight and show violations.

Usage:
    python scripts/launch/trust_preflight_dry_run.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dealix.launch_os.trust_preflight import run_preflight

SAMPLE_DRAFTS = [
    {
        "name": "Clean email draft",
        "draft": {
            "channel": "email",
            "subject": "Sales system improvement for Acme Motors",
            "body": "We can help you improve your lead follow-up process.",
            "body_ar": "يمكننا مساعدتك في تحسين متابعة العملاء المحتملين.",
            "evidence_level": "L3",
            "drafted_by": "founder",
            "pricing_status": "approved_range_required",
            "approval_required": False,
        },
    },
    {
        "name": "Guarantee language violation",
        "draft": {
            "channel": "email",
            "subject": "We guarantee ROI in 30 days",
            "body": "Our system guarantees you will double your revenue.",
            "body_ar": "نضمن لك مضاعفة إيراداتك خلال 30 يوماً.",
            "evidence_level": "L1",
            "drafted_by": "",
            "pricing_status": "draft_only",
            "approval_required": False,
        },
    },
    {
        "name": "WhatsApp without consent",
        "draft": {
            "channel": "whatsapp_after_consent",
            "subject": "",
            "body": "Hello, we wanted to follow up on our conversation.",
            "body_ar": "مرحباً، أردنا المتابعة بشأن حديثنا السابق.",
            "evidence_level": "L2",
            "drafted_by": "founder",
            "pricing_status": "approved_range_required",
            "approval_required": False,
            "consent_record_ref": "",  # Missing — should trigger R05
        },
    },
]


def main() -> None:
    print("=" * 65)
    print("DEALIX — Trust Preflight Dry Run (3 Sample Drafts)")
    print("بوابة الثقة — 3 مسودات تجريبية")
    print("=" * 65)

    for sample in SAMPLE_DRAFTS:
        name = sample["name"]
        draft = sample["draft"]
        passed, violations = run_preflight(draft)

        status = "PASS" if passed else "BLOCKED"
        print(f"\n[{status}] {name}")
        print(f"  Channel: {draft.get('channel')}")
        if violations:
            print(f"  Violations ({len(violations)}):")
            for v in violations:
                icon = "BLOCK" if v.severity == "block" else "WARN"
                print(f"    [{icon}] {v.rule_id}: {v.message_en}")
        else:
            print("  Violations: none")

    print("\n" + "=" * 65)
    print("Legend: BLOCK = hard stop; WARN = advisory only")


if __name__ == "__main__":
    main()
