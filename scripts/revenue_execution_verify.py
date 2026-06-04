#!/usr/bin/env python3
"""Verify the Dealix Revenue Execution OS (V7) is present and safe.

Checks:
  - required revenue-execution / delivery-conversion / proof OS docs exist
  - required generator + validator scripts exist
  - required config + example data exist
  - V7 scripts contain no forbidden external-send patterns

Writes outputs/revenue_execution/revenue_execution_verification.json and
prints PASS/FAIL. Exit code 0 on PASS, 1 on FAIL.

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse
import re

from _v7_revenue_common import (
    CONFIG,
    DATA,
    DOCS,
    REPO,
    SAFETY_BANNER,
    write_json,
)

REQUIRED_DOCS = [
    "revenue-execution-os/00_REVENUE_EXECUTION_OS.md",
    "revenue-execution-os/01_DAILY_REVENUE_MACHINE.md",
    "revenue-execution-os/02_WEEKLY_REVENUE_REVIEW.md",
    "revenue-execution-os/03_REVENUE_PIPELINE_RULES.md",
    "revenue-execution-os/04_DIAGNOSTIC_SALES_PLAYBOOK.md",
    "revenue-execution-os/05_PILOT_CONVERSION_PLAYBOOK.md",
    "revenue-execution-os/06_RETAINER_CONVERSION_PLAYBOOK.md",
    "revenue-execution-os/07_REVENUE_QUALITY_GATE.md",
    "revenue-execution-os/08_FOUNDERS_REVENUE_DASHBOARD.md",
    "revenue-execution-os/09_REVENUE_RISK_REGISTER.md",
    "revenue-execution-os/10_MANUAL_EVENTS_LEDGER.md",
    "revenue-execution-os/11_DIAGNOSTIC_PACK_PROCESS.md",
    "revenue-execution-os/99_REVENUE_EXECUTION_REPORT.md",
    "delivery-conversion-os/00_DELIVERY_CONVERSION_OS.md",
    "delivery-conversion-os/01_DIAGNOSTIC_TO_PILOT.md",
    "delivery-conversion-os/02_PILOT_TO_RETAINER.md",
    "delivery-conversion-os/03_PROOF_ASSET_GENERATION.md",
    "delivery-conversion-os/04_CLIENT_SUCCESS_REVIEW.md",
    "delivery-conversion-os/05_EXPANSION_TRIGGERS.md",
    "delivery-conversion-os/99_DELIVERY_CONVERSION_REPORT.md",
    "proof-os/00_PROOF_ASSET_OS.md",
    "proof-os/01_PROOF_WITHOUT_FAKE_CLAIMS.md",
    "proof-os/02_CASE_STYLE_TEMPLATE.md",
    "proof-os/03_BEFORE_AFTER_WORKFLOW_TEMPLATE.md",
    "proof-os/04_CLIENT_PERMISSION_RULES.md",
    "proof-os/05_ANONYMIZED_PROOF_PROCESS.md",
    "proof-os/99_PROOF_OS_REPORT.md",
    "market-intelligence-os/00_MARKET_INTELLIGENCE_OS.md",
    "knowledge-base-os/00_KNOWLEDGE_BASE_OS.md",
    "operating-memory-os/00_OPERATING_MEMORY_OS.md",
    "automation-boundaries-os/00_AUTOMATION_BOUNDARIES_OS.md",
    "scale-readiness-os/00_SCALE_READINESS_OS.md",
    "crisis-os/00_CRISIS_OS.md",
]

REQUIRED_SCRIPTS = [
    "commercial_generate_400_drafts.py",
    "founder_action_queue_generate.py",
    "founder_revenue_dashboard.py",
    "revenue_manual_events_validate.py",
    "diagnostic_pack_generate.py",
    "proposal_seed_generate.py",
    "proof_asset_template_generate.py",
    "daily_ceo_brief_generate.py",
    "weekly_board_report_generate.py",
    "market_intelligence_brief_generate.py",
    "operating_memory_validate.py",
]

REQUIRED_CONFIG = [
    CONFIG / "market_intelligence_signals.json",
    CONFIG / "operating_memory_schemas.json",
    DATA / "revenue_manual_events.example.jsonl",
]

# Forbidden external-send patterns inside V7 scripts (defense-in-depth).
FORBIDDEN_PATTERNS = [
    r"smtplib",
    r"\.send_message\s*\(",
    r"requests\.post\s*\(\s*['\"]https?://",
    r"twilio",
    r"sendgrid",
]

# Generator/validator scripts that must stay send-free. The verifier scripts
# themselves are excluded because they legitimately *name* the forbidden
# patterns in order to scan for them.
SCANNED_SCRIPTS = REQUIRED_SCRIPTS


def verify() -> dict:
    missing_docs = [d for d in REQUIRED_DOCS if not (DOCS / d).exists()]
    missing_scripts = [s for s in REQUIRED_SCRIPTS if not (REPO / "scripts" / s).exists()]
    missing_config = [str(p.relative_to(REPO)) for p in REQUIRED_CONFIG if not p.exists()]

    forbidden_hits: list[str] = []
    for s in SCANNED_SCRIPTS:
        path = REPO / "scripts" / s
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for pat in FORBIDDEN_PATTERNS:
            if re.search(pat, text):
                forbidden_hits.append(f"{s}: matched forbidden pattern /{pat}/")

    checks = {
        "docs_present": not missing_docs,
        "scripts_present": not missing_scripts,
        "config_present": not missing_config,
        "no_forbidden_send_patterns": not forbidden_hits,
    }
    ok = all(checks.values())

    result = {
        "system": "revenue-execution-os",
        "status": "PASS" if ok else "FAIL",
        "checks": checks,
        "missing_docs": missing_docs,
        "missing_scripts": missing_scripts,
        "missing_config": missing_config,
        "forbidden_hits": forbidden_hits,
        "safety": SAFETY_BANNER,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print JSON to stdout")
    args = parser.parse_args()
    result = verify()
    out = REPO / "outputs" / "revenue_execution" / "revenue_execution_verification.json"
    write_json(out, result)
    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[revenue_execution_verify] {result['status']}")
    for key, val in result["checks"].items():
        print(f"  - {key}: {'OK' if val else 'FAIL'}")
    if result["status"] != "PASS":
        for k in ("missing_docs", "missing_scripts", "missing_config", "forbidden_hits"):
            for item in result[k]:
                print(f"    {k}: {item}")
    print(f"[revenue_execution_verify] {SAFETY_BANNER}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
