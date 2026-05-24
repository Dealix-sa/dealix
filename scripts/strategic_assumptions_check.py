#!/usr/bin/env python3
"""Strategic assumptions staleness check.

Reads PRIVATE_OPS ceo/strategic_assumptions.csv, flags rows where
last_reviewed is older than N days (default 30) or status is `falsified`.
PRIVATE_OPS off → graceful no-op.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.private_ops import is_enabled, missing_private_ops_note, resolve_csv  # noqa: E402

BRIEFS = ROOT / "data/founder_briefs"


def _stale(rows: list[dict[str, str]], max_age_days: int) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    today = date.today()
    for r in rows:
        try:
            d = date.fromisoformat(r.get("last_reviewed", ""))
            age = (today - d).days
            if age > max_age_days:
                out.append({**r, "_age_days": str(age)})
        except (ValueError, TypeError):
            out.append({**r, "_age_days": "unknown"})
    return out


def _falsified(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [r for r in rows if (r.get("status") or "").lower() == "falsified"]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    p.add_argument("--max-age-days", type=int, default=30)
    args = p.parse_args()

    if not is_enabled():
        print(missing_private_ops_note("en"))
        print("ASSUMPTIONS_VERDICT=SKIPPED_PRIVATE_OPS_OFF")
        return 0

    path = resolve_csv("ceo/strategic_assumptions.csv")
    rows: list[dict[str, str]] = []
    if path and path.exists():
        with path.open("r", encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))

    stale = _stale(rows, args.max_age_days)
    falsified = _falsified(rows)
    blob = {
        "generated_at": datetime.now(UTC).isoformat(),
        "private_ops_enabled": True,
        "total_assumptions": len(rows),
        "stale_count": len(stale),
        "falsified_count": len(falsified),
        "stale_ids": [r.get("id") for r in stale],
        "falsified_ids": [r.get("id") for r in falsified],
        "max_age_days": args.max_age_days,
    }

    BRIEFS.mkdir(parents=True, exist_ok=True)
    out = BRIEFS / f"strategic_assumptions_check_{date.today().isoformat()}.md"
    lines = [
        f"# Strategic Assumptions Check — {date.today().isoformat()}",
        "",
        f"Total assumptions: {blob['total_assumptions']}",
        f"Stale (> {args.max_age_days} days): {blob['stale_count']}",
        f"Falsified: {blob['falsified_count']}",
        "",
        "## Stale",
    ]
    for r in stale:
        lines.append(f"- `{r.get('id')}` — {r.get('assumption')}  (age: {r.get('_age_days')} days)")
    lines += ["", "## Falsified"]
    for r in falsified:
        lines.append(f"- `{r.get('id')}` — {r.get('assumption')}")
    lines += [
        "",
        "Walk: `docs/founder/STRATEGIC_ASSUMPTIONS_REGISTER.md`",
        "",
        "ASSUMPTIONS_VERDICT=OK",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    blob["written_path"] = str(out.relative_to(ROOT)).replace("\\", "/")

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("\n".join(lines))
        print(f"\nASSUMPTIONS: OK → {blob['written_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
