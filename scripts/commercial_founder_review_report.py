#!/usr/bin/env python3
"""Regenerate the founder review report (md/csv/top-50) from a draft batch.

Reads the latest (or a given) draft_queue.jsonl and rewrites the founder-facing
artifacts. Does not generate new drafts and never sends anything.
"""

from __future__ import annotations

import argparse
import json
import sys

import commercial_launch_lib as lib


def _load_batch(date: str | None) -> list[dict]:
    out = lib.output_dir(date)
    queue = out / "draft_queue.jsonl"
    if not queue.exists():
        print(f"No draft_queue.jsonl at {queue}. Run the generator first.", file=sys.stderr)
        return []
    drafts = []
    with queue.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                drafts.append(json.loads(line))
    return drafts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rebuild founder review report")
    parser.add_argument("--date", type=str, default=None)
    args = parser.parse_args(argv)

    drafts = _load_batch(args.date)
    if not drafts:
        return 1
    config = lib.load_all_config()
    out = lib.write_outputs(drafts, config, date=args.date)
    print(f"✅ Founder review report rebuilt at {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
