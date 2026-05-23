#!/usr/bin/env python3
"""Generate the beachhead sector scorecard markdown report.

Inputs (in priority order):
  $PRIVATE_OPS/market_attack/beachhead_sector_scorecard.csv  (live)
  scripts/market_attack_bootstrap/market_attack/beachhead_sector_scorecard.csv (fallback)

Optional additional inputs (if present, used to enrich):
  $PRIVATE_OPS/growth/sector_targets.csv
  $PRIVATE_OPS/growth/account_scores.csv
  $PRIVATE_OPS/sales/proposal_queue.csv
  $PRIVATE_OPS/outreach/conversation_log.csv

Output:
  $PRIVATE_OPS/market_attack/beachhead_sector_scorecard.md

The script never crashes on missing inputs; it falls back to seeded
templates and clearly labels the source.
"""

from __future__ import annotations

import sys
from pathlib import Path

from market_attack_common import (  # type: ignore[import-not-found]
    BOOTSTRAP_ROOT,
    ReportContext,
    load_with_fallback,
    now_iso,
    private_ops_root,
    safe_int,
    write_markdown,
)


def _priority_for(score: int) -> str:
    if score >= 36:
        return "P0"
    if score >= 30:
        return "P1"
    if score >= 24:
        return "P2"
    if score >= 18:
        return "hold"
    return "kill"


def main() -> int:
    priv = private_ops_root()
    primary = priv / "market_attack" / "beachhead_sector_scorecard.csv"
    bootstrap = BOOTSTRAP_ROOT / "market_attack" / "beachhead_sector_scorecard.csv"

    _, rows, source = load_with_fallback(primary, bootstrap)
    ctx = ReportContext(
        name="Beachhead Sector Scorecard",
        runtime_paths_checked=[primary],
        fallback_paths_used=[] if source == "runtime" else [bootstrap],
        started_at=now_iso(),
    )

    # Compute total + priority defensively (in case the CSV is stale).
    scored = []
    for row in rows:
        dims = [
            safe_int(row.get("saudi_relevance")),
            safe_int(row.get("buyer_clarity")),
            safe_int(row.get("pain_urgency")),
            safe_int(row.get("high_ticket_potential")),
            safe_int(row.get("proof_fit")),
            safe_int(row.get("delivery_fit")),
            safe_int(row.get("competition_gap")),
            safe_int(row.get("channel_access")),
            safe_int(row.get("trust_risk")),
        ]
        total = sum(dims)
        row["_total"] = total
        row["_priority"] = _priority_for(total)
        scored.append(row)

    scored.sort(key=lambda r: r["_total"], reverse=True)

    lines = ctx.header()
    lines += [
        "## Top sectors",
        "",
        "| Sector | Total | Computed Priority | Stored Priority | Next Action |",
        "| ------ | ----- | ----------------- | --------------- | ----------- |",
    ]
    for r in scored:
        lines.append(
            f"| {r.get('sector','')} | {r['_total']} | {r['_priority']} "
            f"| {r.get('priority','')} | {r.get('next_action','')} |"
        )

    p0 = [r for r in scored if r["_priority"] == "P0"]
    p1 = [r for r in scored if r["_priority"] == "P1"]
    holds = [r for r in scored if r["_priority"] in ("hold", "kill")]

    lines += [
        "",
        "## P0 candidates",
        "",
    ]
    if not p0:
        lines.append("_No P0 sector. Score threshold is ≥ 36._")
    else:
        for r in p0:
            lines.append(
                f"- **{r.get('sector','')}** — score {r['_total']}. "
                f"Next: {r.get('next_action','')}"
            )

    lines += [
        "",
        "## P1 candidates",
        "",
    ]
    if not p1:
        lines.append("_No P1 sector. Score threshold is 30-35._")
    else:
        for r in p1:
            lines.append(
                f"- **{r.get('sector','')}** — score {r['_total']}. "
                f"Next: {r.get('next_action','')}"
            )

    lines += [
        "",
        "## Hold / kill",
        "",
    ]
    if not holds:
        lines.append("_No sectors currently on hold or kill list._")
    else:
        for r in holds:
            lines.append(
                f"- {r.get('sector','')} — {r['_priority']} (score {r['_total']})"
            )

    lines += [
        "",
        "## Notes",
        "",
        "- This is a signal-driven scorecard. It does not promise revenue.",
        "- Re-score every quarter or after any major sector trigger event.",
        "- A beachhead is locked only when total_score ≥ 36 AND the founder writes a 90-day thesis.",
    ]

    out = priv / "market_attack" / "beachhead_sector_scorecard.md"
    write_markdown(out, lines)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    # Allow running both as a module and as a script.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
