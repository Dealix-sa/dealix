#!/usr/bin/env python3
"""Sales funnel worker — refreshes ``founder/sales_funnel.json``."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api.internal.runtime_reader import private_ops_root, sales_funnel_summary  # noqa: E402


def main() -> int:
    try:
        data = sales_funnel_summary()
        out = private_ops_root() / "founder/sales_funnel.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        status, notes = "ok", f"stages={len(data.get('stages', []))}"
        print(f"[OK] wrote {out}")
    except Exception as exc:
        status, notes = "failed", str(exc)[:200]
        print(f"[FAIL] {exc}", file=sys.stderr)

    subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("update_worker_state.py")),
            "--worker", "sales_funnel",
            "--status", status,
            "--notes", notes,
        ],
        check=False,
    )
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
