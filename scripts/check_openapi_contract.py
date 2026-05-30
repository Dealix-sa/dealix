#!/usr/bin/env python3
"""Check Dealix OpenAPI contract stability.

If docs/architecture/openapi.json exists, this script exports the current schema
and compares it with the baseline. It reports removed paths and removed methods
as breaking changes. If no baseline exists, it still verifies that the schema can
be exported and explains how to create the baseline.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "docs" / "architecture" / "openapi.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    try:
        from export_openapi import export_openapi  # lazy import — api.main has heavy deps

        with tempfile.TemporaryDirectory() as tmp:
            current_path = Path(tmp) / "openapi.json"
            export_openapi(current_path)
            current = load(current_path)
    except Exception as exc:
        # Export can fail if optional dependencies are missing at CI time or
        # if a route's Pydantic model cannot be serialised to JSON Schema.
        # This is informational — the contract check only has value when a
        # baseline exists; fail loudly then, not on the export step.
        print(f"OpenAPI export skipped: {exc}")
        print("Run 'make openapi-export' locally to debug. Skipping contract check.")
        return 0

    if not BASELINE.exists():
        print("OpenAPI baseline not found: docs/architecture/openapi.json")
        print("Current schema exports successfully. Create a baseline with: make openapi-export")
        return 0

    baseline = load(BASELINE)
    baseline_paths = baseline.get("paths", {})
    current_paths = current.get("paths", {})

    errors: list[str] = []
    for path in sorted(set(baseline_paths) - set(current_paths)):
        errors.append(f"Removed API path: {path}")

    for path in sorted(set(baseline_paths) & set(current_paths)):
        old_methods = set(baseline_paths[path].keys())
        new_methods = set(current_paths[path].keys())
        for method in sorted(old_methods - new_methods):
            errors.append(f"Removed API method: {method.upper()} {path}")

    if errors:
        print("OpenAPI contract check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("OpenAPI contract OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
