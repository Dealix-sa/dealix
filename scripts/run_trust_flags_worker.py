#!/usr/bin/env python3
"""Refresh the trust flags snapshot."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.update_worker_state import FIELDS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-ops", default=os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"))
    args = parser.parse_args()
    root = Path(args.private_ops)
    cache_path = root / "founder" / "trust_flags.json"

    try:
        from api.internal.runtime_reader import trust_flags  # type: ignore
        os.environ["DEALIX_PRIVATE_OPS"] = str(root)
        payload = trust_flags()
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        status, notes = "ok", f"wrote {cache_path}"
    except Exception as exc:  # noqa: BLE001
        status, notes = "error", f"error: {exc!r}"

    state_path = root / "runtime" / "worker_state.csv"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not state_path.exists()
    with state_path.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(
            {
                "worker": "trust_flags",
                "last_run": datetime.now(timezone.utc).isoformat(),
                "status": status,
                "failures_24h": "0" if status == "ok" else "1",
                "next_run": "",
                "notes": notes,
            }
        )
    print(f"[run_trust_flags_worker] status={status}")
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
