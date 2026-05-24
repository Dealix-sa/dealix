#!/usr/bin/env python3
"""Quarterly capital allocation snapshot.

Reads PRIVATE_OPS ceo/capital_allocations.csv and writes the markdown
snapshot. PRIVATE_OPS off → graceful no-op.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.private_ops import is_enabled, missing_private_ops_note, resolve_csv  # noqa: E402

BRIEFS = ROOT / "data/founder_briefs"


def _current_quarter(now: datetime | None = None) -> str:
    now = now or datetime.now(UTC)
    q = (now.month - 1) // 3 + 1
    return f"{now.year}Q{q}"


def _read_allocations() -> list[dict[str, str]]:
    path = resolve_csv("ceo/capital_allocations.csv")
    if path is None or not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _aggregate(rows: list[dict[str, str]], quarter: str) -> dict[str, Any]:
    subset = [r for r in rows if r.get("quarter") == quarter]
    buckets: dict[str, dict[str, Any]] = defaultdict(lambda: {"allocated_sar": 0, "actual_sar": 0, "roi_estimate": 0.0, "count": 0})
    for r in subset:
        bucket = r.get("bucket", "(unspecified)")
        try:
            buckets[bucket]["allocated_sar"] += int(float(r.get("allocated_sar") or 0))
            buckets[bucket]["actual_sar"] += int(float(r.get("actual_sar") or 0))
            buckets[bucket]["roi_estimate"] += float(r.get("roi_estimate") or 0)
            buckets[bucket]["count"] += 1
        except (TypeError, ValueError):
            continue
    for bucket, vals in buckets.items():
        if vals["count"]:
            vals["roi_estimate"] = round(vals["roi_estimate"] / vals["count"], 2)
    total_allocated = sum(b["allocated_sar"] for b in buckets.values())
    total_actual = sum(b["actual_sar"] for b in buckets.values())
    return {
        "quarter": quarter,
        "buckets": {k: dict(v) for k, v in buckets.items()},
        "total_allocated_sar": total_allocated,
        "total_actual_sar": total_actual,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    p.add_argument("--quarter", default=None, help="e.g. 2026Q2; defaults to current")
    args = p.parse_args()

    if not is_enabled():
        print(missing_private_ops_note("en"))
        print("CAPITAL_VERDICT=SKIPPED_PRIVATE_OPS_OFF")
        return 0

    quarter = args.quarter or _current_quarter()
    rows = _read_allocations()
    blob = _aggregate(rows, quarter)
    blob["generated_at"] = datetime.now(UTC).isoformat()
    blob["private_ops_enabled"] = True

    BRIEFS.mkdir(parents=True, exist_ok=True)
    out = BRIEFS / f"capital_allocation_{quarter}.md"

    lines = [
        f"# Capital Allocation Snapshot — {quarter}",
        "",
        f"Total allocated: {blob['total_allocated_sar']} SAR",
        f"Total actual: {blob['total_actual_sar']} SAR",
        "",
        "## Buckets",
    ]
    if not blob["buckets"]:
        lines.append("- (no rows recorded yet)")
    for bucket, vals in blob["buckets"].items():
        lines.append(
            f"- **{bucket}** — allocated: {vals['allocated_sar']} SAR · "
            f"actual: {vals['actual_sar']} SAR · ROI score: {vals['roi_estimate']} · entries: {vals['count']}"
        )
    lines += [
        "",
        "Walk: `docs/finance/CAPITAL_ALLOCATION_SYSTEM.md`",
        "",
        "CAPITAL_VERDICT=OK",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    blob["written_path"] = str(out.relative_to(ROOT)).replace("\\", "/")

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("\n".join(lines))
        print(f"\nCAPITAL: OK → {blob['written_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
