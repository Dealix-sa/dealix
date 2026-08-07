#!/usr/bin/env python3
"""WhatsApp automation integration — Send approved messages automatically via WhatsApp API."""

import json
import os
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "company" / "runtime"


class WhatsAppAutomation:
    """Integrate with WhatsApp Business API to send messages."""

    def __init__(self):
        """Initialize WhatsApp API client."""
        self.api_key = os.getenv("WHATSAPP_API_KEY", "")
        self.account_id = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
        self.base_url = "https://graph.instagram.com/v18.0"

    def is_configured(self) -> bool:
        """Check if WhatsApp API is properly configured."""
        return bool(self.api_key and self.account_id and self.phone_number_id)

    def send_message(
        self,
        recipient_phone: str,
        message_ar: str,
        message_en: Optional[str] = None,
    ) -> dict:
        """Send WhatsApp message to recipient.

        Args:
            recipient_phone: Phone number in format +966XXXXXXXXX
            message_ar: Message in Khaliji Arabic
            message_en: Optional English translation

        Returns:
            Response dict with status and message ID
        """
        if not self.is_configured():
            return {
                "status": "not_configured",
                "error": "WhatsApp API not configured. Set env vars: WHATSAPP_API_KEY, WHATSAPP_BUSINESS_ACCOUNT_ID, WHATSAPP_PHONE_NUMBER_ID",
                "message_id": None,
            }

        # Normalize phone number
        phone = recipient_phone.replace("+", "").replace("-", "").replace(" ", "")
        if not phone.startswith("966"):
            phone = "966" + phone.lstrip("0")

        url = f"{self.base_url}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {
                "body": message_ar,
            },
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            resp.raise_for_status()

            data = resp.json()
            message_id = data.get("messages", [{}])[0].get("id")

            return {
                "status": "sent",
                "message_id": message_id,
                "phone": phone,
                "timestamp": datetime.now().isoformat(),
                "message_ar": message_ar,
            }

        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "error": str(e),
                "message_id": None,
            }

    def send_approval_queue(self, approval_items: list[dict]) -> list[dict]:
        """Send all approved items from queue.

        Args:
            approval_items: List of approved items from /decisions.html

        Returns:
            List of send results
        """
        results = []

        for item in approval_items:
            if item.get("approval_status") != "approved":
                continue

            if item.get("type") == "objection_response":
                result = self.send_message(
                    item.get("phone"),
                    item.get("draft_response_ar", ""),
                    item.get("draft_response_en"),
                )
                results.append(result)

            elif item.get("type") == "followup_reminder":
                result = self.send_message(
                    item.get("phone"),
                    item.get("draft_message_ar", ""),
                    item.get("draft_message_en"),
                )
                results.append(result)

        return results

    def log_sends(self, results: list[dict]) -> Path:
        """Log all sent messages to file."""
        log_path = RUNTIME_DIR / f"whatsapp_sends_{datetime.now().isoformat()[:10]}.jsonl"

        with open(log_path, "a", encoding="utf-8") as f:
            for result in results:
                f.write(json.dumps(result, ensure_ascii=False) + "\n")

        return log_path


def main() -> int:
    """Test WhatsApp automation."""
    print("📱 WhatsApp Automation Module")
    print("=" * 50)

    wa = WhatsAppAutomation()

    if not wa.is_configured():
        print("⚠️  WhatsApp API not configured")
        print("Set these environment variables:")
        print("  - WHATSAPP_API_KEY")
        print("  - WHATSAPP_BUSINESS_ACCOUNT_ID")
        print("  - WHATSAPP_PHONE_NUMBER_ID")
        return 1

    print("✅ WhatsApp API configured")
    print(f"Account: {wa.account_id}")
    print(f"Phone number ID: {wa.phone_number_id}")

    # Test message (won't actually send without valid API key)
    print("\n📤 Test message (simulation):")
    test_result = wa.send_message(
        "+966501234567",
        "السلام عليكم 👋\nهذا اختبار نظام WhatsApp",
    )

    print(json.dumps(test_result, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    exit(main())
