"""Score strategic assumptions against evidence in private_ops.

Reads founder/strategic_assumptions.csv. Expected columns:
    id, assumption, status, evidence_for, evidence_against, owner, review_date

status one of: validated | contradicted | unknown | watching
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _private_ops_runtime import (  # noqa: E402
    ledger_path,
    parse_args,
    read_csv,
    today_iso,
    write_or_print,
)


def main() -> int:
    args = parse_args("generate_strategy_scorecard")
    p = ledger_path(args.private_ops, "founder", "strategic_assumptions.csv")
    _, rows = read_csv(p)
    if args.strict and not rows:
        print(f"[strict] no rows in {p}", file=sys.stderr)
        return 1

    by_status = Counter((r.get("status") or "unknown").lower() for r in rows)
    lines = [f"# Strategy Scorecard — {today_iso()}\n",
             "Source: private_ops/founder/strategic_assumptions.csv (read-only).\n",
             "## Summary\n"]
    for k in ("validated", "watching", "unknown", "contradicted"):
        lines.append(f"- **{k}**: {by_status.get(k, 0)}")
    lines.append("")

    contradicted = [r for r in rows if (r.get("status") or "").lower() == "contradicted"]
    if contradicted:
        lines.append("## Contradicted assumptions (act first)\n")
        for r in contradicted[:20]:
            lines.append(
                f"- **{r.get('assumption', '?')}** — owner: {r.get('owner', '?')} "
                f"— evidence against: {r.get('evidence_against', '')}"
            )
        lines.append("")

    watching = [r for r in rows if (r.get("status") or "").lower() == "watching"]
    if watching:
        lines.append("## Watching\n")
        for r in watching[:20]:
            lines.append(
                f"- {r.get('assumption', '?')} — owner: {r.get('owner', '?')} "
                f"— review: {r.get('review_date', '?')}"
            )

    write_or_print("\n".join(lines), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
