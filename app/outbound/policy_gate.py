"""Policy gates for controlled live outbound.

Implements the Dealix rule: "no uncontrolled external send".
A message may only go live if every required gate passes.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from app.outbound.config import OutboundSettings
from app.outbound.models import Channel, OutboundContact, OutboundMessage, PolicyVerdict


class PolicyGate:
    """Evaluates whether a message is allowed to leave the system."""

    # Phrases that imply guaranteed returns.
    GUARANTEED_ROI_PATTERNS = (
        r"\bضمان\s+(عائد|ربح|ROI|عائد استثمار)",
        r"\bمضمون\s+(عائد|ربح|نمو|نتيجة)",
        r"\bguaranteed\s+(roi|return|profit|result|revenue)",
        r"\b100%\s+(return|roi|profit|guarantee)",
        r"\bتضاعف\s+(?:إيراداتك|مبيعاتك|أرباحك)\s+في\s+\d+",
        r"\bdouble\s+your\s+(revenue|sales|profit)\s+in\s+\d+",
    )

    # Fake claim / overclaim indicators.
    FAKE_CLAIM_PATTERNS = (
        r"\bأكبر\s+شركة\s+(?:AI|ذكاء اصطناعي)\s+في\s+(?:السعودية|العالم)",
        r"\bالوحيد\s+(?:الذي|التي)\s+(?:تقدم|تقدّم|يقدم|توفّر|يوفّر)",
        r"#1\s+(?:AI|revenue|sales)\s+(?:company|platform|tool)",
        r"\bthe\s+only\s+(?:AI|platform|tool)\s+that\s+(?:guarantees|promises)",
        r"\bفوري\s+100%",
        r"\binstant\s+100%",
    )

    def __init__(self, settings: OutboundSettings | None = None) -> None:
        self.settings = settings or OutboundSettings()
        self._roi_regex = [re.compile(p, re.IGNORECASE) for p in self.GUARANTEED_ROI_PATTERNS]
        self._fake_regex = [re.compile(p, re.IGNORECASE) for p in self.FAKE_CLAIM_PATTERNS]

    def evaluate(
        self,
        contact: OutboundContact,
        message: OutboundMessage,
        approved_by: str | None = None,
    ) -> PolicyVerdict:
        """Return a PolicyVerdict; ok=True only if all gates pass."""
        blockers: list[str] = []
        warnings: list[str] = []

        # 1. Master kill switch
        if not self.settings.external_send_enabled:
            blockers.append("EXTERNAL_SEND_ENABLED=false")

        if self.settings.outbound_mode not in ("controlled_live", "live"):
            blockers.append(f"OUTBOUND_MODE={self.settings.outbound_mode} (not controlled_live/live)")

        # 2. Channel-specific master switches
        if message.channel == Channel.EMAIL and not self.settings.email_send_enabled:
            blockers.append("EMAIL_SEND_ENABLED=false")

        if message.channel == Channel.WHATSAPP and not self.settings.whatsapp_send_enabled:
            blockers.append("WHATSAPP_SEND_ENABLED=false")

        # 3. Approval gate
        if self.settings.outbound_require_approval and not approved_by and message.status != "approved":
            blockers.append("Message not approved")

        # 4. Verified target gate
        if self.settings.outbound_require_verified_target:
            if contact.verification_status not in ("verified", "high"):
                blockers.append(
                    f"Target verification_status={contact.verification_status} (required verified/high)"
                )

        # 5. Source URL gate
        if self.settings.outbound_require_source_url:
            if not contact.source_url or not contact.source_url.startswith(("http://", "https://")):
                blockers.append("Missing valid source_url")

        # 6. Channel-specific consent / opt-out gates
        if message.channel == Channel.EMAIL:
            if contact.email_opt_out:
                blockers.append("Contact email opted out")
            if self.settings.email_require_unsubscribe and "unsubscribe" not in message.body.lower():
                if "إلغاء الاشتراك" not in message.body and "إيقاف" not in message.body:
                    blockers.append("Email body missing unsubscribe/opt-out link")
            if not contact.email:
                blockers.append("Contact has no email address")

        if message.channel == Channel.WHATSAPP:
            if not self.settings.whatsapp_allow_live_send:
                blockers.append("WHATSAPP_ALLOW_LIVE_SEND=false")
            if self.settings.whatsapp_require_opt_in and not contact.whatsapp_opt_in:
                blockers.append("WhatsApp opt-in missing")
            if contact.whatsapp_opt_out:
                blockers.append("WhatsApp opted out")
            if self.settings.whatsapp_require_approved_template and not message.template_name:
                blockers.append("WhatsApp template_name missing")
            if not contact.whatsapp and not contact.phone:
                blockers.append("Contact has no phone/WhatsApp number")

        # 7. Content safety gates
        if self.settings.outbound_block_guaranteed_roi:
            for regex in self._roi_regex:
                if regex.search(message.body) or (message.subject and regex.search(message.subject)):
                    blockers.append(f"Guaranteed ROI/overclaim detected: {regex.pattern[:40]}")
                    break

        if self.settings.outbound_block_fake_claims:
            for regex in self._fake_regex:
                if regex.search(message.body) or (message.subject and regex.search(message.subject)):
                    blockers.append(f"Fake/absolute claim detected: {regex.pattern[:40]}")
                    break

        # 8. Empty body
        if not message.body or not message.body.strip():
            blockers.append("Message body empty")

        return PolicyVerdict(
            ok=len(blockers) == 0,
            channel=message.channel,
            reason="; ".join(blockers) if blockers else "All gates passed",
            blockers=blockers,
            warnings=warnings,
        )

    def approve(self, message: OutboundMessage, approved_by: str) -> OutboundMessage:
        """Mark a message as approved by a human operator."""
        from datetime import datetime

        message.status = "approved"  # type: ignore[assignment]
        message.approved_by = approved_by
        message.approved_at = datetime.utcnow()
        return message
