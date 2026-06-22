#!/usr/bin/env python3
"""
verify_no_auto_external_send.py

Scans the Python source tree for patterns that would send outreach, email,
WhatsApp, or SMS without a human approval gate. Fails the build if any
ungated send is detected.

Approved safe patterns:
- Draft creation (create_draft, draft_to_file)
- Functions whose name contains "safe" and only write files
- Known gateway modules that are expected to contain gated send functions
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# These patterns are forbidden outside known gateway modules.
FORBIDDEN_PATTERNS = [
    re.compile(r"\bauto_send\s*=\s*(True|1|\"yes\"|\"true\"|\'yes\'|\'true\')"),
    re.compile(r"\brequests\.post\s*\(.*api\.whatsapp\.com", re.IGNORECASE),
    re.compile(r"\brequests\.post\s*\(.*twilio\.com", re.IGNORECASE),
]

# Direct paths / prefixes where the existence of send() functions is allowed
# because they are behind explicit approval/env gates.
GATEWAY_ALLOWLIST = {
    "api/routers/autonomous.py",
    "api/routers/email_send.py",
    "api/routers/whatsapp_client_os.py",
    "auto_client_acquisition/email/gmail_send.py",
    "auto_client_acquisition/email/transactional.py",
    "integrations/email.py",
    "integrations/whatsapp.py",
    "scripts/email/create_gmail_drafts_safe.py",
    "scripts/approve_outreach_draft.py",
    "scripts/reject_outreach_draft.py",
    "scripts/verify_no_auto_external_send.py",
}

GATEWAY_ALLOWLIST_PREFIXES = (
    "docs/",
    "tests/",
)

# Scripts that directly generate outreach must not contain ungated send_* calls.
STRICT_NO_SEND_SCRIPTS_PREFIXES = [
    "scripts/revenue/",
    "scripts/command_room/",
    "scripts/launch/",
    "scripts/outbound/",
]


def is_allowlisted(rel_path: str) -> bool:
    if rel_path in GATEWAY_ALLOWLIST:
        return True
    return any(rel_path.startswith(prefix) for prefix in GATEWAY_ALLOWLIST_PREFIXES)


def scan_strict_scripts() -> list[str]:
    bad: list[str] = []
    for prefix in STRICT_NO_SEND_SCRIPTS_PREFIXES:
        d = REPO_ROOT / prefix
        if not d.exists():
            continue
        for py in d.rglob("*.py"):
            rel = py.relative_to(REPO_ROOT).as_posix()
            if is_allowlisted(rel):
                continue
            text = py.read_text(encoding="utf-8", errors="ignore")
            # Any send_* call outside allowlist is forbidden.
            for pat in [
                re.compile(r"\bsend_email\s*\("),
                re.compile(r"\bsend_whatsapp\s*\("),
                re.compile(r"\bsend_sms\s*\("),
                re.compile(r"\bsend_template\s*\("),
                re.compile(r"\bsmtplib\.SMTP\b"),
            ]:
                for m in pat.finditer(text):
                    bad.append(f"{rel}:{m.start()}: matched {pat.pattern}")
            for pat in FORBIDDEN_PATTERNS:
                for m in pat.finditer(text):
                    bad.append(f"{rel}:{m.start()}: matched {pat.pattern}")
    return bad


def scan_auto_send_flags() -> list[str]:
    bad: list[str] = []
    scan_dirs = [
        REPO_ROOT / "scripts",
        REPO_ROOT / "api",
        REPO_ROOT / "core",
        REPO_ROOT / "dealix",
        REPO_ROOT / "auto_client_acquisition",
        REPO_ROOT / "autonomous_growth",
        REPO_ROOT / "integrations",
        REPO_ROOT / "company",
    ]
    for d in scan_dirs:
        if not d.exists():
            continue
        for py in d.rglob("*.py"):
            rel = py.relative_to(REPO_ROOT).as_posix()
            if is_allowlisted(rel):
                continue
            text = py.read_text(encoding="utf-8", errors="ignore")
            pat = re.compile(r"\bauto_send\s*=\s*(True|1|\"yes\"|\"true\"|\'yes\'|\'true\')")
            for m in pat.finditer(text):
                bad.append(f"{rel}:{m.start()}: ungated auto_send=True")
    return bad


def check_env_flags() -> list[str]:
    flags = {
        "EXTERNAL_SEND_ENABLED": ["false", "0"],
        "EMAIL_SEND_ENABLED": ["false", "0"],
        "WHATSAPP_SEND_ENABLED": ["false", "0"],
        "WHATSAPP_ALLOW_LIVE_SEND": ["false", "0"],
        "SMS_SEND_ENABLED": ["false", "0"],
        "OUTBOUND_MODE": ["draft_only"],
    }
    errors: list[str] = []
    for key, safe in flags.items():
        val = os.environ.get(key, "").strip().lower()
        if val and val not in [s.lower() for s in safe]:
            errors.append(
                f"{key}={val!r} is not a safe default for an ungated run. "
                f"Expected one of {safe}."
            )
    return errors


def main() -> int:
    print("No Auto External Send Check")
    print("=" * 50)
    code_errors = scan_strict_scripts() + scan_auto_send_flags()
    env_errors = check_env_flags()

    for e in code_errors:
        print(f"❌ CODE: {e}")
    for e in env_errors:
        print(f"❌ ENV: {e}")

    if not code_errors and not env_errors:
        print("✅ No ungated external-send patterns found.")
        print("✅ External-send env flags are safe.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
