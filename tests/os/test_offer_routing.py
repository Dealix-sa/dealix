"""
Offer Routing Tests
===================
Comprehensive tests for the offer router — all sectors covered.
"""

import pytest
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.os_runtime.offer_router import route_offer, list_supported_sectors, ROUTES


class TestSectorRouting:
    """Test each sector routes to the correct offer."""

    @pytest.mark.parametrize("sector,expected_offer", [
        ("facilities_management", "maintenance_intelligence_os"),
        ("maintenance", "maintenance_intelligence_os"),
        ("contracting", "project_controls_ai_os"),
        ("legal", "legal_knowledge_document_os"),
        ("consulting", "consulting_delivery_intelligence_os"),
        ("real_estate", "property_operations_ai_os"),
        ("international", "gcc_international_ai_pilot"),
        ("international_company", "gcc_international_ai_pilot"),
        ("b2b_services", "revenue_ai_os"),
        ("accounting", "accounting_audit_workflow_ai"),
        ("healthcare_admin", "healthcare_admin_workflow_ai"),
    ])
    def test_sector_routes_to_correct_offer(self, sector, expected_offer):
        result = route_offer({"company": "Test Co", "sector": sector})
        assert result["primary_offer"] == expected_offer, (
            f"Sector '{sector}' should route to '{expected_offer}', got '{result['primary_offer']}'"
        )

    def test_all_sectors_have_entry_offer(self):
        for sector in ROUTES:
            result = route_offer({"company": "Test", "sector": sector})
            assert result["entry_offer"] == "ai_workflow_audit", \
                f"Sector '{sector}' missing entry_offer"

    def test_all_sectors_have_buyer_defined(self):
        for sector in ROUTES:
            result = route_offer({"company": "Test", "sector": sector})
            assert result.get("buyer"), f"Sector '{sector}' missing buyer"
            assert len(result["buyer"]) > 3

    def test_all_sectors_have_pain_angle(self):
        for sector in ROUTES:
            result = route_offer({"company": "Test", "sector": sector})
            assert result.get("pain_angle"), f"Sector '{sector}' missing pain_angle"


class TestSectorNormalization:
    """Test that sector strings are correctly normalized."""

    def test_uppercase_normalized(self):
        result = route_offer({"company": "Test", "sector": "LEGAL"})
        assert result["primary_offer"] == "legal_knowledge_document_os"

    def test_spaces_replaced_with_underscores(self):
        result = route_offer({"company": "Test", "sector": "facilities management"})
        assert result["primary_offer"] == "maintenance_intelligence_os"

    def test_mixed_case_with_spaces(self):
        result = route_offer({"company": "Test", "sector": "Facilities Management"})
        assert result["primary_offer"] == "maintenance_intelligence_os"

    def test_hyphenated_sector(self):
        result = route_offer({"company": "Test", "sector": "b2b-services"})
        assert result["primary_offer"] == "revenue_ai_os"

    def test_empty_sector_uses_default(self):
        result = route_offer({"company": "Test", "sector": ""})
        assert result["sector"] == "unknown"
        assert result["governance_decision"]["sector_matched"] is False

    def test_none_sector_uses_default(self):
        result = route_offer({"company": "Test"})
        assert result["governance_decision"]["sector_matched"] is False


class TestGovernanceDecision:
    """Test governance_decision field is correct."""

    def test_matched_sector_sets_sector_matched_true(self):
        result = route_offer({"company": "Test", "sector": "legal"})
        assert result["governance_decision"]["sector_matched"] is True
        assert result["governance_decision"]["route_used"] == "legal"

    def test_unmatched_sector_sets_sector_matched_false(self):
        result = route_offer({"company": "Test", "sector": "unknown_xyz"})
        assert result["governance_decision"]["sector_matched"] is False
        assert result["governance_decision"]["route_used"] == "default"

    def test_module_is_offer_router(self):
        result = route_offer({"company": "Test", "sector": "legal"})
        assert result["governance_decision"]["module"] == "offer_router"


class TestOutputFields:
    """Test output dict has all required fields."""

    def test_output_has_company(self):
        result = route_offer({"company": "Al Noor Law", "sector": "legal"})
        assert result["company"] == "Al Noor Law"

    def test_output_name_fallback(self):
        result = route_offer({"name": "Name Fallback Co", "sector": "legal"})
        assert result["company"] == "Name Fallback Co"

    def test_output_has_sector(self):
        result = route_offer({"company": "Test", "sector": "legal"})
        assert result["sector"] == "legal"

    def test_output_has_country(self):
        result = route_offer({"company": "Test", "sector": "legal", "country": "ksa"})
        assert result["country"] == "ksa"

    def test_list_supported_sectors_includes_all_known(self):
        sectors = list_supported_sectors()
        expected = ["accounting", "b2b_services", "consulting", "contracting",
                    "facilities_management", "healthcare_admin", "international",
                    "international_company", "legal", "maintenance", "real_estate"]
        for s in expected:
            assert s in sectors
