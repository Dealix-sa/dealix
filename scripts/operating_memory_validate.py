#!/usr/bin/env python3
"""Validate Operating Memory schemas and their embedded examples.

Reads config/operating_memory_schemas.json and checks that:
  - every named schema declares a non-empty 'required' field list
  - every example record satisfies its schema's required fields

Pure validation; no IO beyond reading the config. No sending.

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from _v7_revenue_common import CONFIG, read_json

EXPECTED_SCHEMAS = (
    "decision_memory",
    "client_memory",
    "market_memory",
    "revenue_memory",
)


def validate(path: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    cfg = read_json(path, None)
    if cfg is None:
        return False, [f"config not found or invalid JSON: {path}"]

    schemas = cfg.get("schemas", {})
    for name in EXPECTED_SCHEMAS:
        if name not in schemas:
            errors.append(f"missing schema '{name}'")
            continue
        required = schemas[name].get("required", [])
        if not required:
            errors.append(f"schema '{name}' has empty 'required'")

    examples = cfg.get("examples", {})
    for name, records in examples.items():
        if name not in schemas:
            errors.append(f"example for unknown schema '{name}'")
            continue
        required = schemas[name].get("required", [])
        for i, rec in enumerate(records, start=1):
            for field in required:
                if field not in rec:
                    errors.append(f"{name} example {i}: missing required field '{field}'")

    return (not errors), errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path", nargs="?", default=str(CONFIG / "operating_memory_schemas.json")
    )
    args = parser.parse_args()
    ok, errors = validate(Path(args.path))
    if ok:
        print(f"[operating_memory] PASS — {args.path} schemas valid.")
        return 0
    print(f"[operating_memory] FAIL — {len(errors)} issue(s):")
    for e in errors:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
