#!/usr/bin/env python3
"""Paid launch readiness — env + integration matrix (no Moyasar claim until configured)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.railway_launch import (  # noqa: E402
    check_railway_api_env,
    check_railway_frontend_env,
)

FAILURES: list[str] = []
WARNINGS: list[str] = []


def _set(name: str) -> bool:
    return bool((os.getenv(name) or "").strip())


def check_integration_env() -> None:
    integrations = {
        "MOYASAR_SECRET_KEY": "Moyasar live/test",
        "MOYASAR_WEBHOOK_SECRET": "Moyasar webhook",
        "HUBSPOT_ACCESS_TOKEN": "HubSpot sync",
        "CALENDLY_WEBHOOK_SIGNING_KEY": "Calendly webhooks",
        "CALENDLY_URL": "Calendly booking link",
        "POSTHOG_API_KEY": "PostHog analytics",
        "GMAIL_CLIENT_ID": "Gmail OAuth (drafts)",
    }
    for key, label in integrations.items():
        if _set(key):
            print(f"  ok: {label} ({key})")
        else:
            WARNINGS.append(f"{label}: set {key}")
            print(f"  FOUNDER_ACTION: {label} — {key}")


def check_docs() -> None:
    required = [
        "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md",
        "docs/ops/MANUAL_PAYMENT_SOP.md",
        "docs/commercial/PAID_LAUNCH_TRACKER_AR.md",
        "docs/LAUNCH_GATES.md",
    ]
    for rel in required:
        if (ROOT / rel).is_file():
            print(f"  ok: {rel}")
        else:
            FAILURES.append(f"missing {rel}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--strict",
        action="store_true",
        help="Fail if any integration env or payment keys missing",
    )
    args = p.parse_args()

    print("== verify_paid_launch_readiness ==")
    print("\n== Docs ==")
    check_docs()
    print("\n== Integrations (FOUNDER_ACTION until set) ==")
    check_integration_env()
    print("\n== Railway / deploy env ==")
    api = check_railway_api_env()
    fe = check_railway_frontend_env()
    if api["ready_for_api_deploy"]:
        print("  ok: API deploy env snapshot")
    else:
        WARNINGS.append(f"API env missing: {api['missing_required']}")
    if fe["ready_for_fe_deploy"]:
        print("  ok: Frontend deploy env snapshot")
    else:
        WARNINGS.append(f"Frontend env missing: {fe['missing']}")
    if not api["ready_for_payments"]:
        WARNINGS.append(f"Payments: {api['missing_payments']}")

    print("\n== First paid Diagnostic pipeline ==")
    try:
        from scripts.verify_first_paid_diagnostic_tracker import analyze

        pipe = analyze()
        print(
            f"  pipeline: {pipe['payment_received_real']} paid · "
            f"{pipe['proof_pack_delivered_real']} proof (real companies)"
        )
        print(f"  verdict: {'CLOSED' if pipe['first_close_ready'] else 'PIPELINE_OPEN'}")
        if pipe["crm_kpi_pending"]:
            print("  FOUNDER_ACTION: sync kpi_founder_commercial_import.yaml from CRM export")
    except Exception as exc:
        WARNINGS.append(f"first_paid tracker: {exc}")

    if FAILURES:
        print("\nPAID_LAUNCH_READINESS=FAIL")
        for f in FAILURES:
            print(f"  - {f}")
        return 1

    if args.strict and WARNINGS:
        print("\nPAID_LAUNCH_READINESS=FAIL (strict)")
        for w in WARNINGS:
            print(f"  - {w}")
        return 1

    for w in WARNINGS:
        print(f"  (pending) {w}")
    print("\nPAID_LAUNCH_READINESS=ROADMAP_OK (soft — complete FOUNDER_ACTION for paid)")
    print("Next: docs/commercial/PAID_LAUNCH_TRACKER_AR.md · bash scripts/official_launch_verify.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
