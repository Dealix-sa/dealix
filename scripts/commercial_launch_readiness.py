#!/usr/bin/env python3
"""Commercial launch readiness -> prints GO/NO-GO and writes readiness JSON.

Runs the full daily pipeline if outputs are missing, then verifies all required
daily artifacts exist and the safety audit passed. Read-only / file-only.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import now_iso, output_day_dir, today_str, write_json

ROOT = Path(__file__).resolve().parents[1]

PIPELINE = [
    ["commercial_generate_400_drafts.py", "--target", "400"],
    ["commercial_score_drafts.py"],
    ["commercial_quality_gate.py"],
    ["commercial_compliance_gate.py"],
    ["commercial_founder_review_report.py"],
    ["commercial_safety_audit.py"],
    ["commercial_metrics_summary.py"],
]

REQUIRED_OUTPUTS = [
    "draft_queue.jsonl",
    "founder_review.csv",
    "founder_review.md",
    "top_50_priority.md",
    "rejected_drafts.jsonl",
    "needs_research.jsonl",
    "compliance_report.json",
    "quality_report.json",
    "safety_audit.json",
    "daily_metrics.json",
    "next_actions.md",
    "batch_manifest.json",
    "approved_manual_sends.example.csv",
]


def run_pipeline(day: str) -> list[str]:
    log = []
    for cmd in PIPELINE:
        full = [sys.executable, str(ROOT / "scripts" / cmd[0]), *cmd[1:], "--day", day]
        res = subprocess.run(full, capture_output=True, text=True)
        log.append(f"{cmd[0]} -> rc={res.returncode}")
        if res.returncode != 0:
            log.append(res.stderr.strip()[-500:])
    return log


def run(day: str, regenerate: bool) -> dict:
    d = output_day_dir(day)
    log = []
    if regenerate or not (d / "draft_queue.jsonl").exists():
        log = run_pipeline(day)

    missing = [f for f in REQUIRED_OUTPUTS if not (d / f).exists()]
    safety = (
        json.loads((d / "safety_audit.json").read_text(encoding="utf-8"))
        if (d / "safety_audit.json").exists()
        else {}
    )
    safety_passed = bool(safety.get("passed"))

    go = (not missing) and safety_passed
    report = {
        "generated_at": now_iso(),
        "day": day,
        "required_outputs": REQUIRED_OUTPUTS,
        "missing_outputs": missing,
        "safety_passed": safety_passed,
        "draft_count": safety.get("draft_count"),
        "decision": "GO" if go else "NO-GO",
        "pipeline_log": log,
        "go_scope": [
            "review-only drafts",
            "founder manual review",
            "manual outreach",
            "paid diagnostics",
            "discovery calls",
            "proposals",
        ],
        "no_go_scope": [
            "automated email sending",
            "whatsapp cold outreach",
            "linkedin automation",
            "website form auto-submit",
            "bulk sending",
            "external sending from CI",
        ],
    }
    write_json(d / "commercial_launch_readiness.json", report)
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", default=today_str())
    ap.add_argument("--regenerate", action="store_true")
    args = ap.parse_args()
    r = run(args.day, args.regenerate)
    print(f"Commercial launch readiness: {r['decision']}")
    if r["missing_outputs"]:
        print("  missing:", ", ".join(r["missing_outputs"]))
    return 0 if r["decision"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
