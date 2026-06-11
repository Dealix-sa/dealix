#!/usr/bin/env python3
"""Generate an invoice STUB. This is NOT a tax/legal invoice.

Operational placeholder so the deal desk has a record of what would be billed.
Real invoices go through the customer's accounting system after manual review.

Usage:
    python3 scripts/generate_invoice_stub.py --deal-id latest
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.quote_engine import (  # noqa: E402
    load_deals,
    load_invoices,
    save_invoices,
    next_id,
    now,
)

OUT_DIR = Path(__file__).resolve().parent.parent / "business" / "finance" / "exports"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deal-id", required=True)
    args = parser.parse_args()

    deals_data = load_deals()
    deals = deals_data.get("deals", [])
    if not deals:
        print("ERROR: no deals to invoice.", file=sys.stderr)
        return 1
    if args.deal_id == "latest":
        deal = deals[-1]
    else:
        deal = next((d for d in deals if d.get("id") == args.deal_id or d.get("account_id") == args.deal_id), None)
        if not deal:
            print(f"ERROR: deal {args.deal_id} not found.", file=sys.stderr)
            return 1

    setup = float(deal.get("setup_value") or deal.get("setupValue") or 0)
    monthly = float(deal.get("monthly_value") or deal.get("monthlyValue") or 0)
    line_items = []
    if setup > 0:
        line_items.append({"description": "Setup — one-time", "qty": 1, "unitPrice": setup, "subtotal": setup})
    if monthly > 0:
        line_items.append({"description": "Managed Ops — first month", "qty": 1, "unitPrice": monthly, "subtotal": monthly})
    amount = sum(li["subtotal"] for li in line_items)

    inv_index = load_invoices()
    invoice = {
        "id": next_id("INV-STUB", inv_index["invoices"]),
        "dealId": deal.get("id") or deal.get("account_id"),
        "accountId": deal.get("account_id") or deal.get("accountId"),
        "lineItems": line_items,
        "amount": amount,
        "currency": "SAR",
        "createdAt": now(),
        "vatNote": "VAT handled by customer's accounting system; this stub is not ZATCA-compliant.",
        "demo": True,
    }
    inv_index["invoices"].append(invoice)
    save_invoices(inv_index)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    md = OUT_DIR / f"{invoice['id']}.md"
    md.write_text(
        f"""# Invoice Stub {invoice['id']} (DEMO — NOT A TAX INVOICE)

**Account:** {invoice['accountId']}
**Deal:** {invoice['dealId']}
**Amount:** {amount:,.0f} SAR

## Line items
"""
        + "\n".join(f"- {li['description']} × {li['qty']} = {li['subtotal']:,.0f} SAR" for li in line_items)
        + f"""

## VAT
{invoice['vatNote']}

## Disclaimer
This document is an internal operations stub. It is NOT a ZATCA-compliant invoice. Issue the real invoice through the customer's accounting system. Founder must review before any payment expectation is communicated to the customer.
""",
        encoding="utf-8",
    )
    print(f"wrote {md}")
    print(f"invoice-id: {invoice['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
