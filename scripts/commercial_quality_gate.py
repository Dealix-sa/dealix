"""Quality gate CLI — score draft bodies against the quality rubric.

Pass threshold = 70. Founder priority threshold = 80.
Importable: quality_check(draft) -> (score, reasons).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Run both as `python scripts/<file>.py` and `python -m scripts.<file>`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.commercial_launch_core import load_all_configs, quality_gate


def quality_check(
    draft: dict[str, Any], cfg: dict[str, Any] | None = None
) -> tuple[int, list[str]]:
    cfg = cfg or load_all_configs()
    return quality_gate(draft, cfg)


def gate_file(path: Path) -> dict[str, Any]:
    cfg = load_all_configs()
    threshold = cfg["quality"]["pass_threshold"]
    rows = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    passed = failed = 0
    failures = []
    for d in rows:
        score, reasons = quality_gate(d, cfg)
        if score >= threshold:
            passed += 1
        else:
            failed += 1
            failures.append({"draft_id": d.get("draft_id"), "score": score, "reasons": reasons})
    return {
        "total": len(rows),
        "passed": passed,
        "failed": failed,
        "pass_threshold": threshold,
        "failures": failures[:50],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Quality gate for commercial drafts.")
    ap.add_argument("--file", required=True, help="draft_queue.jsonl path")
    args = ap.parse_args(argv)
    report = gate_file(Path(args.file))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
