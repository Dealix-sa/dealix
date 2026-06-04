#!/usr/bin/env python3
"""Dealix Commercial Launch — Safety Audit.

Scans the commercial-launch surface for any indicator of external sending or
outbound automation. Fails (non-zero exit / pass=False) if a blocked term is
found in scanned files, or if any generated draft has unsafe flags.

The audit is context-aware: the bare word ``requests`` is NOT blocked (it may
be used internally); only outbound-send signatures are.

Usage:
    python scripts/commercial_safety_audit.py [--date YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import commercial_launch_core as core  # noqa: E402

REPO_ROOT = core.REPO_ROOT

# ── Tiered detection ───────────────────────────────────────────────────────
# Tier 1 — ENABLEMENT patterns. A real attempt to switch on sending. ALWAYS a
# hard violation in ANY file type (code, docs, config). These never appear in
# legitimate prose, so they are safe to fail CI on everywhere.
ENABLEMENT_PATTERNS = [
    r"send_allowed\s*[:=]\s*true",
    r"external_send_blocked\s*[:=]\s*false",
    r"no_auto_send\s*[:=]\s*false",
    r"requires_founder_approval\s*[:=]\s*false",
]

# Tier 2 — CODE patterns. Outbound-send code signatures. Hard violation when
# found in executable files (.py/.yml/.yaml); recorded as a warning when found
# in prose (docs may name them inside prohibitions, e.g. "No SMTP").
CODE_PATTERNS = [
    r"\bsmtplib\b",
    r"\bsmtp\b",
    r"\bsend_mail\b",
    r"\bsend_email\b",
    r"\bmailgun\b",
    r"\bsendgrid\b",
    r"\bpostmark\b",
    r"ses\.send",
    r"twilio\.messages\.create",
    r"whatsapp[_\s]?send",
    r"whatsapp\s+api\s+outbound",
    r"linkedin\s+automation",
    r"auto[_\s]?connect",
    r"auto[_\s]?message",
    r"\bselenium\b",
    r"\bplaywright\b",
    r"browser\s+automation",
    r"\bauto_send\b",
    r"\bbulk_send\b",
    r"mass\s+outreach",
    r"inbox\s+automation",
    r"crm\s+push-?send",
    r"requests\.post\([^)]*(send|outreach|message|mail)",
]

CODE_EXTS = {".py", ".yml", ".yaml"}

# This audit script and its tests legitimately NAME the blocked terms in order
# to detect them; they are allow-listed from being treated as violations.
SELF_REFERENTIAL = {
    "scripts/commercial_safety_audit.py",
    "tests/test_commercial_safety_audit.py",
    "tests/test_commercial_no_external_send.py",
    "docs/commercial-launch/06_CHANNEL_POLICY.md",
    "docs/commercial-launch/07_COMPLIANCE_AND_SAFETY_GATES.md",
    "config/commercial_compliance_gates.json",
    "config/commercial_channels.json",
}

# Explicit surface owned by the Commercial Launch OS. We scan ONLY these
# scripts/tests (not every pre-existing file whose name contains "commercial")
# so the audit never false-flags unrelated modules.
MY_SCRIPTS = {
    "commercial_launch_core.py",
    "commercial_generate_400_drafts.py",
    "commercial_safety_audit.py",
    "commercial_founder_review_report.py",
    "commercial_score_drafts.py",
    "commercial_quality_gate.py",
    "commercial_compliance_gate.py",
    "commercial_seed_leads_validate.py",
    "commercial_launch_readiness.py",
    "commercial_metrics_summary.py",
}
MY_TESTS = {
    "test_commercial_generate_400_drafts.py",
    "test_commercial_safety_audit.py",
    "test_commercial_launch_readiness.py",
    "test_commercial_no_external_send.py",
    "test_commercial_quality_gate.py",
    "test_commercial_compliance_gate.py",
    "test_commercial_outputs_schema.py",
}

# Config files owned by this OS.
MY_CONFIGS = set(core.CONFIG_FILES.values())


def _iter_files() -> list[Path]:
    files: list[Path] = []
    # Owned scripts
    for name in MY_SCRIPTS:
        p = REPO_ROOT / "scripts" / name
        if p.exists():
            files.append(p)
    # Owned tests
    for name in MY_TESTS:
        p = REPO_ROOT / "tests" / name
        if p.exists():
            files.append(p)
    # Owned config
    for name in MY_CONFIGS:
        p = REPO_ROOT / "config" / name
        if p.exists():
            files.append(p)
    # All commercial-launch docs
    docs = REPO_ROOT / "docs" / "commercial-launch"
    if docs.is_dir():
        files.extend(docs.rglob("*.md"))
    # The workflow
    wf = REPO_ROOT / ".github" / "workflows" / "commercial-draft-factory.yml"
    if wf.exists():
        files.append(wf)
    return sorted(set(files))


def scan_files() -> dict:
    enable_rx = [(p, re.compile(p, re.IGNORECASE)) for p in ENABLEMENT_PATTERNS]
    code_rx = [(p, re.compile(p, re.IGNORECASE)) for p in CODE_PATTERNS]
    violations = []
    warnings = []
    scanned = []
    for f in _iter_files():
        rel = f.relative_to(REPO_ROOT).as_posix()
        scanned.append(rel)
        allowlisted = rel in SELF_REFERENTIAL
        is_code = f.suffix in CODE_EXTS
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            # Tier 1 — enablement is a hard violation everywhere (unless the
            # audit/test files that legitimately name the pattern to detect it).
            for raw, rx in enable_rx:
                if rx.search(line):
                    rec = {"file": rel, "line": lineno, "pattern": raw,
                           "tier": "enablement", "snippet": line.strip()[:160]}
                    (warnings if allowlisted else violations).append(rec)
            # Tier 2 — code send-signatures: violation in code, warning in prose.
            for raw, rx in code_rx:
                if rx.search(line):
                    rec = {"file": rel, "line": lineno, "pattern": raw,
                           "tier": "code", "snippet": line.strip()[:160]}
                    if allowlisted or not is_code:
                        warnings.append(rec)
                    else:
                        violations.append(rec)
    return {"scanned": scanned, "violations": violations, "warnings": warnings}


def audit_drafts(date_str: str) -> dict:
    """Verify the day's draft_queue (if present) carries safe flags only."""
    out = core.output_dir_for(date_str)
    path = out / "draft_queue.jsonl"
    issues = []
    checked = 0
    if path.exists():
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                checked += 1
                if d.get("send_allowed") is not False:
                    issues.append(f"{d.get('draft_id')}: send_allowed not False")
                if d.get("external_send_blocked") is not True:
                    issues.append(f"{d.get('draft_id')}: external_send_blocked not True")
                if d.get("no_auto_send") is not True:
                    issues.append(f"{d.get('draft_id')}: no_auto_send not True")
                if d.get("requires_founder_approval") is not True:
                    issues.append(f"{d.get('draft_id')}: requires_founder_approval not True")
                if d.get("status") in core.FORBIDDEN_STATUSES:
                    issues.append(f"{d.get('draft_id')}: forbidden status {d.get('status')}")
    return {"drafts_checked": checked, "draft_flag_issues": issues}


