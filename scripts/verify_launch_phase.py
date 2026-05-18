#!/usr/bin/env python3
"""DEALIX_LAUNCH_PHASE=SOFT|PAID_ROADMAP|PAID_READY from governed checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic  # noqa: E402
from dealix.commercial_ops.founder_executive_os import build_founder_executive_snapshot  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def _run(script: str) -> int:
    return subprocess.run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT).returncode


def main() -> int:
    soft_rc = _run("verify_commercial_launch_ready.py")
    _run("verify_paid_launch_readiness.py")
    first = analyze_first_paid_diagnostic()
    snap = build_founder_executive_snapshot()
    phase = snap["launch_phase"]
    if first.get("verdict") == "PASS":
        phase = "PAID_READY"
    elif soft_rc != 0:
        phase = "SOFT"

    print(f"DEALIX_LAUNCH_PHASE={phase}")
    print(f"  soft_launch_exit={soft_rc}")
    print(f"  first_paid_verdict={first.get('verdict')}")
    print("  matrix: docs/commercial/SOFT_VS_PAID_LAUNCH_MATRIX_AR.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
