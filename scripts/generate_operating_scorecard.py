#!/usr/bin/env python3
"""Generate the founder operating scorecard markdown.

Reads CSVs from $DEALIX_PRIVATE_OPS and writes a single markdown
summary to <private_ops>/founder/operating_scorecard.md. The scorecard
is intentionally simple — it is a founder-facing snapshot, not an
analytics warehouse.
"""

from __future__ import annotations

import argparse
import csv
import os
from datetime import datetime, timezone
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8", newline="") as fh:
            return [dict(row) for row in csv.DictReader(fh)]
    except Exception:
        return []


def safe_float(value: str | None) -> float:
    if not value:
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def scorecard(root: Path) -> str:
    cash_rows = read_csv(root / "finance" / "cash_collected.csv")
    payments = read_csv(root / "finance" / "payment_capture_queue.csv")
    proposals = read_csv(root / "sales" / "proposal_queue.csv")
    outreach = read_csv(root / "outreach" / "outreach_queue.csv")
    workers = read_csv(root / "runtime" / "worker_state.csv")
    flags = read_csv(root / "trust" / "trust_flags.csv")
    products = read_csv(root / "product" / "productization_candidates.csv")

    cash_total = sum(safe_float(r.get("amount")) for r in cash_rows)
    pipeline = sum(safe_float(r.get("value")) for r in proposals)

    open_flags = [f for f in flags if (f.get("status") or "open") != "resolved"]
    failures = sum(int(r.get("failures_24h", "0") or "0") for r in workers)

    revenue_score = min(100, int(cash_total / 100)) if cash_total else 0
    trust_score = max(0, 100 - 5 * len(open_flags))
    runtime_score = max(0, 100 - 10 * failures)
    leverage_score = max(0, 100 - len([o for o in outreach if (o.get("status") or "") == "draft"]))
    product_score = min(100, len(products) * 10)

    top_bottleneck = "operations look healthy"
    if open_flags:
        top_bottleneck = f"{len(open_flags)} open trust flag(s)"
    elif failures:
        top_bottleneck = f"{failures} worker failure(s) in last 24h"
    elif not cash_rows:
        top_bottleneck = "no cash collected yet"
    elif pipeline == 0:
        top_bottleneck = "pipeline empty — feed the funnel"

    next_best_action = "review approvals queue"
    if open_flags:
        next_best_action = "resolve trust flags"
    elif failures:
        next_best_action = "retry failing workers / inspect logs"

    now = datetime.now(timezone.utc).isoformat()
    lines = [
        "# Dealix Operating Scorecard",
        "",
        f"_Generated: {now}_",
        "",
        "## Scores",
        f"- Revenue: **{revenue_score}**",
        f"- Trust: **{trust_score}**",
        f"- Runtime: **{runtime_score}**",
        f"- Founder Leverage: **{leverage_score}**",
        f"- Productization: **{product_score}**",
        "",
        "## State",
        f"- Cash collected: {cash_total}",
        f"- Pipeline value: {pipeline}",
        f"- Open trust flags: {len(open_flags)}",
        f"- Worker failures (24h): {failures}",
        f"- Pending payment follow-ups: {len([p for p in payments if (p.get('status') or '') == 'due'])}",
        "",
        "## Top bottleneck",
        f"- {top_bottleneck}",
        "",
        "## Next best action",
        f"- {next_best_action}",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--private-ops",
        default=os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"),
    )
    args = parser.parse_args()
    root = Path(args.private_ops)
    target = root / "founder" / "operating_scorecard.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(scorecard(root), encoding="utf-8")
    print(f"[generate_operating_scorecard] wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
