#!/usr/bin/env python3
"""Verify that all v2 Enterprise Revenue & Distribution artifacts are present.

Source-of-truth spec: docs/runtime/REVENUE_FACTORY_RUNTIME_V2.md

The verifier checks:
  - all 18 v2 documentation files exist and are non-trivial (>50 bytes)
  - the 3 v2 scripts exist (this script + 2 generators)
  - the init shell script exists and is non-trivial
  - the growth_database JSON schema is valid JSON
  - the deploy/cron file exists
  - the GitHub Actions workflow exists

In --strict mode, also checks the two private-ops generated cockpits:
  - docs/founder/sales_cockpit.md
  - docs/founder/approval_center.md
These are skipped in normal mode because they only exist after the cockpit
generators have been run against a populated private-ops tree (server-side).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]

REQUIRED_DOCS: tuple[str, ...] = (
    "docs/runtime/REVENUE_FACTORY_RUNTIME_V2.md",
    "docs/data/GROWTH_DATABASE_MODEL_V2.md",
    "docs/control_plane/SALES_COCKPIT_V2.md",
    "docs/distribution/DISTRIBUTION_PORTFOLIO_V2.md",
    "docs/distribution/EXPERIMENT_ENGINE_V2.md",
    "docs/distribution/EMAIL_DELIVERABILITY_V2.md",
    "docs/trust/SUPPRESSION_AND_OPTOUT_SYSTEM.md",
    "docs/runtime/WORKER_QUEUE_RUNTIME_V2.md",
    "docs/engineering/REVENUE_FACTORY_OBSERVABILITY.md",
    "docs/evals/AI_EVAL_RED_TEAM_SYSTEM.md",
    "docs/founder/BOARD_LEVEL_KPI_STACK_V2.md",
    "docs/founder/REVENUE_WAR_ROOM_V2.md",
    "docs/partners/PARTNER_REVENUE_MACHINE_V2.md",
    "docs/distribution/ABM_STRATEGIC_ACCOUNT_MACHINE_V2.md",
    "docs/localization/ARABIC_SALES_ENGINE.md",
    "docs/product/COMMAND_CENTER_PRODUCT_SPEC_V2.md",
    "docs/finance/BILLING_RECEIVABLES_OS_V2.md",
    "docs/security/SUPPLY_CHAIN_HARDENING_ROADMAP_V2.md",
)

REQUIRED_ARTIFACTS: tuple[str, ...] = (
    "schemas/growth_database.schema.json",
    "scripts/generate_sales_cockpit.py",
    "scripts/generate_approval_center.py",
    "scripts/verify_enterprise_revenue_distribution_v2.py",
    "scripts/init_private_ops.sh",
    "deploy/cron/dealix_growth_factory.cron",
    ".github/workflows/dealix-enterprise-revenue-distribution-v2.yml",
)

STRICT_ONLY: tuple[str, ...] = (
    "docs/founder/sales_cockpit.md",
    "docs/founder/approval_center.md",
)


def _check_min_size(rel: str, min_bytes: int = 50) -> str | None:
    path = REPO / rel
    if not path.exists():
        return f"Missing: {rel}"
    if path.stat().st_size < min_bytes:
        return f"Too short (<{min_bytes}B): {rel}"
    return None


def _check_json_schema(rel: str) -> str | None:
    path = REPO / rel
    if not path.exists():
        return f"Missing: {rel}"
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return f"Invalid JSON in {rel}: {exc.msg} (line {exc.lineno})"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Also require the two generated cockpit markdowns (server-side only).",
    )
    args = parser.parse_args()

    failures: list[str] = []

    for rel in REQUIRED_DOCS:
        err = _check_min_size(rel)
        if err:
            failures.append(err)

    for rel in REQUIRED_ARTIFACTS:
        err = _check_min_size(rel)
        if err:
            failures.append(err)

    schema_err = _check_json_schema("schemas/growth_database.schema.json")
    if schema_err:
        failures.append(schema_err)

    if args.strict:
        for rel in STRICT_ONLY:
            err = _check_min_size(rel)
            if err:
                failures.append(err)

    if failures:
        print("FAIL: Enterprise Revenue Distribution v2 verification failed:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    total = len(REQUIRED_DOCS) + len(REQUIRED_ARTIFACTS) + (len(STRICT_ONLY) if args.strict else 0)
    print(f"PASS: Enterprise Revenue Distribution v2 is ready ({total} artifacts verified).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
