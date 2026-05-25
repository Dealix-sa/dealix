"""Generate the CEO action queue from private revenue ops files.

The queue is the founder's single ranked list of "do this next" actions.
Ranking follows the Revenue Ops Playbook rule:

    cash > proof > retention > trust > learning

This is intentionally a read-only script: it reads the pipeline, proposal,
sample and revenue-action CSVs (if present) and prints a ranked list.
Missing files are tolerated — the queue degrades gracefully so the founder
gets a sensible suggestion even on day zero.
"""
from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return [row for row in reader if any((v or "").strip() for v in row.values())]


def _count(rows: list[dict[str, str]], field: str, predicate) -> int:
    return sum(1 for row in rows if predicate((row.get(field) or "").strip()))


def build_queue(private_ops: Path) -> list[str]:
    pipeline = _read_csv(private_ops / "pipeline" / "pipeline_tracker.csv")
    proposals = _read_csv(private_ops / "sales" / "proposal_tracker.csv")
    samples = _read_csv(private_ops / "delivery" / "sample_quality_log.csv")
    actions = _read_csv(private_ops / "revenue" / "revenue_action_log.csv")

    lead_count = len(pipeline)
    contacted = _count(pipeline, "stage", lambda s: s.lower() in {"contacted", "replied", "sample", "proposal", "paid"})
    replied = _count(pipeline, "stage", lambda s: s.lower() in {"replied", "sample", "proposal", "paid"})
    sample_sent = len(samples) or _count(pipeline, "stage", lambda s: s.lower() in {"sample", "proposal", "paid"})
    proposal_sent = len(proposals) or _count(pipeline, "stage", lambda s: s.lower() in {"proposal", "paid"})
    proposal_open = _count(proposals, "status", lambda s: s.lower() in {"sent", "follow-up", "follow_up", "pending", "open"})
    paid = _count(proposals, "status", lambda s: s.lower() in {"paid", "po", "approved", "won"})

    queue: list[str] = []

    if proposal_open > 0:
        queue.append(
            f"[CASH] Follow up on {proposal_open} open proposal(s) — chase payment / PO / written approval."
        )
    if proposal_sent == 0 and sample_sent > 0:
        queue.append("[CASH] Convert sent samples into a proposal today.")
    if sample_sent == 0 and replied > 0:
        queue.append("[PROOF] Prepare a 5-opportunity sample pack for the warmest reply.")
    if replied == 0 and contacted >= 25:
        queue.append("[LEARNING] Replies are zero on 25+ DMs — review message_performance.csv and rewrite the angle.")
    if contacted < 25:
        queue.append(f"[PIPELINE] Send founder-led DMs — only {contacted}/25 leads contacted this week.")
    if lead_count < 25:
        queue.append(f"[PIPELINE] Add qualified leads — only {lead_count}/25 in the tracker.")
    if paid > 0:
        queue.append(f"[RETENTION] Run delivery kickoff for {paid} paid/approved deal(s) and capture proof.")
    if not actions:
        queue.append("[TRUST] Log today's revenue action in revenue/revenue_action_log.csv before close-day.")

    if not queue:
        queue.append("[LEARNING] All funnel stages have signal — run weekly win/loss review and improve one lever.")
    return queue


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the CEO action queue.")
    parser.add_argument("--private-ops", required=True, help="Path to dealix-ops-private dir")
    args = parser.parse_args()

    private_ops = Path(args.private_ops).expanduser().resolve()
    if not private_ops.exists():
        print(f"ERROR: private ops directory not found: {private_ops}")
        return 1

    queue = build_queue(private_ops)
    print(f"\nCEO Action Queue — {date.today().isoformat()}")
    print("=" * 40)
    for i, item in enumerate(queue, start=1):
        print(f"{i}. {item}")
    print("\nDo the top action first. Cash > proof > retention > trust > learning.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
