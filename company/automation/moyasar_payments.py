#!/usr/bin/env python3
"""Moyasar payment processing — Automate invoice generation and payment links."""

import json
import os
import base64
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "company" / "runtime"


class MoyasarPayments:
    """Moyasar payment gateway integration."""

    def __init__(self):
        """Initialize Moyasar API client."""
        self.api_key = os.getenv("MOYASAR_API_KEY", "")
        self.api_secret = os.getenv("MOYASAR_API_SECRET", "")
        self.base_url = "https://api.moyasar.com/v1"
        self.live_mode = os.getenv("MOYASAR_LIVE_MODE", "false").lower() == "true"

    def is_configured(self) -> bool:
        """Check if Moyasar API is configured."""
        return bool(self.api_key and self.api_secret)

    def get_auth_header(self) -> dict:
        """Generate Basic auth header for Moyasar API."""
        credentials = f"{self.api_key}:{self.api_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded}"}

    def create_payment_link(
        self,
        customer_email: str,
        customer_phone: str,
        customer_name: str,
        description: str,
        amount_sar: int,
        pilot_id: Optional[str] = None,
    ) -> dict:
        """Create a Moyasar payment link for invoice.

        Args:
            customer_email: Customer email
            customer_phone: Customer phone
            customer_name: Customer name
            description: Invoice description (e.g., "Dealix Pilot - 14 days")
            amount_sar: Amount in SAR
            pilot_id: Optional pilot ID for tracking

        Returns:
            Payment link response
        """
        if not self.is_configured():
            return {
                "status": "not_configured",
                "error": "Moyasar API not configured. Set MOYASAR_API_KEY and MOYASAR_API_SECRET",
                "payment_url": None,
            }

        url = f"{self.base_url}/invoices"
        headers = self.get_auth_header()

        # Amount in fils (SAR × 100)
        amount_fils = amount_sar * 100

        payload = {
            "amount": amount_fils,
            "currency": "SAR",
            "description": description,
            "customer": {
                "email": customer_email,
                "name": customer_name,
                "phone": customer_phone,
            },
            "metadata": {
                "pilot_id": pilot_id,
                "created_at": datetime.now().isoformat(),
            },
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            resp.raise_for_status()

            data = resp.json()
            invoice = data.get("invoice", {})

            return {
                "status": "created",
                "invoice_id": invoice.get("id"),
                "payment_url": invoice.get("url"),
                "amount_sar": amount_sar,
                "currency": "SAR",
                "customer_email": customer_email,
                "description": description,
                "expires_at": invoice.get("expires_at"),
                "created_at": datetime.now().isoformat(),
            }

        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "error": str(e),
                "payment_url": None,
            }

    def check_payment_status(self, invoice_id: str) -> dict:
        """Check status of a payment invoice.

        Args:
            invoice_id: Moyasar invoice ID

        Returns:
            Invoice status
        """
        if not self.is_configured():
            return {
                "status": "not_configured",
                "error": "Moyasar API not configured",
            }

        url = f"{self.base_url}/invoices/{invoice_id}"
        headers = self.get_auth_header()

        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()

            data = resp.json()
            invoice = data.get("invoice", {})

            return {
                "status": invoice.get("status"),  # paid, draft, sent, partial, expired
                "invoice_id": invoice.get("id"),
                "amount_sar": invoice.get("amount", 0) / 100,
                "paid_amount_sar": invoice.get("paid_amount", 0) / 100,
                "customer_name": invoice.get("customer", {}).get("name"),
                "created_at": invoice.get("created_at"),
                "updated_at": invoice.get("updated_at"),
            }

        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "error": str(e),
            }

    def create_pilot_invoice(
        self,
        customer_name: str,
        company_name: str,
        customer_email: str,
        customer_phone: str,
        pilot_id: str,
        price_sar: int = 499,
    ) -> dict:
        """Create invoice for pilot signup.

        Args:
            customer_name: Customer name
            company_name: Company name
            customer_email: Email
            customer_phone: Phone
            pilot_id: Pilot ID
            price_sar: Price (default 499)

        Returns:
            Invoice and payment link
        """
        description = f"Dealix Pilot - 14-Day Proof Sprint\nCompany: {company_name}\nPrice: {price_sar} SAR"

        return self.create_payment_link(
            customer_email=customer_email,
            customer_phone=customer_phone,
            customer_name=customer_name,
            description=description,
            amount_sar=price_sar,
            pilot_id=pilot_id,
        )

    def log_payment(self, payment_info: dict) -> Path:
        """Log payment request/status to file."""
        log_path = RUNTIME_DIR / "payments.jsonl"

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payment_info, ensure_ascii=False) + "\n")

        return log_path


def main() -> int:
    """Test Moyasar payments."""
    print("💳 Moyasar Payments Module")
    print("=" * 50)

    moyasar = MoyasarPayments()

    if not moyasar.is_configured():
        print("⚠️  Moyasar API not configured (test mode)")
        print("Set these environment variables to enable live payments:")
        print("  - MOYASAR_API_KEY")
        print("  - MOYASAR_API_SECRET")
        print("  - MOYASAR_LIVE_MODE=true (for production)")

        # Simulate payment link creation
        print("\n📤 Simulated payment link (test mode):")
        result = {
            "status": "created",
            "invoice_id": "INV_test_123",
            "payment_url": "https://moyasar.com/pay/INV_test_123",
            "amount_sar": 499,
            "description": "Dealix Pilot - 14 days",
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print("✅ Moyasar API configured (live mode)")

    # Create test invoice
    print("\n📤 Creating test invoice...")
    invoice = moyasar.create_pilot_invoice(
        customer_name="محمد",
        company_name="عقارات الحمد",
        customer_email="mohammad@qrarat.com",
        customer_phone="+966501234567",
        pilot_id="pilot_test_001",
        price_sar=499,
    )

    print(json.dumps(invoice, ensure_ascii=False, indent=2))

    if invoice.get("status") == "created":
        print(f"\n✅ Payment link created: {invoice.get('payment_url')}")

    return 0


if __name__ == "__main__":
    exit(main())
