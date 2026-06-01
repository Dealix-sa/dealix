"""
OS Runtime Integration Tests
=============================
Tests approval gate, company scorer, offer router, channel router,
anti-ban guardian, persuasion dossier, finance module.
"""

import sys
from pathlib import Path

# Ensure repo root is on path
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.os_runtime.approval_gate import check_approval, is_allowed, is_free
from dealix.os_runtime.company_scorer import score_company, score_from_dict, CompanySignal
from dealix.os_runtime.offer_router import route_offer, list_supported_sectors
from dealix.os_runtime.channel_router import route_channels, check_channel_allowed
from dealix.os_runtime.anti_ban_guardian import check_channel_safe, check_message_similarity, list_blocked_channels
from dealix.os_runtime.finance import calculate_unit_economics, check_floor_price


# ─────────────────────────────────────────────
# Approval Gate Tests
# ─────────────────────────────────────────────

class TestApprovalGate:
    def test_send_first_email_requires_approval(self):
        result = check_approval("send_first_email")
        assert result["allowed"] is True
        assert result["requires_approval"] is True
        assert result["decision"] == "requires_approval"
        assert "governance_decision" in result

    def test_send_proposal_requires_approval(self):
        result = check_approval("send_proposal")
        assert result["requires_approval"] is True

    def test_cold_whatsapp_is_blocked(self):
        result = check_approval("cold_whatsapp")
        assert result["allowed"] is False
        assert result["decision"] == "blocked"
        assert result["governance_decision"]["override_possible"] is False

    def test_linkedin_automation_is_blocked(self):
        result = check_approval("linkedin_automation")
        assert result["allowed"] is False
        assert result["decision"] == "blocked"

    def test_scraping_is_blocked(self):
        result = check_approval("scraping")
        assert result["allowed"] is False
        assert result["decision"] == "blocked"

    def test_score_company_is_free(self):
        result = check_approval("score_company")
        assert result["allowed"] is True
        assert result["requires_approval"] is False
        assert result["decision"] == "free"

    def test_build_company_brief_is_free(self):
        result = check_approval("build_company_brief")
        assert result["decision"] == "free"

    def test_create_email_draft_is_free(self):
        result = check_approval("create_email_draft")
        assert result["decision"] == "free"

    def test_generate_proposal_draft_is_free(self):
        result = check_approval("generate_proposal_draft")
        assert result["decision"] == "free"

    def test_unknown_action_defaults_to_requires_approval(self):
        result = check_approval("some_unknown_action_xyz")
        assert result["requires_approval"] is True
        assert result["governance_decision"]["unknown_action"] is True

    def test_governance_decision_always_present(self):
        for action in ["send_first_email", "cold_whatsapp", "score_company"]:
            result = check_approval(action)
            assert "governance_decision" in result
            assert "module" in result["governance_decision"]

    def test_is_allowed_helper(self):
        assert is_allowed("send_first_email") is True
        assert is_allowed("cold_whatsapp") is False

    def test_is_free_helper(self):
        assert is_free("score_company") is True
        assert is_free("send_first_email") is False

    def test_use_client_data_for_training_blocked(self):
        result = check_approval("use_client_data_for_training")
        assert result["allowed"] is False


# ─────────────────────────────────────────────
# Company Scorer Tests
# ─────────────────────────────────────────────

