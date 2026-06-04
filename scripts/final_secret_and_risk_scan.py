#!/usr/bin/env python3
"""Scan the Startup OS additions for committed secrets and risky patterns.

Scope (by default): the files this initiative adds/owns — config/, data/,
docs/ (the OS trees), scripts/commercial_*, scripts/media_social_*,
scripts/site_launch_*, scripts/api_commercial_*, scripts/final_*,
scripts/startup_os_*, scripts/lib/startup_os_common.py, and the new workflows.
Flags real-looking secrets. Example/placeholder values are allowed.

Read-only. Exit non-zero if a real secret is found.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PATTERNS = {
    "openai_key": re.compile(r"sk-[A-Za-z0-9]{32,}"),
    "anthropic_key": re.compile(r"sk-ant-[A-Za-z0-9_\-]{32,}"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "aws_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "slack_token": re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    "twilio_sid": re.compile(r"AC[0-9a-fA-F]{32}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "smtp_password": re.compile(r"(?i)smtp[_-]?pass(word)?\s*[=:]\s*['\"]?[^\s'\"]{6,}"),
    "generic_secret_assign": re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[=:]\s*['\"][A-Za-z0-9/+_\-]{20,}['\"]"),
}

# Allow obvious placeholders / examples.
ALLOW = re.compile(
    r"(?i)(example|placeholder|your[_-]?|xxxx|<[^>]+>|changeme|dummy|sample|redacted|fake|test[_-]?key|\.\.\.|EXAMPLE)"
)

SCAN_GLOBS = [
    "config/*.json",
    "data/commercial_seed_leads.example.jsonl",
    "scripts/commercial_*.py",
    "scripts/media_social_*.py",
    "scripts/site_launch_*.py",
    "scripts/api_commercial_*.py",
    "scripts/final_*.py",
    "scripts/startup_os_*.py",
    "scripts/lib/startup_os_common.py",
    ".github/workflows/startup-os-verify.yml",
    ".github/workflows/commercial-draft-factory.yml",
    ".github/workflows/media-social-calendar.yml",
    ".github/workflows/site-commercial-verify.yml",
    ".github/workflows/final-launch-control.yml",
]


def scan_paths() -> list[Path]:
    paths: list[Path] = []
    for g in SCAN_GLOBS:
        paths.extend(sorted(ROOT.glob(g)))
    # OS doc trees
    for d in sorted((ROOT / "docs").glob("*-os")):
        paths.extend(sorted(d.rglob("*.md")))
    for d in ("docs/launch-control", "docs/site-launch", "docs/commercial-launch", "docs/go-live", "docs/company-os", "docs/product-os"):
        p = ROOT / d
        if p.exists():
            paths.extend(sorted(p.rglob("*.md")))
    return [p for p in paths if p.is_file()]


def scan() -> list[str]:
    findings: list[str] = []
    for path in scan_paths():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for name, pat in PATTERNS.items():
                m = pat.search(line)
                if m and not ALLOW.search(line):
                    findings.append(f"{path.relative_to(ROOT)}:{lineno}: possible {name}: {m.group(0)[:24]}…")
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="non-zero exit on any finding")
    args = ap.parse_args()
    findings = scan()
    if not findings:
        print(f"Secret & risk scan PASS — scanned {len(scan_paths())} files, no secrets found.")
        return 0
    print("Secret & risk scan findings:")
    for f in findings:
        print(f"  - {f}")
    return 1 if args.strict or findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
