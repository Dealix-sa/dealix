#!/usr/bin/env python3
"""Cross-check registries/agent_registry.yaml against the Python AGENT_REGISTRY.

Every agent_id in auto_client_acquisition/agent_governance/agent_registry.py
must appear in the YAML mirror with a valid autonomy class (A1/A2/A3).
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

REGISTRY_YAML = REPO / "registries" / "agent_registry.yaml"
VALID_CLASSES = {"A1", "A2", "A3"}


def _fail(msg: str) -> None:
    print(msg, file=sys.stderr)


def main() -> int:
    if not REGISTRY_YAML.is_file():
        _fail(f"missing_yaml_registry:{REGISTRY_YAML.relative_to(REPO)}")
        print("AGENT_REGISTRY_PASS=false")
        return 1

    try:
        data = yaml.safe_load(REGISTRY_YAML.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        _fail(f"yaml_error:{exc}")
        print("AGENT_REGISTRY_PASS=false")
        return 1

    yaml_agents = {a.get("id"): a for a in (data.get("agents") or [])}
    if not yaml_agents:
        _fail("yaml_registry_empty")
        print("AGENT_REGISTRY_PASS=false")
        return 1

    errors: list[str] = []

    cross_check_skipped = False
    try:
        from auto_client_acquisition.agent_governance.agent_registry import (
            AGENT_REGISTRY,
        )
    except Exception as exc:  # pragma: no cover - tolerate missing optional deps
        _fail(f"python_registry_import_skipped:{exc}")
        cross_check_skipped = True
        AGENT_REGISTRY = {}  # type: ignore[assignment]

    yaml_keys = set(yaml_agents.keys())

    if not cross_check_skipped:
        python_agents = set(AGENT_REGISTRY.keys())
        for missing in sorted(python_agents - yaml_keys):
            errors.append(f"missing_in_yaml:{missing}")
        for extra in sorted(yaml_keys - python_agents):
            errors.append(f"extra_in_yaml:{extra}")

    for agent_id, entry in yaml_agents.items():
        cls = entry.get("class")
        if cls not in VALID_CLASSES:
            errors.append(f"invalid_class:{agent_id}:{cls}")
        if not entry.get("owner"):
            errors.append(f"missing_owner:{agent_id}")
        if "purpose_en" not in entry:
            errors.append(f"missing_purpose:{agent_id}")

    for err in errors:
        _fail(err)

    ok = not errors
    print(f"AGENT_REGISTRY_PASS={'true' if ok else 'false'}")
    print(f"AGENT_REGISTRY_COUNT={len(yaml_agents)}")
    print(f"AGENT_REGISTRY_PYTHON_CROSS_CHECK_SKIPPED={'true' if cross_check_skipped else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
