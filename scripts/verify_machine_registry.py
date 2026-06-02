#!/usr/bin/env python3
"""Cross-check registries/machine_registry.yaml against .github/workflows/.

Every YAML file under .github/workflows/ must have a matching entry in
machine_registry.yaml. Each entry must have name, file, schedule, class,
owner.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
REGISTRY_YAML = REPO / "registries" / "machine_registry.yaml"
WORKFLOW_DIR = REPO / ".github" / "workflows"
VALID_CLASSES = {"A1", "A2", "A3"}
REQUIRED_FIELDS = ("name", "file", "schedule", "class", "owner", "purpose")


def _fail(msg: str) -> None:
    print(msg, file=sys.stderr)


def main() -> int:
    if not REGISTRY_YAML.is_file():
        _fail(f"missing_machine_registry:{REGISTRY_YAML.relative_to(REPO)}")
        print("MACHINE_REGISTRY_PASS=false")
        return 1

    try:
        data = yaml.safe_load(REGISTRY_YAML.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        _fail(f"yaml_error:{exc}")
        print("MACHINE_REGISTRY_PASS=false")
        return 1

    entries = list(data.get("github_workflows") or [])
    registered_files = {e.get("file") for e in entries}

    errors: list[str] = []

    if WORKFLOW_DIR.is_dir():
        on_disk = {
            f".github/workflows/{p.name}" for p in WORKFLOW_DIR.glob("*.yml")
        }
        for path in sorted(on_disk - registered_files):
            errors.append(f"workflow_not_registered:{path}")
        for path in sorted(registered_files - on_disk):
            errors.append(f"registered_workflow_missing_on_disk:{path}")
    else:
        errors.append("workflow_dir_missing:.github/workflows")

    for entry in entries:
        name = entry.get("name") or "<unknown>"
        for field in REQUIRED_FIELDS:
            if not entry.get(field):
                errors.append(f"missing_field:{name}:{field}")
        cls = entry.get("class")
        if cls and cls not in VALID_CLASSES:
            errors.append(f"invalid_class:{name}:{cls}")

    for err in errors:
        _fail(err)

    ok = not errors
    print(f"MACHINE_REGISTRY_PASS={'true' if ok else 'false'}")
    print(f"MACHINE_REGISTRY_WORKFLOW_COUNT={len(entries)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
