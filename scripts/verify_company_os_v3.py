#!/usr/bin/env python3
"""Verify Dealix Enterprise Company OS v3 documentation layer is present and complete.

Checks every v3 doc, the unified operating database schema, and required
``## Supersedes`` sections on the six docs that explicitly replace older surfaces.

Exit code 0 means all gates pass; 1 means at least one gate failed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

COMPANY_OS_V3_FILES = (
    "docs/company/DEALIX_ENTERPRISE_COMPANY_OS_V3.md",
    "docs/data/UNIFIED_OPERATING_DATABASE.md",
    "docs/runtime/CSV_TO_POSTGRES_MIGRATION_PLAN.md",
    "docs/runtime/WORKER_MESH_OS.md",
    "deploy/PRODUCTION_SERVER_LAYOUT.md",
    "docs/product/CEO_COMMAND_CENTER_V1.md",
    "docs/api/REVENUE_FACTORY_API_SURFACE.md",
    "docs/distribution/DISTRIBUTION_FLYWHEEL.md",
    "docs/distribution/SECTOR_DOMINATION_PLAYBOOK.md",
    "docs/revenue/OFFER_LADDER_V3.md",
    "docs/revenue/PROPOSAL_FACTORY_V3.md",
    "docs/finance/PAYMENT_CAPTURE_OS_V3.md",
    "docs/client_success/CLIENT_EXPANSION_OS.md",
    "docs/content/PROOF_TO_DEMAND_MACHINE.md",
    "docs/partners/PARTNER_ECOSYSTEM_OS_V3.md",
    "docs/agents/AGENT_GOVERNANCE_V3.md",
    "docs/evals/EVAL_CI_GATE.md",
    "docs/finance/COST_CONTROL_OS.md",
    "docs/finance/STRATEGIC_FINANCE_OS.md",
    "docs/founder/GOVERNANCE_BOARD_PACK_V3.md",
)

COMPANY_OS_V3_SCHEMA = "schemas/unified_operating_database.schema.json"

# Files that must contain a ``## Supersedes`` heading because they replace
# an older surface from the docs/ tree.
COMPANY_OS_V3_FILES_WITH_SUPERSEDES = (
    "docs/company/DEALIX_ENTERPRISE_COMPANY_OS_V3.md",
    "docs/product/CEO_COMMAND_CENTER_V1.md",
    "docs/revenue/OFFER_LADDER_V3.md",
    "docs/partners/PARTNER_ECOSYSTEM_OS_V3.md",
    "docs/agents/AGENT_GOVERNANCE_V3.md",
)

MIN_DOC_BYTES = 50


def _missing(paths: tuple[str, ...]) -> list[str]:
    out: list[str] = []
    for rel in paths:
        if not (REPO / rel).is_file():
            out.append(rel)
    return out


def _too_short(paths: tuple[str, ...]) -> list[str]:
    out: list[str] = []
    for rel in paths:
        p = REPO / rel
        if p.is_file() and p.stat().st_size < MIN_DOC_BYTES:
            out.append(rel)
    return out


def _missing_supersedes(paths: tuple[str, ...]) -> list[str]:
    out: list[str] = []
    for rel in paths:
        p = REPO / rel
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8")
        if "## Supersedes" not in text:
            out.append(rel)
    return out


def _schema_ok(quiet: bool) -> bool:
    p = REPO / COMPANY_OS_V3_SCHEMA
    if not p.is_file():
        print(f"missing_v3:{COMPANY_OS_V3_SCHEMA}", file=sys.stderr)
        return False
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"invalid_json_v3:{COMPANY_OS_V3_SCHEMA}:{exc}", file=sys.stderr)
        return False
    required_keys = {"$schema", "$id", "title", "type", "properties", "required"}
    if not required_keys.issubset(data.keys()):
        missing = sorted(required_keys - set(data.keys()))
        print(f"schema_missing_keys_v3:{missing}", file=sys.stderr)
        return False
    props = data.get("properties", {})
    if "tables" not in props or "non_negotiable_rules" not in props:
        print("schema_missing_tables_or_rules_v3", file=sys.stderr)
        return False
    if not quiet:
        print(f"schema_ok_v3:{COMPANY_OS_V3_SCHEMA}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="suppress per-file output")
    args = parser.parse_args()

    missing = _missing(COMPANY_OS_V3_FILES)
    short = _too_short(COMPANY_OS_V3_FILES)
    no_supersedes = _missing_supersedes(COMPANY_OS_V3_FILES_WITH_SUPERSEDES)

    for rel in missing:
        print(f"missing_v3:{rel}", file=sys.stderr)
    for rel in short:
        print(f"too_short_v3:{rel}", file=sys.stderr)
    for rel in no_supersedes:
        print(f"missing_supersedes_v3:{rel}", file=sys.stderr)

    docs_ok = not missing and not short and not no_supersedes
    schema_ok = _schema_ok(args.quiet)

    if not args.quiet:
        print(f"COMPANY_OS_V3_DOCS_PASS={'true' if docs_ok else 'false'}")
        print(f"COMPANY_OS_V3_SCHEMA_PASS={'true' if schema_ok else 'false'}")

    overall = docs_ok and schema_ok
    print(f"COMPANY_OS_V3_PASS={'true' if overall else 'false'}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
