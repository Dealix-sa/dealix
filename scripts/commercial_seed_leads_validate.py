#!/usr/bin/env python3
"""Validate the seed leads JSONL. Checks required fields and consent values.
Never fails the pipeline just because there are zero leads (case 1 is valid:
the generator emits placeholder, research-required drafts)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import commercial_launch_core as core  # noqa: E402

REQUIRED = ["lead_id", "company_name", "country", "vertical_hint"]
VALID_CONSENT = {"none", "opt_in", "opt_out", "pending"}


def validate(path: str | None = None) -> dict:
    leads = core.load_seed_leads(path)
    configs = core.load_all_configs()
    valid_verticals = {v["id"] for v in configs["verticals"]["verticals"]}
    errors: list[str] = []
    warnings: list[str] = []
    for i, lead in enumerate(leads, 1):
        for field in REQUIRED:
            if not lead.get(field):
                errors.append(f"lead #{i}: missing '{field}'")
        if lead.get("vertical_hint") and lead["vertical_hint"] not in valid_verticals:
            warnings.append(f"lead #{i}: unknown vertical_hint '{lead['vertical_hint']}'")
        consent = lead.get("consent_status", "none")
        if consent not in VALID_CONSENT:
            warnings.append(f"lead #{i}: unusual consent_status '{consent}'")
    return {"count": len(leads), "errors": errors, "warnings": warnings, "ok": not errors}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate seed leads.")
    parser.add_argument("--leads", default=None)
    args = parser.parse_args(argv)
    result = validate(args.leads)
    print(f"Seed leads: count={result['count']} ok={result['ok']} "
          f"errors={len(result['errors'])} warnings={len(result['warnings'])}")
    for e in result["errors"]:
        print(f"  ERROR {e}")
    for w in result["warnings"]:
        print(f"  WARN {w}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