def run_audit(date_str: str | None = None, out_dir: Path | None = None) -> dict:
    date_str = date_str or core.today_str()
    file_scan = scan_files()
    draft_scan = audit_drafts(date_str)
    passed = not file_scan["violations"] and not draft_scan["draft_flag_issues"]
    report = {
        "pass": passed,
        "date": date_str,
        "files_scanned": len(file_scan["scanned"]),
        "blocked_terms_found": len(file_scan["violations"]),
        "violations": file_scan["violations"],
        "warnings": file_scan["warnings"],
        "drafts_checked": draft_scan["drafts_checked"],
        "draft_flag_issues": draft_scan["draft_flag_issues"],
        "recommended_fix": (
            "None — no external-send indicators found."
            if passed else
            "Remove the flagged outbound-send code/term. This repository is "
            "draft-only; no SMTP/WhatsApp/LinkedIn automation/auto-submit is allowed."
        ),
    }
    target_dir = out_dir or core.output_dir_for(date_str)
    target_dir.mkdir(parents=True, exist_ok=True)
    with (target_dir / "safety_audit.json").open("w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Commercial launch safety audit.")
    parser.add_argument("--date", default=None)
    args = parser.parse_args(argv)
    report = run_audit(date_str=args.date)
    print(f"Safety audit: pass={report['pass']} files_scanned={report['files_scanned']} "
          f"violations={report['blocked_terms_found']} warnings={len(report['warnings'])} "
          f"drafts_checked={report['drafts_checked']}")
    for v in report["violations"]:
        print(f"  VIOLATION {v['file']}:{v['line']} [{v['pattern']}] {v['snippet']}")
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
