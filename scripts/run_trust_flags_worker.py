#!/usr/bin/env python3
"""Trust flags worker — refreshes ``founder/trust_flags.json``."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api.internal.runtime_reader import private_ops_root, trust_flags  # noqa: E402


def main() -> int:
    try:
        data = trust_flags()
        out = private_ops_root() / "founder/trust_flags.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        status, notes = "ok", f"flags={len(data.get('flags', []))}"
        print(f"[OK] wrote {out}")
    except Exception as exc:
        status, notes = "failed", str(exc)[:200]
        print(f"[FAIL] {exc}", file=sys.stderr)

    subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("update_worker_state.py")),
            "--worker", "trust_flags",
            "--status", status,
            "--notes", notes,
        ],
        check=False,
    )
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
