#!/usr/bin/env python3
"""CEO Summary worker — refreshes the founder operating scorecard.

Reads the private ops runtime (cash collected, approvals open, trust
flags, incidents) and writes founder/operating_scorecard.md. Recorded
as a worker_state update so /workers reflects health.
"""
from __future__ import annotations

import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def _runtime_dir() -> Path:
    raw = os.getenv("PRIVATE_OPS") or os.getenv("DEALIX_PRIVATE_OPS_DIR") or "/opt/dealix-ops-private"
    return Path(raw).expanduser()


def _sum_csv(path: Path, column: str) -> float:
    if not path.exists():
        return 0.0
    total = 0.0
    with path.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            try:
                total += float(row.get(column, "0") or 0)
            except ValueError:
                continue
    return total


def main() -> int:
    base = _runtime_dir()
    if not base.exists():
        print(f"SKIP: private ops not bootstrapped at {base}")
        return 0
    cash_30d = _sum_csv(base / "finance" / "cash_collected.csv", "amount_sar")
    appr = base / "approvals" / "approval_queue.csv"
    open_appr = 0
    if appr.exists():
        with appr.open("r", encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if (r.get("status") or "open") == "open":
                    open_appr += 1
    flags = base / "trust" / "trust_flags.csv"
    n_flags = 0
    if flags.exists():
        with flags.open("r", encoding="utf-8", newline="") as fh:
            n_flags = sum(1 for _ in csv.DictReader(fh))
    out = base / "founder" / "operating_scorecard.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"""# Dealix Operating Scorecard

_Last refresh: {datetime.now(timezone.utc).isoformat()}_

| Pillar    | Signal                                  | Value             |
|-----------|------------------------------------------|-------------------|
| Revenue   | Cash collected (30d, SAR)                | {cash_30d:,.0f}   |
| Trust     | Open trust flags                         | {n_flags}         |
| Delivery  | Approvals open                           | {open_appr}       |
| Growth    | Active sector targets                    | see growth/sector_targets.csv |

Source: scripts/run_ceo_summary_worker.py (CEO Copilot).
""",
        encoding="utf-8",
    )

    # Update worker_state
    state = base / "runtime" / "worker_state.csv"
    state.parent.mkdir(parents=True, exist_ok=True)
    header = ["id", "name", "status", "last_run", "failure_count", "owner"]
    rows: list[dict[str, str]] = []
    if state.exists():
        with state.open("r", encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
    updated = False
    for r in rows:
        if r.get("id") == "ceo_summary":
            r["status"] = "ok"
            r["last_run"] = datetime.now(timezone.utc).isoformat()
            r["failure_count"] = "0"
            updated = True
            break
    if not updated:
        rows.append(
            {
                "id": "ceo_summary",
                "name": "CEO Summary",
                "status": "ok",
                "last_run": datetime.now(timezone.utc).isoformat(),
                "failure_count": "0",
                "owner": "founder",
            }
        )
    with state.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in header})
    print(f"[ok] scorecard written to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
