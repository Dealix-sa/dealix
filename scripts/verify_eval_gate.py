#!/usr/bin/env python3
"""
verify_eval_gate.py — AI eval gate must be defined and parsable.

Validates:
  - evals/*.yaml parse and have non-trivial content
  - scripts/verify_ai_output_quality.py exists and compiles

Does NOT execute the LLM evals (those need API keys + cost); it ensures
the gate itself exists and is wired so CI can run it.
"""
from __future__ import annotations

import py_compile
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FATAL: PyYAML not installed", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
QUALITY_SCRIPT = ROOT / "scripts/verify_ai_output_quality.py"

REQUIRED_EVALS = [
    "governance_eval.yaml",
    "arabic_quality_eval.yaml",
    "outreach_quality_eval.yaml",
    "company_brain_eval.yaml",
    "lead_intelligence_eval.yaml",
]


def main() -> int:
    failures: list[str] = []

    if not EVALS.exists():
        failures.append("evals/ directory missing")
    else:
        for name in REQUIRED_EVALS:
            p = EVALS / name
            if not p.exists():
                failures.append(f"missing eval: evals/{name}")
                continue
            try:
                data = yaml.safe_load(p.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                failures.append(f"invalid yaml in evals/{name}: {exc}")
                continue
            if not data:
                failures.append(f"evals/{name} is empty")

    if not QUALITY_SCRIPT.exists():
        failures.append("scripts/verify_ai_output_quality.py missing")
    else:
        try:
            py_compile.compile(str(QUALITY_SCRIPT), doraise=True)
        except py_compile.PyCompileError as exc:
            failures.append(f"verify_ai_output_quality.py does not compile: {exc}")

    if failures:
        print(f"EVAL GATE: FAIL ({len(failures)} issues)")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"EVAL GATE: PASS ({len(REQUIRED_EVALS)} evals + quality script)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
