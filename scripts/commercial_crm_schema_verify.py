#!/usr/bin/env python3
"""Verify the CRM pipeline schema is well-formed and record-only.

Checks:
- the canonical stages are present and in order,
- every allowed transition references a valid stage,
- the schema declares no_external_send and no_crm_push_send,
- required lead fields are defined.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import load_config

EXPECTED_STAGES = [
    "new",
    "researched",
    "draft_generated",
    "founder_review",
    "manually_contacted",
    "replied_positive",
    "replied_negative",
    "diagnostic_booked",
    "diagnostic_sold",
    "pilot_proposed",
    "pilot_sold",
    "retainer",
    "disqualified",
    "suppressed",
]


def verify() -> list[str]:
    errors: list[str] = []
    schema = load_config("crm_pipeline_schema.json")
    stages = schema.get("stages", [])

    if stages != EXPECTED_STAGES:
        missing = [s for s in EXPECTED_STAGES if s not in stages]
        extra = [s for s in stages if s not in EXPECTED_STAGES]
        if missing:
            errors.append(f"missing stages: {missing}")
        if extra:
            errors.append(f"unexpected stages: {extra}")
        if not missing and not extra:
            errors.append("stage order does not match canonical order")

    stage_set = set(stages)
    for src, dests in schema.get("allowed_transitions", {}).items():
        if src not in stage_set:
            errors.append(f"transition source not a valid stage: {src}")
        for d in dests:
            if d not in stage_set:
                errors.append(f"transition target not a valid stage: {src} -> {d}")

    if schema.get("no_external_send") is not True:
        errors.append("no_external_send must be true")
    if schema.get("no_crm_push_send") is not True:
        errors.append("no_crm_push_send must be true")
    if not schema.get("required_lead_fields"):
        errors.append("required_lead_fields missing")

    return errors


def main() -> int:
    errors = verify()
    if errors:
        print("CRM SCHEMA VERIFY: FAIL", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("CRM SCHEMA VERIFY: PASS — 14 stages, transitions valid, record-only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
