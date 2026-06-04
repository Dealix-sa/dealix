"""Generate the daily Distribution Command Center markdown report.

Reads ledgers from the private ops directory (outside the public repo) and
writes a single founder-facing markdown that names the top action for the day.
"""

import argparse
import csv
from pathlib import Path
from datetime import date


def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def count(rows, field, values):
    values = {v.lower() for v in values}
    return sum(1 for r in rows if (r.get(field) or "").lower() in values)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()

    root = Path(args.private_ops).resolve()
    intelligence = read_csv(root / "intelligence/lead_intelligence_base.csv")
    pipeline = read_csv(root / "pipeline/pipeline_tracker.csv")
    send_queue = read_csv(root / "outreach/outreach_send_queue.csv")
    followups = read_csv(root / "outreach/followup_queue.csv")
    replies = read_csv(root / "outreach/reply_log.csv")
    samples = read_csv(root / "delivery/sample_quality_log.csv")
    proposals = read_csv(root / "sales/proposal_tracker.csv")
    cash = read_csv(root / "revenue/cash_collected.csv")
    channels = read_csv(root / "distribution/channel_scorecard.csv")

    ready = count(send_queue, "status", {"Ready"})
    sent = count(send_queue, "status", {"Sent"})
    positive = count(replies, "reply_type", {"positive", "interested", "yes"})
    planned_followups = count(followups, "status", {"Planned"})
    collected = sum(
        float(r.get("amount_sar") or 0)
        for r in cash
        if (r.get("status") or "").lower() in {"paid", "collected", "done"}
    )

    if len(intelligence) < 500:
        top_action = "Build lead intelligence base toward 500 leads across 5 sectors."
    elif ready > 0:
        top_action = "Review and approve ready outreach queue."
    elif planned_followups > 0:
        top_action = "Execute planned follow-ups."
    elif positive > len(samples):
        top_action = "Prepare samples for positive replies."
    elif len(samples) >= 3 and len(proposals) < 1:
        top_action = "Convert best sample into proposal."
    elif len(proposals) >= 1 and collected <= 0:
        top_action = "Pursue payment / PO / written approval."
    else:
        top_action = "Run weekly distribution review and double down on best channel."

    channel_rows = "\n".join(
        f"| {r.get('channel','')} | {r.get('leads','')} | {r.get('sent','')} | "
        f"{r.get('positive_replies','')} | {r.get('samples','')} | {r.get('proposals','')} | "
        f"{r.get('cash','')} | {r.get('decision','')} |"
        for r in channels
    ) or "| No channel data yet | | | | | | | |"

    content = f"""# Distribution Command Center

## Date
{date.today().isoformat()}

## Top Action
{top_action}

## Funnel Snapshot
- Lead intelligence base: {len(intelligence)}
- Active pipeline: {len(pipeline)}
- Ready outreach: {ready}
- Sent outreach: {sent}
- Planned follow-ups: {planned_followups}
- Replies: {len(replies)}
- Positive replies: {positive}
- Samples: {len(samples)}
- Proposals: {len(proposals)}
- Cash collected: {collected} SAR

## Channel Scorecard
| Channel | Leads | Sent | Positive Replies | Samples | Proposals | Cash | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
{channel_rows}

## CEO Rule
Do not add a new channel until the current top action is complete.
"""

    out_dir = root / "founder"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "distribution_command_center.md"
    out.write_text(content, encoding="utf-8")
    print(f"PASS: distribution command center generated: {out}")


if __name__ == "__main__":
    main()
