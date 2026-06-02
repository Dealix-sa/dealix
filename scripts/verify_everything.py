#!/usr/bin/env python3
"""Master Company OS verifier.

Runs every layer verifier as a subprocess and prints a unified
DEALIX EVERYTHING VERIFICATION report:

    Brand OS: PASS
    Founder Console: PASS
    ...

    RESULT: PASS

Exits 0 iff every child verifier exits 0.

Output is deterministic; lines are stable so CI / Slack can parse them.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Check:
    label: str
    script: str


# Order matters: top-level layer verifiers first, then aggregators, then
# the company_os layer roll-up. Each entry is a (label, script) pair.
CHECKS: tuple[Check, ...] = (
    Check("Brand OS", "verify_brand_system.py"),
    Check("Growth System", "verify_growth_system.py"),
    Check("Marketing System", "verify_marketing_system.py"),
    Check("Product Distribution", "verify_product_distribution.py"),
    Check("Policy-as-Code", "verify_policy_as_code.py"),
    Check("Agent Registry", "verify_agent_registry.py"),
    Check("Machine Registry", "verify_machine_registry.py"),
    Check("Eval Gate", "verify_eval_gate.py"),
    Check("Prompt + Output Safety", "verify_prompt_output_quality.py"),
    Check("AI Governance (aggregate)", "verify_ai_governance_system.py"),
    Check("Launch Readiness", "verify_launch_readiness.py"),
    Check("Execution / Launch Layer", "verify_execution_launch_layer.py"),
    Check("Market Attack", "verify_market_attack_system.py"),
    Check("Scale / Moat", "verify_scale_moat_system.py"),
    Check("Founder Management", "verify_founder_management_system.py"),
    Check("Hypergrowth CEO", "verify_hypergrowth_ceo_layer.py"),
    Check("Founder + CEO + Hypergrowth (aggregate)", "verify_founder_ceo_hypergrowth_layer.py"),
    Check("Company OS layers", "verify_company_os.py"),
)


def _run(script: str) -> tuple[bool, str, str]:
    proc = subprocess.run(  # noqa: S603
        [sys.executable, str(REPO / "scripts" / script)],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0, proc.stdout, proc.stderr


def main() -> int:
    print("DEALIX EVERYTHING VERIFICATION")
    print("")

    results: list[tuple[Check, bool, str, str]] = []
    for check in CHECKS:
        ok, out, err = _run(check.script)
        results.append((check, ok, out, err))
        print(f"{check.label}: {'PASS' if ok else 'FAIL'}")

    missing: list[str] = []
    failed: list[str] = []
    risks: list[str] = []

    for check, ok, out, err in results:
        if ok:
            continue
        failed.append(f"{check.label} ({check.script})")
        for line in (err or "").splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("missing_"):
                missing.append(f"{check.label}: {line}")
            elif line.startswith("banned_phrase_in_doc:"):
                risks.append(f"{check.label}: {line}")
            elif line.startswith("forbidden_") or line.startswith("draft_gate_"):
                risks.append(f"{check.label}: {line}")

    print("")
    if missing:
        print("Missing:")
        for m in missing:
            print(f"- {m}")
        print("")

    if failed:
        print("Failed:")
        for f in failed:
            print(f"- {f}")
        print("")

    if risks:
        print("Risk:")
        for r in risks:
            print(f"- {r}")
        print("")

    overall = all(ok for _, ok, _, _ in results)
    print(f"RESULT: {'PASS' if overall else 'FAIL'}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
