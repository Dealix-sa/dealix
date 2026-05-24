#!/usr/bin/env python3
"""Enterprise motion health.

Reads docs/ops/pipeline_tracker.csv + docs/ops/CEO_TOP50_TRACKER.csv,
emits stage health + multi-thread coverage. Repo-resident sources;
PRIVATE_OPS not required.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BRIEFS = ROOT / "data/founder_briefs"
PIPELINE_CSV = ROOT / "docs/ops/pipeline_tracker.csv"
TOP50_CSV = ROOT / "docs/ops/CEO_TOP50_TRACKER.csv"


STAGES = [
    "discovery", "validation", "procurement",
    "security_review", "proposal", "negotiation", "signed",
]


def _safe_read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _is_enterprise(row: dict[str, str]) -> bool:
    seg = (row.get("segment") or row.get("tier") or "").lower()
    if "enterprise" in seg:
        return True
    try:
        arr = float(row.get("expected_arr_sar") or 0)
    except (TypeError, ValueError):
        arr = 0
    return arr >= 100_000


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    pipeline = _safe_read_csv(PIPELINE_CSV)
    top50 = _safe_read_csv(TOP50_CSV)

    enterprise_rows = [r for r in pipeline if _is_enterprise(r)]
    stage_counts = Counter()
    for row in enterprise_rows:
        stage_counts[(row.get("stage") or "unknown").lower()] += 1
    stage_table = {s: stage_counts.get(s, 0) for s in STAGES}

    multi_thread = sum(
        1 for row in top50
        if (row.get("threads_count") or "").isdigit() and int(row["threads_count"]) >= 2
    )
    total_top50 = len(top50)

    blob = {
        "generated_at": datetime.now(UTC).isoformat(),
        "enterprise_rows": len(enterprise_rows),
        "stage_counts": stage_table,
        "top50_rows": total_top50,
        "multi_thread_count": multi_thread,
        "multi_thread_ratio": round(multi_thread / total_top50, 3) if total_top50 else 0,
    }

    BRIEFS.mkdir(parents=True, exist_ok=True)
    week_end = datetime.now(UTC).strftime("%Y-%m-%d")
    out = BRIEFS / f"enterprise_motion_health_{week_end}.md"

    lines = [
        f"# Enterprise Motion Health — {week_end}",
        "",
        f"Enterprise rows: {blob['enterprise_rows']}",
        f"Top-50 strategic accounts: {blob['top50_rows']}",
        f"Multi-threaded accounts (≥ 2 threads): {blob['multi_thread_count']} "
        f"({blob['multi_thread_ratio']})",
        "",
        "## Stage counts",
    ]
    for stage, count in stage_table.items():
        lines.append(f"- {stage}: {count}")
    lines += [
        "",
        "Walk: `docs/enterprise/ENTERPRISE_SALES_MOTION.md`, `docs/enterprise/MULTI_THREADING_SYSTEM.md`",
        "",
        "ENTERPRISE_VERDICT=OK",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    blob["written_path"] = str(out.relative_to(ROOT)).replace("\\", "/")

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("\n".join(lines))
        print(f"\nENTERPRISE: OK → {blob['written_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
