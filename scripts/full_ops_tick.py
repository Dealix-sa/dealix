#!/usr/bin/env python3
"""Cron-friendly entrypoint: run one Full-Ops tick and print a one-line summary.

Recommended cron line (every 15 minutes):
    */15 * * * *  cd /opt/dealix && python -m scripts.full_ops_tick >> /var/log/dealix/tick.log 2>&1

Exit 0 on success, non-zero on failure. No FastAPI, no DB bootstrap beyond
what the operating loop already initialises. The loop performs zero live sends
and zero live charges — all external actions are queued as approval drafts.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.full_ops.operating_loop import run_tick  # noqa: E402


def main() -> int:
    """Run one tick and print a compact summary line.

    Returns 0 on success, 1 on any exception.
    """
    try:
        summary = run_tick()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR full_ops_tick failed: {exc}", file=sys.stderr)
        return 1

    tick_id = summary.get("tick_id", "unknown")
    sensed = summary.get("work_items_sensed", 0)
    approvals_created = summary.get("approvals_created", 0)
    approvals_blocked = len(summary.get("approvals_blocked", []))
    ledger_path = summary.get("ledger_path", "not_recorded")

    print(
        f"tick_id={tick_id}"
        f" sensed={sensed}"
        f" approvals_required={approvals_created - approvals_blocked}"
        f" approvals_blocked={approvals_blocked}"
        f" ledger={ledger_path}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