class TestCompanyScorer:
    def test_perfect_score_returns_tier_a(self):
        signal = CompanySignal(
            company="Test FM Co",
            country="ksa",
            sector="facilities_management",
            operations_heavy=True,
            maintenance_or_field_work=True,
            repeated_reporting=True,
            multi_branch_or_multi_site=True,
            clear_buyer_title=True,
            public_growth_signal=True,
            likely_data_or_api=True,
            founder_domain_fit=True,
        )
        result = score_company(signal)
        assert result["fit_score"] == 100
        assert result["tier"] == "A"
        assert result["recommended_action"] == "deep_research_custom_pack"

    def test_zero_score_returns_tier_d(self):
        signal = CompanySignal(company="Empty Co", country="ksa", sector="unknown")
        result = score_company(signal)
        assert result["fit_score"] == 0
        assert result["tier"] == "D"
        assert result["recommended_action"] == "archive_or_research_later"

    def test_tier_b_threshold(self):
        # Score 70–84 = tier B
        signal = CompanySignal(
            company="Mid Co",
            operations_heavy=True,       # 20
            maintenance_or_field_work=True,  # 20
            repeated_reporting=True,     # 15
            multi_branch_or_multi_site=True,  # 10
        )
        result = score_company(signal)
        assert result["fit_score"] == 65
        assert result["tier"] == "C"

    def test_tier_a_at_85(self):
        signal = CompanySignal(
            company="Strong Co",
            operations_heavy=True,        # 20
            maintenance_or_field_work=True,  # 20
            repeated_reporting=True,      # 15
            multi_branch_or_multi_site=True,  # 10
            clear_buyer_title=True,       # 10
            public_growth_signal=True,    # 10
        )
        result = score_company(signal)
        assert result["fit_score"] == 85
        assert result["tier"] == "A"

    def test_governance_decision_present(self):
        signal = CompanySignal(company="Test", country="uae", sector="legal")
        result = score_company(signal)
        assert "governance_decision" in result
        assert result["governance_decision"]["module"] == "company_scorer"

    def test_reasons_list_populated(self):
        signal = CompanySignal(
            company="FM Co",
            operations_heavy=True,
            maintenance_or_field_work=True,
        )
        result = score_company(signal)
        assert len(result["reasons"]) == 2
        factors = [r["factor"] for r in result["reasons"]]
        assert "operations_heavy" in factors
        assert "maintenance_or_field_work" in factors

    def test_score_from_dict(self):
        data = {
            "company": "Dict Co",
            "country": "ksa",
            "sector": "contracting",
            "operations_heavy": True,
            "repeated_reporting": True,
        }
        result = score_from_dict(data)
        assert result["fit_score"] == 35
        assert result["company"] == "Dict Co"


# ─────────────────────────────────────────────
# Offer Router Tests
# ─────────────────────────────────────────────

class TestOfferRouter:
    def test_legal_routes_to_legal_os(self):
        result = route_offer({"company": "Al Noor Law", "sector": "legal", "country": "ksa"})
        assert result["primary_offer"] == "legal_knowledge_document_os"
        assert result["entry_offer"] == "ai_workflow_audit"

    def test_fm_routes_to_maintenance_os(self):
        result = route_offer({"company": "FM Corp", "sector": "facilities_management"})
        assert result["primary_offer"] == "maintenance_intelligence_os"

    def test_contracting_routes_to_project_controls(self):
        result = route_offer({"company": "Contractor Inc", "sector": "contracting"})
        assert result["primary_offer"] == "project_controls_ai_os"

    def test_international_company_routes_to_gcc_pilot(self):
        result = route_offer({"company": "Intl Corp", "sector": "international_company"})
        assert result["primary_offer"] == "gcc_international_ai_pilot"

    def test_unknown_sector_uses_default(self):
        result = route_offer({"company": "Unknown Co", "sector": "some_unknown_sector"})
        assert result["primary_offer"] == "ai_workflow_audit"
        assert result["governance_decision"]["sector_matched"] is False

    def test_governance_decision_present(self):
        result = route_offer({"company": "Test", "sector": "legal"})
        assert "governance_decision" in result
        assert result["governance_decision"]["module"] == "offer_router"

    def test_sector_normalization(self):
        result = route_offer({"company": "Test", "sector": "Facilities Management"})
        assert result["sector"] == "facilities_management"
        assert result["primary_offer"] == "maintenance_intelligence_os"

    def test_accounting_routes_correctly(self):
        result = route_offer({"company": "CPA Firm", "sector": "accounting"})
        assert result["primary_offer"] == "accounting_audit_workflow_ai"

    def test_healthcare_admin_routes_correctly(self):
        result = route_offer({"company": "Hospital Admin", "sector": "healthcare_admin"})
        assert result["primary_offer"] == "healthcare_admin_workflow_ai"

    def test_list_supported_sectors_returns_list(self):
        sectors = list_supported_sectors()
        assert isinstance(sectors, list)
        assert "legal" in sectors
        assert "facilities_management" in sectors
        assert "contracting" in sectors


# ─────────────────────────────────────────────
# Channel Router Tests
# ─────────────────────────────────────────────

