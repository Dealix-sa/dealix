#!/usr/bin/env python3
"""Validate every agent output JSON against the contract schema.

Walks `outputs/agents/*.json`. Empty directory → PASS with warning.
Any malformed JSON, missing required field, invalid enum value, or
violation of the A3/safe_to_use rule → FAIL.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

OUTPUT_DIR = REPO / "outputs/agents"
SCHEMA_PATH = REPO / "dealix/contracts/schemas/agent_output_contract.schema.json"


def _load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _validate(data: dict, schema: dict, file_label: str) -> list[str]:
    errors: list[str] = []
    required = schema.get("required", [])
    properties = schema.get("properties", {})

    for field in required:
        if field not in data:
            errors.append(f"{file_label}: missing field {field}")

    for field, spec in properties.items():
        if field not in data:
            continue
        if "enum" in spec:
            if data[field] not in spec["enum"]:
                errors.append(
                    f"{file_label}: invalid {field}={data[field]!r} " f"(allowed: {spec['enum']})"
                )
        if field == "evidence":
            value = data[field]
            if isinstance(value, str):
                if not value.strip():
                    errors.append(f"{file_label}: evidence is empty")
            elif isinstance(value, list):
                if not value:
                    errors.append(f"{file_label}: evidence list is empty")
            else:
                errors.append(f"{file_label}: evidence must be string or list")

    if data.get("approval_class") == "A3" and data.get("safe_to_use") == "Yes":
        errors.append(f"{file_label}: A3 outputs must not be marked safe_to_use=Yes")

    return errors


def main() -> int:
    ensure_stdout_utf8()
    print("# Agent Output Contract")

    if not SCHEMA_PATH.exists():
        print(f"FAIL: missing schema: {SCHEMA_PATH}")
        print("AGENT_OUTPUTS_READY=false")
        return 1

    schema = _load_schema()

    if not OUTPUT_DIR.exists():
        print(f"  warn: no agent outputs directory yet: {OUTPUT_DIR}")
        print("AGENT_OUTPUTS_READY=true")
        return 0

    json_files = sorted(OUTPUT_DIR.glob("*.json"))
    if not json_files:
        print(f"  warn: no agent outputs found under {OUTPUT_DIR}")
        print("AGENT_OUTPUTS_READY=true")
        return 0

    failures: list[str] = []
    for file in json_files:
        label = file.relative_to(REPO).as_posix()
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            failures.append(f"{label}: invalid JSON: {e}")
            print(f"  FAIL: {label}: invalid JSON")
            continue
        if not isinstance(data, dict):
            failures.append(f"{label}: top-level must be an object")
            print(f"  FAIL: {label}: not an object")
            continue
        errs = _validate(data, schema, label)
        if errs:
            failures.extend(errs)
            print(f"  FAIL: {label}")
        else:
            print(f"  ok: {label}")

    if failures:
        print("\nDetails:")
        for f in failures:
            print(f"- {f}")
        print("AGENT_OUTPUTS_READY=false")
        return 1

    print(f"\nPASS: {len(json_files)} agent outputs comply with contract.")
    print("AGENT_OUTPUTS_READY=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
