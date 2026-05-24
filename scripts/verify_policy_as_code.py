#!/usr/bin/env python3
"""
verify_policy_as_code.py — approval and claim policies must be valid YAML
with the right shape, not free-form prose.

Validates:
  - dealix/config/approval_policy.yaml — every action has requires_approval +
    risk_level + creates_evidence
  - dealix/config/claim_policy.yaml — has rules block + roi_or_guarantee not allowed
  - dealix/transformation/engineering_cutover_policy.yaml — parses
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FATAL: PyYAML not installed", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent

APPROVAL = ROOT / "dealix/config/approval_policy.yaml"
CLAIM = ROOT / "dealix/config/claim_policy.yaml"
CUTOVER = ROOT / "dealix/transformation/engineering_cutover_policy.yaml"

REQUIRED_APPROVAL_FIELDS = {"requires_approval", "risk_level", "creates_evidence"}
# 'variable' = the actual risk is decided per-tool in agent_permissions.yaml
# (still requires_approval=true, so the gate is intact).
ALLOWED_RISK_LEVELS = {"low", "medium", "high", "critical", "variable"}


def load_yaml(p: Path) -> tuple[bool, object, str]:
    if not p.exists():
        return False, None, f"missing: {p.relative_to(ROOT)}"
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return False, None, f"invalid yaml in {p.relative_to(ROOT)}: {exc}"
    return True, data, ""


def main() -> int:
    failures: list[str] = []

    # ── approval_policy.yaml
    ok, approval, err = load_yaml(APPROVAL)
    if not ok:
        failures.append(err)
    elif not isinstance(approval, dict) or not approval:
        failures.append("approval_policy.yaml is empty or not a mapping")
    else:
        for action, spec in approval.items():
            if not isinstance(spec, dict):
                failures.append(f"approval action '{action}' is not a mapping")
                continue
            missing = REQUIRED_APPROVAL_FIELDS - set(spec.keys())
            if missing:
                failures.append(f"approval action '{action}' missing fields: {sorted(missing)}")
            risk = spec.get("risk_level")
            if risk not in ALLOWED_RISK_LEVELS:
                failures.append(
                    f"approval action '{action}' has invalid risk_level: {risk!r}"
                )

    # ── claim_policy.yaml
    ok, claim, err = load_yaml(CLAIM)
    if not ok:
        failures.append(err)
    elif not isinstance(claim, dict):
        failures.append("claim_policy.yaml is not a mapping")
    else:
        rules = claim.get("rules") or {}
        if not isinstance(rules, dict) or not rules:
            failures.append("claim_policy.yaml has no 'rules' block")
        else:
            roi = rules.get("roi_or_guarantee") or {}
            if isinstance(roi, dict) and roi.get("allowed") is not False:
                failures.append(
                    "claim_policy.yaml.rules.roi_or_guarantee.allowed must be false (no guarantees)"
                )
            recog = rules.get("revenue_recognition") or {}
            if isinstance(recog, dict) and recog.get("require_payment_proof") is not True:
                failures.append(
                    "claim_policy.yaml.rules.revenue_recognition.require_payment_proof must be true"
                )

    # ── engineering_cutover_policy.yaml
    ok, _cutover, err = load_yaml(CUTOVER)
    if not ok:
        failures.append(err)

    if failures:
        print(f"POLICY-AS-CODE: FAIL ({len(failures)} issues)")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("POLICY-AS-CODE: PASS (approval + claim + cutover policies valid)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
