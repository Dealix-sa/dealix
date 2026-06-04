#!/usr/bin/env python3
"""Company Utilization verifier (V7-aware) — are the V7 tools wired and used?

Confirms the V7 generator/validator scripts exist and that the supporting
config + example data are present so the daily machine can actually run.
Writes outputs/company_utilization/company_utilization_verification.json.

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse

from _v7_revenue_common import CONFIG, DATA, REPO, SAFETY_BANNER, write_json

GENERATOR_SCRIPTS = [
    "commercial_generate_400_drafts.py",
    "founder_action_queue_generate.py",
    "founder_revenue_dashboard.py",
    "diagnostic_pack_generate.py",
    "proposal_seed_generate.py",
    "proof_asset_template_generate.py",
    "daily_ceo_brief_generate.py",
    "weekly_board_report_generate.py",
    "market_intelligence_brief_generate.py",
]

VALIDATOR_SCRIPTS = [
    "revenue_manual_events_validate.py",
    "operating_memory_validate.py",
    "revenue_execution_verify.py",
    "master_startup_command_verify.py",
]

SUPPORTING_ASSETS = [
    CONFIG / "market_intelligence_signals.json",
    CONFIG / "operating_memory_schemas.json",
    DATA / "revenue_manual_events.example.jsonl",
]


def verify() -> dict:
    missing_gen = [s for s in GENERATOR_SCRIPTS if not (REPO / "scripts" / s).exists()]
    missing_val = [s for s in VALIDATOR_SCRIPTS if not (REPO / "scripts" / s).exists()]
    missing_assets = [
        str(p.relative_to(REPO)) for p in SUPPORTING_ASSETS if not p.exists()
    ]
    checks = {
        "generators_present": not missing_gen,
        "validators_present": not missing_val,
        "supporting_assets_present": not missing_assets,
    }
    ok = all(checks.values())
    result = {
        "system": "company-utilization-os",
        "status": "PASS" if ok else "FAIL",
        "generators": len(GENERATOR_SCRIPTS),
        "validators": len(VALIDATOR_SCRIPTS),
        "checks": checks,
        "missing_generators": missing_gen,
        "missing_validators": missing_val,
        "missing_assets": missing_assets,
        "safety": SAFETY_BANNER,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    write_json(
        REPO / "outputs" / "company_utilization" / "company_utilization_verification.json",
        result,
    )
    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[company_utilization_verify] {result['status']}")
    for key, val in result["checks"].items():
        print(f"  - {key}: {'OK' if val else 'FAIL'}")
    print(f"[company_utilization_verify] {SAFETY_BANNER}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
