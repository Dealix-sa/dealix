#!/usr/bin/env python3
"""
Dealix CRM / Lead Schema Verification.

Verifies:
  - config/crm_pipeline_schema.json exists and has required lead fields + stages
  - data/commercial_seed_leads.example.jsonl exists and conforms
  - no "send" fields leak into the schema or example leads

Writes outputs/final_launch_control/crm_schema_verification.json.
Exit 0 if pass, 1 otherwise.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCHEMA = REPO / "config" / "crm_pipeline_schema.json"
SEED = REPO / "data" / "commercial_seed_leads.example.jsonl"
OUT = REPO / "outputs" / "final_launch_control" / "crm_schema_verification.json"

REQUIRED_FIELDS = {"lead_id", "company", "vertical", "stage", "source", "priority_score"}
SEND_FIELD_TERMS = {"send_now", "auto_send", "smtp_password", "outbound_token", "access_token"}


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    errors = []

    schema_ok = SCHEMA.exists()
    allowed_stages: set[str] = set()
    if schema_ok:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        req = set(schema.get("lead_required_fields", []))
        allowed_stages = set(schema.get("allowed_stages", []))
        if not REQUIRED_FIELDS.issubset(req):
            errors.append(f"schema missing required fields: {REQUIRED_FIELDS - req}")
        if not allowed_stages:
            errors.append("schema has no allowed_stages")
        if schema.get("send_policy", {}).get("external_send_allowed") is not False:
            errors.append("schema send_policy.external_send_allowed must be False")
    else:
        errors.append("config/crm_pipeline_schema.json missing")

    seed_ok = SEED.exists()
    lead_count = 0
    if seed_ok:
        for line in SEED.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            lead_count += 1
            lead = json.loads(line)
            missing = REQUIRED_FIELDS - set(lead.keys())
            if missing:
                errors.append(f"lead {lead.get('lead_id')} missing {missing}")
            if allowed_stages and lead.get("stage") not in allowed_stages:
                errors.append(f"lead {lead.get('lead_id')} has invalid stage {lead.get('stage')}")
            for k in lead.keys():
                if k.lower() in SEND_FIELD_TERMS:
                    errors.append(f"lead {lead.get('lead_id')} has forbidden send field {k}")
    else:
        errors.append("data/commercial_seed_leads.example.jsonl missing")

    passed = not errors
    result = {
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "schema_present": schema_ok,
        "seed_present": seed_ok,
        "lead_count": lead_count,
        "errors": errors,
        "pass": passed,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[crm-schema] {'PASS' if passed else 'FAIL'} — {lead_count} example leads")
    for e in errors:
        print(f"  - {e}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
