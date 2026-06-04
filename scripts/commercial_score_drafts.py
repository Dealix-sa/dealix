#!/usr/bin/env python3
"""Re-score drafts (quality / compliance / fit / priority) without sending.

Thin CLI over commercial_launch_lib scoring functions. Prints a JSON summary.
"""

from __future__ import annotations

import json
import sys

import commercial_launch_lib as lib


def main(argv: list[str] | None = None) -> int:
    config = lib.load_all_config()
    drafts = lib.generate_drafts(target=400, config=config)
    summary = lib.summarize(drafts)
    avg_priority = round(sum(d["priority_score"] for d in drafts) / len(drafts), 4)
    print(json.dumps({"summary": summary, "avg_priority_score": avg_priority}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
