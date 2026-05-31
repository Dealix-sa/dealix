"""ZATCA e-invoice issuance after Moyasar payment confirmation.

Triggered by the Moyasar webhook after `status == "paid"`.
Non-fatal: if ZATCA creds are missing or the API call fails, the error
is logged and payment processing continues (NO_ZATCA_BLOCK_PAYMENT).

Phase 2 mandate (effective June 2024):
  - B2B invoices (>1000 SAR): real-time clearance required
  - B2C simplified invoices: report within 24 hours
  - All invoices: UBL 2.1 XML with TLV QR code

Environment variables required for live mode:
  ZATCA_CSID        — Cryptographic Stamp Identifier
  ZATCA_SECRET      — ZATCA API secret
  ZATCA_SANDBOX     — "true" (default) | "false" for production
"""

from __future__ import annotations

import logging
import os
import uuid
from datetime import UTC, datetime
from typing import Any

log = logging.getLogger(__name__)

_SANDBOX = os.getenv("ZATCA_SANDBOX", "true").lower() not in ("false", "0", "no")
_VAT_RATE = 0.15  # 15% KSA VAT
_SELLER_VAT = os.getenv("ZATCA_SELLER_VAT_NUMBER", "")
_SELLER_NAME = os.getenv("ZATCA_SELLER_NAME", "Dealix")
_SELLER_CITY = os.getenv("ZATCA_SELLER_CITY", "Riyadh")


async def issue_zatca_invoice(*, payment: dict[str, Any]) -> dict[str, Any]:
    """Issue a ZATCA-compliant e-invoice for a confirmed Moyasar payment.

    Returns a result dict with `status` and `invoice_uuid`.
    Never raises — logs errors and returns `{"status": "skipped", "reason": ...}`.
    """
    csid = os.getenv("ZATCA_CSID", "")
    secret = os.getenv("ZATCA_SECRET", "")

    if not csid or not secret:
        log.info(
            "zatca_invoice_skipped: ZATCA_CSID/ZATCA_SECRET not configured — "
            "set in Railway env vars to enable e-invoicing"
        )
        return {"status": "skipped", "reason": "zatca_creds_not_configured"}

    amount_halalas = payment.get("amount", 0)
    amount_sar = amount_halalas / 100
    vat_amount = round(amount_sar * _VAT_RATE / (1 + _VAT_RATE), 2)
    base_amount = round(amount_sar - vat_amount, 2)
    payment_id = payment.get("id", "")
    source = payment.get("source", {}) if isinstance(payment.get("source"), dict) else {}
    customer_name = source.get("company", source.get("name", "العميل"))
    invoice_uuid = str(uuid.uuid4())
    issue_date = datetime.now(UTC).strftime("%Y-%m-%d")
    issue_time = datetime.now(UTC).strftime("%H:%M:%S")

    # Determine invoice type: B2B (clearance) vs B2C (simplified/report)
    is_b2b = amount_sar > 1000

    try:
        from integrations.zatca import FatoorahClient, build_invoice_xml

        xml_b64 = build_invoice_xml(
            invoice_uuid=invoice_uuid,
            issue_date=issue_date,
            issue_time=issue_time,
            seller_name=_SELLER_NAME,
            seller_vat=_SELLER_VAT,
            seller_city=_SELLER_CITY,
            buyer_name=customer_name,
            line_amount=base_amount,
            vat_amount=vat_amount,
            total_amount=amount_sar,
            is_b2b=is_b2b,
            payment_ref=payment_id,
        )

        client = FatoorahClient(csid=csid, secret=secret, sandbox=_SANDBOX)

        if is_b2b:
            result = await client.clear_invoice(xml_b64=xml_b64, uuid_value=invoice_uuid)
            action = "clearance"
        else:
            result = await client.report_invoice(xml_b64=xml_b64, uuid_value=invoice_uuid)
            action = "report"

        log.info(
            "zatca_invoice_issued action=%s uuid=%s amount_sar=%.2f sandbox=%s",
            action, invoice_uuid, amount_sar, _SANDBOX,
        )
        return {
            "status": "issued",
            "action": action,
            "invoice_uuid": invoice_uuid,
            "amount_sar": amount_sar,
            "vat_amount": vat_amount,
            "sandbox": _SANDBOX,
            "zatca_response": result,
        }

    except ImportError:
        log.warning("zatca_invoice_skipped: integrations.zatca not available")
        return {"status": "skipped", "reason": "zatca_module_unavailable"}
    except Exception as exc:
        log.error("zatca_invoice_failed uuid=%s error=%s", invoice_uuid, exc)
        return {"status": "error", "reason": str(exc), "invoice_uuid": invoice_uuid}
