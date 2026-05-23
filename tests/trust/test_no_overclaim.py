"""ClaimGuard must refuse known overclaim patterns."""
from __future__ import annotations

from dealix.trust.claim_guard import ClaimGuard


def test_blocks_guarantee_claim():
    guard = ClaimGuard()
    assert not guard.is_safe("We guarantee a 10x return for every client.")


def test_blocks_certified_partner_claim():
    guard = ClaimGuard()
    assert not guard.is_safe("Dealix is certified by Acme and partners with Globex.")


def test_allows_safe_pitch():
    guard = ClaimGuard()
    text = "Dealix helps Saudi B2B teams build a ranked outbound pack in one week."
    assert guard.is_safe(text)


def test_register_can_extend_patterns():
    guard = ClaimGuard.from_register()
    # The default register should still include the baseline patterns.
    assert not guard.is_safe("award-winning")
