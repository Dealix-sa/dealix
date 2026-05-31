"""Trust-check doctrine: no overclaim, no fake partnerships, no PII leakage."""

from __future__ import annotations


def test_blocks_overclaim(orch):
    """No 3: لا Execution بلا Trust Check."""
    result = orch.trust_check.check(
        agent_id="copywriter",
        proposed_text="Our system has 100% accuracy and is infallible.",
    )
    assert not result.passed
    assert any("overclaim" in r for r in result.reasons)


def test_blocks_false_partnership(orch):
    result = orch.trust_check.check(
        agent_id="partner_pitch",
        proposed_text="We are partners with Aramco — let me show you our deal.",
    )
    assert not result.passed
    assert any("partnership" in r for r in result.reasons)


def test_pii_in_external_content_blocked(orch):
    result = orch.trust_check.check(
        agent_id="revenue_hunter",
        proposed_text="Cold outreach draft",
        context={"contains_pii": True, "audience": "external"},
    )
    assert not result.passed
    assert any("PII" in r for r in result.reasons)


def test_pricing_change_without_approval_blocked(orch):
    result = orch.trust_check.check(
        agent_id="pricing",
        proposed_text="proposing new pricing",
        context={"affects_pricing": True},
    )
    assert not result.passed
    assert any("pricing change" in r.lower() for r in result.reasons)


def test_clean_text_passes(orch):
    result = orch.trust_check.check(
        agent_id="copywriter",
        proposed_text="Dealix helps founders ship more proposals each week.",
    )
    assert result.passed
