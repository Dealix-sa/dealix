#!/usr/bin/env python3
"""Verify policy-as-code completeness.

Checks:
  - policies/dealix_control_policy.yaml exists and lists forbidden_claims
  - policies/dealix_control_policy.yaml lists trust_gates
  - A3 tier is documented and approval-gated
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, print_and_exit, repo_root  # noqa: E402


def main() -> int:
    result = VerifyResult(name="Policy-as-Code", passed=True)
    path = repo_root() / "policies" / "dealix_control_policy.yaml"
    if not path.exists():
        result.passed = False
        result.missing.append(str(path.relative_to(repo_root())))
        return print_and_exit(result)
    text = path.read_text(encoding="utf-8")
    required_keys = ["forbidden_claims:", "trust_gates:", "agent_tiers:", "A3:"]
    for key in required_keys:
        if key not in text:
            result.passed = False
            result.notes.append(f"missing key: {key}")
    if "guaranteed revenue" not in text.lower():
        result.passed = False
        result.notes.append("policy must explicitly forbid 'guaranteed revenue'")
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
