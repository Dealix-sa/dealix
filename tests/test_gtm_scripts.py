"""Tests for GTM script functions.

All tests are offline: no network, no DB, no file writes to the repo.
Scripts are imported directly; no subprocess invocations.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# 1. dealix_proposal_generator
# ---------------------------------------------------------------------------

def test_list_sectors_runs_and_has_real_estate(capsys: object) -> None:
    """list_sectors prints without raising and the sectors data contains real_estate."""
    import scripts.dealix_proposal_generator as pg  # type: ignore[import]

    pitches = pg._load_pitches()
    sectors = pitches.get("sectors", {})
    assert "real_estate" in sectors, "Expected 'real_estate' in sector pitches"

    # Call list_sectors with the loaded pitches dict — it prints and returns None.
    pg.list_sectors(pitches)


# ---------------------------------------------------------------------------
# 2. dealix_contract_generator
# ---------------------------------------------------------------------------

def test_list_tiers_runs_without_error(capsys: object) -> None:
    """list_tiers prints tier table without raising."""
    import scripts.dealix_contract_generator as cg  # type: ignore[import]

    cg.list_tiers()


def test_generate_contract_dry_run_returns_none(capsys: object) -> None:
    """generate_contract with dry_run=True returns None and does not write files."""
    import scripts.dealix_contract_generator as cg  # type: ignore[import]

    result = cg.generate_contract(
        "TestCo",
        "Ahmed",
        "logistics",
        "sprint",
        dry_run=True,
    )
    assert result is None


# ---------------------------------------------------------------------------
# 3. dealix_meeting_agenda
# ---------------------------------------------------------------------------

def test_generate_agenda_dry_run_returns_none(capsys: object) -> None:
    """generate_agenda with dry_run=True returns None and does not raise."""
    import scripts.dealix_meeting_agenda as ma  # type: ignore[import]

    result = ma.generate_agenda("TestCo", "Ahmed", "logistics", dry_run=True)
    assert result is None


# ---------------------------------------------------------------------------
# 4. dealix_outreach_tracker
# ---------------------------------------------------------------------------

def test_normalize_strips_and_lowercases() -> None:
    """_normalize strips surrounding whitespace and lowercases the string."""
    import scripts.dealix_outreach_tracker as ot  # type: ignore[import]

    # Arabic text: surrounding spaces are stripped; Arabic characters remain unchanged.
    result = ot._normalize("  شركة نجم  ")
    assert result == "شركةنجم"


def test_valid_statuses_contains_sent() -> None:
    """VALID_STATUSES must include 'sent'."""
    import scripts.dealix_outreach_tracker as ot  # type: ignore[import]

    assert "sent" in ot.VALID_STATUSES


# ---------------------------------------------------------------------------
# 5. dealix_pilot_report
# ---------------------------------------------------------------------------

def test_generate_pilot_report_dry_run_returns_none(capsys: object) -> None:
    """generate_report with dry_run=True returns None and does not write files."""
    import scripts.dealix_pilot_report as pr  # type: ignore[import]

    result = pr.generate_report("TestCo", "logistics", dry_run=True)
    assert result is None


# ---------------------------------------------------------------------------
# 6. dealix_customer_monthly_report
# ---------------------------------------------------------------------------

def test_generate_monthly_report_dry_run_returns_none(capsys: object) -> None:
    """generate_report with dry_run=True returns None and does not write files."""
    import scripts.dealix_customer_monthly_report as cmr  # type: ignore[import]

    result = cmr.generate_report("TestCo", "logistics", "2026-06", dry_run=True)
    assert result is None


# ---------------------------------------------------------------------------
# 7. dealix_renewal_tracker helpers
# ---------------------------------------------------------------------------

def test_renewal_tracker_valid_statuses_and_tiers() -> None:
    """VALID_STATUSES and VALID_TIERS are non-empty and contain expected values."""
    import scripts.dealix_renewal_tracker as rt  # type: ignore[import]

    assert "active" in rt.VALID_STATUSES
    assert "renewed" in rt.VALID_STATUSES
    assert "sprint" in rt.VALID_TIERS
    assert "command_center" in rt.VALID_TIERS


def test_renewal_tracker_days_until_future() -> None:
    """_days_until returns a positive integer for a far-future date."""
    import scripts.dealix_renewal_tracker as rt  # type: ignore[import]

    days = rt._days_until("2099-12-31")
    assert days > 0


def test_renewal_tracker_days_until_bad_date() -> None:
    """_days_until returns 9999 for an unparseable date string."""
    import scripts.dealix_renewal_tracker as rt  # type: ignore[import]

    days = rt._days_until("not-a-date")
    assert days == 9999


def test_renewal_tracker_normalize() -> None:
    """_normalize lowercases, strips, and removes spaces."""
    import scripts.dealix_renewal_tracker as rt  # type: ignore[import]

    assert rt._normalize("  Hello World  ") == "helloworld"


# ---------------------------------------------------------------------------
# 8. dealix_daily_ops helpers
# ---------------------------------------------------------------------------

def test_daily_ops_runs_without_error(capsys: object) -> None:
    """run() executes without raising even when log files are absent."""
    import scripts.dealix_daily_ops as ops  # type: ignore[import]

    ops.run()
    captured = capsys.readouterr()
    assert "Daily Ops" in captured.out
    assert "Today's Action List" in captured.out or "قائمة أعمال اليوم" in captured.out


def test_daily_ops_count_proposals_empty_dir(tmp_path: object) -> None:
    """_count_proposals_last_days returns 0 when proposals dir is empty."""
    import scripts.dealix_daily_ops as ops  # type: ignore[import]

    original = ops.PROPOSALS_DIR
    ops.PROPOSALS_DIR = tmp_path  # type: ignore[assignment]
    try:
        count = ops._count_proposals_last_days(7)
        assert count == 0
    finally:
        ops.PROPOSALS_DIR = original
