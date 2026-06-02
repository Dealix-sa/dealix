#!/usr/bin/env python3
"""Verify the Dealix Market Production OS layer.

Checks (no third-party deps beyond PyYAML):
  1. All schemas/*.schema.json parse and carry $schema / $id / title / type.
  2. data/sectors/sectors.yaml parses, has the 10 canonical sectors, and its
     sector keys match the `sector` enum in schemas/prospect.schema.json.
  3. The synthetic example records in data/templates/market_os_*_example.jsonl
     structurally conform to their schema (required fields present + enum values valid).
  4. Doctrine invariants hold: every outreach_draft example has
     unsubscribe_included=true and an approval_status; suppression + reply schemas
     expose the immediate-suppress path.
  5. The keystone docs (master index, compliance core, control room, metrics) exist.

Prints `DEALIX_MARKET_PRODUCTION_OS_VERDICT=PASS|FAIL` and exits 0/1.
Pass `--write-report` to stamp the verdict into reports/gtm/DAILY_GTM_REPORT.md.

This verifier deliberately re-derives enum/required constraints from the schema
files themselves, so it does not drift when a schema changes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "schemas"
TEMPLATES_DIR = REPO_ROOT / "data" / "templates"

SCHEMA_FILES = [
    "prospect.schema.json",
    "outreach_draft.schema.json",
    "email_account.schema.json",
    "sending_batch.schema.json",
    "suppression.schema.json",
    "approval_action.schema.json",
    "reply.schema.json",
    "job_signal.schema.json",
]

# example file -> schema file
EXAMPLES = {
    "market_os_prospect_example.jsonl": "prospect.schema.json",
    "market_os_outreach_draft_example.jsonl": "outreach_draft.schema.json",
    "market_os_suppression_example.jsonl": "suppression.schema.json",
    "market_os_job_signal_example.jsonl": "job_signal.schema.json",
}

CANONICAL_SECTORS = {
    "marketing_agencies",
    "training_companies",
    "clinics",
    "real_estate_teams",
    "recruitment_agencies",
    "professional_services",
    "restaurant_groups",
    "education_providers",
    "logistics_companies",
    "local_saas",
}

KEYSTONE_DOCS = [
    "docs/market_os/MARKET_PRODUCTION_OS_AR.md",
    "docs/outreach/EMAIL_DELIVERABILITY_POLICY_AR.md",
    "docs/outreach/COLD_EMAIL_COMPLIANCE_AR.md",
    "docs/outreach/UNSUBSCRIBE_POLICY_AR.md",
    "docs/outreach/SENDING_RAMP_PLAN_AR.md",
    "docs/gtm/GTM_CONTROL_ROOM_AR.md",
    "docs/gtm/GTM_METRICS_AR.md",
]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _enum_map(schema: dict) -> dict[str, set[str]]:
    """Map property name -> allowed enum values (top-level properties only)."""
    out: dict[str, set[str]] = {}
    for name, spec in schema.get("properties", {}).items():
        if isinstance(spec, dict) and isinstance(spec.get("enum"), list):
            out[name] = set(spec["enum"])
    return out


def _iter_jsonl(path: Path):
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        yield line_no, json.loads(line)


def run_checks() -> tuple[bool, list[str], list[str]]:
    """Return (ok, errors, info). Pure: never writes."""
    errors: list[str] = []
    info: list[str] = []
    schemas: dict[str, dict] = {}

    # 1. Schemas parse + required meta keys
    for name in SCHEMA_FILES:
        path = SCHEMAS_DIR / name
        if not path.exists():
            errors.append(f"missing schema: schemas/{name}")
            continue
        try:
            schema = _load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON in schemas/{name}: {exc}")
            continue
        for key in ("$schema", "$id", "title", "type"):
            if key not in schema:
                errors.append(f"schemas/{name} missing '{key}'")
        schemas[name] = schema
    if schemas:
        info.append(f"schemas parsed: {len(schemas)}/{len(SCHEMA_FILES)}")

    # 2. sectors.yaml
    sectors_path = REPO_ROOT / "data" / "sectors" / "sectors.yaml"
    if not sectors_path.exists():
        errors.append("missing data/sectors/sectors.yaml")
    else:
        try:
            doc = yaml.safe_load(sectors_path.read_text(encoding="utf-8"))
            keys = {s["key"] for s in doc.get("sectors", [])}
            missing = CANONICAL_SECTORS - keys
            extra = keys - CANONICAL_SECTORS
            if missing:
                errors.append(f"sectors.yaml missing sectors: {sorted(missing)}")
            if extra:
                errors.append(f"sectors.yaml has unknown sectors: {sorted(extra)}")
            # cross-check vs prospect schema enum
            prospect = schemas.get("prospect.schema.json", {})
            enum = set(prospect.get("properties", {}).get("sector", {}).get("enum", []))
            if enum and enum != CANONICAL_SECTORS:
                errors.append("prospect.schema sector enum != canonical sectors")
            if enum and keys and enum != keys:
                errors.append("sectors.yaml keys != prospect.schema sector enum")
            for s in doc.get("sectors", []):
                for field in ("name_ar", "name_en", "priority", "first_offer"):
                    if field not in s:
                        errors.append(f"sector {s.get('key')!r} missing '{field}'")
            info.append(f"sectors.yaml: {len(keys)} sectors")
        except yaml.YAMLError as exc:
            errors.append(f"invalid YAML in sectors.yaml: {exc}")

    # 3 + 4. Example records conform + doctrine invariants
    for fname, schema_name in EXAMPLES.items():
        path = TEMPLATES_DIR / fname
        schema = schemas.get(schema_name)
        if not path.exists():
            errors.append(f"missing example: data/templates/{fname}")
            continue
        if schema is None:
            continue
        required = schema.get("required", [])
        enums = _enum_map(schema)
        count = 0
        try:
            for line_no, rec in _iter_jsonl(path):
                count += 1
                for field in required:
                    if field not in rec:
                        errors.append(f"{fname}:{line_no} missing required '{field}'")
                for field, allowed in enums.items():
                    if field in rec and rec[field] not in allowed:
                        errors.append(f"{fname}:{line_no} '{field}'={rec[field]!r} not in enum")
                # doctrine invariants for drafts
                if schema_name == "outreach_draft.schema.json":
                    if rec.get("unsubscribe_included") is not True:
                        errors.append(
                            f"{fname}:{line_no} draft must have unsubscribe_included=true"
                        )
                    if "approval_status" not in rec:
                        errors.append(f"{fname}:{line_no} draft missing approval_status")
                    if (
                        rec.get("send_status") == "sent"
                        and rec.get("approval_status") != "approved"
                    ):
                        errors.append(f"{fname}:{line_no} sent draft without approval")
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSONL in {fname}: {exc}")
        info.append(f"{fname}: {count} record(s) checked")

    # 4b. suppression + reply suppress path exist in schemas
    supp = schemas.get("suppression.schema.json", {})
    supp_reasons = set(supp.get("properties", {}).get("reason", {}).get("enum", []))
    for needed in ("unsubscribe", "bounce", "complaint"):
        if needed not in supp_reasons:
            errors.append(f"suppression schema missing reason '{needed}'")
    reply = schemas.get("reply.schema.json", {})
    reply_actions = set(reply.get("properties", {}).get("next_action", {}).get("enum", []))
    if "suppress" not in reply_actions:
        errors.append("reply schema missing 'suppress' next_action")

    # 5. Keystone docs
    for rel in KEYSTONE_DOCS:
        if not (REPO_ROOT / rel).exists():
            errors.append(f"missing keystone doc: {rel}")

    return (not errors, errors, info)


def _stamp_report(verdict: str) -> None:
    report = REPO_ROOT / "reports" / "gtm" / "DAILY_GTM_REPORT.md"
    if not report.exists():
        return
    text = report.read_text(encoding="utf-8")
    import re

    new = re.sub(
        r"DEALIX_MARKET_PRODUCTION_OS_VERDICT=\w+",
        f"DEALIX_MARKET_PRODUCTION_OS_VERDICT={verdict}",
        text,
    )
    if new != text:
        report.write_text(new, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Dealix Market Production OS layer.")
    parser.add_argument(
        "--write-report", action="store_true", help="stamp verdict into the daily GTM report"
    )
    args = parser.parse_args()

    ok, errors, info = run_checks()
    for line in info:
        print(f"  - {line}")
    if errors:
        print("\nFAILURES:")
        for err in errors:
            print(f"  ! {err}")
    verdict = "PASS" if ok else "FAIL"
    if args.write_report:
        _stamp_report(verdict)
    print(f"\nDEALIX_MARKET_PRODUCTION_OS_VERDICT={verdict}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
