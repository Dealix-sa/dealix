"""Contract: the Commercial Launch OS contains NO external-send code.

This test names the blocked outbound-send terms on purpose in order to assert
they do not appear in this OS's executable surface. It is allow-listed in the
safety audit's SELF_REFERENTIAL set for exactly that reason.
"""

from __future__ import annotations

from pathlib import Path

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "scripts"))

import commercial_launch_core as core
import commercial_safety_audit as audit

REPO_ROOT = Path(__file__).resolve().parents[1]

# Outbound-send signatures that must never appear in our executable files.
FORBIDDEN_IN_CODE = [
    "smtplib",
    "sendgrid",
    "mailgun",
    "postmark",
    "ses.send",
    "twilio.messages.create",
    "auto_send",
    "bulk_send",
]


def _my_code_files() -> list[Path]:
    files = [REPO_ROOT / "scripts" / n for n in audit.MY_SCRIPTS]
    wf = REPO_ROOT / ".github" / "workflows" / "commercial-draft-factory.yml"
    if wf.exists():
        files.append(wf)
    return [f for f in files if f.exists()]


def test_no_external_send_imports_in_code():
    # commercial_safety_audit.py legitimately names the patterns to detect them.
    import re
    skip = {"commercial_safety_audit.py"}
    for f in _my_code_files():
        if f.name in skip:
            continue
        text = f.read_text(encoding="utf-8").lower()
        for term in FORBIDDEN_IN_CODE:
            # Word-boundary aware so legitimate names like `no_auto_send` (which
            # contains `auto_send`) are not false positives.
            rx = re.compile(r"\b" + re.escape(term.lower()) + r"\b")
            assert not rx.search(text), f"{f.name} contains forbidden term {term}"


def test_safety_audit_passes_on_clean_repo():
    report = audit.run_audit(date_str="2026-01-01")
    assert report["pass"] is True
    assert report["blocked_terms_found"] == 0
    assert report["violations"] == []


def test_safety_audit_flags_injected_enablement(tmp_path):
    # Sanity: the enablement detector actually fires on a bad line.
    import re
    rx = [re.compile(p, re.IGNORECASE) for p in audit.ENABLEMENT_PATTERNS]
    bad = "send_allowed: true"
    assert any(r.search(bad) for r in rx)
    good = "send_allowed: false"
    assert not any(r.search(good) for r in rx)
