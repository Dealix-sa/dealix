#!/usr/bin/env python3
"""Validate the example seed-leads file against the CRM lead schema.

Ensures the example data is well-formed and carries no individual contact
details / consent overreach. Never performs any outreach.
"""

from __future__ import annotations

import json
import sys

import commercial_launch_lib as lib

SEED_FILE = lib.DATA_DIR / "commercial_seed_leads.example.jsonl"


def validate() -> dict:
    schema = lib.load_config("crm_pipeline_schema.json")
    required = set(schema["lead_fields"])
    errors: list[str] = []
    rows = 0
    if not SEED_FILE.exists():
        return {"verdict": "FAIL", "errors": [f"missing {SEED_FILE}"], "rows": 0}
    with SEED_FILE.open(encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            rows += 1
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {i}: invalid json: {exc}")
                continue
            missing = required - set(rec.keys())
            if missing:
                errors.append(f"line {i}: missing fields {sorted(missing)}")
            if rec.get("consent_status") not in (None, "none", "opt_in", "public"):
                errors.append(f"line {i}: unexpected consent_status {rec.get('consent_status')}")
            # guard: example file must not contain personal email/phone fields
            for forbidden in ("email", "phone", "mobile", "personal_email"):
                if forbidden in rec:
                    errors.append(f"line {i}: must not contain personal field '{forbidden}'")
    return {"verdict": "PASS" if not errors else "FAIL", "errors": errors, "rows": rows}


def main(argv: list[str] | None = None) -> int:
    result = validate()
    if result["verdict"] == "PASS":
        print(f"✅ Seed leads valid: {result['rows']} example rows.")
        return 0
    print("❌ Seed leads invalid:", file=sys.stderr)
    for e in result["errors"]:
        print(f"   {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
