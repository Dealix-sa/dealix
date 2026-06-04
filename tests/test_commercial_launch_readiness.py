"""Tests for the Commercial Launch readiness gate."""

from __future__ import annotations

from dealix.commercial_launch.readiness import evaluate_readiness


def test_readiness_passes_overall() -> None:
    report = evaluate_readiness(target=400, run_generation=True)
    failed = [c.name for c in report.checks if not c.passed]
    assert report.passed, f"failed checks: {failed}"


def test_five_verticals_check() -> None:
    report = evaluate_readiness(run_generation=False)
    check = next(c for c in report.checks if c.name == "five_verticals_locked")
    assert check.passed


def test_offer_ladder_conservative_check() -> None:
    report = evaluate_readiness(run_generation=False)
    check = next(c for c in report.checks if c.name == "offer_ladder_conservative")
    assert check.passed


def test_channel_policy_blocks_send_check() -> None:
    report = evaluate_readiness(run_generation=False)
    check = next(c for c in report.checks if c.name == "channel_policy_blocks_send")
    assert check.passed


def test_safety_scan_clean_check() -> None:
    report = evaluate_readiness(run_generation=False)
    check = next(c for c in report.checks if c.name == "safety_scan_clean")
    assert check.passed


def test_go_no_go_flags() -> None:
    report = evaluate_readiness(run_generation=False)
    g = report.go_no_go
    assert g["go_for_draft_generation"] is True
    assert g["go_for_founder_manual_review"] is True
    assert g["no_go_for_automated_sending"] is True
    assert g["no_go_for_whatsapp_cold_outreach"] is True
    assert g["no_go_for_linkedin_automation"] is True


def test_docs_present_check() -> None:
    report = evaluate_readiness(run_generation=False)
    check = next(c for c in report.checks if c.name == "docs_present")
    assert check.passed, check.detail
