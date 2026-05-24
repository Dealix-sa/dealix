"""Trust guardrails block overclaim, runaway pricing, and silent partners."""

from __future__ import annotations

from dealix.hermes.core.schemas import TrustCheckOutcome
from dealix.hermes.trust.guardrails import (
    PRICING_CEILING_AUTONOMOUS_SAR,
    PRICING_FLOOR_SAR,
    TrustContext,
    trust_check,
)


def _ctx(**kw):  # type: ignore[no-untyped-def]
    return TrustContext(
        target_id=kw.get("target_id", "x"),
        target_kind=kw.get("target_kind", "message"),
        text=kw.get("text"),
        payload=kw.get("payload", {}),
        action=kw.get("action"),
        verified_partners=kw.get("verified_partners", []),
    )


def test_clean_message_passes() -> None:
    result = trust_check(_ctx(text="Quick note about our service."))
    assert result.outcome == TrustCheckOutcome.ALLOW
    assert result.violations == []


def test_overclaim_is_denied() -> None:
    result = trust_check(_ctx(text="100% ROI guaranteed for every client."))
    assert result.outcome == TrustCheckOutcome.DENY
    assert any(v.startswith("overclaim_pattern") for v in result.violations)


def test_arabic_overclaim_is_denied() -> None:
    result = trust_check(_ctx(text="نتائج مضمونة بدون مخاطر تمامًا."))
    assert result.outcome == TrustCheckOutcome.DENY


def test_unverified_partner_claim_is_denied() -> None:
    result = trust_check(_ctx(text="We are the official partner of MegaCorp."))
    assert result.outcome == TrustCheckOutcome.DENY


def test_verified_partner_claim_passes() -> None:
    result = trust_check(
        _ctx(
            text="MegaCorp — official partner of MegaCorp confirmed.",
            verified_partners=["MegaCorp"],
        )
    )
    assert result.outcome == TrustCheckOutcome.ALLOW


def test_pricing_below_floor_is_denied() -> None:
    result = trust_check(_ctx(payload={"price_sar": PRICING_FLOOR_SAR - 1}))
    assert result.outcome == TrustCheckOutcome.DENY
    assert any(v.startswith("pricing_below_floor") for v in result.violations)


def test_pricing_above_autonomous_ceiling_is_denied() -> None:
    result = trust_check(
        _ctx(payload={"price_sar": PRICING_CEILING_AUTONOMOUS_SAR + 1})
    )
    assert result.outcome == TrustCheckOutcome.DENY


def test_external_action_escalates() -> None:
    result = trust_check(_ctx(text="Hi there", action="send_external_message"))
    assert result.outcome == TrustCheckOutcome.ESCALATE
    assert any(v.startswith("requires_approval") for v in result.violations)


def test_sovereign_only_proposal_escalates() -> None:
    result = trust_check(_ctx(text="Hi", action="send_external_proposal"))
    assert result.outcome == TrustCheckOutcome.ESCALATE
    assert any(v.startswith("sovereign_only_action") for v in result.violations)


def test_sovereign_action_escalates() -> None:
    result = trust_check(_ctx(text="Hi", action="sign_contract"))
    assert result.outcome == TrustCheckOutcome.ESCALATE
