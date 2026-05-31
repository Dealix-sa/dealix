"""Tests for OmniChannelOrchestrator."""
from __future__ import annotations

import pytest

from auto_client_acquisition.omni_channel_os.orchestrator import (
    OmniChannelOrchestrator,
    PipelineResult,
    _update_quota,
)
from auto_client_acquisition.omni_channel_os.schemas import (
    Company,
    CompanySize,
    DailyQuota,
    GCCCountry,
    Language,
    Sector,
)


def _company(**kwargs) -> Company:
    defaults = dict(
        name="TestCo",
        sector=Sector.legal,
        country=GCCCountry.KSA,
        language=Language.arabic,
        company_size=CompanySize.sme,
    )
    defaults.update(kwargs)
    return Company(**defaults)


@pytest.fixture()
def orchestrator() -> OmniChannelOrchestrator:
    return OmniChannelOrchestrator()


class TestOmniChannelOrchestrator:
    def test_run_batch_with_one_company_increments_total(
        self, orchestrator: OmniChannelOrchestrator
    ) -> None:
        company = _company(name="Al Nasser Law", sector=Sector.legal)
        result = orchestrator.run_batch([company])
        assert result.total_companies == 1

    def test_run_batch_errors_empty_for_valid_company(
        self, orchestrator: OmniChannelOrchestrator
    ) -> None:
        company = _company()
        result = orchestrator.run_batch([company])
        assert result.errors == []

    def test_run_batch_founder_queue_has_items_for_manual_channels(
        self, orchestrator: OmniChannelOrchestrator
    ) -> None:
        company = _company(sector=Sector.legal)
        result = orchestrator.run_batch([company])
        # Legal sector generates manual assets (email, linkedin) -> founder queue
        assert len(result.founder_queue) > 0

    def test_run_batch_total_assets_greater_than_zero(
        self, orchestrator: OmniChannelOrchestrator
    ) -> None:
        company = _company()
        result = orchestrator.run_batch([company])
        assert result.total_assets > 0

    def test_run_batch_quota_is_populated(
        self, orchestrator: OmniChannelOrchestrator
    ) -> None:
        company = _company()
        result = orchestrator.run_batch([company])
        assert result.quota is not None
        assert result.quota.company_briefs_done == 1

    def test_run_batch_quota_has_correct_date(
        self, orchestrator: OmniChannelOrchestrator
    ) -> None:
        company = _company()
        result = orchestrator.run_batch([company], date="2026-01-15")
        assert result.quota is not None
        assert result.quota.date == "2026-01-15"

    def test_run_batch_report_is_generated(
        self, orchestrator: OmniChannelOrchestrator
    ) -> None:
        company = _company()
        result = orchestrator.run_batch([company])
        assert result.report is not None

    def test_run_batch_multiple_companies(
        self, orchestrator: OmniChannelOrchestrator
    ) -> None:
        companies = [
            _company(name="Co A", sector=Sector.legal),
            _company(name="Co B", sector=Sector.facilities_management),
            _company(name="Co C", sector=Sector.consulting),
        ]
        result = orchestrator.run_batch(companies)
        assert result.total_companies == 3
        assert result.errors == []

    def test_run_batch_empty_input(
        self, orchestrator: OmniChannelOrchestrator
    ) -> None:
        result = orchestrator.run_batch([])
        assert result.total_companies == 0
        assert result.errors == []


class TestUpdateQuota:
    def test_email_increments_email_counter(self) -> None:
        quota = DailyQuota(date="2026-01-01")
        _update_quota(quota, "email_draft")
        assert quota.email_drafts_done == 1

    def test_linkedin_increments_linkedin_counter(self) -> None:
        quota = DailyQuota(date="2026-01-01")
        _update_quota(quota, "linkedin_connection_note")
        assert quota.linkedin_drafts_done == 1

    def test_whatsapp_increments_whatsapp_counter(self) -> None:
        quota = DailyQuota(date="2026-01-01")
        _update_quota(quota, "whatsapp_optin_reply")
        assert quota.whatsapp_drafts_done == 1

    def test_call_script_increments_call_scripts_counter(self) -> None:
        quota = DailyQuota(date="2026-01-01")
        _update_quota(quota, "call_script")
        assert quota.call_scripts_done == 1
