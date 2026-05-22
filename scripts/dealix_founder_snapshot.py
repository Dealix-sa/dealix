#!/usr/bin/env python3
"""Single-command founder snapshot — fans out across existing verifiers.

Composes (does not re-implement):
  - scripts/founder_strongest_plan_status.py
  - scripts/founder_comprehensive_plan_status.py
  - scripts/verify_full_autonomous_ops_stack.py

Prints a single consolidated verdict line:
  FOUNDER_SNAPSHOT_VERDICT=GREEN | AMBER | RED

Usage:
  python scripts/dealix_founder_snapshot.py
  python scripts/dealix_founder_snapshot.py --json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "scripts"


@dataclass
class CheckResult:
    name: str
    cmd: list[str]
    exit_code: int
    pass_: bool
    tail: str  # last ~6 lines of stdout, trimmed


def _run(name: str, cmd: list[str], timeout: int = 90) -> CheckResult:
    try:
        completed = subprocess.run(
            cmd,
            cwd=str(_REPO),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        return CheckResult(
            name=name, cmd=cmd, exit_code=127, pass_=False, tail=f"FileNotFoundError: {exc}"
        )
    except subprocess.TimeoutExpired as exc:
        return CheckResult(
            name=name, cmd=cmd, exit_code=124, pass_=False, tail=f"TimeoutExpired after {exc.timeout}s"
        )
    out = (completed.stdout or "") + ("\n" + completed.stderr if completed.stderr else "")
    tail_lines = [line for line in out.splitlines() if line.strip()][-6:]
    return CheckResult(
        name=name,
        cmd=cmd,
        exit_code=completed.returncode,
        pass_=(completed.returncode == 0),
        tail="\n".join(tail_lines),
    )


def build_snapshot() -> dict:
    py = sys.executable
    checks = [
        _run(
            "strongest_plan",
            [py, str(_SCRIPTS / "founder_strongest_plan_status.py")],
        ),
        _run(
            "comprehensive_plan",
            [py, str(_SCRIPTS / "founder_comprehensive_plan_status.py")],
        ),
        _run(
            "full_autonomous_ops_stack",
            [py, str(_SCRIPTS / "verify_full_autonomous_ops_stack.py")],
        ),
    ]
    passed = sum(1 for c in checks if c.pass_)
    total = len(checks)
    if passed == total:
        verdict = "GREEN"
    elif passed == 0:
        verdict = "RED"
    else:
        verdict = "AMBER"
    return {
        "verdict": verdict,
        "passed": passed,
        "total": total,
        "checks": [asdict(c) for c in checks],
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Consolidated founder snapshot.")
    p.add_argument("--json", action="store_true", help="emit full JSON in addition to the verdict line")
    args = p.parse_args()
    snap = build_snapshot()
    print(f"FOUNDER_SNAPSHOT_VERDICT={snap['verdict']}")
    print(f"passed={snap['passed']}/{snap['total']}")
    for c in snap["checks"]:
        marker = "ok" if c["pass_"] else "FAIL"
        print(f"  [{marker}] {c['name']} (exit={c['exit_code']})")
    if args.json:
        print(json.dumps(snap, ensure_ascii=False, indent=2))
    return 0 if snap["verdict"] == "GREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
