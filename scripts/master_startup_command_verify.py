#!/usr/bin/env python3
"""Verify the Master Startup Command Center (V7) and all V7 OS layers.

Confirms every V7 OS layer has its 00_*.md and 99_*_REPORT.md, the master
command center docs exist, and the verify/generator scripts are present.

Writes outputs/master_command_center/master_command_verification.json.
Exit code 0 on PASS, 1 on FAIL.

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse

from _v7_revenue_common import DOCS, REPO, SAFETY_BANNER, write_json

# Each OS layer must expose an overview (00) and an evidence report (99).
OS_LAYERS = {
    "revenue-execution-os": ("00_REVENUE_EXECUTION_OS.md", "99_REVENUE_EXECUTION_REPORT.md"),
    "delivery-conversion-os": ("00_DELIVERY_CONVERSION_OS.md", "99_DELIVERY_CONVERSION_REPORT.md"),
    "proof-os": ("00_PROOF_ASSET_OS.md", "99_PROOF_OS_REPORT.md"),
    "market-intelligence-os": ("00_MARKET_INTELLIGENCE_OS.md", "99_MARKET_INTELLIGENCE_REPORT.md"),
    "knowledge-base-os": ("00_KNOWLEDGE_BASE_OS.md", "99_KNOWLEDGE_BASE_REPORT.md"),
    "operating-memory-os": ("00_OPERATING_MEMORY_OS.md", "99_OPERATING_MEMORY_REPORT.md"),
    "automation-boundaries-os": ("00_AUTOMATION_BOUNDARIES_OS.md", "99_AUTOMATION_BOUNDARIES_REPORT.md"),
    "scale-readiness-os": ("00_SCALE_READINESS_OS.md", "99_SCALE_READINESS_REPORT.md"),
    "crisis-os": ("00_CRISIS_OS.md", "99_CRISIS_OS_REPORT.md"),
    "master-command-center": ("00_MASTER_COMMAND_CENTER.md", "99_MASTER_COMMAND_CENTER_REPORT.md"),
}

MASTER_DOCS = [
    "master-command-center/00_MASTER_COMMAND_CENTER.md",
    "master-command-center/01_DAILY_STARTUP_COMMANDS.md",
    "master-command-center/02_WEEKLY_STARTUP_COMMANDS.md",
    "master-command-center/03_MONTHLY_STARTUP_COMMANDS.md",
    "master-command-center/04_ALL_SYSTEMS_INDEX.md",
    "master-command-center/05_FOUNDER_ONE_PAGE_CONTROL.md",
    "master-command-center/99_MASTER_COMMAND_CENTER_REPORT.md",
]

REQUIRED_SCRIPTS = [
    "revenue_execution_verify.py",
    "master_startup_command_verify.py",
    "founder_action_queue_generate.py",
    "founder_revenue_dashboard.py",
    "daily_ceo_brief_generate.py",
    "weekly_board_report_generate.py",
]


def verify() -> dict:
    missing_layer_docs: list[str] = []
    for layer, (overview, report) in OS_LAYERS.items():
        for name in (overview, report):
            rel = f"{layer}/{name}"
            if not (DOCS / rel).exists():
                missing_layer_docs.append(rel)

    missing_master = [d for d in MASTER_DOCS if not (DOCS / d).exists()]
    missing_scripts = [s for s in REQUIRED_SCRIPTS if not (REPO / "scripts" / s).exists()]

    checks = {
        "all_os_layers_documented": not missing_layer_docs,
        "master_command_center_complete": not missing_master,
        "verify_scripts_present": not missing_scripts,
    }
    ok = all(checks.values())
    result = {
        "system": "master-command-center",
        "status": "PASS" if ok else "FAIL",
        "os_layers_checked": len(OS_LAYERS),
        "checks": checks,
        "missing_layer_docs": missing_layer_docs,
        "missing_master_docs": missing_master,
        "missing_scripts": missing_scripts,
        "safety": SAFETY_BANNER,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    out = REPO / "outputs" / "master_command_center" / "master_command_verification.json"
    write_json(out, result)
    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[master_startup_command_verify] {result['status']} "
          f"({result['os_layers_checked']} OS layers)")
    for key, val in result["checks"].items():
        print(f"  - {key}: {'OK' if val else 'FAIL'}")
    if result["status"] != "PASS":
        for k in ("missing_layer_docs", "missing_master_docs", "missing_scripts"):
            for item in result[k]:
                print(f"    {k}: {item}")
    print(f"[master_startup_command_verify] {SAFETY_BANNER}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
