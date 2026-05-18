#!/usr/bin/env python3
"""Founder Executive Rise — one governed day (morning stack + status JSON)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.founder_executive_os import build_founder_executive_snapshot  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def _run(cmd: list[str]) -> int:
    print(f"\n>> {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=ROOT).returncode


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json-only", action="store_true", help="Skip subprocesses; print snapshot only")
    p.add_argument("--api-base", default="https://api.dealix.me")
    p.add_argument("--evening", action="store_true")
    p.add_argument("--weekly", action="store_true")
    args = p.parse_args()

    snap = build_founder_executive_snapshot(api_base=args.api_base)
    out = ROOT / "data" / "founder_briefs" / "executive_rise_snapshot.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"FOUNDER_EXECUTIVE_LAUNCH_PHASE={snap['launch_phase']}")
    print(f"RAILWAY_VERDICT={snap['railway_verdict']}")
    print(f"FIRST_PAID={snap['first_paid'].get('verdict')}")
    for b in snap.get("blockers", [])[:8]:
        print(f"  blocker: {b}")

    if args.json_only:
        print(json.dumps(snap, ensure_ascii=False, indent=2))
        return 0

    py = sys.executable
    if args.evening:
        return _run([py, str(ROOT / "scripts/founder_evening_evidence.py")])

    steps: list[list[str]] = [
        [py, str(ROOT / "scripts/verify_railway_production_config.py")],
        [py, str(ROOT / "scripts/bootstrap_founder_kpi_import.py")],
        [py, str(ROOT / "scripts/apply_kpi_founder_commercial.py"), "--status"],
        [py, str(ROOT / "scripts/founder_strongest_plan_status.py")],
        [py, str(ROOT / "scripts/verify_first_paid_diagnostic_tracker.py")],
        [py, str(ROOT / "scripts/verify_launch_phase.py")],
    ]
    if args.weekly:
        steps.append(["bash", str(ROOT / "scripts/founder_motion_a_weekly_review.sh")])

    rc = 0
    for cmd in steps:
        if cmd[0] == "bash" and sys.platform == "win32":
            cmd = ["bash"] + cmd[1:]
        rc = max(rc, _run(cmd))

    print(f"\nSnapshot: {out.relative_to(ROOT)}")
    print(f"Playbook: {snap['playbook']}")
    print("FOUNDER_EXECUTIVE_RISE_DAY=OK" if rc == 0 else f"FOUNDER_EXECUTIVE_RISE_DAY=WARN exit={rc}")
    return 0 if rc <= 1 else rc


if __name__ == "__main__":
    raise SystemExit(main())
