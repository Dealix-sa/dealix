#!/usr/bin/env python3
"""Create a Moyasar hosted-invoice link for a customer — one founder command.

Bridges:
  - dealix/payments/moyasar.py            (real Moyasar HTTP client)
  - auto_client_acquisition/payment_ops/  (state machine + no-fake-revenue gate)

Doctrine respected:
  - No live charge unless DEALIX_MOYASAR_MODE=live is set on the environment.
  - Records an invoice-intent in payment_ops (so the founder cockpit + verifiers
    see the same source of truth as the API at /api/v1/payment-ops/*).
  - Default is --dry-run; no network call is made until the founder explicitly
    asks for --live or --moyasar-test.

Usage:
  Dry run (no Moyasar call, just print the planned invoice):
    python scripts/founder_create_payment_link.py \\
      --customer "Agency X" --amount-sar 999 \\
      --description "Dealix Pilot — 7 days"

  Moyasar test mode (real API, test key, no real money):
    MOYASAR_SECRET_KEY=sk_test_xxx \\
    python scripts/founder_create_payment_link.py \\
      --customer "Agency X" --amount-sar 999 \\
      --description "Dealix Pilot — 7 days" --moyasar-test

  Live (must opt in explicitly):
    MOYASAR_SECRET_KEY=sk_live_xxx DEALIX_MOYASAR_MODE=live \\
    python scripts/founder_create_payment_link.py \\
      --customer "Agency X" --amount-sar 999 \\
      --description "Dealix Pilot — 7 days" --live
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _sar_to_halalas(amount_sar: float) -> int:
    if amount_sar <= 0:
        raise ValueError("amount_sar must be > 0")
    if amount_sar > 1_000_000:
        raise ValueError("amount_sar must be <= 1,000,000 (PaymentStateRecord cap)")
    # Round to nearest halala to avoid float drift.
    return int(round(amount_sar * 100))


def _build_metadata(customer: str, payment_id: str, intent_id: str) -> dict[str, str]:
    return {
        "customer_handle": customer,
        "dealix_payment_id": payment_id,
        "dealix_invoice_intent_id": intent_id,
    }


async def _create_moyasar_invoice(
    *,
    amount_halalas: int,
    description: str,
    callback_url: str | None,
    metadata: dict[str, str],
) -> dict[str, Any]:
    # Imported lazily so --dry-run doesn't require httpx.
    from dealix.payments.moyasar import MoyasarClient

    client = MoyasarClient()  # picks up MOYASAR_SECRET_KEY from env
    return await client.create_invoice(
        amount_halalas=amount_halalas,
        currency="SAR",
        description=description,
        callback_url=callback_url,
        metadata=metadata,
    )


def run(args: argparse.Namespace) -> dict[str, Any]:
    """Pure function so tests can call without going through argparse."""
    amount_halalas = _sar_to_halalas(args.amount_sar)

    if args.live and args.moyasar_test:
        raise ValueError("--live and --moyasar-test are mutually exclusive")

    method = (
        "moyasar_live" if args.live
        else "moyasar_test" if args.moyasar_test
        else "manual_other"
    )

    # Create the payment_ops intent FIRST so we have a stable id to embed in
    # the Moyasar invoice metadata. This also runs the no-live-charge gate.
    from auto_client_acquisition.payment_ops import create_invoice_intent

    rec = create_invoice_intent(
        customer_handle=args.customer,
        amount_sar=float(args.amount_sar),
        method=method,
    )

    planned = {
        "payment_id": rec.payment_id,
        "invoice_intent_id": rec.invoice_intent_id,
        "customer_handle": rec.customer_handle,
        "amount_sar": rec.amount_sar,
        "amount_halalas": amount_halalas,
        "method": rec.method,
        "status": rec.status,
        "description": args.description,
        "callback_url": args.callback_url,
    }

    if args.dry_run:
        return {
            "mode": "dry_run",
            "planned_invoice": planned,
            "moyasar_invoice": None,
            "payment_url": None,
            "safety_summary": rec.safety_summary,
        }

    metadata = _build_metadata(args.customer, rec.payment_id, rec.invoice_intent_id or "")
    invoice = asyncio.run(
        _create_moyasar_invoice(
            amount_halalas=amount_halalas,
            description=args.description,
            callback_url=args.callback_url,
            metadata=metadata,
        )
    )
    payment_url = invoice.get("url") or invoice.get("source", {}).get("url")
    return {
        "mode": "live" if args.live else "moyasar_test",
        "planned_invoice": planned,
        "moyasar_invoice": invoice,
        "payment_url": payment_url,
        "safety_summary": rec.safety_summary,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Create a Moyasar hosted-invoice link.")
    p.add_argument("--customer", required=True, help="customer_handle (e.g. 'agency-alpha')")
    p.add_argument("--amount-sar", required=True, type=float, help="amount in SAR (e.g. 999)")
    p.add_argument("--description", required=True, help="invoice description shown on Moyasar")
    p.add_argument("--callback-url", default=None, help="optional Moyasar callback URL")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", default=True, help="default; no Moyasar call")
    mode.add_argument("--moyasar-test", action="store_true", help="call Moyasar with test key")
    mode.add_argument("--live", action="store_true", help="call Moyasar live (requires DEALIX_MOYASAR_MODE=live)")
    args = p.parse_args()

    # --moyasar-test / --live override the default --dry-run.
    if args.moyasar_test or args.live:
        args.dry_run = False

    if args.live and os.environ.get("DEALIX_MOYASAR_MODE") != "live":
        print("ERR: --live requires DEALIX_MOYASAR_MODE=live (NO_LIVE_CHARGE gate)", file=sys.stderr)
        return 2

    try:
        result = run(args)
    except (ValueError, RuntimeError) as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
