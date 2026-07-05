#!/usr/bin/env python3
"""Dealix daily self runner.

Runs the safe daily operating sequence without human prompting. The runner is
read-only or draft-only: it prepares reports, drafts, queues, and checks, then
stops for founder approval before any customer-facing action.
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "reports" / "autopilot"

COMMANDS = [
    ["scripts/ops/free_llm_provider_radar.py", "--task", "coding", "--limit", "3"],
    ["scripts/ops/free_llm_provider_radar.py", "--task", "arabic", "--limit", "3"],
    ["scripts/ops/free_llm_provider_radar.py", "--task", "batch", "--limit", "3"],
    ["scripts/ops/free_llm_provider_radar.py", "--task", "sensitive", "--limit", "3"],
    ["scripts/dealix_daily_operator.py", "--mode", "demo"],
    ["scripts/ops/daily_commercial_draft_pack.py"],
    ["scripts/distribution_day.py"],
    ["scripts/check_draft_quality.py"],
    ["scripts/distribution_metrics.py"],
]


def run_command(args: list[str]) -> dict[str, object]:
    script = ROOT / args[0]
    label = " ".join(args)
    if not script.exists():
        return {"command": label, "status": "skipped", "reason": "missing script"}

    proc = subprocess.run(
        [sys.executable, str(script), *args[1:]],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": label,
        "status": "ok" if proc.returncode == 0 else "failed",
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-2500:],
        "stderr_tail": proc.stderr[-2500:],
    }


def write_report(results: list[dict[str, object]]) -> Path:
    today = dt.date.today().isoformat()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / f"daily-self-runner-{today}.md"
    ok_count = sum(1 for item in results if item.get("status") == "ok")
    lines = [
        f"# Dealix Daily Self Runner — {today}",
        "",
        f"Completed steps: {ok_count}/{len(results)}",
        "",
        "## Rule",
        "This run prepares provider choices, reports, drafts, queues, and quality checks. It does not send customer-facing messages or approve commitments.",
        "",
        "## Results",
        "",
    ]
    for item in results:
        lines.append(f"### {item['command']}")
        lines.append(f"- Status: `{item['status']}`")
        if item.get("reason"):
            lines.append(f"- Reason: {item['reason']}")
        if item.get("returncode") is not None:
            lines.append(f"- Return code: `{item['returncode']}`")
        lines.append("")
    lines.extend(
        [
            "## Founder next action",
            "Review generated drafts and queues, then approve only accurate, compliant, non-overclaiming commercial actions.",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    (REPORT_DIR / f"daily-self-runner-{today}.json").write_text(
        json.dumps({"date": today, "results": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def main() -> int:
    results = [run_command(command) for command in COMMANDS]
    report = write_report(results)
    print(f"Wrote: {report}")
    failed = [item for item in results if item.get("status") == "failed"]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
