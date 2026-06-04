#!/usr/bin/env python3
"""Quality gate over the daily draft queue -> quality_report.json.

Flags drafts below quality thresholds. Does not send anything.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import (
    now_iso,
    output_day_dir,
    read_jsonl,
    today_str,
    write_json,
)

MIN_QUALITY = 60
MIN_BODY_LEN = 80


def run(day: str) -> dict:
    d = output_day_dir(day)
    drafts = read_jsonl(d / "draft_queue.jsonl")
    failed = []
    for dr in drafts:
        reasons = []
        if dr["quality_score"] < MIN_QUALITY:
            reasons.append(f"quality<{MIN_QUALITY}")
        if len(dr.get("body", "")) < MIN_BODY_LEN:
            reasons.append("body_too_short")
        if not dr.get("subject"):
            reasons.append("missing_subject")
        if not dr.get("cta"):
            reasons.append("missing_cta")
        if reasons:
            failed.append({"draft_id": dr["draft_id"], "reasons": reasons})
    report = {
        "generated_at": now_iso(),
        "day": day,
        "total": len(drafts),
        "min_quality": MIN_QUALITY,
        "passed": len(drafts) - len(failed),
        "failed": len(failed),
        "pass_rate": round((len(drafts) - len(failed)) / max(len(drafts), 1), 4),
        "failures": failed[:200],
    }
    write_json(d / "quality_report.json", report)
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", default=today_str())
    args = ap.parse_args()
    r = run(args.day)
    print(f"Quality gate: {r['passed']}/{r['total']} passed ({r['pass_rate']:.1%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
