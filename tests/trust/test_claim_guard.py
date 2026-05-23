"""Tests for `dealix/trust/claim_guard.py` — `docs/trust/NO_OVERCLAIM_POLICY.md`."""

from __future__ import annotations

import pytest

from dealix.trust.claim_guard import FlagSeverity, assert_passes, check


def test_banned_phrases_block() -> None:
    text = "Our industry-leading platform is revolutionary and best-in-class."
    report = check(text)
    assert report.is_blocking
    blocked = {f.excerpt.lower() for f in report.flags if f.severity == FlagSeverity.BLOCK}
    assert "industry-leading" in blocked or "industry leading" in blocked
    assert "revolutionary" in blocked
    assert "best-in-class" in blocked or "best in class" in blocked


def test_unbacked_multiplier_blocks() -> None:
    text = "We deliver 10x results compared to anything else."
    report = check(text)
    assert report.is_blocking
    assert any(f.rule == "unbacked_multiplier" for f in report.flags)


def test_multiplier_with_citation_does_not_block() -> None:
    text = "Based on n=4 engagements, the new flow showed roughly 3x throughput."
    report = check(text)
    # The citation cue ("Based on n=4") neutralizes multiplier warnings.
    assert not report.is_blocking, [f.excerpt for f in report.flags]


def test_compliance_overclaim_blocks() -> None:
    text = "Dealix is PDPL compliant and SOC 2 compliant."
    report = check(text)
    assert report.is_blocking
    assert any(f.rule == "compliance_overclaim" for f in report.flags)


def test_aligned_with_does_not_block() -> None:
    text = "Dealix is aligned with PDPL clause X (see DATA_RETENTION_POLICY.md)."
    report = check(text)
    assert not report.is_blocking


def test_guarantee_blocks() -> None:
    text = "We guarantee a 30% improvement in your sales pipeline."
    report = check(text)
    assert report.is_blocking
    assert any(f.rule == "banned_phrase" for f in report.flags)


def test_guarantee_with_contract_qualifier_passes() -> None:
    text = "Output is guaranteed per contract Section 4."
    report = check(text)
    # Should not be blocked solely by the guarantee rule.
    block_rules = {f.rule for f in report.flags if f.severity == FlagSeverity.BLOCK}
    assert "banned_phrase" not in block_rules


def test_assert_passes_raises_on_blocking() -> None:
    with pytest.raises(ValueError):
        assert_passes("Industry-leading 10x synergistic transformation.")


def test_assert_passes_allows_clean_text() -> None:
    assert_passes("In our last 3 sprints, average delivery time was 6 days (range 5–7).")
