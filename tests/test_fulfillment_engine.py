"""Tests for the Fulfillment & Client Success Engine.

Covers engagement creation, progress reports, renewal assessment,
engagement health, safety invariants, and bilingual output.
"""
from __future__ import annotations

import pytest

from dealix.company_intelligence.fulfillment_engine import (
    ClientEngagement,
    EngagementStatus,
    ProgressReport,
    RenewalAssessment,
    SatisfactionLevel,
    assess_renewal,
    calculate_engagement_health,
    create_engagement,
    generate_progress_report,
)

TENANT = "tenant_test_fulfillment"
SOURCE = "test_source"


# -----------------------------------------------------------------------
# Engagement creation
# -----------------------------------------------------------------------


class TestEngagementCreation:
    def test_diagnostic_engagement(self):
        eng = create_engagement(
            tenant_id=TENANT,
            client_name="Ahmad",
            client_company="TestCo",
            offer_type="free_diagnostic",
            source_id=SOURCE,
        )
        assert isinstance(eng, ClientEngagement)
        assert eng.offer_type == "free_diagnostic"
        assert eng.duration_days == 1
        assert len(eng.milestones) == 2  # data intake + deliver report
        assert eng.status == EngagementStatus.ONBOARDING
        assert eng.auto_charge is False
        assert eng.auto_renew is False

    def test_pilot_engagement(self):
        eng = create_engagement(
            tenant_id=TENANT,
            client_name="Faisal",
            client_company="CloudSoft",
            offer_type="revenue_command_pilot",
            engagement_value=10000.0,
            source_id=SOURCE,
        )
        assert eng.offer_type == "revenue_command_pilot"
        assert eng.duration_days == 30
        assert len(eng.milestones) == 8  # 8 standard pilot milestones
        assert eng.engagement_value == 10000.0

    def test_unknown_offer_type(self):
        eng = create_engagement(
            tenant_id=TENANT,
            client_name="Test",
            client_company="Co",
            offer_type="custom",
            source_id=SOURCE,
        )
        assert eng.duration_days == 30
        assert len(eng.milestones) == 0

    def test_deterministic_id(self):
        e1 = create_engagement(
            tenant_id=TENANT, client_name="Test",
            client_company="Co", offer_type="free_diagnostic",
            source_id=SOURCE,
        )
        e2 = create_engagement(
            tenant_id=TENANT, client_name="Test",
            client_company="Co", offer_type="free_diagnostic",
            source_id=SOURCE,
        )
        assert e1.engagement_id == e2.engagement_id
        assert e1.engagement_id.startswith("engagement_")

    def test_diagnostic_milestones_content(self):
        eng = create_engagement(
            tenant_id=TENANT, client_name="Test",
            client_company="Co", offer_type="free_diagnostic",
            source_id=SOURCE,
        )
        titles = [m.title for m in eng.milestones]
        assert "Data intake and sector analysis" in titles
        assert "Deliver diagnostic report" in titles

    def test_pilot_milestones_content(self):
        eng = create_engagement(
            tenant_id=TENANT, client_name="Test",
            client_company="Co", offer_type="revenue_command_pilot",
            source_id=SOURCE,
        )
        titles = [m.title for m in eng.milestones]
        assert "Onboarding and data collection" in titles
        assert "Company Brain v1 build" in titles
        assert "Stop/extend/redesign decision" in titles


# -----------------------------------------------------------------------
# Progress reports
# -----------------------------------------------------------------------


class TestProgressReport:
    def _make_engagement(self):
        return create_engagement(
            tenant_id=TENANT, client_name="Test",
            client_company="TestCo",
            offer_type="revenue_command_pilot",
            source_id=SOURCE,
        )

    def test_basic_report(self):
        eng = self._make_engagement()
        report = generate_progress_report(
            tenant_id=TENANT, engagement=eng,
            week_number=1, source_id=SOURCE,
        )
        assert isinstance(report, ProgressReport)
        assert report.report_period == "week_1"
        assert report.summary_ar
        assert report.summary_en
        assert report.approval_required is True

    def test_report_metrics(self):
        eng = self._make_engagement()
        report = generate_progress_report(
            tenant_id=TENANT, engagement=eng,
            week_number=1, source_id=SOURCE,
        )
        assert "milestones_completed" in report.metrics
        assert "milestones_total" in report.metrics
        assert "progress_percent" in report.metrics

    def test_deterministic_id(self):
        eng = self._make_engagement()
        r1 = generate_progress_report(
            tenant_id=TENANT, engagement=eng,
            week_number=1, source_id=SOURCE,
        )
        r2 = generate_progress_report(
            tenant_id=TENANT, engagement=eng,
            week_number=1, source_id=SOURCE,
        )
        assert r1.report_id == r2.report_id
        assert r1.report_id.startswith("report_")

    def test_bilingual_summary(self):
        eng = self._make_engagement()
        report = generate_progress_report(
            tenant_id=TENANT, engagement=eng,
            week_number=1, source_id=SOURCE,
        )
        # Arabic summary should contain Arabic text
        assert any(ord(c) > 0x600 for c in report.summary_ar)
        # English summary should have company name
        assert "TestCo" in report.summary_en


