#!/usr/bin/env python3
"""
verify_policy_as_code.py — confirm the 11 invariants in
policies/dealix_control_policy.yaml resolve against the canonical sources.

Exit codes:
  0 = PASS
  1 = FAIL
  2 = missing deps (yaml not installed, file not found)

Output: KEY=value lines + a markdown summary.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CANON = {
    "approval_policy": ROOT / "dealix" / "config" / "approval_policy.yaml",
    "claim_policy": ROOT / "dealix" / "config" / "claim_policy.yaml",
    "governance_os": ROOT / "auto_client_acquisition" / "governance_os" / "policies" / "default_registry.yaml",
}
WRAPPER = ROOT / "policies" / "dealix_control_policy.yaml"


def _load_yaml(path: Path):
    try:
        import yaml  # type: ignore
    except ImportError:
        print("POLICY_AS_CODE=fail reason=pyyaml_not_installed")
        sys.exit(2)
    if not path.exists():
        print(f"POLICY_AS_CODE=fail reason=missing_file path={path}")
        sys.exit(1)
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> int:
    strict = "--strict" in sys.argv
    failures: list[str] = []
    warnings: list[str] = []

    approval = _load_yaml(CANON["approval_policy"])
    claim = _load_yaml(CANON["claim_policy"])
    gov = _load_yaml(CANON["governance_os"])
    wrapper = _load_yaml(WRAPPER)

    # Invariants
    if not approval.get("external_message", {}).get("requires_approval"):
        failures.append("NO_LIVE_SEND: external_message.requires_approval != true")
    if not claim.get("rules", {}).get("revenue_recognition", {}).get("require_payment_proof"):
        failures.append("NO_LIVE_CHARGE / NO_FAKE_REVENUE: revenue_recognition.require_payment_proof != true")
    forbidden = gov.get("forbidden_customer_facing_actions", [])
    for needed in ("cold_whatsapp_auto_send", "linkedin_dm_automation", "production_web_scraping"):
        if needed not in forbidden:
            failures.append(f"forbidden_customer_facing_actions missing: {needed}")
    if not approval.get("case_study_publish", {}).get("requires_approval"):
        failures.append("NO_UNAPPROVED_TESTIMONIAL: case_study_publish.requires_approval != true")
    rule_num = claim.get("rules", {}).get("numeric_claim_in_customer_pack", {})
    if rule_num.get("must_have_source_or") != "is_estimate_true":
        failures.append("NO_UNSOURCED_NUMERIC_CLAIM: must_have_source_or != is_estimate_true")
    rule_roi = claim.get("rules", {}).get("roi_or_guarantee", {})
    if rule_roi.get("allowed") is not False:
        failures.append("NO_ROI_OR_GUARANTEE: roi_or_guarantee.allowed != false")

    # Wrapper sanity
    if wrapper.get("kind") != "dealix.control_policy":
        warnings.append("control_policy.kind drifted")
    extends = wrapper.get("extends", [])
    expected = {
        "dealix/config/approval_policy.yaml",
        "dealix/config/claim_policy.yaml",
        "auto_client_acquisition/governance_os/policies/default_registry.yaml",
    }
    if expected - set(extends):
        warnings.append(f"control_policy.extends missing: {expected - set(extends)}")

    verdict = "PASS" if not failures and (not strict or not warnings) else "FAIL"

    print(f"POLICY_AS_CODE={verdict.lower()}")
    print(f"POLICY_AS_CODE_FAILS={len(failures)}")
    print(f"POLICY_AS_CODE_WARNS={len(warnings)}")
    if failures:
        print("\n## Policy-as-Code FAILURES")
        for f in failures:
            print(f"  - {f}")
    if warnings:
        print("\n## Policy-as-Code WARNINGS")
        for w in warnings:
            print(f"  - {w}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
