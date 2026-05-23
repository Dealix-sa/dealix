#!/usr/bin/env python3
"""Verify the policy-as-code file declares the required rules."""

from __future__ import annotations

from pathlib import Path

from _verify_common import ROOT, Verifier

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


def populate(v: Verifier) -> None:
    path = ROOT / "policies" / "dealix_control_policy.yaml"
    if not v.check_file("policies/dealix_control_policy.yaml"):
        return
    text = Path(path).read_text(encoding="utf-8")
    for rule in REQUIRED_RULES:
        v.custom(f"id: {rule}" in text, f"policy declares rule {rule}")


if __name__ == "__main__":
    from _verify_common import main_for

    main_for("policy-as-code", populate)
