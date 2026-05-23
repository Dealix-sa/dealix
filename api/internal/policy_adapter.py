"""
Loader for the Dealix control policy file (YAML).

Returns a list of rule dicts. Falls back to an empty list with
source='fallback' if the file is missing or PyYAML is not installed.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

POLICY_PATH = Path("policies/dealix_control_policy.yaml")


def load_policies() -> dict[str, Any]:
    """Return {"rules": [...], "source": "yaml"|"fallback"}."""
    if not POLICY_PATH.exists():
        return {"rules": [], "source": "fallback", "path": str(POLICY_PATH)}
    try:
        import yaml  # type: ignore[import-not-found]
    except Exception:
        return {"rules": [], "source": "fallback", "path": str(POLICY_PATH), "error": "pyyaml_missing"}
    try:
        raw = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8")) or {}
    except Exception as exc:  # noqa: BLE001
        return {"rules": [], "source": "fallback", "path": str(POLICY_PATH), "error": str(exc)}
    rules = raw.get("rules") if isinstance(raw, dict) else None
    if not isinstance(rules, list):
        return {"rules": [], "source": "yaml", "path": str(POLICY_PATH)}
    return {"rules": rules, "source": "yaml", "path": str(POLICY_PATH)}
