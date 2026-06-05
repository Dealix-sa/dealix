"""Contract tests for the Self-Growth and Distribution OS generators."""

from __future__ import annotations

from datetime import date

import pytest

from scripts.growth import _common
from scripts.growth.generate_case_safe_content import build_markdown, load_inputs
from scripts.growth.generate_content_calendar import _default_start, build_calendar
from scripts.growth.generate_experiment_backlog import build_records
from scripts.growth.generate_free_tool_specs import build_tools
from scripts.growth.generate_nurture_sequences import build_sequences
from scripts.growth.generate_partner_targets import build_rows
from scripts.growth.generate_sector_pages import build_pages
from scripts.growth.generate_template_library import build_templates

_ALLOWED = set(_common.ALLOWED_CTA)


def test_assert_single_cta_accepts_allowed() -> None:
    for cta in _common.ALLOWED_CTA:
        assert _common.assert_single_cta(cta) == cta


def test_assert_single_cta_rejects_unknown() -> None:
    with pytest.raises(ValueError):
        _common.assert_single_cta("Buy Now")


def test_build_tools_has_seven_single_cta_tools() -> None:
    tools = build_tools()
    assert len(tools) == 7
    assert all(t["cta"] in _ALLOWED for t in tools)
    assert [t["id"] for t in tools] == sorted(t["id"] for t in tools)


def test_build_templates_counts() -> None:
    templates = build_templates()
    assert sum(1 for t in templates if t["tier"] == "free") == 8
    assert sum(1 for t in templates if t["tier"] == "paid") == 5


def test_build_pages_ten_sectors_single_cta() -> None:
    pages = build_pages()
    assert len(pages) == 10
    assert all(p["cta"] in _ALLOWED for p in pages)
    assert all(p["slug"].startswith("/ar/industries/") for p in pages)


def test_build_sequences_one_cta_per_message() -> None:
    seq = build_sequences()
    assert len(seq["seven_day"]) == 8
    assert len(seq["thirty_day"]) == 4
    for msg in seq["seven_day"] + seq["thirty_day"]:
        assert msg["cta"] in _ALLOWED


def test_build_rows_seven_partner_types() -> None:
    rows = build_rows()
    assert len(rows) == 7
    # single_cta is the last column.
    assert all(row[-1] in _ALLOWED for row in rows)


def test_build_records_backlog_unique_ids() -> None:
    records = build_records()
    ids = [r["id"] for r in records]
    assert len(ids) == len(set(ids))
    assert all(r["status"] == "backlog" for r in records)


def test_build_calendar_length_and_cta() -> None:
    entries = build_calendar(date(2026, 6, 7), 5)
    assert len(entries) == 35
    assert all(e["single_cta"] in _ALLOWED for e in entries)
    assert all(len(e["repurpose_targets"]) == 12 for e in entries)


def test_build_calendar_rejects_zero_weeks() -> None:
    with pytest.raises(ValueError):
        build_calendar(date(2026, 6, 7), 0)


def test_default_start_is_sunday() -> None:
    start = _default_start(date(2026, 6, 5))
    assert start.weekday() == 6


def test_case_safe_markdown_has_no_customer_name() -> None:
    records = load_inputs()
    markdown = build_markdown(records)
    assert "customer_name" not in markdown
    assert "company_name" not in markdown
    # The only permitted use of "logo" is the disclaimer that no logo appears.
    assert "no customer name or logo appears" in markdown.lower()
    assert "not a guarantee" in markdown
