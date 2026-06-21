#!/usr/bin/env python3
"""
Score targets from ledgers/prospects.csv or data/outreach/saudi_target_intake.csv.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import REPO_ROOT, load_csv, score_target, today_str, write_csv


def main() -> int:
    parser = argparse.ArgumentParser(description="Score Saudi ICP targets")
    parser.add_argument("--input", default="ledgers/prospects.csv")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    input_path = REPO_ROOT / args.input
    rows = load_csv(input_path)
    if not rows:
        print(f"No rows found in {input_path}")
        return 1

    scored: list[dict[str, str]] = []
    for row in rows:
        result = score_target(row)
        out_row = dict(row)
        out_row["dealix_score"] = str(result["score"])
        out_row["dealix_tier"] = result["tier"]
        out_row["dealix_score_reasons"] = ";".join(result["reasons"])
        scored.append(out_row)

    scored.sort(key=lambda r: float(r["dealix_score"]), reverse=True)

    if args.output:
        write_csv(REPO_ROOT / args.output, scored, list(scored[0].keys()))

    report_dir = REPO_ROOT / "reports" / "revenue" / today_str()
    report_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "date": today_str(),
        "input": str(input_path.relative_to(REPO_ROOT)),
        "total": len(scored),
        "hot": sum(1 for r in scored if r["dealix_tier"] == "hot"),
        "warm": sum(1 for r in scored if r["dealix_tier"] == "warm"),
        "cold": sum(1 for r in scored if r["dealix_tier"] == "cold"),
    }
    (report_dir / "score_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Scored {len(scored)} targets; hot={summary['hot']} warm={summary['warm']} cold={summary['cold']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
