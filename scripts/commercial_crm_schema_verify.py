#!/usr/bin/env python3
"""Verify the CRM pipeline schema has all canonical stages and safety invariants."""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "config" / "crm_pipeline_schema.json"

EXPECTED_STAGES = ["raw lead", "researched", "draft generated", "founder review",
                   "manually contacted", "replied positive", "discovery booked",
                   "diagnostic proposed", "diagnostic sold", "pilot proposed",
                   "pilot sold", "retainer", "expansion", "disqualified", "suppressed"]


def main() -> int:
    if not SCHEMA.exists():
        print("crm_pipeline_schema.json missing", file=sys.stderr)
        return 1
    schema = json.loads(SCHEMA.read_text())
    errors: list[str] = []
    for stage in EXPECTED_STAGES:
        if stage not in schema.get("stages", []):
            errors.append(f"missing stage: {stage}")
    inv = schema.get("invariants", {})
    if not inv.get("no_crm_push_send"):
        errors.append("invariant no_crm_push_send must be true")
    if not inv.get("suppressed_never_contacted"):
        errors.append("invariant suppressed_never_contacted must be true")
    if schema.get("external_send") != "forbidden":
        errors.append("external_send must be 'forbidden'")
    ok = not errors
    print(json.dumps({"ok": ok, "stages": len(schema.get("stages", [])), "errors": errors}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
