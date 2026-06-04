#!/usr/bin/env python3
"""Commercial metrics summary. Combines draft-factory output metrics with a
manual/example commercial funnel (revenue is NEVER assumed — it is manual
input or example values). Review-only; sends nothing."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import commercial_launch_core as core  # noqa: E402

# Manual / example funnel — replace with real founder-entered values.
EXAMPLE_FUNNEL = {
    "approved_manual": 0,
    "manual_sent": 0,
    "replies_positive": 0,
    "replies_negative": 0,
    "qualified_calls": 0,
    "diagnostics_sold": 0,
    "pilots_sold": 0,
    "retainers_started": 0,
    "revenue_pipeline_sar": 0,
    "realized_revenue_sar": 0,
}


def summarize(date_str: str, funnel: dict | None = None) -> dict:
    funnel = funnel or dict(EXAMPLE_FUNNEL)
    metrics_path = core.output_dir_for(date_str) / "daily_metrics.json"
    draft_metrics = {}
    if metrics_path.exists():
        draft_metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    sent = funnel.get("manual_sent", 0) or 0
    pos = funnel.get("replies_positive", 0) or 0
    funnel["reply_rate"] = round(pos / sent, 3) if sent else 0.0
    return {
        "date": date_str,
        "draft_factory": {
            "drafts_generated": draft_metrics.get("drafts_generated", 0),
            "founder_review_count": draft_metrics.get("founder_review_count", 0),
            "rejected_quality": draft_metrics.get("rejected_quality", 0),
            "rejected_compliance": draft_metrics.get("rejected_compliance", 0),
            "needs_research": draft_metrics.get("needs_research", 0),
        },
        "manual_funnel": funnel,
        "note": "Revenue and reply metrics are manual/example values, not assumed.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Commercial metrics summary.")
    parser.add_argument("--date", default=None)
    args = parser.parse_args(argv)
    date_str = args.date or core.today_str()
    summary = summarize(date_str)
    out = core.output_dir_for(date_str)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "commercial_metrics.json").open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
