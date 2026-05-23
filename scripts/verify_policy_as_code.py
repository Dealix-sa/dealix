#!/usr/bin/env python3
"""Verify policies/dealix_control_policy.yaml is structurally valid."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[verify_policy_as_code] PyYAML not installed", file=sys.stderr)
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = REPO_ROOT / "policies" / "dealix_control_policy.yaml"

REQUIRED_CLASSES = {"A0", "A1", "A2", "A3"}
REQUIRED_RULES = {
    "no_a3_auto",
    "no_suppressed_outreach",
    "high_risk_requires_evidence",
    "no_guaranteed_revenue_claims",
    "approved_a2_can_request_execution",
    "public_proof_requires_approval",
    "pricing_commit_requires_approval",
    "data_export_requires_escalation",
}


def main() -> int:
    if not POLICY_PATH.exists():
        print(f"[verify_policy_as_code] missing: {POLICY_PATH}")
        return 1
    data = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8")) or {}
    failures = []

    classes = {c.get("id") for c in data.get("approval_classes", []) if isinstance(c, dict)}
    missing_classes = REQUIRED_CLASSES - classes
    if missing_classes:
        failures.append(f"missing approval_classes: {sorted(missing_classes)}")

    rule_ids = {r.get("id") for r in data.get("rules", []) if isinstance(r, dict)}
    missing_rules = REQUIRED_RULES - rule_ids
    if missing_rules:
        failures.append(f"missing rules: {sorted(missing_rules)}")

    if not data.get("trust_gates"):
        failures.append("trust_gates section is empty")

    if failures:
        for f in failures:
            print(f"[verify_policy_as_code] FAIL: {f}")
        return 1

    print(f"[verify_policy_as_code] PASS  classes={len(classes)} rules={len(rule_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
