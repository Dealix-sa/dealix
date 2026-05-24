#!/usr/bin/env python3
"""Read-only audit of secret-bearing settings.

Phase 0 / Track E (cross-cutting compliance).

Walks Settings.model_fields, finds every SecretStr-typed field, and prints
which are configured vs missing. Does NOT print secret values — only
presence + a SHA-256 prefix hash for change detection across runs.

Usage:
    python scripts/secrets_rotation_audit.py [--json]

Exit code:
    0  — clean
    2  — at least one production-critical secret missing
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from typing import Any

# Production-critical secrets — if any of these is missing when
# APP_ENV=production, exit non-zero.
PRODUCTION_CRITICAL = {
    "moyasar_secret_key",
    "moyasar_webhook_secret",
    "jwt_secret_key",
    "app_secret_key",
}


def _short_hash(value: str) -> str:
    """Return first 8 chars of SHA-256 — change-detectable, not reversible."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]


def audit() -> dict[str, Any]:
    from pydantic import SecretStr

    from core.config.settings import Settings

    s = Settings()
    rows: list[dict[str, Any]] = []
    missing_critical: list[str] = []

    for name, info in Settings.model_fields.items():
        annotation = info.annotation
        # Match SecretStr or `SecretStr | None`.
        ann_str = str(annotation)
        if "SecretStr" not in ann_str:
            continue
        raw = getattr(s, name, None)
        if isinstance(raw, SecretStr):
            secret = raw.get_secret_value()
        else:
            secret = raw
        present = bool(secret) and secret not in ("", "change-me")
        row = {
            "field": name,
            "present": present,
            "hash_prefix": _short_hash(secret) if present and isinstance(secret, str) else None,
        }
        rows.append(row)
        if not present and name in PRODUCTION_CRITICAL and s.is_production:
            missing_critical.append(name)

    return {
        "env": s.app_env,
        "total_secret_fields": len(rows),
        "present_count": sum(1 for r in rows if r["present"]),
        "missing_count": sum(1 for r in rows if not r["present"]),
        "missing_critical_in_production": missing_critical,
        "fields": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix secrets rotation audit (read-only).")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of table")
    args = parser.parse_args()

    # Ensure repo root on path so `core.config.settings` imports cleanly.
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(here)
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    report = audit()

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Dealix secrets audit — env={report['env']}")
        print(
            f"  {report['present_count']}/{report['total_secret_fields']} "
            f"secret-typed fields present"
        )
        if report["missing_critical_in_production"]:
            print("  MISSING CRITICAL (production):")
            for f in report["missing_critical_in_production"]:
                print(f"    - {f}")
        else:
            print("  no critical secrets missing for the current env")
        print()
        # Only present/absent is printed — hash-prefix is intentionally
        # omitted from the human-readable output (CodeQL CWE-532 safe).
        # Use --json for the full diff-friendly view that includes hashes.
        for row in report["fields"]:
            status = "OK " if row["present"] else "-- "
            print(f"  {status}{row['field']}")

    return 2 if report["missing_critical_in_production"] else 0


if __name__ == "__main__":
    sys.exit(main())
