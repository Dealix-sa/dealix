#!/usr/bin/env python3
"""Run every V9 verifier and write the master verification report.

Writes outputs/v9_verification/V9_MASTER_VERIFICATION.md and exits non-zero if
any system fails. Static, read-only, artifact-only — no external sending.
"""

from __future__ import annotations

import importlib
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402
import _v9_aggregate as agg  # noqa: E402

# Aggregate roll-ups to include in the master report.
AGGREGATES = {
    "company_utilization": "company_utilization_verify",
    "startup_os": "startup_os_verify",
    "final_launch_control": "final_launch_control_verify",
    "master_startup_command": "master_startup_command_verify",
    "execution_intelligence": "execution_intelligence_verify",
}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    system_results: dict[str, str] = {}
    for key, module_name in agg.V9_MODULES.items():
        mod = importlib.import_module(module_name)
        report = mod.verify()
        system_results[key] = report.get("verdict", "FAIL")

    aggregate_results: dict[str, str] = {}
    for key, module_name in AGGREGATES.items():
        mod = importlib.import_module(module_name)
        report = mod.verify()
        aggregate_results[key] = report.get("verdict", "FAIL")

    overall = "PASS" if (
        all(v == "PASS" for v in system_results.values())
        and all(v == "PASS" for v in aggregate_results.values())
    ) else "FAIL"

    lines = ["# V9 Master Verification", ""]
    lines.append(f"_Date: {date.today().isoformat()}_")
    lines.append("")
    lines.append(f"## Overall Verdict: {overall}")
    lines.append("")
    lines.append("## Systems")
    lines.append("")
    lines.append("| System | Verdict |")
    lines.append("| --- | --- |")
    for k, v in system_results.items():
        lines.append(f"| {k} | {v} |")
    lines.append("")
    lines.append("## Aggregates")
    lines.append("")
    lines.append("| Aggregate | Verdict |")
    lines.append("| --- | --- |")
    for k, v in aggregate_results.items():
        lines.append(f"| {k} | {v} |")
    lines.append("")
    lines.append("## Safety")
    lines.append("")
    lines.append("- No external sending. No secrets. Artifact-only verification.")
    lines.append("- Founder approval remains required for anything customer-facing.")
    lines.append("")

    v9_lib.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (v9_lib.OUTPUT_DIR / "V9_MASTER_VERIFICATION.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8")

    print(f"V9 master verification overall={overall}")
    for k, v in {**system_results, **aggregate_results}.items():
        print(f"  - {k}: {v}")
    print(f"V9_MASTER_VERDICT={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
