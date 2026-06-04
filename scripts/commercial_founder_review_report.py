#!/usr/bin/env python3
"""Regenerate the founder review report (markdown + csv) for a given day from
the already-generated draft_queue.jsonl. Review-only; sends nothing."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import commercial_launch_core as core  # noqa: E402


def load_queue(date_str: str) -> list[dict]:
    path = core.output_dir_for(date_str) / "draft_queue.jsonl"
    drafts = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                drafts.append(json.loads(line))
    return drafts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rebuild founder review report.")
    parser.add_argument("--date", default=None)
    args = parser.parse_args(argv)
    date_str = args.date or core.today_str()
    out = core.output_dir_for(date_str)
    if not (out / "draft_queue.jsonl").exists():
        print(f"No draft_queue.jsonl for {date_str}. Run the generator first.", file=sys.stderr)
        return 1
    configs = core.load_all_configs()
    drafts = load_queue(date_str)
    core.write_founder_review_md(drafts, configs, date_str, out)
    core.write_top_50(drafts, date_str, out)
    core.write_next_actions(drafts, configs, date_str, out)
    print(f"Founder review report rebuilt for {date_str} at {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
