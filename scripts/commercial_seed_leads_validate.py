#!/usr/bin/env python3
"""Validate the seed leads JSONL against the CRM schema and consent/suppression rules."""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "config" / "crm_pipeline_schema.json"
SEED = ROOT / "data" / "commercial_seed_leads.example.jsonl"
REQUIRED = ["lead_id", "company_name", "vertical", "country", "source", "consent", "suppressed", "stage"]
VERTICALS = {"facilities_management", "contracting_project_controls", "real_estate_property_ops",
             "legal_professional_services", "consulting_training_b2b"}


def main() -> int:
    if not SEED.exists() or not SCHEMA.exists():
        print("seed leads or schema missing", file=sys.stderr)
        return 1
    schema = json.loads(SCHEMA.read_text())
    stages = set(schema["stages"])
    errors: list[str] = []
    seen_ids: set[str] = set()
    n = 0
    for ln, line in enumerate(SEED.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        n += 1
        row = json.loads(line)
        for k in REQUIRED:
            if k not in row:
                errors.append(f"line {ln}: missing {k}")
        if row.get("lead_id") in seen_ids:
            errors.append(f"line {ln}: duplicate lead_id {row.get('lead_id')}")
        seen_ids.add(row.get("lead_id"))
        if row.get("vertical") not in VERTICALS:
            errors.append(f"line {ln}: invalid vertical {row.get('vertical')}")
        if row.get("stage") not in stages:
            errors.append(f"line {ln}: invalid stage {row.get('stage')}")
        # consent/suppression invariant: suppressed leads must not be 'contactable'
        if row.get("suppressed") and row.get("consent"):
            errors.append(f"line {ln}: suppressed lead must not have consent=true")
    ok = not errors
    print(json.dumps({"ok": ok, "rows": n, "errors": errors[:20]}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
