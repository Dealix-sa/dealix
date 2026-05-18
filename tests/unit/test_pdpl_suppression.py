"""
Unit tests — PDPL contactability (suppression) check.
اختبارات الوحدة — فحص قابلية التواصل وفق نظام حماية البيانات الشخصية.

Tests that contactability_check correctly enforces PDPL consent rules:
- WHATSAPP_TEMPLATE requires explicit active (GRANTED) consent → BLOCKED without it
- WHATSAPP_TEMPLATE with withdrawn consent → BLOCKED
- Email inbound is customer-initiated → SAFE without consent
- EMAIL_DRAFT requires active consent → not SAFE without it

These tests exercise the real ConsentRegistry rather than a mock so the
suppression gate is verified end-to-end.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.customer_data_plane.consent_registry import ConsentRegistry
from auto_client_acquisition.customer_data_plane.contactability import contactability_check
from auto_client_acquisition.customer_data_plane.schemas import (
    ChannelKind,
    ContactabilityVerdict,
)


# ── Fixtures ───────────────────────────────────────────────────────

@pytest.fixture()
def registry() -> ConsentRegistry:
    """Fresh, isolated consent registry per test."""
    return ConsentRegistry()


# ── Tests ──────────────────────────────────────────────────────────

class TestWhatsAppTemplateSuppression:
    """WhatsApp template messages require active consent (PDPL Article 4)."""

    def test_active_consent_is_safe(self, registry: ConsentRegistry) -> None:
        registry.grant(contact_id="c001", channel=ChannelKind.WHATSAPP_TEMPLATE)
        result = contactability_check(
            contact_id="c001",
            channel=ChannelKind.WHATSAPP_TEMPLATE,
            registry=registry,
        )
        assert result.verdict == ContactabilityVerdict.SAFE

    def test_no_record_is_blocked(self, registry: ConsentRegistry) -> None:
        result = contactability_check(
            contact_id="c002",
            channel=ChannelKind.WHATSAPP_TEMPLATE,
            registry=registry,
        )
        assert result.verdict == ContactabilityVerdict.BLOCKED

    def test_withdrawn_consent_is_blocked(self, registry: ConsentRegistry) -> None:
        registry.grant(contact_id="c003", channel=ChannelKind.WHATSAPP_TEMPLATE)
        registry.withdraw(contact_id="c003", channel=ChannelKind.WHATSAPP_TEMPLATE)
        result = contactability_check(
            contact_id="c003",
            channel=ChannelKind.WHATSAPP_TEMPLATE,
            registry=registry,
        )
        assert result.verdict == ContactabilityVerdict.BLOCKED

    def test_unknown_consent_is_blocked(self, registry: ConsentRegistry) -> None:
        # A contact with consent only on a different channel must not be
        # contactable on WHATSAPP_TEMPLATE.
        registry.grant(contact_id="c004", channel=ChannelKind.EMAIL_DRAFT)
        result = contactability_check(
            contact_id="c004",
            channel=ChannelKind.WHATSAPP_TEMPLATE,
            registry=registry,
        )
        assert result.verdict == ContactabilityVerdict.BLOCKED


class TestEmailSuppression:
    """Email drafts require active consent; inbound email is always safe."""

    def test_email_inbound_is_always_safe(self, registry: ConsentRegistry) -> None:
        result = contactability_check(
            contact_id="c010",
            channel=ChannelKind.EMAIL_INBOUND,
            registry=registry,
        )
        assert result.verdict == ContactabilityVerdict.SAFE

    def test_email_draft_needs_active_consent(self, registry: ConsentRegistry) -> None:
        result = contactability_check(
            contact_id="c011",
            channel=ChannelKind.EMAIL_DRAFT,
            registry=registry,
        )
        assert result.verdict != ContactabilityVerdict.SAFE

    def test_email_draft_with_active_consent_is_safe(
        self, registry: ConsentRegistry
    ) -> None:
        registry.grant(contact_id="c012", channel=ChannelKind.EMAIL_DRAFT)
        result = contactability_check(
            contact_id="c012",
            channel=ChannelKind.EMAIL_DRAFT,
            registry=registry,
        )
        assert result.verdict == ContactabilityVerdict.SAFE


class TestResultNotes:
    """Every contactability result must carry compliance safety notes."""

    def test_blocked_result_has_notes(self, registry: ConsentRegistry) -> None:
        registry.grant(contact_id="c020", channel=ChannelKind.WHATSAPP_TEMPLATE)
        registry.withdraw(contact_id="c020", channel=ChannelKind.WHATSAPP_TEMPLATE)
        result = contactability_check(
            contact_id="c020",
            channel=ChannelKind.WHATSAPP_TEMPLATE,
            registry=registry,
        )
        assert result.verdict == ContactabilityVerdict.BLOCKED
        assert result.safety_notes

    def test_safe_result_has_notes(self, registry: ConsentRegistry) -> None:
        result = contactability_check(
            contact_id="c021",
            channel=ChannelKind.WHATSAPP_INBOUND,
            registry=registry,
        )
        assert result.verdict == ContactabilityVerdict.SAFE
        assert result.safety_notes
