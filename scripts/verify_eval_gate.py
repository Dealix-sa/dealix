#!/usr/bin/env python3
"""Verify evals/gates/dealix_agent_eval_gate.yaml has required suites."""

from __future__ import annotations

import sys
from pathlib import Path

GATE_PATH = (
    Path(__file__).resolve().parents[1]
    / "evals"
    / "gates"
    / "dealix_agent_eval_gate.yaml"
)
REQUIRED_SUITES = {
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
}


def main() -> int:
    if not GATE_PATH.exists():
        print(f"FAIL: missing eval gate {GATE_PATH}")
        return 1
    try:
        import yaml  # type: ignore
    except ImportError:
        print("FAIL: PyYAML not installed; pip install pyyaml")
        return 1
    with GATE_PATH.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        print("FAIL: eval gate is not a mapping")
        return 1
    suites = data.get("suites") or []
    suite_ids = {s.get("id") for s in suites if isinstance(s, dict)}
    missing = REQUIRED_SUITES - suite_ids
    if missing:
        print(f"FAIL: missing suites: {sorted(missing)}")
        return 1
    thresholds = data.get("thresholds") or {}
    if not thresholds.get("critical_must_pass", False):
        print("FAIL: thresholds.critical_must_pass must be true")
        return 1
    print(f"OK: eval_gate v{data.get('version', '?')}")
    print(f"  suites: {sorted(suite_ids)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
