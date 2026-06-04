#!/usr/bin/env python3
"""Summarize today's commercial outputs into daily_metrics.json (no fabricated numbers)."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5.lib import out_dir  # noqa: E402


def main() -> int:
    d = out_dir()
    q = d / "draft_queue.jsonl"
    drafts = [json.loads(l) for l in q.read_text(encoding="utf-8").splitlines() if l.strip()] if q.exists() else []
    by_v: dict[str, int] = {}
    for x in drafts:
        by_v[x["vertical"]] = by_v.get(x["vertical"], 0) + 1
    summary = {
        "date": d.name,
        "drafts_generated": len(drafts),
        "by_vertical": by_v,
        "manual_sends": 0,
        "replies": 0,
        "positive_replies": 0,
        "note": "Engagement metrics are founder-entered; the system fabricates nothing and sends nothing.",
    }
    (d / "daily_metrics.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
