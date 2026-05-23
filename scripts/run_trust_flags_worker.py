#!/usr/bin/env python3
"""Refresh a derived view of open trust flags (safe, read-only).

Reads trust/trust_flags.csv and writes a summary line under runtime/.
"""

from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ROOT = os.environ.get("PRIVATE_OPS") or os.environ.get("PRIVATE_OPS_ROOT") or "/opt/dealix-ops-private"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=DEFAULT_ROOT)
    args = p.parse_args()
    root = Path(args.root).expanduser().resolve()

    src = root / "trust" / "trust_flags.csv"
    out = root / "runtime" / "trust_flags_summary.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    open_total = 0
    high = 0
    if src.exists():
        with src.open("r", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if (r.get("status") or "").lower() == "open":
                    open_total += 1
                    if (r.get("severity") or "").lower() in ("high", "critical"):
                        high += 1

    write_header = not out.exists()
    with out.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["as_of", "open_total", "open_high"])
        if write_header:
            writer.writeheader()
        writer.writerow(
            {
                "as_of": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "open_total": open_total,
                "open_high": high,
            }
        )

    print(f"[trust_flags_worker] open={open_total} high={high}")
    subprocess.run(
        [sys.executable, "scripts/update_worker_state.py", "--worker", "trust_flags_worker", "--status", "ok"],
        check=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
