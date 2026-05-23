#!/usr/bin/env python3
"""Verify policies/dealix_control_policy.yaml against required rule ids.

The Dealix control policy is the machine-readable counterpart to the
12 non-negotiables in CLAUDE.md. This script asserts that every required
rule id is present and minimally well-formed.

Exit 0 on success, 1 on any failure.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Tuple

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = REPO_ROOT / "policies" / "dealix_control_policy.yaml"

REQUIRED_RULES = [
    "no_a3_auto",
    "no_suppressed_outreach",
    "high_risk_requires_evidence",
    "no_guaranteed_revenue_claims",
    "approved_a2_can_request_execution",
    "public_proof_requires_approval",
    "pricing_commit_requires_approval",
    "data_export_requires_escalation",
    "payment_terms_require_escalation",
    "contract_change_requires_escalation",
    "destructive_operation_requires_escalation",
]

REQUIRED_RULE_FIELDS = {"id", "description", "severity", "trigger", "action", "owner"}
ALLOWED_SEVERITIES = {"block", "warn", "escalate"}


def load_policy() -> dict:
    if not POLICY_PATH.exists():
        raise SystemExit(f"missing policy file: {POLICY_PATH}")
    with POLICY_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def main() -> int:
    policy = load_policy()
    metadata = policy.get("metadata") or {}
    rules = policy.get("rules") or []

    results: List[Tuple[str, bool, str]] = []
    results.append((
        "metadata present",
        bool(metadata) and "version" in metadata and "created" in metadata,
        f"version={metadata.get('version')!r} created={metadata.get('created')!r}",
    ))
    results.append((
        "rules is a list",
        isinstance(rules, list) and len(rules) > 0,
        f"got {type(rules).__name__} of length "
        f"{len(rules) if isinstance(rules, list) else 'n/a'}",
    ))

    rule_index = {r.get("id"): r for r in rules if isinstance(r, dict)}
    for rule_id in REQUIRED_RULES:
        rule = rule_index.get(rule_id)
        if rule is None:
            results.append((f"rule {rule_id} present", False, "missing"))
            continue
        missing_fields = REQUIRED_RULE_FIELDS - set(rule.keys())
        severity_ok = rule.get("severity") in ALLOWED_SEVERITIES
        if missing_fields:
            results.append((
                f"rule {rule_id} fields",
                False,
                f"missing fields: {sorted(missing_fields)}",
            ))
        elif not severity_ok:
            results.append((
                f"rule {rule_id} severity",
                False,
                f"got {rule.get('severity')!r}",
            ))
        else:
            results.append((f"rule {rule_id} valid", True, "ok"))

    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print("Dealix policy-as-code verification")
    print("-" * 40)
    for label, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {label}: {detail}")
    print("-" * 40)
    print(f"summary: {passed}/{total} checks passed "
          f"({len(REQUIRED_RULES)} required rules)")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
