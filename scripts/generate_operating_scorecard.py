#!/usr/bin/env python3
"""Generate the Dealix Operating Scorecard markdown report.

Reads the private ops tree and writes a single markdown document at
${DEALIX_PRIVATE_OPS}/founder/operating_scorecard.md so the founder can
see revenue, trust, runtime, and leverage scores in one place.
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from api.internal import runtime_reader  # noqa: E402  (after sys.path edit)


def _score_block(funnel, finance, trust, workers) -> dict[str, int]:
    revenue_score = min(
        100, int(finance["cash_collected_sar"] / 1000) + funnel["positive_replies"] * 5
    )
    trust_score = max(0, 100 - trust["count"] * 10 - trust["a3_attempts"] * 20)
    failures = 0
    for row in workers["workers"]:
        try:
            failures += int(row.get("failures_24h") or 0)
        except ValueError:
            continue
    runtime_score = max(0, 100 - failures * 5)
    founder_leverage = min(
        100, funnel["approved_outreach"] * 2 + funnel["positive_replies"] * 5
    )
    product_score = 40 if funnel["proposals"] > 0 else 20
    return {
        "revenue": revenue_score,
        "trust": trust_score,
        "runtime": runtime_score,
        "leverage": founder_leverage,
        "product": product_score,
    }


def build(root: Path) -> tuple[str, Path]:
    os.environ.setdefault("DEALIX_PRIVATE_OPS", str(root))
    funnel = runtime_reader.sales_funnel()
    finance = runtime_reader.finance_summary()
    trust = runtime_reader.trust_flags()
    workers = runtime_reader.workers_health()
    approvals = runtime_reader.approvals_list()
    scores = _score_block(funnel, finance, trust, workers)

    bottleneck = "no_data"
    if funnel["pending_approval"] > 5:
        bottleneck = "founder_review_backlog"
    elif funnel["positive_replies"] == 0 and funnel["sent"] > 0:
        bottleneck = "messaging_or_targeting"
    elif funnel["payment_capture"] > 0:
        bottleneck = "payment_capture"

    next_action = "Review pending approvals." if funnel["pending_approval"] > 0 else (
        "Follow up on positive replies." if funnel["positive_replies"] > 0
        else "Add A leads to the lead intelligence base."
    )

    out_path = root / "founder" / "operating_scorecard.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()

    md = f"""# Dealix Operating Scorecard

Generated: {now}
Private ops root: {root}
Source: {funnel['source']}

## Scores (0-100)

- Revenue Score: **{scores['revenue']}**
- Trust Score: **{scores['trust']}**
- Runtime Score: **{scores['runtime']}**
- Founder Leverage Score: **{scores['leverage']}**
- Productization Score: **{scores['product']}**

## Funnel

- Lead intelligence: {funnel['lead_intelligence_count']}
- A leads: {funnel['a_leads']}
- Pending approval: {funnel['pending_approval']}
- Approved outreach: {funnel['approved_outreach']}
- Sent: {funnel['sent']}
- Replies (inbound): {funnel['replies']}
- Positive replies: {funnel['positive_replies']}
- Samples: {funnel['samples']}
- Proposals: {funnel['proposals']}
- Payment capture: {funnel['payment_capture']}

## Finance

- Cash collected (SAR): {finance['cash_collected_sar']}
- Pipeline (SAR): {finance['pipeline_sar']}
- Weighted pipeline (SAR): {finance['weighted_pipeline_sar']}
- Payment follow-ups: {finance['payment_follow_ups']}

## Trust

- Open trust flags: {trust['count']}
- Suppression entries: {trust['suppression_count']}
- A3 attempts: {trust['a3_attempts']}

## Workers

- Worker rows: {workers['count']}

## Top bottleneck

`{bottleneck}`

## Next best action

> {next_action}

## Approvals waiting

- Pending approvals: {approvals['count']}
"""
    out_path.write_text(md, encoding="utf-8")
    return md, out_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--private-ops",
        default=os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"),
    )
    args = parser.parse_args(argv)
    root = Path(args.private_ops).expanduser().resolve()
    if not root.exists():
        print(
            f"WARNING: private ops root {root} does not exist. "
            "Run scripts/bootstrap_private_ops_runtime.py first.",
            file=sys.stderr,
        )
        root.mkdir(parents=True, exist_ok=True)
    md, out_path = build(root)
    print(md)
    print(f"\nwritten: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
