#!/usr/bin/env python3
"""Verify the eval gate declares the required suites."""

from __future__ import annotations

from pathlib import Path

from _verify_common import ROOT, Verifier

REQUIRED_SUITES = [
    "no_guaranteed_claims",
    "approval_bypass",
    "prompt_injection",
    "sensitive_data_leakage",
    "suppression_compliance",
    "evidence_required",
    "arabic_business_quality",
    "proposal_safety",
    "tool_misuse",
    "A3_escalation",
    "proof_safety",
    "pricing_safety",
    "data_export_safety",
    "contract_safety",
    "payment_terms_safety",
]


def populate(v: Verifier) -> None:
    if not v.check_file("evals/gates/dealix_agent_eval_gate.yaml"):
        return
    text = Path(ROOT / "evals" / "gates" / "dealix_agent_eval_gate.yaml").read_text(encoding="utf-8")
    for suite in REQUIRED_SUITES:
        v.custom(f"id: {suite}" in text, f"eval gate declares suite: {suite}")
    v.check_file("docs/evals/EVAL_GATE_V1.md")
    v.check_file("docs/evals/PROMPT_OUTPUT_EVAL_MATRIX.md")


if __name__ == "__main__":
    from _verify_common import main_for

    main_for("eval-gate", populate)
