#!/usr/bin/env python3
"""Dealix OS master certification orchestrator.

Runs the 8 C-level verifications in a deterministic order, writes a
single certification report to `$PRIVATE_OPS/founder/dealix_os_certification.md`,
and exits non-zero on any failure. Used by `make certify`.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

CHECKS: Sequence[tuple[str, str, list[str]]] = (
    ("C1 Repository Structure", "scripts/verify_repository_structure.py", ["--private-ops"]),
    ("C1 Code Health", "scripts/verify_code_health.py", ["--private-ops"]),
    ("C2 Private Ops Contracts", "scripts/verify_private_ops_contracts.py", ["--private-ops"]),
    ("C2 Server Runtime", "scripts/verify_server_runtime.py", ["--private-ops"]),
    ("C3 Revenue Runtime", "scripts/verify_revenue_runtime.py", ["--private-ops"]),
    ("C4 Prompt Output Quality", "scripts/verify_prompt_output_quality.py", ["--private-ops"]),
    ("C4 Trust Security Runtime", "scripts/verify_trust_security_runtime.py", ["--private-ops"]),
    ("C5 Business Evidence", "scripts/verify_business_evidence.py", ["--private-ops"]),
)


def run_check(name: str, script: str, args: list[str], private_ops: Path) -> dict[str, object]:
    cmd: list[str] = [sys.executable, str(REPO / script)]
    for part in args:
        if part == "--private-ops":
            cmd.extend(["--private-ops", str(private_ops)])
        else:
            cmd.append(part)
    print(f"\n## {name}")
    print("+ " + " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)  # noqa: S603
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, end="" if result.stderr.endswith("\n") else "\n")
    status = "PASS" if result.returncode == 0 else "FAIL"
    return {
        "name": name,
        "status": status,
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
    }


def certification_level(results: list[dict[str, object]]) -> str:
    failed = [r for r in results if r["status"] == "FAIL"]
    if not failed:
        return "CERTIFIED"
    if len(failed) == len(results):
        return "NOT CERTIFIED"
    return "PARTIAL"


def main() -> int:
    ensure_stdout_utf8()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-ops", required=True, type=Path)
    args = parser.parse_args()

    results = [run_check(name, script, opts, args.private_ops) for name, script, opts in CHECKS]
    certification = certification_level(results)

    report_lines = [
        "# Dealix OS Certification Report",
        "",
        "## Date",
        datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "",
        "## Certification",
        certification,
        "",
        "## Checks",
        "",
    ]
    for r in results:
        report_lines.append(f"- {r['status']}: {r['name']}")
    report_lines += [
        "",
        "## Required CEO Action",
        (
            "None — all checks passed."
            if certification == "CERTIFIED"
            else "Fix all FAIL checks before adding new systems or scaling outreach."
        ),
        "",
    ]

    out = args.private_ops / "founder/dealix_os_certification.md"
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(report_lines), encoding="utf-8")
        print(f"\nReport written: {out}")
    except OSError as e:
        print(f"\nWARNING: could not write report to {out}: {e}")

    print(f"\nCERTIFICATION={certification}")
    return 0 if certification == "CERTIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
