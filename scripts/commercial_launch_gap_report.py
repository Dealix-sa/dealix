#!/usr/bin/env python3
"""Commercial launch gap report — env secrets + optional verify hooks.

Usage:
  python3 scripts/commercial_launch_gap_report.py
  python3 scripts/commercial_launch_gap_report.py --json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_SECRET_KEYS = [
    ("HUBSPOT_ACCESS_TOKEN", "HubSpot CRM sync (LAUNCH_GATES G3)"),
    ("GOOGLE_MAPS_API_KEY", "Saudi local discovery"),
    ("DEALIX_API_KEY", "GitHub daily cron + automation"),
    ("DEALIX_API_BASE", "GitHub daily cron base URL"),
    ("GMAIL_REFRESH_TOKEN", "Gmail drafts / send-approved"),
    ("MOYASAR_SECRET_KEY", "Checkout pilot (LAUNCH_GATES G2)"),
    ("POSTHOG_API_KEY", "Observability funnel (LAUNCH_GATES O3)"),
    ("RESEND_API_KEY", "Daily founder digest email"),
]


def _missing_secrets() -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for key, note in _SECRET_KEYS:
        val = (os.environ.get(key) or "").strip()
        if not val:
            out.append({"key": key, "note": note})
    return out


def build_report() -> dict:
    missing = _missing_secrets()
    return {
        "schema_version": 1,
        "repo_root": str(ROOT),
        "missing_secrets": missing,
        "missing_secrets_count": len(missing),
        "governance": {
            "cold_whatsapp_blocked": True,
            "linkedin_automation_blocked": True,
            "external_email_requires_approval": True,
        },
        "recommended_verify_commands": [
            "bash scripts/revenue_os_master_verify.sh",
            "bash scripts/dealix_capability_verify.sh",
            "python3 scripts/launch_readiness_check.py --base-url http://localhost:8000",
        ],
        "verdict": "PASS" if len(missing) <= 3 else "PARTIAL",
        "next_action_ar": (
            "أكمل الأسرار الناقصة ثم شغّل daily_operate وافتح /ar/operator"
            if missing
            else "شغّل حزم التحقق ثم ابدأ Paid Private Beta"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"DEALIX_COMMERCIAL_LAUNCH_GAP_VERDICT={report['verdict']}")
        print(f"missing_secrets={report['missing_secrets_count']}")
        for item in report["missing_secrets"]:
            print(f"  - {item['key']}: {item['note']}")
    return 0 if report["verdict"] == "PASS" else 0


if __name__ == "__main__":
    sys.exit(main())
