#!/usr/bin/env python3
"""Dealix — Custom Systems OS CLI.

Runs a governed custom-system engagement (custom design profile + structure
blueprint + complete bilingual spec) end-to-end. Never sends anything
externally; only writes local artifacts and ledger rows.

Usage::

    python scripts/dealix_custom_system.py --demo
    python scripts/dealix_custom_system.py --customer-id c1 --customer-name "Acme" \
        --engagement-id e1 --paid-pilots 3 --modules sales,support \
        --workflows weekly_growth,monthly_report --workflow-owner
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from auto_client_acquisition.custom_systems_os.engagement_runner import (  # noqa: E402
    run_custom_system_engagement,
)
from auto_client_acquisition.data_os.source_passport import SourcePassport  # noqa: E402


def _passport() -> SourcePassport:
    return SourcePassport(
        source_id="cli-demo-src",
        source_type="client_upload",
        owner="demo",
        allowed_use=frozenset({"internal_analysis"}),
        contains_pii=False,
        sensitivity="medium",
        retention_policy="project_duration",
        ai_access_allowed=True,
        external_use_allowed=False,
    )


def _csv(value: str) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dealix Custom Systems OS — governed runner")
    parser.add_argument("--demo", action="store_true", help="Run a synthetic end-to-end demo")
    parser.add_argument("--customer-id", default="")
    parser.add_argument("--customer-name", default="")
    parser.add_argument("--engagement-id", default="")
    parser.add_argument("--paid-pilots", type=int, default=0)
    parser.add_argument("--modules", default="", help="comma-separated module names")
    parser.add_argument("--workflows", default="", help="comma-separated workflow names")
    parser.add_argument("--direction", default="saudi_executive_trust")
    parser.add_argument("--sector", default=None)
    parser.add_argument("--workflow-owner", action="store_true")
    parser.add_argument("--adoption-score", type=float, default=0.0)
    parser.add_argument("--out-dir", default="var/custom-systems-exports")
    args = parser.parse_args(argv)

    if args.demo:
        args.customer_id = args.customer_id or "demo-customer"
        args.customer_name = args.customer_name or "Demo Company"
        args.engagement_id = args.engagement_id or "demo-engagement"
        args.paid_pilots = args.paid_pilots or 3
        args.modules = args.modules or "sales_inbox,support_desk"
        args.workflows = args.workflows or "weekly_growth,monthly_report"
        args.workflow_owner = True
        args.adoption_score = args.adoption_score or 75.0

    if not (args.customer_id and args.customer_name and args.engagement_id):
        parser.error(
            "--customer-id, --customer-name and --engagement-id are required (or use --demo)"
        )

    result = run_custom_system_engagement(
        customer_id=args.customer_id,
        customer_name=args.customer_name,
        engagement_id=args.engagement_id,
        passport=_passport(),
        paid_pilots_completed=args.paid_pilots,
        declared_modules=_csv(args.modules),
        declared_workflows=_csv(args.workflows),
        direction_name=args.direction,
        sector=args.sector,
        workflow_owner_present=args.workflow_owner,
        adoption_score=args.adoption_score,
        out_dir=args.out_dir,
        write_ledger=True,
    )

    summary = {
        "engagement_id": result.engagement_id,
        "next_step": result.next_step,
        "delivery_mode": result.delivery_mode,
        "passport_valid": result.passport_valid,
        "governance_decision": result.governance_decision,
        "safety_passed": result.safety_passed,
        "proof_score": result.proof_score,
        "proof_band": result.proof_band,
        "proof_complete": result.proof_complete,
        "capital_assets": len(result.capital_assets),
        "spec_written_files": result.spec_written_files,
        "retainer": result.retainer.get("recommended_offer", ""),
        "blocked_reasons": result.blocked_reasons,
        "safe_to_send": False,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
