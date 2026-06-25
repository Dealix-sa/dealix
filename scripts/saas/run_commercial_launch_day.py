#!/usr/bin/env python3
"""Founder-led commercial launch day for Dealix.

Draft-only. No email, WhatsApp, SMS, payment, or external send.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from scripts.commercial.run_sales_agent_company_brain_day import main as run_sales_agent_day

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "reports" / "saas" / "COMMERCIAL_LAUNCH_DAY.md"
ACTIONS = [
    "Review the generated Sales Agent + Company Brain packs.",
    "Pick 10 Saudi B2B companies with a verified source_url and clear pain hypothesis.",
    "Prepare 3 founder-reviewed discovery call attempts.",
    "Create 1 scoped proposal only after qualification.",
    "Update HubSpot or the deal ledger after every founder action.",
]


def main() -> int:
    run_sales_agent_day()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    lines = [
        "# Dealix Commercial Launch Day",
        "",
        f"Generated at: {now}",
        "",
        "## Safety",
        "",
        "No external sending. No live WhatsApp. No SMS. Manual review only.",
        "",
        "## Generated operating assets",
        "",
        "- reports/commercial/sales_agent_company_brain/latest.md",
        "- reports/commercial/sales_agent_company_brain/latest.json",
        "",
        "## Founder actions",
        "",
    ]
    lines.extend(f"{i}. {action}" for i, action in enumerate(ACTIONS, 1))
    lines.extend(["", "## Verdict", "", "READY_FOR_FOUNDER_LED_COMMERCIAL_ACTION"])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("COMMERCIAL_LAUNCH_DAY_READY")
    print(REPORT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
