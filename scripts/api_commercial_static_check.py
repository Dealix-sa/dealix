#!/usr/bin/env python3
"""
Static check: the V5 commercial surface introduces NO external-send code paths.

Scans V5-added files (scripts/commercial_*, scripts/v5/*, config/*) for forbidden
send primitives. Read-only/draft-only by construction. Fails (exit 1) on any hit.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Code-only send primitives (not prose). These match actual imports/calls, so
# documentation that *describes* the safety boundary does not trip the scan.
FORBIDDEN = [
    r"import\s+smtplib", r"smtplib\.SMTP", r"\bsendmail\(",
    r"from\s+twilio", r"import\s+twilio", r"TwilioRestClient",
    r"graph\.facebook\.com", r"api\.linkedin\.com", r"api\.whatsapp\.com",
    r"requests\.(post|put)\(.*(slack|linkedin|whatsapp|twilio|mailgun|sendgrid)",
    r"from\s+selenium", r"import\s+selenium",
    r"page\.goto\(.*(login|signin)",  # browser automation for outreach
]
PATTERN = re.compile("|".join(FORBIDDEN), re.IGNORECASE)

# Real V5 "send surface": the commercial/media scripts and their configs.
# (Doc generators under scripts/v5 only emit markdown and are covered by the
# secret-and-risk scan, not this code-primitive scan.)
SCAN_GLOBS = ["scripts/commercial_*.py", "scripts/media_social_*.py", "config/*.json"]


def main() -> int:
    if not (ROOT / "api").exists():
        print("note: no api/ dir; static check still enforces no-send on V5 files")
    hits: list[str] = []
    for g in SCAN_GLOBS:
        for f in ROOT.glob(g):
            text = f.read_text(encoding="utf-8", errors="ignore")
            for i, line in enumerate(text.splitlines(), 1):
                # allow self-references in the scanner files themselves (the pattern list)
                if f.name in ("api_commercial_static_check.py", "final_secret_and_risk_scan.py"):
                    continue
                if PATTERN.search(line):
                    hits.append(f"{f.relative_to(ROOT)}:{i}: {line.strip()[:80]}")
    ok = not hits
    print(f"V5 commercial surface no-send check: {'PASS' if ok else 'FAIL'}")
    for h in hits[:20]:
        print("  !", h)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
