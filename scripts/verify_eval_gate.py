#!/usr/bin/env python3
"""Verify evals/gates/dealix_agent_eval_gate.yaml has the required suites."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[verify_eval_gate] PyYAML not installed", file=sys.stderr)
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
PATH = REPO_ROOT / "evals" / "gates" / "dealix_agent_eval_gate.yaml"

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
    "proof_safety",
    "pricing_safety",
}


def main() -> int:
    if not PATH.exists():
        print(f"[verify_eval_gate] missing: {PATH}")
        return 1
    data = yaml.safe_load(PATH.read_text(encoding="utf-8")) or {}
    suites = {s.get("id") for s in data.get("suites", []) if isinstance(s, dict)}
    missing = REQUIRED_SUITES - suites
    if missing:
        print(f"[verify_eval_gate] FAIL: missing suites {sorted(missing)}")
        return 1
    print(f"[verify_eval_gate] PASS  suites={len(suites)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
