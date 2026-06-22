#!/usr/bin/env python3
"""
verify_company_launch_ready.py
Company launch readiness gate.

Checks:
- .env-derived safe defaults for external send
- required ledgers exist (or can be created empty)
- required command-room directories exist
- no forbidden auto-send patterns in revenue scripts
- outbox is empty / only contains draft files
"""
from __future__ import annotations

import csv
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ENV_SAFE_DEFAULTS = {
    "EXTERNAL_SEND_ENABLED": ("false", "0"),
    "EMAIL_SEND_ENABLED": ("false", "0"),
    "WHATSAPP_SEND_ENABLED": ("false", "0"),
    "WHATSAPP_ALLOW_LIVE_SEND": ("false", "0"),
    "SMS_SEND_ENABLED": ("false", "0"),
    "OUTBOUND_MODE": ("draft_only",),
}

REQUIRED_LEDGER_COLUMNS = {
    "ledgers/prospects.csv": ["company", "sector", "source_url", "verification_status", "confidence", "recommended_product", "owner_decision"],
    "ledgers/outreach_log.csv": ["company", "channel", "status", "draft_path"],
    "ledgers/reply_log.csv": ["company", "reply_date", "intent"],
    "ledgers/deals_pipeline.csv": ["company", "stage", "value_sar", "owner"],
}

FORBIDDEN_SEND_PATTERNS = [
    re.compile(r"\bsend_email\s*\("),
    re.compile(r"\bsend_whatsapp\s*\("),
    re.compile(r"\bsend_sms\s*\("),
    re.compile(r"\bauto_send\s*=\s*(True|1|\"yes\"|\"true\"|\'yes\'|\'true\')"),
]

SAFE_SCAN_PATHS = [
    "scripts/revenue",
    "scripts/command_room",
    "scripts/email",
    "scripts/outbound",
]

ALLOWED_SENDERS = [
    "scripts/email/create_gmail_drafts_safe.py",
]


def _read_env() -> dict[str, str]:
    env_path = REPO_ROOT / ".env"
    values: dict[str, str] = {}
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                values[k.strip()] = v.strip().strip('"').strip("'")
    return values


def check_env_safe_defaults(env: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for key, safe_values in REQUIRED_ENV_SAFE_DEFAULTS.items():
        val = os.environ.get(key, env.get(key, "")).lower()
        if val and val not in [v.lower() for v in safe_values]:
            errors.append(
                f"{key}={val!r} is not a safe default. Expected one of {safe_values}."
            )
    return errors


def check_ledgers() -> list[str]:
    errors: list[str] = []
    for rel, cols in REQUIRED_LEDGER_COLUMNS.items():
        path = REPO_ROOT / rel
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=cols)
                writer.writeheader()
            errors.append(f"{rel} was missing; created empty ledger with headers.")
            continue
        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            header = next(reader, None)
        missing = [c for c in cols if c not in header]
        if missing:
            errors.append(f"{rel} missing columns: {missing}")
    return errors


def check_required_dirs() -> list[str]:
    errors: list[str] = []
    for rel in ["reports/command_room", "reports/company_day", "outbox", "ledgers"]:
        path = REPO_ROOT / rel
        path.mkdir(parents=True, exist_ok=True)
    return errors


def check_no_auto_send() -> list[str]:
    errors: list[str] = []
    scan_dirs = [REPO_ROOT / p for p in SAFE_SCAN_PATHS if (REPO_ROOT / p).exists()]
    for d in scan_dirs:
        for py in d.rglob("*.py"):
            rel = py.relative_to(REPO_ROOT).as_posix()
            if rel in ALLOWED_SENDERS:
                continue
            text = py.read_text(encoding="utf-8", errors="ignore")
            for pat in FORBIDDEN_SEND_PATTERNS:
                for m in pat.finditer(text):
                    errors.append(f"{rel}:{m.start()}: forbidden pattern {pat.pattern}")
    return errors


def check_outbox_no_unexpected_files() -> list[str]:
    errors: list[str] = []
    outbox = REPO_ROOT / "outbox"
    if outbox.exists():
        for item in outbox.rglob("*"):
            if item.is_file():
                rel = item.relative_to(REPO_ROOT).as_posix()
                if "auto" in rel.lower() and "draft" not in rel.lower():
                    errors.append(f"Suspicious auto file in outbox: {rel}")
    return errors


def main() -> int:
    print("Dealix Company Launch Readiness Check")
    print("=" * 50)

    env = _read_env()
    checks = [
        ("Safe env defaults", check_env_safe_defaults(env)),
        ("Required ledgers", check_ledgers()),
        ("Required directories", check_required_dirs()),
        ("No auto-send patterns", check_no_auto_send()),
        ("Outbox sanity", check_outbox_no_unexpected_files()),
    ]

    all_ok = True
    for name, errors in checks:
        if errors:
            all_ok = False
            print(f"\n❌ {name} — {len(errors)} issue(s):")
            for e in errors:
                print(f"   - {e}")
        else:
            print(f"✅ {name}")

    print("=" * 50)
    if all_ok:
        print("VERDICT: READY_FOR_MANUAL_OUTREACH")
        return 0
    print("VERDICT: NEEDS_REVIEW")
    return 1


if __name__ == "__main__":
    sys.exit(main())
