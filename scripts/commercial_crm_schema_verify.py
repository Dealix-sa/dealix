#!/usr/bin/env python3
"""Verify the CRM pipeline schema is well-formed and send-free.

Checks required keys, stage list completeness, and that the schema explicitly
declares zero send capability. Read-only.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import CONFIG_DIR, load_json

REQUIRED_STAGES = {
    "raw_lead",
    "researched",
    "draft_generated",
    "founder_review",
    "manually_contacted",
    "replied_positive",
    "discovery_booked",
    "diagnostic_proposed",
    "diagnostic_sold",
    "pilot_proposed",
    "pilot_sold",
    "retainer",
    "expansion",
    "disqualified",
    "suppressed",
}


def verify() -> list[str]:
    errors: list[str] = []
    schema = load_json(CONFIG_DIR / "crm_pipeline_schema.json")
    stages = set(schema.get("pipeline_stages", []))
    missing = REQUIRED_STAGES - stages
    if missing:
        errors.append(f"missing pipeline stages: {sorted(missing)}")
    if schema.get("_meta", {}).get("send_capability") != "none":
        errors.append("send_capability must be 'none'")
    for f in (
        "lead_record",
        "reply_classification",
        "suppression_triggers",
        "forbidden_capabilities",
    ):
        if f not in schema:
            errors.append(f"missing top-level key: {f}")
    for cap in ("automated_external_send", "crm_push_send"):
        if cap not in schema.get("forbidden_capabilities", []):
            errors.append(f"forbidden_capabilities must include '{cap}'")
    return errors


def main() -> int:
    errors = verify()
    if not errors:
        print("CRM schema verify PASS — send-free, all stages present.")
        return 0
    print("CRM schema verify FAIL:")
    for e in errors:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
