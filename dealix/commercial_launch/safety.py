"""Safety audit for the Commercial Launch OS.

Two jobs:
  1. Static scan of the commercial-launch source + generated artifacts for any
     active external-send / automation / scraping code.
  2. Invariant check on every generated draft (send_allowed=False, etc.).

The audit FAILS (non-zero) if anything that could send externally is found.

Forbidden patterns are assembled from fragments so the audit's own denylist
does not flag itself. Lines tagged with the marker below are skipped.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dealix.commercial_launch.engine import (
    ROOT,
    iter_jsonl,
    validate_draft_invariants,
)

ALLOW_MARKER = "safety-audit-allow"  # lines containing this are skipped

# Patterns that indicate ACTIVE external sending / automation / scraping.
# Each is built from raw-string fragments so the literal token does not appear
# verbatim in this denylist and self-flag. # safety-audit-allow
ACTIVE_SEND_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("smtp_client", re.compile(r"\bsmtp" + r"lib\b|\bSMTP" + r"\s*\(", re.I)),  # safety-audit-allow
    ("send_message", re.compile(r"\.send_" + r"message\s*\(", re.I)),  # safety-audit-allow
    ("send_mail", re.compile(r"\bsend_" + r"mail\s*\(", re.I)),  # safety-audit-allow
    ("send" + "grid", re.compile(r"\bsend" + r"grid\b", re.I)),  # safety-audit-allow
    ("mail" + "gun", re.compile(r"\bmail" + r"gun\b", re.I)),  # safety-audit-allow
    ("twilio_send", re.compile(r"twilio[^\n]*\.(create|" + r"send)\s*\(", re.I)),  # safety-audit-allow
    ("whatsapp_send", re.compile(r"whats" + r"app[^\n]*\.(send|create)\s*\(", re.I)),  # safety-audit-allow
    ("linked" + "in_automation", re.compile(r"linked" + r"in[ _-]?(automat|auto_connect|auto_message)", re.I)),  # safety-audit-allow
    ("selenium_outreach", re.compile(r"\bsele" + r"nium\b", re.I)),  # safety-audit-allow
    ("playwright_outreach", re.compile(r"\bplay" + r"wright\b", re.I)),  # safety-audit-allow
    ("send_allowed_true", re.compile(r"send_allowed" + r"[\"']?\s*[:=]\s*[Tt]rue")),  # safety-audit-allow
    ("external_send_blocked_false", re.compile(r"external_send_blocked" + r"[\"']?\s*[:=]\s*[Ff]alse")),  # safety-audit-allow
    ("post_allowed_true", re.compile(r"post_allowed" + r"[\"']?\s*[:=]\s*[Tt]rue")),  # safety-audit-allow
    ("external_post_blocked_false", re.compile(r"external_post_blocked" + r"[\"']?\s*[:=]\s*[Ff]alse")),  # safety-audit-allow
    ("scheduler_api", re.compile(r"\b(buff" + r"er|hoot" + r"suite|spro" + r"ut|late" + r"r_com)\b\.?\w*\s*\(", re.I)),  # safety-audit-allow
]

# requests.post to an *external send* endpoint (not generic requests usage).
_REQUESTS_SEND = re.compile(
    r"requests\.post\([^)]*(api\.|/send|/messages|/mail|outreach|notify)", re.I
)


@dataclass
class SafetyFinding:
    file: str
    line: int
    rule: str
    snippet: str


@dataclass
class SafetyReport:
    passed: bool = True
    scanned_files: int = 0
    findings: list[SafetyFinding] = field(default_factory=list)
    draft_violations: list[dict[str, Any]] = field(default_factory=list)
    drafts_checked: int = 0
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "scanned_files": self.scanned_files,
            "findings": [f.__dict__ for f in self.findings],
            "draft_violations": self.draft_violations,
            "drafts_checked": self.drafts_checked,
            "notes": self.notes,
        }


def _scan_targets(root: Path) -> list[Path]:
    targets: list[Path] = []
    targets += sorted((root / "scripts").glob("commercial_*.py"))
    pkg = root / "dealix" / "commercial_launch"
    if pkg.exists():
        targets += sorted(pkg.glob("*.py"))
    # generated artifacts
    out = root / "outputs" / "commercial_launch"
    if out.exists():
        targets += sorted(out.glob("**/*.jsonl"))
    return targets


def scan_files(root: Path | None = None) -> SafetyReport:
    r = root or ROOT
    report = SafetyReport()
    for path in _scan_targets(r):
        report.scanned_files += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if ALLOW_MARKER in line:
                continue
            for rule, pattern in ACTIVE_SEND_PATTERNS:
                if pattern.search(line):
                    report.findings.append(
                        SafetyFinding(file=str(path.relative_to(r)), line=i, rule=rule, snippet=line.strip()[:160])
                    )
            if _REQUESTS_SEND.search(line):
                report.findings.append(
                    SafetyFinding(file=str(path.relative_to(r)), line=i, rule="requests_external_send", snippet=line.strip()[:160])
                )
    if report.findings:
        report.passed = False
    return report


def audit_outputs_dir(run_date: str, base_dir: Path | None = None, root: Path | None = None) -> SafetyReport:
    """Full audit: static scan + invariant check on a day's draft queue."""
    r = root or ROOT
    report = scan_files(r)
    out = (base_dir or (r / "outputs" / "commercial_launch")) / run_date
    dq = out / "draft_queue.jsonl"
    for draft in iter_jsonl(dq):
        report.drafts_checked += 1
        problems = validate_draft_invariants(draft)
        if problems:
            report.draft_violations.append({"draft_id": draft.get("draft_id"), "problems": problems})

    # Social & media queue (review-only marketing posts).
    sq = out / "social_queue.jsonl"
    if sq.exists():
        from dealix.commercial_launch.social import validate_post_invariants

        for post in iter_jsonl(sq):
            report.drafts_checked += 1
            problems = validate_post_invariants(post)
            if problems:
                report.draft_violations.append({"post_id": post.get("post_id"), "problems": problems})

    if report.draft_violations:
        report.passed = False
    if report.passed:
        report.notes.append("No active external-send/post code found. All drafts and posts are review-only.")
    return report


def write_safety_audit(report: SafetyReport, run_date: str, base_dir: Path | None = None, root: Path | None = None) -> str:
    r = root or ROOT
    out = (base_dir or (r / "outputs" / "commercial_launch")) / run_date
    out.mkdir(parents=True, exist_ok=True)
    path = out / "safety_audit.json"
    path.write_text(json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)
