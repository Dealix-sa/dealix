#!/usr/bin/env python3
"""
Build a batch outreach queue with cooldown and max follow-up gates.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.revenue._lib import (
    REPO_ROOT,
    load_csv,
    normalize_email,
    today_str,
    days_since,
    write_csv,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build batch outreach queue")
    parser.add_argument("--input", default="data/outreach/ready_batch_2026-06-15.csv")
    parser.add_argument("--outreach-log", default="ledgers/outreach_log.csv")
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--cooldown-days", type=int, default=7)
    parser.add_argument("--max-followups", type=int, default=3)
    args = parser.parse_args()

    rows = load_csv(REPO_ROOT / args.input)
    log_rows = load_csv(REPO_ROOT / args.outreach_log)

    contact_history: dict[str, list[dict[str, str]]] = {}
    for log in log_rows:
        email = normalize_email(log.get("email", ""))
        if email:
            contact_history.setdefault(email, []).append(log)

    queue: list[dict[str, str]] = []
    skipped: list[str] = []
    for row in rows:
        email = normalize_email(row.get("email", ""))
        history = contact_history.get(email, [])
        if len(history) >= args.max_followups + 1:
            skipped.append(f"{row.get('company')} (max follow-ups)")
            continue
        recent = [h for h in history if days_since(h.get("sent_at", "")) is not None and days_since(h.get("sent_at", "")) < args.cooldown_days]
        if recent:
            skipped.append(f"{row.get('company')} (cooldown)")
            continue
        queue.append({
            **row,
            "batch_id": f"batch_{today_str()}",
            "queued_at": today_str(),
            "status": "ready_to_review",
            "step": "1",
        })
        if len(queue) >= args.batch_size:
            break

    out_path = REPO_ROOT / "data" / "outreach" / f"batch_queue_{today_str()}.csv"
    if queue:
        write_csv(out_path, queue, list(queue[0].keys()))
    print(f"✅ Queued {len(queue)} companies for outreach → {out_path}")
    if skipped:
        print(f"⚠️ Skipped {len(skipped)} companies:")
        for s in skipped[:10]:
            print(f"  - {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
