#!/usr/bin/env python3
"""Verify evals/gates/dealix_agent_eval_gate.yaml exists and is well-formed.

Schema assertions:
  - class_gates contains A1, A2, A3 with min_pass_rate fields
  - referenced_datasets all exist on disk
  - safety_gates contains banned_claims_suppression + external_send_approval
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
GATE_PATH = REPO / "evals" / "gates" / "dealix_agent_eval_gate.yaml"


def _fail(msg: str) -> None:
    print(msg, file=sys.stderr)


def main() -> int:
    if not GATE_PATH.is_file():
        _fail(f"missing_eval_gate:{GATE_PATH.relative_to(REPO)}")
        print("EVAL_GATE_PASS=false")
        return 1

    try:
        data = yaml.safe_load(GATE_PATH.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        _fail(f"yaml_error:{exc}")
        print("EVAL_GATE_PASS=false")
        return 1

    errors: list[str] = []

    class_gates = data.get("class_gates") or {}
    for cls in ("A1", "A2", "A3"):
        if cls not in class_gates:
            errors.append(f"missing_class_gate:{cls}")
        elif "min_pass_rate" not in class_gates[cls]:
            errors.append(f"missing_min_pass_rate:{cls}")

    for ds in data.get("referenced_datasets") or []:
        if not (REPO / ds).is_file():
            errors.append(f"missing_dataset:{ds}")

    safety = data.get("safety_gates") or {}
    for required in ("banned_claims_suppression", "external_send_approval"):
        if required not in safety:
            errors.append(f"missing_safety_gate:{required}")

    for err in errors:
        _fail(err)

    ok = not errors
    print(f"EVAL_GATE_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
