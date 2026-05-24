#!/usr/bin/env python3
"""Verify prompt-output quality docs + eval gate are in place.

Lightweight stand-in for a heavier eval runner: this script checks that the
prompt/output evaluation matrix is defined and that the eval gate references
the same suites the matrix lists.
"""

from __future__ import annotations

from pathlib import Path

from _verify_common import ROOT, Verifier


def populate(v: Verifier) -> None:
    if not v.check_file("docs/evals/PROMPT_OUTPUT_EVAL_MATRIX.md"):
        return
    if not v.check_file("evals/gates/dealix_agent_eval_gate.yaml"):
        return

    matrix = Path(ROOT / "docs" / "evals" / "PROMPT_OUTPUT_EVAL_MATRIX.md").read_text(encoding="utf-8")
    gate = Path(ROOT / "evals" / "gates" / "dealix_agent_eval_gate.yaml").read_text(encoding="utf-8")

    expected = [
        "no_guaranteed_claims",
        "prompt_injection",
        "sensitive_data_leakage",
        "approval_bypass",
        "tool_misuse",
    ]
    for token in expected:
        v.custom(
            token in matrix and token in gate,
            f"matrix + gate both reference: {token}",
        )


if __name__ == "__main__":
    from _verify_common import main_for

    main_for("prompt-output-quality", populate)
