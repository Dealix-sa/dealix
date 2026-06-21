"""Payment Link — thin wrapper around MoyasarClient for commercial offers.

Constitutional gate: NO_LIVE_CHARGE — invoice created in test mode unless
MOYASAR_LIVE_MODE=1 is explicitly set. All payment events require
founder approval before being surfaced to the customer.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from typing import Any

from pydantic import BaseModel, Field
from typing import cast


_LIVE_MODE = os.getenv("MOYASAR_LIVE_MODE", "0").strip() in ("1", "true", "yes")

# Service tiers with prices in SAR
SERVICE_TIERS: dict[str, dict[str, Any]] = {
    "sprint_499": {
        "name_ar": "برنامج الأسبوع المكثف",
        "name_en": "Intensive Week Sprint",
        "amount_sar": 499,
        "amount_halalas": 49900,
    },
    "data_pack_1500": {
        "name_ar": "حزمة البيانات",
        "name_en": "Data Intelligence Pack",
        "amount_sar": 1500,
        "amount_halalas": 150000,
    },
    "managed_ops_2999": {
        "name_ar": "Managed Ops الأساسي",
        "name_en": "Managed Ops Basic",
        "amount_sar": 2999,
        "amount_halalas": 299900,
    },
    "managed_ops_4999": {
        "name_ar": "Managed Ops المتقدم",
        "name_en": "Managed Ops Advanced",
        "amount_sar": 4999,
        "amount_halalas": 499900,
    },
    "custom_ai_15000": {
        "name_ar": "Executive AI Partner",
        "name_en": "Executive AI Partner",
        "amount_sar": 15000,
        "amount_halalas": 1500000,
    },
}


class PaymentLinkRequest(BaseModel):
    service_tier: str | None = Field(
        None,
        description="Key from SERVICE_TIERS; leave blank for custom invoice amounts",
    )
    amount_sar: float | None = Field(None, description="Amount in SAR for custom invoices")
    amount_halalas: int | None = Field(None, description="Amount in halalas for custom invoices")
    customer_name: str = Field(..., min_length=1)
    customer_email: str = ""
    account_id: str = ""
    pilot_id: str = ""
    callback_url: str = ""
    description: str = ""
    notes: str = ""


class PaymentLinkResponse(BaseModel):
    payment_url: str
    invoice_id: str
    invoice_ref: str
    amount_sar: int
    service_name_ar: str
    service_name_en: str
    is_live_mode: bool
    expires_at: str
    approval_status: str = "approval_required"
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        import json
        return cast(dict[str, Any], json.loads(self.model_dump_json()))


class PaymentLinkError(Exception):
    pass


async def create_payment_link(req: PaymentLinkRequest) -> PaymentLinkResponse:
    """Generate a Moyasar hosted invoice link for a Dealix service tier.

    Raises PaymentLinkError if the tier is unknown or Moyasar call fails.
    In sandbox mode (default), returns a placeholder URL with invoice_id prefixed 'sandbox_'.
    """
    tier = SERVICE_TIERS.get(req.service_tier) if req.service_tier else None
    if req.service_tier and tier is None:
        raise PaymentLinkError(
            f"Unknown service tier: {req.service_tier}. "
            f"Valid tiers: {list(SERVICE_TIERS)}"
        )

    if tier:
        description = (
            f"Dealix — {tier['name_ar']} / {tier['name_en']}"
            f" — {req.customer_name}"
            + (f" — {req.notes}" if req.notes else "")
        )
        amount_sar = tier["amount_sar"]
        amount_halalas = tier["amount_halalas"]
        service_name_ar = tier["name_ar"]
        service_name_en = tier["name_en"]
    else:
        if req.amount_halalas is None and req.amount_sar is None:
            raise PaymentLinkError(
                "Custom payment links require amount_sar or amount_halalas."
            )
        if req.amount_halalas is not None:
            amount_halalas = req.amount_halalas
            amount_sar = req.amount_sar if req.amount_sar is not None else (amount_halalas / 100)
        else:
            assert req.amount_sar is not None
            amount_halalas = int(req.amount_sar * 100)
            amount_sar = req.amount_sar
        description = req.description or f"Dealix Invoice — {req.customer_name}"
        if req.notes:
            description += f" — {req.notes}"
        service_name_ar = "فاتورة Dealix"
        service_name_en = "Dealix Invoice"

    expires_at = (datetime.now(UTC) + timedelta(days=7)).isoformat()

    if not _LIVE_MODE:
        # Sandbox mode — return placeholder without hitting Moyasar API
        import hashlib
        sandbox_id = "sandbox_" + hashlib.sha256(
            f"{req.account_id}{req.service_tier or 'custom'}{datetime.now(UTC).date()}".encode()
        ).hexdigest()[:12]
        return PaymentLinkResponse(
            payment_url=f"https://sandbox.moyasar.com/invoices/{sandbox_id}",
            invoice_id=sandbox_id,
            invoice_ref=sandbox_id,
            amount_sar=amount_sar,
            service_name_ar=service_name_ar,
            service_name_en=service_name_en,
            is_live_mode=False,
            expires_at=expires_at,
        )

    # Live mode — call Moyasar
    from dealix.payments.moyasar import MoyasarClient  # noqa: PLC0415
    client = MoyasarClient()
    metadata: dict[str, str] = {
        "account_id": req.account_id or "",
        "pilot_id": req.pilot_id or "",
        "customer_name": req.customer_name,
        "service_tier": req.service_tier or "custom",
    }
    try:
        invoice = await client.create_invoice(
            amount_halalas=amount_halalas,
            description=description,
            callback_url=req.callback_url or None,
            metadata=metadata,
        )
    except Exception as exc:
        raise PaymentLinkError(f"Moyasar API error: {exc}") from exc

    return PaymentLinkResponse(
        payment_url=invoice.get("url", ""),
        invoice_id=invoice.get("id", ""),
        invoice_ref=invoice.get("id", ""),
        amount_sar=amount_sar,
        service_name_ar=service_name_ar,
        service_name_en=service_name_en,
        is_live_mode=True,
        expires_at=expires_at,
    )
