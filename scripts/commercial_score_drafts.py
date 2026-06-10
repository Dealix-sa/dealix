#!/usr/bin/env python3
"""Re-score and rank the daily draft queue by priority.

Recomputes priority_score = quality*0.3 + compliance*0.2 + fit*0.5 and writes
a ranked view back, plus needs_research.jsonl for low-fit drafts. Sends nothing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import output_day_dir, read_jsonl, today_str, write_jsonl


def run(day: str) -> dict:
    d = output_day_dir(day)
    drafts = read_jsonl(d / "draft_queue.jsonl")
    for dr in drafts:
        dr["priority_score"] = round(
            dr["quality_score"] * 0.3 + dr["compliance_score"] * 0.2 + dr["fit_score"] * 0.5, 2
        )
    drafts.sort(key=lambda x: x["priority_score"], reverse=True)
    write_jsonl(d / "draft_queue.jsonl", drafts)
    needs_research = [dr for dr in drafts if dr.get("research_required")]
    write_jsonl(d / "needs_research.jsonl", needs_research)
    return {"total": len(drafts), "needs_research": len(needs_research)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", default=today_str())
    args = ap.parse_args()
    r = run(args.day)
    print(f"Scored {r['total']} drafts; {r['needs_research']} need research")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
