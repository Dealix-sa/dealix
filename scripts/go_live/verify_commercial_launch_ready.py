#!/usr/bin/env python3
"""Check whether Dealix is ready for controlled commercial launch."""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REQUIRED_FILES = [
    "app/outbound/policy_gate.py",
    "app/outbound/rate_limiter.py",
    "app/outbound/email_sender.py",
    "app/outbound/whatsapp_sender.py",
    "app/outbound/provider_router.py",
    "scripts/outbound/check_live_outbound_env.py",
    "scripts/outbound/run_controlled_live_outbound.py",
    "scripts/outbound/sync_outbound_events.py",
    "db/migrations/versions/20260616_014_controlled_live_outbound.py",
    "migrations/20260616_controlled_live_outbound.sql",
    "docs/ops/CONTROLLED_LIVE_OUTBOUND.md",
    "docs/ops/RAILWAY_PRODUCTION_RUNBOOK.md",
]

REQUIRED_ENV = [
    "APP_ENV",
    "ENVIRONMENT",
    "EXTERNAL_SEND_ENABLED",
    "OUTBOUND_MODE",
]


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    missing_files = [f for f in REQUIRED_FILES if not (root / f).exists()]
    missing_env = [e for e in REQUIRED_ENV if not os.getenv(e)]

    print("=== Dealix Commercial Launch Readiness ===")
    if missing_files:
        print("❌ Missing files:")
        for f in missing_files:
            print(f"  - {f}")
    else:
        print("✅ All required files present.")

    if missing_env:
        print("⚠️  Missing env vars (set them in Railway/.env):")
        for e in missing_env:
            print(f"  - {e}")
    else:
        print("✅ Required env vars present.")

    if missing_files or missing_env:
        print("\nVERDICT: NOT READY")
        return 1

    print("\nVERDICT: READY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
