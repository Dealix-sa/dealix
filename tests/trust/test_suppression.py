"""Tests for `dealix/trust/suppression.py` — `docs/trust/SUPPRESSION_LIST_POLICY.md`."""

from __future__ import annotations

from pathlib import Path

import pytest

from dealix.trust.suppression import (
    SuppressionList,
    SuppressionViolation,
    assert_not_suppressed,
    normalize,
    set_default_list,
)


def test_email_normalization() -> None:
    assert normalize("email", "Foo+test@Example.com") == "foo@example.com"
    assert normalize("email", "  user@example.com  ") == "user@example.com"


def test_linkedin_normalization() -> None:
    assert (
        normalize("linkedin", "https://www.linkedin.com/in/abc/") == "linkedin:abc"
    )
    assert normalize("linkedin", "linkedin.com/in/abc") == "linkedin:abc"


def test_phone_normalization() -> None:
    assert normalize("phone", "+966 555-12-34-567") == "phone:9665551234567"
    assert normalize("phone", "+966 (555) 1234567") == "phone:9665551234567"


def test_domain_normalization() -> None:
    assert normalize("domain", "https://Example.com/path") == "domain:example.com"


def test_add_and_check_membership() -> None:
    lst = SuppressionList()
    assert not lst.is_suppressed("email", "user@example.com")
    lst.add(
        "email",
        "User@Example.com",
        reason="explicit opt-out",
        source="reply",
        owner="founder",
    )
    assert lst.is_suppressed("email", "user@example.com")
    assert lst.is_suppressed("email", "user+abuse@example.com")  # +tag normalized


def test_add_is_idempotent_monotonic() -> None:
    lst = SuppressionList()
    first = lst.add("email", "x@y.com", reason="r1", source="s", owner="founder")
    second = lst.add("email", "x@y.com", reason="r2", source="s", owner="founder")
    # Monotonic — re-adding the same identifier returns the original entry,
    # so the original metadata (reason etc.) is preserved.
    assert first.reason == second.reason == "r1"
    assert len(lst) == 1


def test_assert_not_suppressed_raises() -> None:
    lst = SuppressionList()
    lst.add("email", "user@example.com", reason="opt-out", source="reply", owner="founder")
    set_default_list(lst)
    try:
        with pytest.raises(SuppressionViolation):
            assert_not_suppressed("email", "USER@example.com")
    finally:
        # Reset to a fresh empty list to avoid leaking into other tests.
        set_default_list(SuppressionList())


def test_csv_round_trip(tmp_path: Path) -> None:
    csv_path = tmp_path / "suppression.csv"
    lst = SuppressionList(csv_path=csv_path)
    lst.add("email", "a@b.com", reason="opt-out", source="reply", owner="founder")
    lst.add("linkedin", "linkedin.com/in/abc", reason="suppression", source="manual", owner="founder")

    # Reload from disk into a fresh instance.
    reloaded = SuppressionList(csv_path=csv_path)
    assert reloaded.is_suppressed("email", "a@b.com")
    assert reloaded.is_suppressed("linkedin", "https://linkedin.com/in/abc/")
    assert len(reloaded) == 2
