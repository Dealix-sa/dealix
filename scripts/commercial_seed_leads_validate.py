#!/usr/bin/env python3
"""Validate the example seed leads file.

Ensures every lead has the required CRM fields, a known vertical, a valid
starting stage, and an opt_in_status. These are synthetic example leads used
only to exercise the draft factory — never real contact data.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import DATA_DIR, load_config, read_jsonl

VALID_OPT_IN = {"unknown", "opted_in", "not_opted_in"}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    leads = read_jsonl(path)
    if not leads:
        return [f"no leads found at {path}"]

    schema = load_config("crm_pipeline_schema.json")
    stages = set(schema.get("stages", []))
    verticals = {v["id"] for v in load_config("commercial_verticals.json")["verticals"]}
    required = [
        "lead_id",
        "company_name",
        "vertical",
        "country",
        "city",
        "buyer_title",
        "stage",
        "source",
        "opt_in_status",
    ]

    seen_ids: set[str] = set()
    for i, lead in enumerate(leads):
        for field in required:
            if not str(lead.get(field, "")).strip():
                errors.append(f"lead#{i}: missing field '{field}'")
        lid = lead.get("lead_id")
        if lid in seen_ids:
            errors.append(f"lead#{i}: duplicate lead_id '{lid}'")
        seen_ids.add(lid)
        if lead.get("vertical") not in verticals:
            errors.append(f"lead#{i}: unknown vertical '{lead.get('vertical')}'")
        if lead.get("stage") not in stages:
            errors.append(f"lead#{i}: invalid stage '{lead.get('stage')}'")
        if lead.get("opt_in_status") not in VALID_OPT_IN:
            errors.append(f"lead#{i}: invalid opt_in_status '{lead.get('opt_in_status')}'")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate example seed leads.")
    parser.add_argument("--file", default=str(DATA_DIR / "commercial_seed_leads.example.jsonl"))
    args = parser.parse_args()

    errors = validate(Path(args.file))
    if errors:
        print("SEED LEADS VALIDATE: FAIL", file=sys.stderr)
        for e in errors[:25]:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"SEED LEADS VALIDATE: PASS — {args.file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
