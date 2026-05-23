#!/usr/bin/env python3
"""Verify policies/dealix_control_policy.yaml is loadable and complete."""
from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_IDS = {
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
}


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    path = repo / "policies" / "dealix_control_policy.yaml"
    if not path.exists():
        print("FAIL: policy file missing:", path)
        return 1
    try:
        import yaml  # type: ignore
    except ImportError:
        print("WARN: pyyaml not installed; cannot fully verify policy structure")
        return 0
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    rules = data.get("rules") or []
    ids = {r.get("id") for r in rules}
    missing = REQUIRED_IDS - ids
    print("[policy-as-code]")
    print(f"  rules present: {len(ids)}")
    print(f"  missing required rules: {sorted(missing)}")
    print("RESULT:", "FAIL" if missing else "PASS")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
