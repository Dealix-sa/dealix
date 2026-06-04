#!/usr/bin/env python3
"""Commercial Safety Audit — the no-send guarantee.

Two layers of enforcement:

1. Draft-flag integrity (authoritative): every generated draft MUST carry
   send_allowed=false, external_send_blocked=true, requires_founder_approval=true,
   no_auto_send=true. Any deviation fails the audit.

2. Code-surface scan: the launch tooling (scripts + launch configs + the four
   launch workflows) must contain NO outbound-send construct — no smtplib,
   SendGrid/Mailgun/Postmark/SES, no Twilio/WhatsApp send, no LinkedIn
   automation, no browser automation for outreach, no bulk/mass send, no CRM
   push-send, and no flag literal that re-enables sending.

The audit scans for *sending capability*, not mere policy mentions. The
defensive scanner/gate files (which name these constructs on purpose) are
excluded from the code scan. Writes safety_audit.json and exits non-zero on
any violation.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import (
    COMMERCIAL_OUTPUTS,
    ROOT,
    read_jsonl,
    today_str,
    write_json,
)

# Files that legitimately name forbidden constructs (audits, gates, policy configs).
SCANNER_ALLOWLIST = {
    "scripts/commercial_safety_audit.py",
    "scripts/final_secret_and_risk_scan.py",
    "scripts/commercial_compliance_gate.py",
    "scripts/commercial_quality_gate.py",
    "scripts/api_commercial_static_check.py",
    "scripts/final_launch_control_verify.py",
    "scripts/commercial_crm_schema_verify.py",
    "scripts/media_social_verify.py",
    "config/commercial_channels.json",
    "config/commercial_compliance_gates.json",
    "config/commercial_risk_terms.json",
    "config/crm_pipeline_schema.json",
}

# Positive outbound-send constructs (real capability), not negations or policy text.
FORBIDDEN_CONSTRUCTS = [
    r"import\s+smtplib",
    r"from\s+smtplib",
    r"smtplib\.SMTP",
    r"server\.sendmail",
    r"\.sendmail\(",
    r"\bsend_email\s*\(",
    r"\bsend_mail\s*\(",
    r"\bsendgrid\b",
    r"\bmailgun\b",
    r"\bpostmark\b",
    r"ses\.send_email",
    r"ses\.send_raw_email",
    r"twilio\.rest",
    r"twilio\.messages\.create",
    r"whatsapp.*\.send\(",
    r"linkedin[_-]?api\b",
    r"linkedin.*\.send_message\(",
    r"auto[_-]?connect\s*\(",
    r"selenium\.webdriver",
    r"playwright\.sync_api",
    r"\bbulk_send\b",
    r"\bmass_send\b",
    r"crm[_-]?push[_-]?send",
    r"inbox[_-]?automation",
]

# Flag literals that would re-enable sending.
FORBIDDEN_FLAG_LITERALS = [
    r'"send_allowed"\s*:\s*true',
    r'"external_send_blocked"\s*:\s*false',
    r'"no_auto_send"\s*:\s*false',
    r"send_allowed\s*=\s*True",
    r"external_send_blocked\s*=\s*False",
    r"no_auto_send\s*=\s*False",
]


def _launch_surface() -> list[Path]:
    paths: list[Path] = []
    for pattern in [
        "scripts/commercial_*.py",
        "scripts/media_social_*.py",
        "scripts/site_launch_*.py",
        "scripts/api_commercial_*.py",
        "scripts/final_*.py",
        "scripts/_commercial_common.py",
        "config/commercial_*.json",
        "config/media_social_*.json",
        "config/ad_campaigns_*.json",
        "config/crm_pipeline_*.json",
        "config/analytics_events.json",
        ".github/workflows/commercial-draft-factory.yml",
        ".github/workflows/media-social-calendar.yml",
        ".github/workflows/site-commercial-verify.yml",
        ".github/workflows/final-launch-control.yml",
    ]:
        paths.extend(sorted(ROOT.glob(pattern)))
    return paths


def scan_code_surface() -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    constructs = [re.compile(p, re.IGNORECASE) for p in FORBIDDEN_CONSTRUCTS]
    literals = [re.compile(p, re.IGNORECASE) for p in FORBIDDEN_FLAG_LITERALS]
    for path in _launch_surface():
        rel = path.relative_to(ROOT).as_posix()
        if rel in SCANNER_ALLOWLIST:
            continue
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for rx in constructs + literals:
            m = rx.search(text)
            if m:
                violations.append({"file": rel, "pattern": rx.pattern, "match": m.group(0)[:60]})
    return violations


def scan_draft_flags(day: str) -> tuple[int, list[dict[str, Any]]]:
    queue = COMMERCIAL_OUTPUTS / day / "draft_queue.jsonl"
    drafts = read_jsonl(queue)
    violations: list[dict[str, Any]] = []
    for d in drafts:
        if d.get("send_allowed") is not False:
            violations.append(
                {
                    "draft_id": d.get("draft_id"),
                    "flag": "send_allowed",
                    "value": d.get("send_allowed"),
                }
            )
        if d.get("external_send_blocked") is not True:
            violations.append(
                {
                    "draft_id": d.get("draft_id"),
                    "flag": "external_send_blocked",
                    "value": d.get("external_send_blocked"),
                }
            )
        if d.get("requires_founder_approval") is not True:
            violations.append(
                {
                    "draft_id": d.get("draft_id"),
                    "flag": "requires_founder_approval",
                    "value": d.get("requires_founder_approval"),
                }
            )
        if d.get("no_auto_send") is not True:
            violations.append(
                {
                    "draft_id": d.get("draft_id"),
                    "flag": "no_auto_send",
                    "value": d.get("no_auto_send"),
                }
            )
    return len(drafts), violations


def run(day: str) -> dict[str, Any]:
    code_violations = scan_code_surface()
    draft_count, flag_violations = scan_draft_flags(day)
    passed = not code_violations and not flag_violations
    return {
        "date": day,
        "passed": passed,
        "drafts_checked": draft_count,
        "code_violations": code_violations,
        "flag_violations": flag_violations,
        "files_scanned": len(_launch_surface()),
        "guarantee": "No external send capability present. AI drafts; founder sends manually.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the commercial safety audit.")
    parser.add_argument("--date", default=today_str())
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    report = run(args.date)
    out = Path(args.out) if args.out else COMMERCIAL_OUTPUTS / args.date / "safety_audit.json"
    write_json(out, report)

    if report["passed"]:
        print(
            f"SAFETY AUDIT: PASS — {report['drafts_checked']} drafts, "
            f"{report['files_scanned']} files scanned, 0 violations."
        )
        return 0
    print("SAFETY AUDIT: FAIL", file=sys.stderr)
    for v in report["code_violations"]:
        print(f"  code: {v['file']} :: {v['pattern']}", file=sys.stderr)
    for v in report["flag_violations"][:10]:
        print(f"  flag: {v}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
