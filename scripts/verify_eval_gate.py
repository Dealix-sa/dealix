#!/usr/bin/env python3
"""Verify evals/gates/dealix_agent_eval_gate.yaml is present and blocking suites are declared."""
from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_BLOCKING = {
    "no_guaranteed_claims",
    "approval_bypass",
    "prompt_injection",
    "sensitive_data_leakage",
    "suppression_compliance",
    "evidence_required",
    "proposal_safety",
    "tool_misuse",
    "A3_escalation",
    "proof_safety",
    "pricing_safety",
    "data_export_safety",
    "contract_safety",
    "payment_terms_safety",
}


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    path = repo / "evals" / "gates" / "dealix_agent_eval_gate.yaml"
    if not path.exists():
        print("FAIL: eval gate missing:", path)
        return 1
    try:
        import yaml  # type: ignore
    except ImportError:
        print("WARN: pyyaml not installed; cannot fully verify eval gate")
        return 0
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    suites = data.get("suites") or []
    blocking_ids = {s.get("id") for s in suites if s.get("blocking")}
    missing = REQUIRED_BLOCKING - blocking_ids
    print("[eval-gate]")
    print(f"  blocking suites: {sorted(blocking_ids)}")
    print(f"  missing blocking suites: {sorted(missing)}")
    print("RESULT:", "FAIL" if missing else "PASS")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
