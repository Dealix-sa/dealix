#!/usr/bin/env python3
"""verify_policy_as_code.py — confirm policies/dealix_control_policy.yaml is law.

The file must parse, must declare every banned-claim rule, and must
explicitly forbid direct external sends.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML missing", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parents[1]
POLICY = REPO / "policies" / "dealix_control_policy.yaml"

REQUIRED_RULES = (
    "no_guaranteed_revenue_claims",
    "no_direct_external_send",
    "approval_required_for_external_action",
    "audit_required_for_external_action",
    "no_suppressed_outreach",
    "no_a3_auto_execution",
)


def main() -> int:
    if not POLICY.exists():
        print(f"missing_policy:{POLICY.relative_to(REPO)}", file=sys.stderr)
        return 1
    try:
        data = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"invalid_yaml:{exc}", file=sys.stderr)
        return 1

    if not isinstance(data, dict):
        print("policy_root_not_mapping", file=sys.stderr)
        return 1

    rules = data.get("rules") or {}
    failures: list[str] = []
    for name in REQUIRED_RULES:
        if name not in rules:
            failures.append(f"missing_rule:{name}")
            continue
        spec = rules[name]
        if not isinstance(spec, dict):
            failures.append(f"bad_rule_shape:{name}")
            continue
        if spec.get("enforced") is not True:
            failures.append(f"rule_not_enforced:{name}")

    # The policy must point at an audit sink and an approval queue.
    for key in ("approval_queue", "audit_log"):
        if not data.get(key):
            failures.append(f"missing_top_level:{key}")

    for f in failures:
        print(f, file=sys.stderr)
    ok = not failures
    print(f"POLICY_AS_CODE_PASS={'true' if ok else 'false'} (failures={len(failures)})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
