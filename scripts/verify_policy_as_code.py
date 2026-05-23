#!/usr/bin/env python3
"""Verify policies/dealix_control_policy.yaml has the required structure."""

from __future__ import annotations

import sys
from pathlib import Path

POLICY_PATH = Path(__file__).resolve().parents[1] / "policies" / "dealix_control_policy.yaml"
REQUIRED_CLASSES = {"A0", "A1", "A2", "A3"}
REQUIRED_RULES = {
    "no_a3_auto",
    "no_suppressed_outreach",
    "high_risk_requires_evidence",
    "no_guaranteed_revenue_claims",
    "approved_a2_can_request_execution",
}


def main() -> int:
    if not POLICY_PATH.exists():
        print(f"FAIL: missing policy file {POLICY_PATH}")
        return 1
    try:
        import yaml  # type: ignore
    except ImportError:
        print("FAIL: PyYAML not installed; pip install pyyaml")
        return 1
    with POLICY_PATH.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        print("FAIL: policy is not a mapping")
        return 1

    classes = data.get("approval_classes")
    if not isinstance(classes, dict):
        print("FAIL: approval_classes must be a mapping")
        return 1
    missing_classes = REQUIRED_CLASSES - set(classes.keys())
    if missing_classes:
        print(f"FAIL: missing approval classes: {sorted(missing_classes)}")
        return 1

    rules = data.get("rules") or []
    rule_ids = {r.get("id") for r in rules if isinstance(r, dict)}
    missing_rules = REQUIRED_RULES - rule_ids
    if missing_rules:
        print(f"FAIL: missing rules: {sorted(missing_rules)}")
        return 1

    a3 = classes.get("A3", {}) or {}
    if a3.get("external_action_allowed") is True:
        print("FAIL: A3 must not allow external action")
        return 1

    print(f"OK: policy_as_code v{data.get('version', '?')}")
    print(f"  approval_classes: {sorted(classes.keys())}")
    print(f"  rules: {sorted(rule_ids)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
