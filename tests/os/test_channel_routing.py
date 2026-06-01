"""
Channel Routing Tests
=====================
Tests channel router and anti-ban enforcement.
"""

import pytest
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.os_runtime.channel_router import (
    route_channels,
    check_channel_allowed,
    SECTOR_CHANNEL_MAP,
)


class TestDoctrineEnforcement:
    """Doctrine: no cold WhatsApp, no LinkedIn automation, no scraping."""

    def test_cold_whatsapp_not_in_any_recommendations(self):
        """cold_whatsapp must NEVER appear in recommended channels."""
        for sector in SECTOR_CHANNEL_MAP:
            result = route_channels({"company": "Test", "sector": sector})
            assert "cold_whatsapp" not in result["recommended_channels"], \
                f"cold_whatsapp in recommendations for sector '{sector}'"

    def test_linkedin_automation_not_in_any_recommendations(self):
        for sector in SECTOR_CHANNEL_MAP:
            result = route_channels({"company": "Test", "sector": sector})
            assert "linkedin_automation" not in result["recommended_channels"]

    def test_scraping_not_in_any_recommendations(self):
        for sector in SECTOR_CHANNEL_MAP:
            result = route_channels({"company": "Test", "sector": sector})
            assert "scraping" not in result["recommended_channels"]

    def test_cold_whatsapp_always_in_blocked_channels(self):
        result = route_channels({"company": "Test", "sector": "b2b_services"})
        assert "cold_whatsapp" in result["blocked_channels"]

    def test_linkedin_automation_always_blocked(self):
        result = route_channels({"company": "Test", "sector": "legal"})
        assert "linkedin_automation" in result["blocked_channels"]


class TestSectorChannelRouting:
    """Test correct channel sets per sector."""

    @pytest.mark.parametrize("sector,expected_primary", [
        ("legal", "referral"),
        ("facilities_management", "email"),
        ("accounting", "referral"),
        ("consulting", "linkedin_assisted"),
    ])
    def test_primary_channel_by_sector(self, sector, expected_primary):
        result = route_channels({"company": "Test", "sector": sector})
        assert result["primary_channel"] == expected_primary, \
            f"Sector '{sector}' expected primary '{expected_primary}', got '{result['primary_channel']}'"

    def test_inbound_gets_email_as_primary(self):
        result = route_channels({"company": "Inbound Co", "inbound": True})
        assert result["primary_channel"] == "email"
        assert result["governance_decision"]["inbound"] is True


class TestApprovalRequirement:
    """All channels must require founder approval."""

    def test_all_routes_require_founder_approval(self):
        for sector in SECTOR_CHANNEL_MAP:
            result = route_channels({"company": "Test", "sector": sector})
            assert result["requires_founder_approval"] is True

    def test_inbound_route_requires_approval(self):
        result = route_channels({"company": "Test", "inbound": True})
        assert result["requires_founder_approval"] is True


class TestCheckChannelAllowed:
    """Test channel permission checks."""

    @pytest.mark.parametrize("channel,expected_allowed", [
        ("email", True),
        ("website_form", True),
        ("phone_intro", True),
        ("referral", True),
        ("linkedin_assisted", True),
        ("executive_email", True),
        ("partner_referral", True),
        ("cold_whatsapp", False),
        ("linkedin_automation", False),
        ("scraping", False),
    ])
    def test_channel_allowed_status(self, channel, expected_allowed):
        result = check_channel_allowed(channel)
        assert result["allowed"] == expected_allowed, \
            f"Channel '{channel}' allowed={result['allowed']}, expected {expected_allowed}"

    def test_unknown_channel_not_allowed(self):
        result = check_channel_allowed("some_random_channel_xyz")
        assert result["allowed"] is False


class TestGovernanceDecision:
    """Test governance_decision field."""

    def test_governance_decision_present(self):
        result = route_channels({"company": "Test", "sector": "legal"})
        assert "governance_decision" in result

    def test_doctrine_enforced_flag(self):
        result = route_channels({"company": "Test", "sector": "legal"})
        assert result["governance_decision"]["doctrine_enforced"] is True

    def test_module_is_channel_router(self):
        result = route_channels({"company": "Test", "sector": "legal"})
        assert result["governance_decision"]["module"] == "channel_router"

    def test_always_blocked_in_governance(self):
        result = route_channels({"company": "Test", "sector": "b2b_services"})
        always_blocked = result["governance_decision"]["always_blocked"]
        assert "cold_whatsapp" in always_blocked
        assert "linkedin_automation" in always_blocked
        assert "scraping" in always_blocked
