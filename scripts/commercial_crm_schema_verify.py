#!/usr/bin/env python3
"""Verify the commercial CRM / lead pipeline schema and example seed leads.

Checks:
- config/crm_pipeline_schema.json exists and is well-formed
- required lead fields present in schema
- allowed stages present
- no send / sensitive fields anywhere in schema or example leads
- data/commercial_seed_leads.example.jsonl matches the schema

Exit 0 on PASS, 1 on FAIL.

Usage:
    python scripts/commercial_crm_schema_verify.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from launch_os import paths  # noqa: E402
from launch_os.verify import Check, summarize, print_checks  # noqa: E402

REQUIRED_LEAD_FIELDS = {"lead_id", "company", "vertical", "stage"}
REQUIRED_STAGES = {"new", "qualified", "diagnostic_booked", "pilot_proposed", "retainer", "disqualified"}
FORBIDDEN_FIELDS = {"email", "phone", "mobile", "whatsapp", "send_allowed", "auto_send", "smtp", "api_key"}


def run() -> dict:
    checks: list[Check] = []

    schema_path = paths.CRM_SCHEMA
    checks.append(Check("crm_schema_exists", schema_path.exists(), detail=paths.rel(schema_path)))
    schema: dict = {}
    if schema_path.exists():
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            checks.append(Check("crm_schema_valid_json", True))
        except json.JSONDecodeError as e:
            checks.append(Check("crm_schema_valid_json", False, detail=str(e)))

    req_fields = set(schema.get("lead_required_fields", []))
    checks.append(
        Check(
            "required_lead_fields_present",
            REQUIRED_LEAD_FIELDS.issubset(req_fields),
            detail=f"missing={sorted(REQUIRED_LEAD_FIELDS - req_fields)}",
        )
    )
    stages = set(schema.get("stages", []))
    checks.append(
        Check(
            "allowed_stages_present",
            REQUIRED_STAGES.issubset(stages),
            detail=f"missing={sorted(REQUIRED_STAGES - stages)}",
        )
    )
    # Forbidden fields must be declared, and must NOT be in required/optional.
    declared_forbidden = set(schema.get("forbidden_fields", []))
    checks.append(
        Check(
            "send_fields_declared_forbidden",
            FORBIDDEN_FIELDS.issubset(declared_forbidden),
            detail=f"missing={sorted(FORBIDDEN_FIELDS - declared_forbidden)}",
        )
    )
    active_fields = set(schema.get("lead_required_fields", [])) | set(schema.get("lead_optional_fields", []))
    leaked = active_fields & FORBIDDEN_FIELDS
    checks.append(Check("no_send_fields_in_active_schema", len(leaked) == 0, detail=f"leaked={sorted(leaked)}"))

    # Example seed leads.
    seed = paths.SEED_LEADS
    checks.append(Check("seed_leads_example_exists", seed.exists(), detail=paths.rel(seed)))
    if seed.exists():
        rows = []
        bad_rows = 0
        forbidden_in_rows = 0
        for line in seed.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                bad_rows += 1
                continue
            rows.append(row)
            if not REQUIRED_LEAD_FIELDS.issubset(row.keys()):
                bad_rows += 1
            if FORBIDDEN_FIELDS & set(row.keys()):
                forbidden_in_rows += 1
        checks.append(Check("seed_leads_well_formed", bad_rows == 0, detail=f"bad_rows={bad_rows}"))
        checks.append(Check("seed_leads_no_forbidden_fields", forbidden_in_rows == 0))
        checks.append(Check("seed_leads_nonempty", len(rows) > 0, critical=False, detail=f"rows={len(rows)}"))

    return summarize(checks)


def main() -> int:
    result = run()
    print_checks("crm", [Check(**c) for c in result["checks"]])
    print("[crm] PASS" if result["pass"] else "[crm] FAIL")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
