#!/usr/bin/env python3
"""L8 — GitHub Governance verifier.

Parses .github/workflows/*.yml; asserts required workflows exist + each has jobs.runs-on.
No GitHub API calls. Exit 0=PASS, 1=FAIL.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # parsing degrades gracefully

REPO = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = REPO / ".github" / "workflows"

REQUIRED_WORKFLOWS = [
    "ci.yml",
    "codeql.yml",
    "verify-full-autonomous-ops.yml",
    "governed-full-ops-daily.yml",
    "dealix-master-verify.yml",
]


def parse_workflow(path: Path) -> tuple[bool, str]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return False, f"read error: {e}"
    if yaml is None:
        if "jobs:" in text and "runs-on" in text:
            return True, "ok (yaml lib unavailable, structural ok)"
        return False, "no jobs/runs-on found (yaml lib unavailable)"
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        return False, f"yaml parse error: {e}"
    if not isinstance(data, dict):
        return False, "not a mapping"
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        return False, "no jobs defined"
    for jname, job in jobs.items():
        if not isinstance(job, dict):
            return False, f"job {jname!r} not a mapping"
        if "runs-on" not in job and "uses" not in job:
            return False, f"job {jname!r} missing runs-on/uses"
    return True, f"ok ({len(jobs)} jobs)"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--private-ops", default=None, help="ignored at L8")
    ap.add_argument(
        "--required", action="append", default=[], help="additional required workflow names"
    )
    args = ap.parse_args()

    required = list(REQUIRED_WORKFLOWS) + list(args.required)
    failures: list[str] = []
    workflow_count = 0

    if not WORKFLOWS_DIR.is_dir():
        msg = f"missing workflows directory: {WORKFLOWS_DIR}"
        if args.json:
            print(json.dumps({"layer": 8, "verdict": "FAIL", "missing": [msg], "summary": msg}))
        else:
            print(msg)
        return 1

    for wf in sorted(WORKFLOWS_DIR.glob("*.yml")):
        workflow_count += 1
        ok, msg = parse_workflow(wf)
        if not ok:
            failures.append(f"{wf.name}: {msg}")

    present = {p.name for p in WORKFLOWS_DIR.glob("*.yml")}
    missing_required = [name for name in required if name not in present]
    for name in missing_required:
        failures.append(f"missing required workflow: {name}")

    verdict = "PASS" if not failures else "FAIL"
    summary = f"{workflow_count} workflows parsed; required missing: {len(missing_required)}"
    if args.json:
        print(
            json.dumps(
                {
                    "layer": 8,
                    "verdict": verdict,
                    "workflow_count": workflow_count,
                    "missing_required": missing_required,
                    "errors": failures,
                    "summary": summary,
                }
            )
        )
    else:
        print(summary)
        for f in failures:
            print(f"  - {f}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
