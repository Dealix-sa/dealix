#!/usr/bin/env python3
"""Verify evals/gates/dealix_agent_eval_gate.yaml against the required suites.

Each suite must declare id, description, type, pass_threshold, severity,
owner, and at least one sample case.

Exit 0 on success, 1 on any failure.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Tuple

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
GATE_PATH = REPO_ROOT / "evals" / "gates" / "dealix_agent_eval_gate.yaml"

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

REQUIRED_FIELDS = {
    "id",
    "description",
    "type",
    "pass_threshold",
    "severity",
    "owner",
    "sample_cases",
}
ALLOWED_TYPES = {"deterministic", "llm-judge"}
ALLOWED_SEVERITIES = {"block", "warn"}


def load_gate() -> dict:
    if not GATE_PATH.exists():
        raise SystemExit(f"missing eval gate: {GATE_PATH}")
    with GATE_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def main() -> int:
    gate = load_gate()
    suites = gate.get("suites") or []
    results: List[Tuple[str, bool, str]] = []

    results.append((
        "suites is a non-empty list",
        isinstance(suites, list) and len(suites) > 0,
        f"got {type(suites).__name__} length "
        f"{len(suites) if isinstance(suites, list) else 'n/a'}",
    ))

    by_id = {s.get("id"): s for s in suites if isinstance(s, dict)}
    for suite_id in REQUIRED_SUITES:
        suite = by_id.get(suite_id)
        if suite is None:
            results.append((f"suite {suite_id} present", False, "missing"))
            continue
        missing = REQUIRED_FIELDS - set(suite.keys())
        if missing:
            results.append((
                f"suite {suite_id} fields",
                False,
                f"missing {sorted(missing)}",
            ))
            continue
        if suite.get("type") not in ALLOWED_TYPES:
            results.append((
                f"suite {suite_id} type",
                False,
                f"got {suite.get('type')!r}",
            ))
            continue
        if suite.get("severity") not in ALLOWED_SEVERITIES:
            results.append((
                f"suite {suite_id} severity",
                False,
                f"got {suite.get('severity')!r}",
            ))
            continue
        try:
            threshold = float(suite.get("pass_threshold"))
        except (TypeError, ValueError):
            results.append((
                f"suite {suite_id} pass_threshold",
                False,
                f"non-numeric {suite.get('pass_threshold')!r}",
            ))
            continue
        if not 0.0 <= threshold <= 1.0:
            results.append((
                f"suite {suite_id} pass_threshold",
                False,
                f"out of range {threshold}",
            ))
            continue
        sample_cases = suite.get("sample_cases") or []
        if not isinstance(sample_cases, list) or not sample_cases:
            results.append((
                f"suite {suite_id} sample_cases",
                False,
                "must have at least 1 sample case",
            ))
            continue
        results.append((f"suite {suite_id} valid", True, "ok"))

    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print("Dealix eval-gate verification")
    print("-" * 40)
    for label, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {label}: {detail}")
    print("-" * 40)
    print(f"summary: {passed}/{total} checks passed "
          f"({len(REQUIRED_SUITES)} required suites)")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
