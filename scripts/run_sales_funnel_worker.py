#!/usr/bin/env python3
"""Snapshot the sales funnel into channel/sector scorecards.

Reads outreach + conversation_log + proposals and rolls them up into
distribution scorecards under the private ops tree.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from api.internal import runtime_reader  # noqa: E402


def _aggregate_channels(outreach, conversations, proposals, payments):
    bucket = defaultdict(lambda: {
        "sent": 0,
        "replies": 0,
        "positive_replies": 0,
        "samples": 0,
        "proposals": 0,
        "payments": 0,
    })
    for row in outreach:
        ch = row.get("channel") or "unknown"
        if (row.get("state") or "") == "sent":
            bucket[ch]["sent"] += 1
    for row in conversations:
        ch = row.get("channel") or "unknown"
        if (row.get("direction") or "") == "inbound":
            bucket[ch]["replies"] += 1
        if (row.get("sentiment") or "") == "positive":
            bucket[ch]["positive_replies"] += 1
    for row in proposals:
        stage = row.get("stage") or ""
        ch = "proposals"
        if stage == "sample":
            bucket[ch]["samples"] += 1
        elif stage == "proposal":
            bucket[ch]["proposals"] += 1
    for _row in payments:
        bucket["payments"]["payments"] += 1
    return bucket


def _write_channel(root: Path, bucket):
    path = root / "distribution" / "channel_scorecard.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = ["channel", "sent", "replies", "positive_replies", "samples", "proposals", "payments"]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        writer.writeheader()
        for channel, vals in bucket.items():
            writer.writerow({"channel": channel, **{k: vals.get(k, 0) for k in headers if k != "channel"}})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--private-ops",
        default=os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"),
    )
    args = parser.parse_args(argv)
    root = Path(args.private_ops).expanduser().resolve()
    os.environ["DEALIX_PRIVATE_OPS"] = str(root)

    outreach = runtime_reader.read_runtime("outreach_queue")["rows"]
    conversations = runtime_reader.read_runtime("conversation_log")["rows"]
    proposals = runtime_reader.read_runtime("proposal_queue")["rows"]
    payments = runtime_reader.read_runtime("payment_capture_queue")["rows"]

    bucket = _aggregate_channels(outreach, conversations, proposals, payments)
    _write_channel(root, bucket)

    import subprocess
    subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "update_worker_state.py"),
            "--worker", "sales_funnel",
            "--status", "ok",
            "--private-ops", str(root),
        ],
        check=False,
    )
    print(f"channel scorecard refreshed at {root / 'distribution' / 'channel_scorecard.csv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
