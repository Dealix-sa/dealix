"""Doctrine guards for the cold-email motion (Market Production OS).

These reinforce the non-negotiables for outbound email:
- every cold email must carry a working opt-out;
- subjects must not impersonate a reply/forward thread;
- guaranteed-outcome language is blocked;
- a suppressed (opted-out) recipient is never re-contacted;
- 250 sends/day is NOT allowed from an unhealthy / un-warmed domain.
"""

from __future__ import annotations

from dealix.market_production_os.compliance_gate import check_draft
from dealix.market_production_os.draft_factory import build_draft
from dealix.market_production_os.models import email_sha256
from dealix.market_production_os.sending_ramp import allowed_sends

_SENDER = {
    "from_name": "Dealix",
    "from_email": "team@go.dealix-mail.sa",
    "physical_address": "Riyadh, KSA",
}


def _draft(**overrides):
    prospect = {
        "prospect_id": "pr_g",
        "company": "Guard Co (sample)",
        "sector": "marketing_agencies",
        "personalization_level": "P2",
        "personalization_note": "ملاحظة حقيقية",
        "language": "ar",
    }
    draft = build_draft(prospect, sender_identity=_SENDER, offer="revenue_diagnostic")
    draft.update(overrides)
    return draft


def test_cold_email_without_optout_is_blocked() -> None:
    res = check_draft(_draft(unsubscribe_included=False, unsubscribe_method="none"))
    assert res.allowed is False
    assert "missing_unsubscribe" in res.failures


def test_fake_reply_subject_is_blocked() -> None:
    assert check_draft(_draft(subject="Re: متابعة")).allowed is False
    assert check_draft(_draft(subject="Fwd: عرض")).allowed is False


def test_guaranteed_outcome_is_blocked() -> None:
    assert check_draft(_draft(body="نضمن لك نتائج مبيعات")).allowed is False
    assert check_draft(_draft(body="We guarantee results")).allowed is False


def test_suppressed_recipient_is_never_recontacted() -> None:
    h = email_sha256("opted-out@example.test")
    res = check_draft(_draft(), suppressed_hashes={h}, recipient_email_sha256=h)
    assert res.allowed is False
    assert "recipient_suppressed" in res.failures


def test_full_volume_blocked_from_unhealthy_domain() -> None:
    unhealthy = {
        "account_id": "x",
        "spf": True,
        "dkim": False,
        "dmarc": False,
        "warmup_status": "cold",
        "daily_cap": 250,
    }
    assert allowed_sends(3, unhealthy) == 0
