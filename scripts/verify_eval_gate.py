#!/usr/bin/env python3
"""Verify the eval gate file is present and lists required gates."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, print_and_exit, repo_root  # noqa: E402

REQUIRED_GATES = [
    "prompt_safety",
    "output_no_guarantee_claims",
    "source_attribution",
    "external_action_blocked_without_approval",
    "registry_completeness",
    "machine_observability",
    "incident_response_runbook",
]


def main() -> int:
    result = VerifyResult(name="Eval Gate", passed=True)
    path = repo_root() / "evals" / "gates" / "dealix_agent_eval_gate.yaml"
    if not path.exists():
        result.passed = False
        result.missing.append(str(path.relative_to(repo_root())))
        return print_and_exit(result)
    text = path.read_text(encoding="utf-8")
    for gate in REQUIRED_GATES:
        if gate not in text:
            result.passed = False
            result.notes.append(f"missing gate: {gate}")
    result.notes.append(f"required gates: {len(REQUIRED_GATES)}")
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
