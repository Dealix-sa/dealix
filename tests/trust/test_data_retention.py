"""Tests for `dealix/trust/data_retention.py`."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from dealix.trust.data_retention import (
    DataCategory,
    RetentionRecord,
    build_deletion_report,
    is_eligible_for_deletion,
    retention_days,
)


def _record(category: DataCategory, days_old: int, dpa_override: int | None = None) -> RetentionRecord:
    return RetentionRecord(
        record_id=f"r-{category.value}-{days_old}",
        category=category,
        last_touched_at=datetime.now(UTC) - timedelta(days=days_old),
        dpa_override_days=dpa_override,
    )


def test_indefinite_categories_never_eligible() -> None:
    assert retention_days(DataCategory.PUBLIC_LEAD) is None
    rec = _record(DataCategory.PUBLIC_LEAD, days_old=10_000)
    assert not is_eligible_for_deletion(rec)


def test_buyer_contact_eligible_after_24_months() -> None:
    fresh = _record(DataCategory.BUYER_CONTACT, days_old=100)
    stale = _record(DataCategory.BUYER_CONTACT, days_old=800)
    assert not is_eligible_for_deletion(fresh)
    assert is_eligible_for_deletion(stale)


def test_financial_record_retains_10_years() -> None:
    nine_years = _record(DataCategory.FINANCIAL_RECORD, days_old=9 * 365)
    eleven_years = _record(DataCategory.FINANCIAL_RECORD, days_old=11 * 365)
    assert not is_eligible_for_deletion(nine_years)
    assert is_eligible_for_deletion(eleven_years)


def test_dpa_override_shortens_window() -> None:
    rec = _record(DataCategory.CLIENT_CONFIDENTIAL, days_old=45, dpa_override=30)
    assert is_eligible_for_deletion(rec)


def test_build_deletion_report_segregates_eligible() -> None:
    records = [
        _record(DataCategory.BUYER_CONTACT, days_old=100),
        _record(DataCategory.BUYER_CONTACT, days_old=800),
        _record(DataCategory.PUBLIC_LEAD, days_old=10_000),
        _record(DataCategory.FINANCIAL_RECORD, days_old=11 * 365),
    ]
    report = build_deletion_report(records)
    assert len(report.eligible) == 2
    assert len(report.not_eligible) == 2
    summary = report.summary()
    assert summary["eligible"] == 2
    assert summary["by_category"]["buyer_contact"] == 1
    assert summary["by_category"]["financial_record"] == 1
