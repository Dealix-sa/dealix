#!/usr/bin/env python3
"""CEO summary worker — refreshes the founder pulse view.

Reads private runtime CSVs and writes ``founder/ceo_summary.json`` plus
a `worker_state.csv` heartbeat. Never sends externally.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

# Ensure the api package is importable when running the worker directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api.internal.runtime_reader import ceo_summary, private_ops_root  # noqa: E402


def main() -> int:
    try:
        summary = ceo_summary()
        out = private_ops_root() / "founder/ceo_summary.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        status = "ok"
        notes = f"source={summary.get('source')}"
        print(f"[OK] wrote {out}")
    except Exception as exc:
        status = "failed"
        notes = str(exc)[:200]
        print(f"[FAIL] {exc}", file=sys.stderr)

    subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("update_worker_state.py")),
            "--worker", "ceo_summary",
            "--status", status,
            "--notes", notes,
        ],
        check=False,
    )
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
