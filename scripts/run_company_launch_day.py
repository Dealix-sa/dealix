#!/usr/bin/env python3
"""
One-command company launch day runner.

Runs all health checks, revenue machine, command room, server preflight,
and emits a final CEO report.
"""
from __future__ import annotations

import os
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VENV_PYTHON = REPO_ROOT / ".venv" / "Scripts" / "python.exe"
PYTHON = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable

TODAY = os.environ.get("DEALIX_DATE", date.today().isoformat())

STEPS = [
    ("Repo health checks", [PYTHON, "scripts/verify_company_launch_ready.py"]),
    ("Target validation", [PYTHON, "scripts/revenue/find_targets_manual_workflow.py", "--validate", "ledgers/prospects.csv"]),
    ("Score targets", [PYTHON, "scripts/revenue/score_targets.py", "--input", "ledgers/prospects.csv"]),
    ("Generate outreach", [PYTHON, "scripts/revenue/generate_outreach.py", "--input", "ledgers/prospects.csv"]),
    ("Generate follow-ups", [PYTHON, "scripts/revenue/generate_followups.py", "--cooldown-days", "1"]),
    ("Generate proposals", [PYTHON, "scripts/revenue/generate_proposal_brief.py", "--input", "ledgers/prospects.csv"]),
    ("Build command room", [PYTHON, "scripts/command_room/build_command_room.py"]),
    ("Server preflight", [PYTHON, "scripts/server/server_preflight.py"]),
    ("Daily CEO report", [PYTHON, "scripts/revenue/generate_daily_revenue_report.py"]),
]


def run_step(name: str, cmd: list[str]) -> tuple[bool, str]:
    print(f"\n▶ {name}")
    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=180)
    ok = result.returncode == 0
    last_lines = (result.stdout + result.stderr).strip().splitlines()[-5:]
    detail = "\n".join(last_lines)
    if ok:
        print(f"✅ {name}\n{detail}")
    else:
        print(f"❌ {name}\n{detail}")
    return ok, detail


def main() -> int:
    print("=" * 70)
    print("Dealix Company Launch Day")
    print("=" * 70)

    results: list[tuple[str, bool, str]] = []
    for name, cmd in STEPS:
        ok, detail = run_step(name, cmd)
        results.append((name, ok, detail))

    # Server preflight missing env vars is a warning, not a pipeline blocker
    non_server_ok = all(ok for name, ok, _ in results if "Server" not in name)
    all_ok = all(ok for _, ok, _ in results)

    if all_ok:
        verdict = "READY_FOR_MANUAL_OUTREACH"
    else:
        # Determine blocker category
        failed_names = [name for name, ok, _ in results if not ok]
        if all("Server" in name for name in failed_names):
            verdict = "NEEDS_SERVER_FIX"
        elif any("Target" in name or "Score" in name for name in failed_names):
            verdict = "NEEDS_TARGET_VERIFICATION"
        elif any("Repo health" in name for name in failed_names):
            verdict = "NEEDS_COMPLIANCE_REVIEW"
        else:
            verdict = "BLOCKED"

    report_lines = [
        f"# Company Launch Day Report — {TODAY}",
        "",
        f"**Verdict:** `{verdict}`",
        "",
        "## Steps",
        "",
    ]
    for name, ok, detail in results:
        status = "✅" if ok else "❌"
        report_lines.append(f"### {status} {name}")
        report_lines.append(detail)
        report_lines.append("")

    report_lines.extend([
        "## Next actions",
        "- Review drafts in outbox/YYYY-MM-DD/",
        "- Open reports/command_room/index.html",
        "- Update ledgers/outreach_log.csv after manual sends",
        "",
    ])

    out_dir = REPO_ROOT / "reports" / "company_launch"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"COMPANY_DAY_{TODAY}.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    print("\n" + "=" * 70)
    print(f"VERDICT: {verdict}")
    print(f"Report: {report_path}")
    print("=" * 70)
    # Return 0 if revenue/compliance pipeline is healthy; server env can be fixed later
    return 0 if non_server_ok else 1


if __name__ == "__main__":
    sys.exit(main())
