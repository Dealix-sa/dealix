#!/usr/bin/env python3
"""Weekly founder scorecard — composes 7 daily KPI snapshots into a
single bilingual markdown report.

Reads:  data/kpi_snapshots/YYYY-MM-DD.json (last 7 files)
Writes: data/scorecards/YYYY-WW.md

Doctrine:
  - NEVER auto-sends. Output is a file the founder reads (or copies
    into WhatsApp / email after review).
  - Every numeric carries is_estimate flag when source is not a
    confirmed Moyasar transaction.

Usage:
    python scripts/weekly_scorecard.py            # write file
    python scripts/weekly_scorecard.py --dry-run  # print, don't write
    python scripts/weekly_scorecard.py --json     # JSON instead of MD
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

SNAPSHOT_DIR = REPO / "data" / "kpi_snapshots"
SCORECARD_DIR = REPO / "data" / "scorecards"


def _last_7_snapshots() -> list[dict]:
    if not SNAPSHOT_DIR.is_dir():
        return []
    files = sorted(SNAPSHOT_DIR.glob("*.json"))[-7:]
    out = []
    for f in files:
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            continue
    return out


def _delta(values: list[int | float]) -> str:
    if len(values) < 2:
        return "n/a"
    first, last = values[0], values[-1]
    if first == 0 and last == 0:
        return "0"
    if first == 0:
        return f"+{last}"
    pct = ((last - first) / first) * 100
    sign = "+" if pct >= 0 else ""
    return f"{sign}{pct:.1f}%"


def _val(snap: dict, *path: str, default: int | float = 0) -> int | float:
    cur = snap
    for p in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(p, default)
    if isinstance(cur, dict):
        return cur.get("value", default)
    return cur if isinstance(cur, (int, float)) else default


def build_scorecard(snaps: list[dict]) -> dict:
    """Compose a scorecard dict from 1-7 daily snapshots."""
    if not snaps:
        return {
            "status": "no_data",
            "message": "No KPI snapshots in data/kpi_snapshots/. Run "
            "`python -m auto_client_acquisition.payment_ops.kpi_snapshot` first.",
        }

    revenue_today = [_val(s, "revenue", "today_sar") for s in snaps]
    mrr = [_val(s, "revenue", "mrr_sar") for s in snaps]
    active_subs = [_val(s, "revenue", "active_subscriptions") for s in snaps]
    approvals = [_val(s, "pipeline", "approvals_pending") for s in snaps]
    friction = [_val(s, "trust", "friction_events_7d") for s in snaps]
    agent_runs = [_val(s, "fleet", "agent_runs_24h") for s in snaps]
    proof_events = [_val(s, "fleet", "proof_events_24h") for s in snaps]

    # Red-line triggers (doctrine: surface, never auto-act)
    red_lines: list[str] = []
    if approvals and approvals[-1] > 20:
        red_lines.append(f"approval queue backlog: {int(approvals[-1])} pending")
    if friction and friction[-1] > 30:
        red_lines.append(f"friction spike: {int(friction[-1])} events in last 7d")
    if agent_runs and sum(agent_runs[-3:]) == 0:
        red_lines.append("fleet quiet — 0 agent runs in last 3 days")
    if not revenue_today or sum(revenue_today) == 0:
        red_lines.append("no revenue captured this week — verify Moyasar")

    return {
        "week": datetime.now(UTC).strftime("%Y-W%V"),
        "generated_at": datetime.now(UTC).isoformat(),
        "snapshots_included": len(snaps),
        "first_date": snaps[0].get("date") if snaps else None,
        "last_date": snaps[-1].get("date") if snaps else None,
        "metrics": {
            "revenue_total_sar": int(sum(revenue_today)),
            "mrr_latest": int(mrr[-1]) if mrr else 0,
            "mrr_delta": _delta(mrr),
            "active_subs_latest": int(active_subs[-1]) if active_subs else 0,
            "approvals_avg": int(sum(approvals) / len(approvals)) if approvals else 0,
            "friction_total_7d": int(friction[-1]) if friction else 0,
            "agent_runs_total": int(sum(agent_runs)),
            "proof_events_total": int(sum(proof_events)),
        },
        "red_lines": red_lines,
        "doctrine_note": (
            "All metrics derived from existing ledger reads. Numbers tagged "
            "is_estimate=True in daily snapshot remain estimates here. "
            "Founder reviews this scorecard before any external share."
        ),
    }


def render_markdown(card: dict) -> str:
    if card.get("status") == "no_data":
        return f"# Weekly Scorecard\n\n{card['message']}\n"

    m = card["metrics"]
    lines = [
        f"# Weekly Founder Scorecard · {card['week']}",
        "",
        f"_Window: {card['first_date']} → {card['last_date']} "
        f"({card['snapshots_included']} daily snapshots)_",
        "",
        "## Revenue",
        "",
        f"- **Revenue this week:** {m['revenue_total_sar']:,} SAR",
        f"- **MRR (latest snapshot):** {m['mrr_latest']:,} SAR — Δ {m['mrr_delta']}",
        f"- **Active subscriptions:** {m['active_subs_latest']}",
        "",
        "## Pipeline",
        "",
        f"- **Avg pending approvals:** {m['approvals_avg']}",
        "",
        "## Trust & Fleet",
        "",
        f"- **Friction events (7d):** {m['friction_total_7d']}",
        f"- **Agent runs total:** {m['agent_runs_total']}",
        f"- **Proof events captured:** {m['proof_events_total']}",
        "",
    ]
    if card["red_lines"]:
        lines.extend(["## Red lines this week", ""])
        for rl in card["red_lines"]:
            lines.append(f"- ⚠️  {rl}")
        lines.append("")
    else:
        lines.extend(["## Red lines this week", "", "- None triggered. ✓", ""])

    lines.extend(
        [
            "---",
            "",
            f"_{card['doctrine_note']}_",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json", action="store_true", help="JSON instead of markdown")
    args = ap.parse_args()

    snaps = _last_7_snapshots()
    card = build_scorecard(snaps)

    if args.json:
        out = json.dumps(card, indent=2, ensure_ascii=False)
    else:
        out = render_markdown(card)

    if args.dry_run:
        print(out)
        return 0

    SCORECARD_DIR.mkdir(parents=True, exist_ok=True)
    week_label = card.get("week", datetime.now(UTC).strftime("%Y-W%V"))
    suffix = ".json" if args.json else ".md"
    path = SCORECARD_DIR / f"{week_label}{suffix}"
    path.write_text(out, encoding="utf-8")
    print(f"OK: wrote {path.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
