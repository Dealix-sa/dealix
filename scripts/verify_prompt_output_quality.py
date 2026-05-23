#!/usr/bin/env python3
"""Verify the prompt output eval matrix is present.

This is a presence check; the full scoring runs inside the Eval Guardian
runtime and writes its results to evals/eval_status.csv.

Exit 0 on success, 1 on failure.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MATRIX_PATH = REPO_ROOT / "docs" / "evals" / "PROMPT_OUTPUT_EVAL_MATRIX.md"
MIN_BYTES = 200


def main() -> int:
    print("Dealix prompt-output-quality verification")
    print("-" * 40)
    if not MATRIX_PATH.exists():
        print(f"  [FAIL] missing {MATRIX_PATH}")
        print("summary: FAIL")
        return 1
    size = MATRIX_PATH.stat().st_size
    if size < MIN_BYTES:
        print(f"  [FAIL] {MATRIX_PATH} is too small ({size} bytes; min {MIN_BYTES})")
        print("summary: FAIL")
        return 1
    print(f"  [PASS] {MATRIX_PATH} ({size} bytes)")
    print("summary: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
