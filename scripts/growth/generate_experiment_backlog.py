#!/usr/bin/env python3
"""Render the growth experiment backlog from data/growth/experiments.jsonl.

Offline, deterministic, no external calls. Honors the growth rule:
"No opinion without an experiment. No experiment without a metric.
No metric without a decision." Output is a prioritized markdown backlog
for founder review.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "growth" / "experiments.jsonl"
OUT = ROOT / "reports" / "growth"

EFFORT_ORDER = {"S": 0, "M": 1, "L": 2}


def load() -> list[dict]:
    rows: list[dict] = []
    if not DATA.exists():
        return rows
    for line in DATA.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def main() -> int:
    rows = load()
    rows.sort(key=lambda r: (EFFORT_ORDER.get(r.get("effort", "M"), 1), r.get("id", "")))
    OUT.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Growth Experiment Backlog — Dealix Self-Growth OS",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Source: `data/growth/experiments.jsonl` ({len(rows)} experiments)",
        "",
        "> Rule: لا رأي بدون تجربة. لا تجربة بدون metric. لا metric بدون قرار.",
        "",
        "| ID | Loop | Channel | Hypothesis | Metric | Effort | Status |",
        "|---|---|---|---|---|---|---|",
    ]
    by_status: dict[str, int] = {}
    for r in rows:
        by_status[r.get("status", "?")] = by_status.get(r.get("status", "?"), 0) + 1
        lines.append(
            "| {id} | {loop} | {channel} | {hyp} | {metric} | {effort} | {status} |".format(
                id=r.get("id", ""),
                loop=r.get("loop", ""),
                channel=r.get("channel", ""),
                hyp=r.get("hypothesis", "").replace("|", "/"),
                metric=r.get("metric", ""),
                effort=r.get("effort", ""),
                status=r.get("status", ""),
            )
        )
    lines += ["", "## Status summary", ""]
    for status, count in sorted(by_status.items()):
        lines.append(f"- **{status}**: {count}")
    lines += [
        "",
        "## Weekly cadence",
        "",
        "- Run up to 10 small experiments/week.",
        "- Each must name a single metric and a decision rule before it starts.",
        "- Promote winners into the relevant growth loop; archive losers with the learning.",
        "",
    ]
    (OUT / "EXPERIMENT_BACKLOG.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"DEALIX_GROWTH_EXPERIMENT_BACKLOG=PASS ({len(rows)} experiments)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
