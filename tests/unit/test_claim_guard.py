"""Unit tests for the ClaimGuard pattern matcher."""
from __future__ import annotations

from dealix.trust.claim_guard import ClaimGuard


def test_default_patterns_block_guarantee():
    assert ClaimGuard().scan("guaranteed result") != []


def test_default_patterns_block_proven():
    assert ClaimGuard().scan("proven framework") != []


def test_safe_text_returns_no_violations():
    text = "We help Saudi B2B teams build outbound packs in one week."
    assert ClaimGuard().scan(text) == []


def test_custom_patterns_only():
    guard = ClaimGuard(forbidden=(r"\bsecret sauce\b",))
    assert guard.scan("our secret sauce") != []
    assert guard.scan("guaranteed") == []
