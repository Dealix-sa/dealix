"""SuppressionList behavior."""
from __future__ import annotations

from dealix.trust.suppression import SuppressionList


def test_add_is_idempotent():
    s = SuppressionList()
    assert s.add("a@example.com") is True
    assert s.add("a@example.com") is False
    assert len(s.entries) == 1


def test_normalizes_case_and_whitespace():
    s = SuppressionList()
    s.add(" A@Example.com  ")
    assert s.contains("a@example.com")


def test_filter_excludes_suppressed():
    s = SuppressionList()
    s.add("dropme@example.com")
    out = s.filter(["dropme@example.com", "keepme@example.com"])
    assert out == ["keepme@example.com"]


def test_remove_returns_true_only_when_present():
    s = SuppressionList()
    s.add("x@example.com")
    assert s.remove("x@example.com") is True
    assert s.remove("x@example.com") is False
