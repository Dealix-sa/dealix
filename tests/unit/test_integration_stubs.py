"""Coverage tests for integration stub modules that are currently at 0%.

These tests import and exercise the public interfaces of integration stubs
that ship disabled-by-default (LinkedIn, n8n) and template modules
(arabic_templates) to ensure coverage gates pass in CI.

No external API calls are made — these stubs are safe by design.
"""
from __future__ import annotations

import os

import pytest

os.environ.setdefault("APP_ENV", "test")


# ── arabic_templates ──────────────────────────────────────────────────────────

def test_arabic_templates_email_template_registry():
    from integrations.arabic_templates import EMAIL_TEMPLATES, EmailTemplate

    assert len(EMAIL_TEMPLATES) >= 5
    tmpl = EMAIL_TEMPLATES["outreach_initial"]
    assert isinstance(tmpl, EmailTemplate)
    assert tmpl.template_id == "outreach_initial"
    assert tmpl.category == "outreach"
    assert tmpl.channel == "email"
    assert "{company_name}" in tmpl.subject_ar or "{company_name}" in tmpl.subject_en


def test_arabic_templates_whatsapp_template_registry():
    from integrations.arabic_templates import WHATSAPP_TEMPLATES, WhatsAppTemplate

    assert len(WHATSAPP_TEMPLATES) >= 3
    tmpl = WHATSAPP_TEMPLATES["initial_outreach"]
    assert isinstance(tmpl, WhatsAppTemplate)
    assert tmpl.channel == "whatsapp"
    assert tmpl.category == "outreach"


def test_arabic_templates_render_email_ar():
    from integrations.arabic_templates import render_template

    result = render_template(
        "outreach_initial",
        "email",
        {
            "contact_name": "أحمد",
            "company_name": "ديليكس",
            "service_description": "أتمتة المبيعات",
            "trigger_reason": "نمو الشركة",
            "buyer_company": "شركة التقنية",
            "value_proposition": "زيادة المبيعات",
            "sender_name": "سامي",
            "phone_number": "+966501234567",
        },
        locale="ar",
    )
    assert result["channel"] == "email"
    assert result["locale"] == "ar"
    assert "أحمد" in result["body"]
    assert "subject" in result


def test_arabic_templates_render_email_en():
    from integrations.arabic_templates import render_template

    result = render_template(
        "outreach_initial",
        "email",
        {
            "contact_name": "Ahmed",
            "company_name": "Dealix",
            "service_description": "sales automation",
            "trigger_reason": "company growth",
            "buyer_company": "Tech Co",
            "value_proposition": "increase revenue",
            "sender_name": "Sami",
            "phone_number": "+966501234567",
        },
        locale="en",
    )
    assert "Ahmed" in result["body"]
    assert result["locale"] == "en"


def test_arabic_templates_render_whatsapp():
    from integrations.arabic_templates import render_template

    result = render_template(
        "initial_outreach",
        "whatsapp",
        {
            "contact_name": "أحمد",
            "sender_name": "سامي",
            "company_name": "ديليكس",
            "trigger_reason": "نمو الشركة",
            "topic": "أتمتة المبيعات",
        },
        locale="ar",
    )
    assert result["channel"] == "whatsapp"
    assert "message" in result


def test_arabic_templates_render_unknown_template_raises():
    from integrations.arabic_templates import render_template

    with pytest.raises(ValueError, match="not found"):
        render_template("nonexistent_id", "email", {})


def test_arabic_templates_render_unknown_channel_raises():
    from integrations.arabic_templates import render_template

    with pytest.raises(ValueError, match="Unknown channel"):
        render_template("outreach_initial", "fax", {})


def test_arabic_templates_list_all():
    from integrations.arabic_templates import list_templates

    templates = list_templates()
    assert len(templates) >= 10
    channels = {t["channel"] for t in templates}
    assert "email" in channels
    assert "whatsapp" in channels


def test_arabic_templates_list_email_only():
    from integrations.arabic_templates import list_templates

    templates = list_templates(channel="email")
    assert all(t["channel"] == "email" for t in templates)
    assert len(templates) >= 5


def test_arabic_templates_list_whatsapp_only():
    from integrations.arabic_templates import list_templates

    templates = list_templates(channel="whatsapp")
    assert all(t["channel"] == "whatsapp" for t in templates)
    assert len(templates) >= 3


# ── linkedin ──────────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_linkedin_client_is_disabled_by_default():
    from integrations.linkedin import LinkedInClient, LinkedInPostResult

    client = LinkedInClient()
    result = await client.post_text("Test post")
    assert isinstance(result, LinkedInPostResult)
    assert result.disabled is True
    assert result.success is False
    assert result.post_urn is None
    assert "disabled" in result.reason.lower() or "ToS" in result.reason


def test_linkedin_post_result_dataclass():
    from integrations.linkedin import LinkedInPostResult

    r = LinkedInPostResult(success=False, disabled=True, reason="ToS compliance", post_urn="urn:123")
    assert r.post_urn == "urn:123"
    assert r.disabled is True


# ── n8n ───────────────────────────────────────────────────────────────────────

def test_n8n_result_dataclass():
    from integrations.n8n import N8NResult

    r = N8NResult(success=True, status_code=200, response_data={"ok": True})
    assert r.success is True
    assert r.status_code == 200
    assert r.error is None


@pytest.mark.anyio
async def test_n8n_client_unconfigured_returns_error():
    """N8NClient.send_event returns error when N8N_WEBHOOK_URL is not set."""
    from integrations.n8n import N8NClient

    client = N8NClient()
    # In test mode, n8n_webhook_url is not set → should return error immediately.
    if not client.configured:
        result = await client.send_event("test_event", {"key": "value"})
        assert result.success is False
        assert result.error is not None


def test_n8n_client_configured_property():
    from integrations.n8n import N8NClient

    client = N8NClient()
    assert isinstance(client.configured, bool)


# ── calendar ──────────────────────────────────────────────────────────────────

def test_calendar_event_result_dataclass():
    from integrations.calendar import CalendarEventResult

    r = CalendarEventResult(
        success=True, provider="google", event_id="evt123", html_link="https://cal.google.com/evt"
    )
    assert r.success is True
    assert r.provider == "google"
    assert r.meeting_link is None
    assert r.error is None


@pytest.mark.anyio
async def test_google_calendar_unconfigured_returns_error():
    from integrations.calendar import GoogleCalendarClient

    client = GoogleCalendarClient()
    if not client.configured:
        from datetime import datetime, timezone
        result = await client.create_event(
            summary="Test",
            description="Test event",
            start=datetime(2026, 6, 1, 10, 0, tzinfo=timezone.utc),
            end=datetime(2026, 6, 1, 11, 0, tzinfo=timezone.utc),
        )
        assert result.success is False
        assert result.provider == "google"
        assert result.error is not None


def test_google_calendar_configured_property():
    from integrations.calendar import GoogleCalendarClient

    client = GoogleCalendarClient()
    assert isinstance(client.configured, bool)


@pytest.mark.anyio
async def test_calendly_list_events_unconfigured_returns_empty():
    from integrations.calendar import CalendlyClient

    client = CalendlyClient()
    if not client.configured:
        events = await client.list_scheduled_events()
        assert events == []


def test_calendly_scheduling_link_unconfigured():
    from integrations.calendar import CalendlyClient

    client = CalendlyClient()
    if not client.settings.calendly_user_uri:
        link = client.scheduling_link()
        assert link is None


def test_calendly_configured_property():
    from integrations.calendar import CalendlyClient

    client = CalendlyClient()
    assert isinstance(client.configured, bool)
