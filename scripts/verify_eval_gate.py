#!/usr/bin/env python3
"""Verify ``evals/gates/dealix_agent_eval_gate.yaml`` has all required suites."""

from __future__ import annotations

import sys
from pathlib import Path

GATE = Path("evals/gates/dealix_agent_eval_gate.yaml")
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
    "data_export_safety",
    "contract_safety",
    "payment_terms_safety",
}


def _load() -> list[str]:
    text = GATE.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore[import-not-found]

        data = yaml.safe_load(text) or {}
        return [s.get("name") for s in data.get("suites", []) if isinstance(s, dict)]
    except ImportError:
        names: list[str] = []
        in_suites = False
        for raw in text.splitlines():
            line = raw.rstrip()
            if not line or line.lstrip().startswith("#"):
                continue
            if not line.startswith(" "):
                in_suites = line.startswith("suites")
                continue
            if in_suites and line.lstrip().startswith("- name:"):
                names.append(line.split(":", 1)[1].strip())
        return names


def main() -> int:
    if not GATE.exists():
        print("[FAIL] eval gate yaml missing", file=sys.stderr)
        return 1
    names = set(_load())
    missing = REQUIRED_SUITES - names
    if missing:
        print(f"[FAIL] missing eval suites: {sorted(missing)}", file=sys.stderr)
        return 1
    print(f"[PASS] eval gate: {len(names)} suites")
    return 0


if __name__ == "__main__":
    sys.exit(main())
