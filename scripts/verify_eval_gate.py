#!/usr/bin/env python3
"""verify_eval_gate.py — every named eval suite must parse and have cases.

Required eval files come from `evals/` (named in the manifest). Each must
be parseable YAML and define at least 3 cases. Empty eval files are a
common Claude Code shortcut — this verifier catches them.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML missing", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parents[1]
EVALS_DIR = REPO / "evals"

REQUIRED_EVALS = (
    "governance_eval.yaml",
    "arabic_quality_eval.yaml",
    "outreach_quality_eval.yaml",
    "lead_intelligence_eval.yaml",
    "company_brain_eval.yaml",
)

MIN_CASES = 3


def case_count(data) -> int:
    if isinstance(data, dict):
        for key in ("cases", "tests", "scenarios", "examples", "checks", "items"):
            v = data.get(key)
            if isinstance(v, list):
                return len(v)
        # fall back: any list at the top level
        for v in data.values():
            if isinstance(v, list):
                return len(v)
    return 0


def main() -> int:
    if not EVALS_DIR.is_dir():
        print("missing_dir:evals", file=sys.stderr)
        return 1

    failures: list[str] = []
    for name in REQUIRED_EVALS:
        p = EVALS_DIR / name
        if not p.exists():
            failures.append(f"missing:evals/{name}")
            continue
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            failures.append(f"invalid_yaml:evals/{name} ({exc})")
            continue
        n = case_count(data)
        if n < MIN_CASES:
            failures.append(f"too_few_cases:evals/{name} ({n}<{MIN_CASES})")

    for f in failures:
        print(f, file=sys.stderr)
    ok = not failures
    print(f"EVAL_GATE_PASS={'true' if ok else 'false'} (failures={len(failures)})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
