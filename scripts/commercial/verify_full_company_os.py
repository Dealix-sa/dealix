#!/usr/bin/env python3
"""Verify Dealix Full Company OS foundation.

This verifier is intentionally local and conservative. It confirms that the
runner can generate draft-only operating artifacts and that obvious live-action
adapters were not introduced in this feature slice.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_PATHS = [
    "dealix/full_company_os/__init__.py",
    "dealix/full_company_os/kernel.py",
    "scripts/commercial/run_full_company_os.py",
    "scripts/commercial/render_full_company_os_issue.py",
    "docs/commercial/FULL_COMPANY_OS_IMPLEMENTATION.md",
    "docs/commercial/FULL_COMPANY_OS_EXECUTION_BASELINE.md",
    "docs/commercial/DAILY_AUTONOMOUS_OPERATING_MODEL.md",
    "data/full_company_os/targets.example.json",
]

FORBIDDEN_ENABLEMENT_PATTERNS = [
    re.compile(r"send_email\s*\(", re.IGNORECASE),
    re.compile(r"send_whatsapp\s*\(", re.IGNORECASE),
    re.compile(r"auto_post\s*\(", re.IGNORECASE),
    re.compile(r"capture_payment\s*\(", re.IGNORECASE),
    re.compile(r"merge_pull_request\s*\(", re.IGNORECASE),
    re.compile(r"PRODUCTION_MUTATION_ENABLED\s*=\s*true", re.IGNORECASE),
    re.compile(r"EXTERNAL_SEND_ENABLED\s*=\s*true", re.IGNORECASE),
]

OUTPUT_ROOT = ROOT / "reports" / "full_company_os_verify"


def fail(message: str) -> int:
    print(f"FULL_COMPANY_OS_VERIFY=FAIL {message}")
    return 1


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def verify_required_paths() -> list[str]:
    errors: list[str] = []
    for item in REQUIRED_PATHS:
        if not (ROOT / item).exists():
            errors.append(f"missing:{item}")
    return errors


def verify_no_live_action_enablement() -> list[str]:
    errors: list[str] = []
    scanned = [
        ROOT / "dealix" / "full_company_os" / "kernel.py",
        ROOT / "scripts" / "commercial" / "run_full_company_os.py",
        ROOT / "scripts" / "commercial" / "render_full_company_os_issue.py",
    ]
    for path in scanned:
        text = read_text(path)
        for pattern in FORBIDDEN_ENABLEMENT_PATTERNS:
            if pattern.search(text):
                errors.append(f"forbidden_live_pattern:{path.relative_to(ROOT)}:{pattern.pattern}")
    return errors


def run_cycle() -> tuple[int, str]:
    cmd = [
        sys.executable,
        "scripts/commercial/run_full_company_os.py",
        "--client",
        "dealix",
        "--mode",
        "draft-only",
        "--limit",
        "10",
        "--output-root",
        str(OUTPUT_ROOT.relative_to(ROOT)),
        "--json",
    ]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    return proc.returncode, proc.stdout


def run_issue_renderer() -> tuple[int, str]:
    cmd = [
        sys.executable,
        "scripts/commercial/render_full_company_os_issue.py",
        "--company-os-json",
        str((OUTPUT_ROOT / "latest.json").relative_to(ROOT)),
        "--revenue-json",
        "reports/full_company_os/revenue_path/first_paid_client_path.json",
        "--output",
        str((OUTPUT_ROOT / "daily_issue.md").relative_to(ROOT)),
    ]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    return proc.returncode, proc.stdout


def verify_outputs() -> list[str]:
    errors: list[str] = []
    required_outputs = [
        OUTPUT_ROOT / "latest.json",
        OUTPUT_ROOT / "latest.md",
    ]
    for path in required_outputs:
        if not path.exists():
            errors.append(f"missing_output:{path.relative_to(ROOT)}")
    bundle_path = OUTPUT_ROOT / "latest.json"
    if bundle_path.exists():
        try:
            bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid_json:{exc}")
        else:
            if not bundle.get("drafts"):
                errors.append("no_drafts_generated")
            if not bundle.get("approvals"):
                errors.append("no_approval_queue_generated")
            if not bundle.get("proof_log"):
                errors.append("no_proof_log_generated")
            if any(item.get("status") != "pending_founder_review" for item in bundle.get("drafts", [])):
                errors.append("draft_status_not_pending_review")
    return errors


def verify_daily_issue_output() -> list[str]:
    errors: list[str] = []
    issue_body = OUTPUT_ROOT / "daily_issue.md"
    if not issue_body.exists():
        return [f"missing_output:{issue_body.relative_to(ROOT)}"]
    text = issue_body.read_text(encoding="utf-8")
    required_phrases = [
        "Dealix Daily Command",
        "Drafts pending review",
        "Approval queue",
        "First paid client / Money Now",
        "Safety lock",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"missing_issue_phrase:{phrase}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(verify_required_paths())
    errors.extend(verify_no_live_action_enablement())
    if errors:
        return fail(" ".join(errors))
    rc, output = run_cycle()
    if rc != 0:
        print(output)
        return fail("runner_failed")
    errors.extend(verify_outputs())
    issue_rc, issue_output = run_issue_renderer()
    if issue_rc != 0:
        print(issue_output)
        return fail("daily_issue_renderer_failed")
    errors.extend(verify_daily_issue_output())
    if errors:
        print(output)
        print(issue_output)
        return fail(" ".join(errors))
    print("FULL_COMPANY_OS_VERIFY=PASS mode=draft-only external_send=false payment_capture=false production_mutation=false daily_issue=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
