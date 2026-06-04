"""No-External-Send Safety Audit for the Commercial Launch OS.

Context-aware: it flags *executable sending code* and *unsafe data flags*, NOT
policy prose. Markdown docs are allowed to say "No SMTP / No WhatsApp" because
that is the policy. Generic `requests` usage is not blocked unless it is a
sending pattern.

Fails (pass=False) if it finds:
  * real send code (smtplib, sendgrid, mailgun, SES/Twilio sends, .sendmail, ...)
  * outreach automation tokens in code (auto_send, bulk_send, auto_connect, ...)
  * unsafe draft flags (send_allowed:true, external_send_blocked:false, ...)
  * forbidden statuses (sent, auto_sent, queued_for_send, ...)
  * a draft record missing a mandatory safety flag
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date as date_cls
from pathlib import Path
from typing import Any

# Run both as `python scripts/<file>.py` and `python -m scripts.<file>`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.commercial_launch_core import (
    MANDATORY_FLAGS,
    OUTPUT_ROOT,
    REPO_ROOT,
)

SELF_NAME = "commercial_safety_audit.py"

# This OS's own tests (explicit allowlist — avoids scanning unrelated commercial tests)
OS_TEST_FILES = [
    "test_commercial_generate_400_drafts.py",
    "test_commercial_safety_audit.py",
    "test_commercial_launch_readiness.py",
    "test_commercial_no_external_send.py",
    "test_commercial_quality_gate.py",
    "test_commercial_compliance_gate.py",
    "test_commercial_outputs_schema.py",
    "test_commercial_founder_review_report.py",
    "test_commercial_seed_leads_validate.py",
]
# Output files that legitimately echo blocked terms (audit/readiness reports) — never scan.
SKIP_OUTPUT_NAMES = {"safety_audit.json", "readiness.json"}

# Executable sending code (applies to .py / .yml / .json — not to prose .md)
CODE_PATTERNS = [
    r"import\s+smtplib",
    r"from\s+smtplib",
    r"smtplib\.",
    r"\.sendmail\s*\(",
    r"server\.send_message\s*\(",
    r"\bsendgrid\b",
    r"\bmailgun\b",
    r"postmark(app)?\.",
    r"ses\.send_email\s*\(",
    r"twilio[\s\S]{0,40}messages\.create",
    r"selenium\.webdriver",
    r"playwright[\s\S]{0,20}\.goto\s*\([\s\S]{0,60}contact",
]

# Outreach automation tokens in code (underscored identifiers; prose uses hyphens)
AUTOMATION_PATTERNS = [
    r"(?<!no_)auto_send\b",
    r"\bbulk_send\b",
    r"\bauto_connect\b",
    r"\bauto_message\b",
    r"\bmass_outreach\b",
    r"\bpush_send\b",
    r"\bwhatsapp_send\b",
    r"whatsapp_api_outbound",
    r"\blinkedin_automation\b",
    r"\binbox_automation\b",
]

# Unsafe data flags / forbidden statuses (apply everywhere)
FLAG_PATTERNS = [
    r'"send_allowed"\s*:\s*true',
    r'"external_send_blocked"\s*:\s*false',
    r'"no_auto_send"\s*:\s*false',
    r'"requires_founder_approval"\s*:\s*false',
    r'"status"\s*:\s*"(sent|auto_sent|queued_for_send|smtp_ready|whatsapp_ready|linkedin_auto_ready)"',
]


def _scan_targets() -> list[Path]:
    targets: list[Path] = []
    targets += sorted((REPO_ROOT / "scripts").glob("commercial_*.py"))
    for name in OS_TEST_FILES:
        p = REPO_ROOT / "tests" / name
        if p.exists():
            targets.append(p)
    targets += sorted((REPO_ROOT / "config").glob("commercial_*.json"))
    targets += sorted((REPO_ROOT / "docs" / "commercial-launch").rglob("*.md"))
    wf = REPO_ROOT / ".github" / "workflows" / "commercial-draft-factory.yml"
    if wf.exists():
        targets.append(wf)
    if OUTPUT_ROOT.exists():
        targets += sorted(OUTPUT_ROOT.rglob("*.jsonl"))
        targets += [
            p for p in sorted(OUTPUT_ROOT.rglob("*.json")) if p.name not in SKIP_OUTPUT_NAMES
        ]
    return [t for t in targets if t.name != SELF_NAME]


def _check_draft_records(path: Path, violations: list[dict]) -> None:
    """Structurally validate every draft record in a draft_queue jsonl."""
    if path.name != "draft_queue.jsonl":
        return
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        for flag, expected in MANDATORY_FLAGS.items():
            if rec.get(flag) != expected:
                violations.append(
                    {
                        "file": str(path.relative_to(REPO_ROOT)),
                        "line": i,
                        "type": "draft_flag",
                        "detail": f"{flag}={rec.get(flag)} (expected {expected})",
                    }
                )


def run_safety_audit() -> dict[str, Any]:
    targets = _scan_targets()
    violations: list[dict] = []
    blocked_terms: list[str] = []
    files_scanned = 0

    for path in targets:
        files_scanned += 1
        text = path.read_text(encoding="utf-8", errors="ignore")
        is_prose = path.suffix == ".md"

        patterns = list(FLAG_PATTERNS)
        if not is_prose:
            patterns += CODE_PATTERNS + AUTOMATION_PATTERNS

        for pat in patterns:
            for m in re.finditer(pat, text, re.IGNORECASE):
                line_no = text[: m.start()].count("\n") + 1
                snippet = m.group(0)
                blocked_terms.append(snippet)
                violations.append(
                    {
                        "file": str(path.relative_to(REPO_ROOT)),
                        "line": line_no,
                        "type": "pattern",
                        "detail": snippet,
                    }
                )
        if path.suffix == ".jsonl":
            _check_draft_records(path, violations)

    passed = len(violations) == 0
    return {
        "schema_version": "1.0",
        "run_date": date_cls.today().isoformat(),
        "pass": passed,
        "files_scanned": files_scanned,
        "violations": violations,
        "warnings": [] if passed else ["Resolve all violations before any manual outreach."],
        "blocked_terms_found": sorted(set(blocked_terms)),
        "recommended_fix": (
            "None — no external-send capability detected."
            if passed
            else "Remove send/automation code and reset draft flags to the safe defaults."
        ),
        "doctrine": "AI drafts only. Founder approves. No external sending.",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="No-external-send safety audit.")
    ap.add_argument("--out", default=None, help="Write safety_audit.json to this path.")
    args = ap.parse_args(argv)
    report = run_safety_audit()

    if args.out:
        out = Path(args.out)
    else:
        dirs = (
            sorted([p for p in OUTPUT_ROOT.glob("*") if p.is_dir()]) if OUTPUT_ROOT.exists() else []
        )
        out = (dirs[-1] / "safety_audit.json") if dirs else (OUTPUT_ROOT / "safety_audit.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "pass": report["pass"],
                "files_scanned": report["files_scanned"],
                "violations": len(report["violations"]),
                "out": str(out),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
