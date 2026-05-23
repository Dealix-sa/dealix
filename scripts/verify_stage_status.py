#!/usr/bin/env python3
"""
verify_stage_status.py — assert the stage status file references a real gate.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STAGE_FILE = REPO / "DEALIX_STAGE_STATUS.md"
GATES_DIR = REPO / "readiness" / "gates"


REQUIRED_STAGES = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
]


def main() -> int:
    if not STAGE_FILE.exists():
        print(f"[FAIL] missing {STAGE_FILE.relative_to(REPO)}")
        return 1
    text = STAGE_FILE.read_text(encoding="utf-8")
    for stage in REQUIRED_STAGES:
        if not re.search(rf"\b{stage}\b", text):
            print(f"[FAIL] DEALIX_STAGE_STATUS.md missing stage {stage}")
            return 1

    gate_files = sorted(GATES_DIR.glob("gate_*.md"))
    if len(gate_files) < 10:
        print(f"[FAIL] expected 10 gate files, found {len(gate_files)}")
        return 1

    print(f"[OK] verify_stage_status: {len(gate_files)} gates declared, all stages referenced")
    return 0


if __name__ == "__main__":
    sys.exit(main())
