#!/usr/bin/env python3
"""Summarize a day's commercial launch metrics from the generated artifacts.

Combines daily_metrics.json, quality_report.json, compliance_report.json, and
safety_audit.json into a single metrics_summary.json + markdown digest. All
business outcome numbers (replies, revenue, etc.) remain manual-input and are
echoed as schema only — never assumed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import (
    COMMERCIAL_OUTPUTS,
    load_config,
    today_str,
    write_json,
    write_text,
)


def _read(path: Path) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize commercial launch metrics.")
    parser.add_argument("--date", default=today_str())
    args = parser.parse_args()

    out_dir = COMMERCIAL_OUTPUTS / args.date
    daily = _read(out_dir / "daily_metrics.json")
    quality = _read(out_dir / "quality_report.json")
    compliance = _read(out_dir / "compliance_report.json")
    safety = _read(out_dir / "safety_audit.json")
    manual_schema = [m["key"] for m in load_config("commercial_metrics.json")["metrics"]]

    summary = {
        "date": args.date,
        "automated": {
            "drafts_generated": daily.get("drafts_generated"),
            "ready_for_review": daily.get("ready_for_review"),
            "rejected": daily.get("rejected"),
            "needs_research": daily.get("needs_research"),
            "target_met": daily.get("target_met"),
            "avg_quality_score": quality.get("avg_quality_score"),
            "avg_compliance_score": compliance.get("avg_compliance_score"),
            "safety_passed": safety.get("passed"),
        },
        "manual_input_required": dict.fromkeys(manual_schema),
        "note": "Outcome numbers are manual-input. The repo never assumes real figures.",
    }
    write_json(out_dir / "metrics_summary.json", summary)

    md = [
        f"# Commercial Metrics Summary — {args.date}",
        "",
        f"- Drafts generated: {summary['automated']['drafts_generated']}",
        f"- Ready for review: {summary['automated']['ready_for_review']}",
        f"- Target met (>=400): {summary['automated']['target_met']}",
        f"- Avg quality score: {summary['automated']['avg_quality_score']}",
        f"- Avg compliance score: {summary['automated']['avg_compliance_score']}",
        f"- Safety audit passed: {summary['automated']['safety_passed']}",
        "",
        "## Manual-input metrics (founder fills)",
        *[f"- {k}: —" for k in manual_schema],
    ]
    write_text(out_dir / "metrics_summary.md", "\n".join(md) + "\n")
    print(f"METRICS SUMMARY: written for {args.date}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
