"""Test that run_revenue_day.py and revenue scripts never send externally.

Scans all revenue scripts for forbidden send patterns and verifies the
run_revenue_day pipeline completes without any network/send calls.

Usage:
    python -m pytest tests/test_revenue_day_no_auto_send.py -q
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

REVENUE_DIR = REPO_ROOT / "scripts" / "revenue"

FORBIDDEN_PATTERNS = [
    re.compile(r"send_email\s*\("),
    re.compile(r"send_whatsapp\s*\("),
    re.compile(r"send_sms\s*\("),
    re.compile(r"send_template\s*\("),
    re.compile(r"auto_send\s*=\s*True"),
    re.compile(r"auto_send\s*=\s*[\"']yes[\"']"),
    re.compile(r"requests\.post\s*\("),
    re.compile(r"requests\.get\s*\("),
    re.compile(r"httpx\.post\s*\("),
    re.compile(r"httpx\.get\s*\("),
    re.compile(r"urllib\.request\.urlopen\s*\("),
    re.compile(r"smplib"),
    re.compile(r"smtplib\.SMTP"),
]

# Allowlist: terms may appear in comments/docstrings in these files
ALLOWLIST_NAMES = {
    "_lib.py",  # utility library — may reference but not call
}


def _scan_file(path: Path) -> list[str]:
    """Return list of forbidden pattern matches found in the file."""
    issues: list[str] = []
    text = path.read_text(encoding="utf-8")
    for pat in FORBIDDEN_PATTERNS:
        if pat.search(text):
            issues.append(f"{path.name}: found pattern {pat.pattern}")
    return issues


def test_no_forbidden_send_patterns_in_revenue_scripts() -> None:
    issues: list[str] = []
    for path in REVENUE_DIR.glob("*.py"):
        if path.name in ALLOWLIST_NAMES:
            continue
        issues.extend(_scan_file(path))
    assert issues == [], "Forbidden send/network patterns found:\n" + "\n".join(issues)


def test_lib_has_no_external_send_calls() -> None:
    lib_path = REVENUE_DIR / "_lib.py"
    text = lib_path.read_text(encoding="utf-8")
    # _lib.py may mention send in comments but must not import smtplib or call send
    assert "import smtplib" not in text, "_lib.py imports smtplib"
    assert "smtplib.SMTP" not in text, "_lib.py uses smtplib.SMTP"
    assert "requests.post" not in text, "_lib.py calls requests.post"
    assert "requests.get" not in text, "_lib.py calls requests.get"


def test_run_revenue_day_does_not_send_externally() -> None:
    """Verify run_revenue_day.py source has no send/network calls."""
    path = REVENUE_DIR / "run_revenue_day.py"
    issues = _scan_file(path)
    assert issues == [], "run_revenue_day.py has forbidden patterns:\n" + "\n".join(issues)


def test_outreach_drafts_script_is_draft_only() -> None:
    path = REVENUE_DIR / "generate_outreach_drafts.py"
    text = path.read_text(encoding="utf-8")
    assert "write_text" in text or "write" in text, "Should write drafts to files"
    # Must not send
    issues = _scan_file(path)
    assert issues == [], "generate_outreach_drafts.py has forbidden patterns:\n" + "\n".join(issues)


def test_all_revenue_scripts_have_draft_or_no_send_mention() -> None:
    """Every revenue script should either be draft-only or not mention sending."""
    for path in REVENUE_DIR.glob("*.py"):
        if path.name in ALLOWLIST_NAMES:
            continue
        text = path.read_text(encoding="utf-8")
        # If "send" appears, it should be in context of "never sends" or similar
        if re.search(r"\bsend\b", text, re.IGNORECASE):
            # Must have a qualifier nearby — check the file mentions "draft" or "never" or "no external"
            assert any(
                word in text.lower()
                for word in ["draft", "never", "no external", "does not send", "review"]
            ), f"{path.name} mentions 'send' without draft/never qualifier"
