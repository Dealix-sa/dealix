#!/usr/bin/env python3
"""Launch-readiness board — aggregate the existing offline verify gates.

This is an operating / CI-hygiene tool. It runs a curated subset of the
repo's ``scripts/verify_*`` gate checks and prints one green/red board.
It adds NO product capability and NO API route — it only AGGREGATES
checks that already exist, so a single command answers "are the launch
gates green?".

Usage:
    python scripts/launch_readiness.py            # human-readable board
    python scripts/launch_readiness.py --json     # machine-readable
    python scripts/launch_readiness.py --gate proof_pack   # one gate only

Exit code:
    0  — every selected gate passed
    1  — one or more gates failed

The curated subset is intentionally offline + fast (doc/file structural
gates). Network smoke checks live in ``scripts/launch_readiness_check.py``
and ``scripts/smoke_staging.py`` and are out of scope here.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]

# Curated subset: offline, fast, structural gates. Each entry is a gate
# name -> the verify script that decides pass/fail via its exit code.
GATES: dict[str, str] = {
    "proof_pack": "verify_proof_pack.py",
    "quality_score": "verify_quality_score.py",
    "sellability": "verify_sellability.py",
    "service_files": "verify_service_files.py",
    "governance": "verify_governance.py",
}


def _run_gate(script: str, *, timeout: float = 120.0) -> dict[str, object]:
    """Run one verify script and capture its pass/fail + output."""
    path = _REPO / "scripts" / script
    if not path.is_file():
        return {
            "script": script,
            "passed": False,
            "exit_code": None,
            "duration_s": 0.0,
            "detail": f"verify script not found: {script}",
        }
    started = time.monotonic()
    try:
        proc = subprocess.run(  # noqa: S603 — fixed sys.executable + known repo script paths
            [sys.executable, str(path)],
            cwd=str(_REPO),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {
            "script": script,
            "passed": False,
            "exit_code": None,
            "duration_s": round(time.monotonic() - started, 2),
            "detail": f"gate timed out after {timeout}s",
        }
    duration = round(time.monotonic() - started, 2)
    tail = (proc.stderr or proc.stdout or "").strip().splitlines()
    return {
        "script": script,
        "passed": proc.returncode == 0,
        "exit_code": proc.returncode,
        "duration_s": duration,
        "detail": tail[-1] if tail else "",
    }


def evaluate(gate_names: list[str]) -> dict[str, object]:
    """Run the selected gates and return an aggregate result dict."""
    results: dict[str, dict[str, object]] = {}
    for name in gate_names:
        results[name] = _run_gate(GATES[name])
    all_pass = all(r["passed"] for r in results.values())
    return {
        "all_pass": all_pass,
        "gates_total": len(results),
        "gates_passed": sum(1 for r in results.values() if r["passed"]),
        "gates_failed": sum(1 for r in results.values() if not r["passed"]),
        "gates": results,
    }


def _print_board(report: dict[str, object]) -> None:
    """Print the human-readable green/red board."""
    gates: dict[str, dict[str, object]] = report["gates"]  # type: ignore[assignment]
    print("Dealix Launch Readiness Board")
    print("-" * 52)
    for name, r in gates.items():
        mark = "PASS" if r["passed"] else "FAIL"
        line = f"  [{mark}]  {name:<16} ({r['duration_s']}s)"
        if not r["passed"] and r["detail"]:
            line += f"  -> {r['detail']}"
        print(line)
    print("-" * 52)
    verdict = "GREEN — all gates passed" if report["all_pass"] else "RED — gate failure"
    print(
        f"  {report['gates_passed']}/{report['gates_total']} gates passed  ::  {verdict}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate offline launch-readiness verify gates into one board.",
    )
    parser.add_argument(
        "--json", action="store_true", help="emit the board as JSON"
    )
    parser.add_argument(
        "--gate",
        action="append",
        choices=sorted(GATES),
        help="run only this gate (repeatable); default runs all",
    )
    args = parser.parse_args(argv)

    gate_names = args.gate or sorted(GATES)
    report = evaluate(gate_names)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        _print_board(report)

    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
