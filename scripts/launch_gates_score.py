#!/usr/bin/env python3
"""Parse docs/LAUNCH_GATES.md and count closed vs open gates."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATES_MD = ROOT / "docs" / "LAUNCH_GATES.md"

STATUS_RE = re.compile(r"\|\s*([A-Z]\d+)\s*\|[^|]+\|\s*([✅🟡🔴🚫])")


def score_gates() -> dict:
    text = GATES_MD.read_text(encoding="utf-8") if GATES_MD.is_file() else ""
    closed = 0
    partial = 0
    open_ = 0
    blocked = 0
    gates: list[dict] = []
    for m in STATUS_RE.finditer(text):
        gid, icon = m.group(1), m.group(2)
        if icon == "✅":
            closed += 1
            st = "closed"
        elif icon == "🟡":
            partial += 1
            st = "partial"
        elif icon == "🚫":
            blocked += 1
            st = "blocked"
        else:
            open_ += 1
            st = "open"
        gates.append({"id": gid, "status": st})
    total = len(gates)
    return {
        "total_gates": total,
        "closed": closed,
        "partial": partial,
        "open": open_,
        "blocked": blocked,
        "launch_ready": closed >= 24 and total >= 30,
        "target_closed": 24,
        "gates_sample": gates[:10],
    }


def main() -> int:
    report = score_gates()
    verdict = "PASS" if report["launch_ready"] else "PARTIAL"
    print(f"LAUNCH_GATES_VERDICT={verdict}")
    print(
        f"closed={report['closed']}/{report['total_gates']} "
        f"open={report['open']} blocked={report['blocked']}"
    )
    return 0 if report["launch_ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
