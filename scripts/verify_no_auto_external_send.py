#!/usr/bin/env python3
"""
Dealix Verify No-Auto-External-Send Gate
Ensures outbound remains approval-gated by default.
"""

import os
import sys
from pathlib import Path


SEND_ENVS = [
    "EXTERNAL_SEND_ENABLED",
    "EMAIL_SEND_ENABLED",
    "WHATSAPP_SEND_ENABLED",
    "WHATSAPP_ALLOW_LIVE_SEND",
    "SMS_SEND_ENABLED",
]

ALLOWED_OVERRIDE_FILE = Path(__file__).parent.parent / ".dealix_allow_external_send"


def load_local_env_files() -> None:
    base = Path(__file__).parent.parent
    for env_name in [".env", ".env.local"]:
        env_path = base / env_name
        if not env_path.exists():
            continue

        for raw_line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            if key and key not in os.environ:
                os.environ[key] = value


def check_env_vars() -> list[str]:
    issues = []
    for env_name in SEND_ENVS:
        value = os.environ.get(env_name, "false").lower().strip()
        if value in ("true", "1", "yes", "on"):
            if not ALLOWED_OVERRIDE_FILE.exists():
                issues.append(
                    f"CRITICAL: {env_name}={value} but no override file found at {ALLOWED_OVERRIDE_FILE}"
                )
                continue

            content = ALLOWED_OVERRIDE_FILE.read_text(encoding="utf-8", errors="ignore")
            if env_name not in content:
                issues.append(
                    f"CRITICAL: {env_name}={value} but not explicitly whitelisted in {ALLOWED_OVERRIDE_FILE}"
                )
    return issues


def check_settings_table() -> list[str]:
    issues = []
    try:
        import mysql.connector

        db_url = os.environ.get("DATABASE_URL", "")
        if not db_url or "mysql" not in db_url:
            return issues

        connection = mysql.connector.connect(
            host="localhost",
            user=os.environ.get("DB_USER", "dealix"),
            password=os.environ.get("DB_PASSWORD", "dealix_pass_2026"),
            database="dealix",
            port=3306,
            connect_timeout=5,
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT `value` FROM settings WHERE `key` = 'outbound_mode'")
        row = cursor.fetchone()
        if row:
            mode = (row.get("value") or "").strip().lower()
            if mode not in ("", "draft_only"):
                issues.append(f"CRITICAL: settings.outbound_mode='{mode}' (must be 'draft_only')")
        cursor.close()
        connection.close()
    except ImportError:
        return issues
    except Exception as error:
        issues.append(f"WARNING: Could not check DB settings: {error}")
    return issues


def check_drafts_have_approval() -> list[str]:
    issues = []
    try:
        import mysql.connector

        connection = mysql.connector.connect(
            host="localhost",
            user=os.environ.get("DB_USER", "dealix"),
            password=os.environ.get("DB_PASSWORD", "dealix_pass_2026"),
            database="dealix",
            port=3306,
            connect_timeout=5,
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id FROM drafts
            WHERE sent = TRUE AND approved = FALSE
            LIMIT 1
            """
        )
        row = cursor.fetchone()
        if row:
            issues.append(
                f"CRITICAL: Draft id={row['id']} is sent but not approved"
            )
        cursor.close()
        connection.close()
    except ImportError:
        return issues
    except Exception as error:
        issues.append(f"WARNING: Could not check drafts table: {error}")
    return issues


def check_codebase_for_auto_send() -> list[str]:
    issues = []
    base = Path(__file__).parent.parent
    scripts_dir = base / "scripts"
    suspicious_patterns = [
        "# auto-send",
        "auto_send",
        "auto_send=True",
        "autoSend=True",
        "unapproved_send",
        "send_without_approval",
        "bypass_approval",
        "WHATSAPP_ALLOW_LIVE_SEND = true",
        "EXTERNAL_SEND_ENABLED = true",
    ]

    if not scripts_dir.exists():
        return issues

    for script_path in scripts_dir.rglob("*.py"):
        if script_path.name == Path(__file__).name:
            continue
        content = script_path.read_text(encoding="utf-8", errors="ignore")
        for pattern in suspicious_patterns:
            if pattern in content:
                issues.append(
                    f"SUSPICIOUS: '{pattern}' found in {script_path.relative_to(base)}"
                )
    return issues


def main():
    load_local_env_files()

    print("=" * 70)
    print("  DEALIX - NO-AUTO-EXTERNAL-SEND SAFETY GATE")
    print("=" * 70)
    print()

    issues = []
    issues.extend(check_env_vars())
    issues.extend(check_settings_table())
    issues.extend(check_drafts_have_approval())
    issues.extend(check_codebase_for_auto_send())

    critical = [issue for issue in issues if issue.startswith("CRITICAL")]
    warnings = [issue for issue in issues if issue.startswith("WARNING")]
    suspicious = [issue for issue in issues if issue.startswith("SUSPICIOUS")]

    print(f"  Critical issues: {len(critical)}")
    print(f"  Warnings: {len(warnings)}")
    print(f"  Suspicious: {len(suspicious)}")

    if critical:
        print()
        print("  BLOCKING CRITICAL ISSUES:")
        for item in critical:
            print(f"     - {item}")

    if warnings:
        print()
        print("  WARNINGS:")
        for item in warnings:
            print(f"     - {item}")

    if suspicious:
        print()
        print("  SUSPICIOUS CODE:")
        for item in suspicious:
            print(f"     - {item}")

    print()

    outbound_mode = os.environ.get("OUTBOUND_MODE", "") or "draft_only"
    if critical:
        print("  GATE RESULT: BLOCKED")
        print("  OUTBOUND_MODE: draft_only (forced due to blockers)")
        print()
        print("  Next action: Fix critical issues, then re-run.")
        sys.exit(1)

    if warnings:
        print("  GATE RESULT: PASS WITH WARNINGS")
        print(f"  OUTBOUND_MODE: {outbound_mode}")
        print()
        print("  Next action: Address warnings, but system can operate.")
        sys.exit(0)

    print("  GATE RESULT: PASS")
    print(f"  OUTBOUND_MODE: {outbound_mode}")
    print()
    print("  All safety checks passed. System is in safe mode.")
    sys.exit(0)


if __name__ == "__main__":
    main()