# -----------------------------------------------------------------------
# Renewal assessment
# -----------------------------------------------------------------------


class TestRenewalAssessment:
    def _make_engagement(self, **overrides):
        defaults = dict(
            tenant_id=TENANT, client_name="Test",
            client_company="TestCo",
            offer_type="revenue_command_pilot",
            source_id=SOURCE,
        )
        defaults.update(overrides)
        return create_engagement(**defaults)

    def test_basic_assessment(self):
        eng = self._make_engagement()
        assessment = assess_renewal(
            tenant_id=TENANT, engagement=eng, source_id=SOURCE,
        )
        assert isinstance(assessment, RenewalAssessment)
        assert 0 <= assessment.renewal_probability <= 100
        assert assessment.auto_renew is False
        assert assessment.auto_charge is False

    def test_diagnostic_upsell_opportunity(self):
        eng = self._make_engagement(offer_type="free_diagnostic")
        assessment = assess_renewal(
            tenant_id=TENANT, engagement=eng, source_id=SOURCE,
        )
        # Free diagnostic should suggest pilot upsell
        upsell_text = " ".join(assessment.upsell_opportunities)
        assert "Revenue Command Pilot" in upsell_text or "30" in upsell_text

    def test_deterministic_id(self):
        eng = self._make_engagement()
        a1 = assess_renewal(
            tenant_id=TENANT, engagement=eng, source_id=SOURCE,
        )
        a2 = assess_renewal(
            tenant_id=TENANT, engagement=eng, source_id=SOURCE,
        )
        assert a1.assessment_id == a2.assessment_id
        assert a1.assessment_id.startswith("renewal_")


# -----------------------------------------------------------------------
# Engagement health
# -----------------------------------------------------------------------


class TestEngagementHealth:
    def test_empty_engagements(self):
        health = calculate_engagement_health([])
        assert health["total_engagements"] == 0
        assert health["health"] == "no_data"

    def test_healthy_portfolio(self):
        eng = ClientEngagement(
            tenant_id=TENANT, client_name="Test",
            client_company="Co", offer_type="pilot",
            status=EngagementStatus.ACTIVE,
            satisfaction=SatisfactionLevel.SATISFIED,
            engagement_value=5000.0,
            auto_charge=False, auto_renew=False,
            source_id=SOURCE,
        )
        health = calculate_engagement_health([eng])
        assert health["active"] == 1
        assert health["total_value"] == 5000.0
        assert health["health"] in ("healthy", "excellent")

    def test_at_risk_portfolio(self):
        engs = [
            ClientEngagement(
                tenant_id=TENANT, client_name=f"Test{i}",
                client_company=f"Co{i}", offer_type="pilot",
                status=EngagementStatus.AT_RISK,
                auto_charge=False, auto_renew=False,
                source_id=SOURCE,
            )
            for i in range(5)
        ]
        health = calculate_engagement_health(engs)
        assert health["health"] == "critical"


# -----------------------------------------------------------------------
# Safety invariants
# -----------------------------------------------------------------------


class TestFulfillmentEngineSafety:
    def test_engagement_never_auto_charge(self):
        with pytest.raises(ValueError, match="auto_charge must be False"):
            ClientEngagement(
                tenant_id=TENANT, client_name="Test",
                client_company="Co", offer_type="pilot",
                auto_charge=True, auto_renew=False,
                source_id=SOURCE,
            )

    def test_engagement_never_auto_renew(self):
        with pytest.raises(ValueError, match="auto_renew must be False"):
            ClientEngagement(
                tenant_id=TENANT, client_name="Test",
                client_company="Co", offer_type="pilot",
                auto_charge=False, auto_renew=True,
                source_id=SOURCE,
            )

    def test_renewal_assessment_never_auto_renew(self):
        with pytest.raises(ValueError, match="auto_renew must be False"):
            RenewalAssessment(
                tenant_id=TENANT, engagement_id="e1",
                client_name="Test", client_company="Co",
                auto_renew=True, auto_charge=False,
                source_id=SOURCE,
            )

    def test_renewal_assessment_never_auto_charge(self):
        with pytest.raises(ValueError, match="auto_charge must be False"):
            RenewalAssessment(
                tenant_id=TENANT, engagement_id="e1",
                client_name="Test", client_company="Co",
                auto_renew=False, auto_charge=True,
                source_id=SOURCE,
            )
