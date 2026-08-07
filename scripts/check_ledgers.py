#!/usr/bin/env python3
"""Validate Dealix founder ledgers against their lightweight contract.

This script intentionally has no third-party dependencies (no ``jsonschema``)
so it can run early in CI and inside the existing pytest suite. It is a fast,
structural guard — not a full JSON Schema validator. For each ledger it checks:

- the data file and its ``*.schema.json`` both exist and parse as JSON,
- the required top-level keys are present and ``ledger`` matches the file name,
- ``version`` is a positive integer and ``records`` is a list,
- every record carries its required fields with non-empty ids,
- enum fields only use allowed values,
- record ids are unique and match their ``XXX-NNNN`` prefix.

Empty ledgers (``"records": []``) are valid: we never fabricate pipeline data.

Run directly:  ``python scripts/check_ledgers.py``
Exit code 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGERS_DIR = ROOT / "ledgers"

# Minimal contract mirrored from the JSON Schemas in ledgers/*.schema.json.
# Keep these in sync when a schema's required fields or enums change.
CONTRACT: dict[str, dict] = {
    "prospects": {
        "id_prefix": "PRO",
        "required": ["id", "company", "sector", "stage", "source", "created"],
        "enums": {
            "stage": [
                "identified",
                "qualified",
                "contacted",
                "meeting",
                "proposal",
                "won",
                "lost",
            ]
        },
    },
    "deals": {
        "id_prefix": "DEAL",
        "required": ["id", "title", "offer", "stage", "currency", "opened"],
        "enums": {
            "stage": [
                "diagnostic",
                "pilot",
                "proof",
                "proposal",
                "negotiation",
                "won",
                "lost",
            ],
            "currency": ["SAR"],
            "status": ["open", "won", "lost", "on_hold"],
        },
    },
    "experiments": {
        "id_prefix": "EXP",
        "required": ["id", "hypothesis", "metric", "status", "started"],
        "enums": {
            "status": ["proposed", "running", "done", "abandoned"],
            "result": ["pending", "supported", "refuted", "inconclusive"],
        },
    },
    "risks": {
        "id_prefix": "RISK",
        "required": ["id", "title", "category", "severity", "status", "created"],
        "enums": {
            "category": [
                "commercial",
                "product",
                "security",
                "compliance",
                "operational",
                "financial",
            ],
            "severity": ["low", "medium", "high", "critical"],
            "likelihood": ["low", "medium", "high"],
            "status": ["open", "mitigating", "closed", "accepted"],
        },
    },
}

TOP_LEVEL_REQUIRED = ("ledger", "version", "records")


def _load_json(path: Path, errors: list[str]) -> object | None:
    if not path.exists():
        errors.append(f"Missing file: {path.relative_to(ROOT)}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return None


def _validate_ledger(name: str, spec: dict, errors: list[str]) -> None:
    schema_path = LEDGERS_DIR / f"{name}.schema.json"
    data_path = LEDGERS_DIR / f"{name}.json"

    schema = _load_json(schema_path, errors)
    if isinstance(schema, dict) and "$defs" not in schema:
        errors.append(f"{name}.schema.json is missing a '$defs' block")

    data = _load_json(data_path, errors)
    if not isinstance(data, dict):
        if data is not None:
            errors.append(f"{name}.json must be a JSON object, got {type(data).__name__}")
        return

    for key in TOP_LEVEL_REQUIRED:
        if key not in data:
            errors.append(f"{name}.json missing top-level key: {key}")

    if data.get("ledger") != name:
        errors.append(f"{name}.json has ledger={data.get('ledger')!r}, expected {name!r}")

    version = data.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        errors.append(f"{name}.json version must be an integer >= 1, got {version!r}")

    records = data.get("records")
    if not isinstance(records, list):
        errors.append(f"{name}.json 'records' must be a list")
        return

    id_pattern = re.compile(rf"^{spec['id_prefix']}-[0-9]{{4,}}$")
    seen_ids: set[str] = set()

    for index, record in enumerate(records):
        where = f"{name}.json records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{where} must be an object")
            continue

        for field in spec["required"]:
            value = record.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append(f"{where} missing required field: {field}")

        record_id = record.get("id")
        if isinstance(record_id, str):
            if not id_pattern.match(record_id):
                errors.append(f"{where} id {record_id!r} must match {spec['id_prefix']}-NNNN")
            if record_id in seen_ids:
                errors.append(f"{where} duplicate id: {record_id}")
            seen_ids.add(record_id)

        for field, allowed in spec["enums"].items():
            value = record.get(field)
            if value is not None and value not in allowed:
                errors.append(f"{where} field {field}={value!r} not in {allowed}")


def validate_all(root: Path | None = None) -> list[str]:
    """Validate every ledger. Returns a list of human-readable errors (empty = OK)."""
    global ROOT, LEDGERS_DIR
    if root is not None:
        ROOT = Path(root).resolve()
        LEDGERS_DIR = ROOT / "ledgers"

    errors: list[str] = []
    if not LEDGERS_DIR.exists():
        errors.append(f"Missing ledgers directory: {LEDGERS_DIR}")
        return errors

    for name, spec in CONTRACT.items():
        _validate_ledger(name, spec, errors)
    return errors


def main() -> int:
    errors = validate_all()
    if errors:
        print("Ledger contract check failed:\n", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        print("\nDEALIX_LEDGERS_VERDICT=FAIL", file=sys.stderr)
        return 1

    counts = []
    for name in CONTRACT:
        data = json.loads((LEDGERS_DIR / f"{name}.json").read_text(encoding="utf-8"))
        counts.append(f"{name}={len(data['records'])}")
    print("Ledger contract OK: " + ", ".join(counts))
    print("DEALIX_LEDGERS_VERDICT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
