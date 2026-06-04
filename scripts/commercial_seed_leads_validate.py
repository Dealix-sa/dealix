#!/usr/bin/env python3
"""Validate the example seed-leads file against the CRM schema.

Ensures required fields exist, vertical ids are known, stages are valid, and no
real PII transport is implied. Read-only; sends nothing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import CONFIG_DIR, DATA_DIR, load_json, load_offers, load_seed_leads  # noqa: E402


def validate(path: Path) -> dict:
    schema = load_json(CONFIG_DIR / "crm_pipeline_schema.json")
    offers = load_offers()
    valid_verticals = {v["id"] for v in offers["verticals"]}
    valid_stages = set(schema["pipeline_stages"])
    required = schema["lead_record"]["required_fields"]

    leads = load_seed_leads(path)
    errors: list[str] = []
    for lead in leads:
        for f in required:
            if f not in lead:
                errors.append(f"{lead.get('lead_id','?')}: missing required field '{f}'")
        if lead.get("vertical") not in valid_verticals:
            errors.append(f"{lead.get('lead_id','?')}: unknown vertical '{lead.get('vertical')}'")
        if lead.get("stage") not in valid_stages:
            errors.append(f"{lead.get('lead_id','?')}: invalid stage '{lead.get('stage')}'")
    return {"count": len(leads), "errors": errors, "passed": not errors}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=str(DATA_DIR / "commercial_seed_leads.example.jsonl"))
    args = ap.parse_args()
    r = validate(Path(args.path))
    if r["passed"]:
        print(f"Seed leads valid: {r['count']} records.")
        return 0
    print("Seed lead validation FAILED:")
    for e in r["errors"]:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
