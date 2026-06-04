#!/usr/bin/env python3
"""Rebuild the founder review report from a draft queue.

Reads outputs/commercial_launch/<date>/draft_queue.jsonl and (re)writes the
ranked founder_review.csv / founder_review.md and a compact digest. This is the
queue the founder works from — every row is review-only and sent manually.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import (
    COMMERCIAL_OUTPUTS,
    GOVERNING_RULE,
    load_config,
    read_jsonl,
    today_str,
    write_csv,
    write_text,
)


def build_report(drafts: list[dict[str, Any]], day: str) -> dict[str, Any]:
    rules = load_config("commercial_founder_review_rules.json")
    cols = rules["review_columns"]
    approved = [d for d in drafts if d.get("status") == "ready_for_founder_review"]
    ranked = sorted(approved, key=lambda d: d.get("priority_score", 0), reverse=True)
    rows = [[d.get(c, "") for c in cols] for d in ranked]
    return {"cols": cols, "rows": rows, "ranked": ranked, "approved": approved}


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild founder review report.")
    parser.add_argument("--date", default=today_str())
    args = parser.parse_args()

    out_dir = COMMERCIAL_OUTPUTS / args.date
    drafts = read_jsonl(out_dir / "draft_queue.jsonl")
    if not drafts:
        print(f"No drafts at {out_dir / 'draft_queue.jsonl'}")
        return 1

    rep = build_report(drafts, args.date)
    write_csv(out_dir / "founder_review.csv", rep["cols"], rep["rows"])

    lines = [
        f"# Founder Review Queue — {args.date}",
        "",
        f"> {GOVERNING_RULE}",
        "",
        f"- Total drafts: **{len(drafts)}**",
        f"- Ready for review: **{len(rep['approved'])}**",
        "",
        "| # | Priority | Company | Vertical | Channel | Lang | Offer | Subject |",
        "|---|----------|---------|----------|---------|------|-------|---------|",
    ]
    for idx, d in enumerate(rep["ranked"][:100], 1):
        lines.append(
            f"| {idx} | {d.get('priority_score')} | {d.get('company_name')} | {d.get('vertical')} | "
            f"{d.get('channel')} | {d.get('language')} | {d.get('offer_name')} | "
            f"{str(d.get('subject', '')).replace('|', '/')} |"
        )
    write_text(out_dir / "founder_review.md", "\n".join(lines) + "\n")

    print(
        f"FOUNDER REVIEW REPORT: rebuilt for {args.date} — {len(rep['approved'])} ready of {len(drafts)}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
