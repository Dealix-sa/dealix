#!/usr/bin/env python3
"""Founder leverage dashboard — Make / Manage / Move ratio from time audit.

Reads PRIVATE_OPS ceo/leverage_time_audit.csv. When PRIVATE_OPS is not
configured the script exits 0 with the standard bilingual note.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.private_ops import is_enabled, missing_private_ops_note, resolve_csv  # noqa: E402

BRIEFS = ROOT / "data/founder_briefs"


def _read_audit() -> list[dict[str, str]]:
    path = resolve_csv("ceo/leverage_time_audit.csv")
    if path is None or not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _ratio(rows: list[dict[str, str]], window: int = 4) -> dict[str, Any]:
    recent = rows[-window:] if rows else []
    totals = {"make": 0, "manage": 0, "move": 0}
    for r in recent:
        for bucket in totals:
            try:
                totals[bucket] += int(float(r.get(f"{bucket}_hours") or 0))
            except (TypeError, ValueError):
                continue
    total = sum(totals.values()) or 1
    return {
        "window_weeks": window,
        "totals": totals,
        "ratio": {k: round(v / total, 3) for k, v in totals.items()},
        "rows_used": len(recent),
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    p.add_argument("--window", type=int, default=4)
    args = p.parse_args()

    if not is_enabled():
        print(missing_private_ops_note("en"))
        print("LEVERAGE_VERDICT=SKIPPED_PRIVATE_OPS_OFF")
        return 0

    rows = _read_audit()
    blob = {
        "generated_at": datetime.now(UTC).isoformat(),
        "private_ops_enabled": True,
        "row_count": len(rows),
        "summary": _ratio(rows, window=args.window),
    }
    BRIEFS.mkdir(parents=True, exist_ok=True)
    week_end = datetime.now(UTC).strftime("%Y-%m-%d")
    out = BRIEFS / f"founder_leverage_{week_end}.md"

    lines = [
        f"# Founder Leverage Dashboard — {week_end}",
        "",
        f"Window: last {args.window} weeks",
        f"Rows used: {blob['summary']['rows_used']}",
        "",
        "## Hours",
    ]
    for bucket, hours in blob["summary"]["totals"].items():
        lines.append(f"- {bucket.title()}: {hours} hours")
    lines += ["", "## Ratios"]
    for bucket, pct in blob["summary"]["ratio"].items():
        lines.append(f"- {bucket.title()}: {pct}")
    lines += [
        "",
        "Target: move ratio ≥ 0.40 by week 12, ≥ 0.55 by week 24.",
        "",
        "Walk: `docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md`",
        "",
        "LEVERAGE_VERDICT=OK",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    blob["written_path"] = str(out.relative_to(ROOT)).replace("\\", "/")

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("\n".join(lines))
        print(f"\nLEVERAGE: OK → {blob['written_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