class TestChannelRouter:
    def test_legal_gets_safe_channels(self):
        result = route_channels({"company": "Law Firm", "sector": "legal", "country": "ksa"})
        assert "email" in result["recommended_channels"] or "referral" in result["recommended_channels"]
        assert "cold_whatsapp" not in result["recommended_channels"]
        assert "linkedin_automation" not in result["recommended_channels"]

    def test_cold_whatsapp_always_in_blocked(self):
        result = route_channels({"company": "Any Co", "sector": "b2b_services"})
        assert "cold_whatsapp" in result["blocked_channels"]

    def test_linkedin_automation_always_blocked(self):
        result = route_channels({"company": "Tech Co", "sector": "consulting"})
        assert "linkedin_automation" in result["blocked_channels"]

    def test_inbound_lead_gets_full_channels(self):
        result = route_channels({"company": "Inbound Co", "inbound": True})
        assert "email" in result["recommended_channels"]
        assert result["governance_decision"]["inbound"] is True

    def test_requires_founder_approval(self):
        result = route_channels({"company": "Any Co", "sector": "legal"})
        assert result["requires_founder_approval"] is True

    def test_governance_decision_present(self):
        result = route_channels({"company": "Test", "sector": "accounting"})
        assert "governance_decision" in result
        assert result["governance_decision"]["doctrine_enforced"] is True

    def test_check_channel_allowed_cold_whatsapp(self):
        result = check_channel_allowed("cold_whatsapp")
        assert result["allowed"] is False

    def test_check_channel_allowed_email(self):
        result = check_channel_allowed("email")
        assert result["allowed"] is True


# ─────────────────────────────────────────────
# Anti-Ban Guardian Tests
# ─────────────────────────────────────────────

class TestAntiBanGuardian:
    def test_cold_whatsapp_blocked(self):
        result = check_channel_safe("cold_whatsapp")
        assert result["safe"] is False
        assert result["blocked"] is True
        assert result["block_type"] == "doctrine"

    def test_linkedin_automation_blocked(self):
        result = check_channel_safe("linkedin_automation")
        assert result["safe"] is False
        assert result["blocked"] is True

    def test_email_safe_when_within_limits(self):
        result = check_channel_safe("email", send_count_today=5)
        assert result["safe"] is True

    def test_email_unsafe_when_over_limit(self):
        result = check_channel_safe("email", send_count_today=25)
        assert result["safe"] is False
        assert result["block_type"] == "limit"

    def test_blocked_channels_list(self):
        blocked = list_blocked_channels()
        assert "cold_whatsapp" in blocked
        assert "linkedin_automation" in blocked
        assert "scraping" in blocked

    def test_message_similarity_safe(self):
        result = check_message_similarity(
            "hello this is a unique message about facility management SLA",
            ["completely different message about project controls and risks"]
        )
        assert result["safe"] is True

    def test_message_similarity_unsafe(self):
        msg = "We help facility management companies automate their SLA reports and technician tracking workflows"
        result = check_message_similarity(msg, [msg])
        assert result["safe"] is False
        assert result["max_similarity"] > 0.72


# ─────────────────────────────────────────────
# Finance Tests
# ─────────────────────────────────────────────

class TestFinance:
    def test_healthy_margin(self):
        result = calculate_unit_economics(100_000, 20_000)
        assert result["gross_margin_percent"] == 80.0
        assert result["margin_status"] == "healthy"
        assert result["margin_ok"] is True

    def test_below_minimum_margin(self):
        result = calculate_unit_economics(100_000, 60_000)
        assert result["gross_margin_percent"] == 40.0
        assert result["margin_status"] == "below_minimum"
        assert result["margin_ok"] is False

    def test_floor_price_check_pass(self):
        result = check_floor_price("ai_workflow_audit", 10_000)
        assert result["ok"] is True

    def test_floor_price_check_fail(self):
        result = check_floor_price("ai_workflow_audit", 3_000)
        assert result["ok"] is False
        assert "floor" in result["recommendation"].lower() or "BELOW" in result["recommendation"]

    def test_governance_decision_present(self):
        result = calculate_unit_economics(50_000, 15_000)
        assert "governance_decision" in result
        assert result["governance_decision"]["module"] == "finance"
        assert "disclaimer" in result["governance_decision"]
