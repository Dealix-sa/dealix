#!/usr/bin/env python3
"""Generate the mission control markdown for the founder."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from pathlib import Path


def _read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="../dealix-ops-private")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"ERROR: private root missing: {root}")
        return 1

    pipeline = _read(root / "pipeline" / "pipeline_tracker.csv")
    actions = _read(root / "revenue" / "revenue_action_log.csv")
    cash = _read(root / "revenue" / "cash_collected.csv")
    proposals = _read(root / "sales" / "proposal_tracker.csv")

    a_priority = [p for p in pipeline if (p.get("priority") or "").strip() == "A"]
    today = dt.date.today().isoformat()

    out_path = root / "founder" / "mission_control.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        f"# Mission Control\nGenerated on: {today}\n\n"
        f"## Pipeline\n- Total opportunities: {len(pipeline)}\n- A-priority: {len(a_priority)}\n\n"
        f"## Actions\n- Logged actions (lifetime): {len(actions)}\n\n"
        f"## Proposals\n- Open: {sum(1 for p in proposals if (p.get('status') or '').strip() in ('Sent','Negotiating','Verbal yes'))}\n\n"
        f"## Cash\n- Confirmed payments: {sum(1 for c in cash if (c.get('status') or '').strip().lower() == 'confirmed')}\n",
        encoding="utf-8",
    )
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
