"""
Approval Gates Tests
====================
Tests the approval gate system — exhaustive coverage of all action categories.
"""

import pytest
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.os_runtime.approval_gate import (
    check_approval,
    is_allowed,
    is_free,
    list_blocked_actions,
    list_approval_required_actions,
    list_free_actions,
    NEVER_ALLOWED,
    REQUIRES_APPROVAL,
    FREE_ACTIONS,
)


class TestNeverAllowedActions:
    """Actions that must always be blocked — doctrine non-negotiables."""

    @pytest.mark.parametrize("action", [
        "cold_whatsapp",
        "cold_whatsapp_outreach",
        "whatsapp_automation",
        "linkedin_automation",
        "auto_linkedin_dm",
        "scraping",
        "web_scraping",
        "robo_call",
        "auto_dialing",
        "use_client_data_for_training",
        "guaranteed_outcome_claim",
        "pii_in_logs",
    ])
    def test_action_is_blocked(self, action):
        result = check_approval(action)
        assert result["allowed"] is False, f"Action '{action}' should be blocked"
        assert result["decision"] == "blocked"
        assert result["governance_decision"]["override_possible"] is False

    def test_blocked_has_governance_decision(self):
        result = check_approval("cold_whatsapp")
        assert "governance_decision" in result
        assert result["governance_decision"]["doctrine_enforced"] is True


class TestRequiresApprovalActions:
    """Actions that require explicit founder approval."""

    @pytest.mark.parametrize("action", [
        "send_first_email",
        "send_followup_email",
        "share_pricing",
        "send_proposal",
        "request_client_credentials",
        "use_production_api",
        "access_client_systems",
        "deploy_to_client_environment",
        "run_automated_actions_externally",
        "delete_client_data",
        "share_client_data",
        "submit_website_form",
        "linkedin_connect",
        "linkedin_message",
        "phone_intro",
    ])
    def test_action_requires_approval(self, action):
        result = check_approval(action)
        assert result["allowed"] is True, f"Action '{action}' should be allowed (with approval)"
        assert result["requires_approval"] is True
        assert result["decision"] == "requires_approval"
        assert result["auto_execute"] is False

    def test_requires_approval_has_escalation(self):
        result = check_approval("send_first_email")
        assert "escalation" in result["governance_decision"]


class TestFreeActions:
    """Actions that don't need approval."""

    @pytest.mark.parametrize("action", [
        "research_company_public",
        "build_company_brief",
        "create_email_draft",
        "generate_proposal_draft",
        "analyze_sample_data",
        "create_architecture_doc",
        "run_internal_qa",
        "score_company",
        "classify_reply",
        "prepare_discovery_brief",
        "route_offer",
        "route_channels",
        "check_approval",
        "validate_configs",
    ])
    def test_action_is_free(self, action):
        result = check_approval(action)
        assert result["allowed"] is True
        assert result["requires_approval"] is False
        assert result["decision"] == "free"
        assert result["auto_execute"] is True


class TestHelperFunctions:
    """Test is_allowed, is_free helpers."""

    def test_is_allowed_blocked(self):
        assert is_allowed("cold_whatsapp") is False

    def test_is_allowed_requires_approval(self):
        assert is_allowed("send_first_email") is True

    def test_is_allowed_free(self):
        assert is_allowed("score_company") is True

    def test_is_free_blocked(self):
        assert is_free("cold_whatsapp") is False

    def test_is_free_requires_approval(self):
        assert is_free("send_first_email") is False

    def test_is_free_free_action(self):
        assert is_free("score_company") is True


class TestListFunctions:
    """Test list helpers."""

    def test_list_blocked_actions(self):
        blocked = list_blocked_actions()
        assert "cold_whatsapp" in blocked
        assert "linkedin_automation" in blocked
        assert isinstance(blocked, list)
        assert blocked == sorted(blocked)  # Must be sorted

    def test_list_approval_required_actions(self):
        actions = list_approval_required_actions()
        assert "send_first_email" in actions
        assert "send_proposal" in actions
        assert isinstance(actions, list)

    def test_list_free_actions(self):
        actions = list_free_actions()
        assert "score_company" in actions
        assert "build_company_brief" in actions


class TestUnknownActionDefault:
    """Unknown actions should default to requires_approval."""

    def test_unknown_requires_approval(self):
        result = check_approval("completely_unknown_action_xyz_abc")
        assert result["requires_approval"] is True
        assert result["governance_decision"]["unknown_action"] is True

    def test_unknown_is_allowed(self):
        result = check_approval("random_future_action")
        assert result["allowed"] is True  # Allowed but with approval


class TestSetIntegrity:
    """Test that the three sets don't overlap."""

    def test_no_overlap_between_never_allowed_and_requires_approval(self):
        overlap = NEVER_ALLOWED & REQUIRES_APPROVAL
        assert len(overlap) == 0, f"Actions in both NEVER_ALLOWED and REQUIRES_APPROVAL: {overlap}"

    def test_no_overlap_between_never_allowed_and_free(self):
        overlap = NEVER_ALLOWED & FREE_ACTIONS
        assert len(overlap) == 0, f"Actions in both NEVER_ALLOWED and FREE_ACTIONS: {overlap}"

    def test_no_overlap_between_requires_approval_and_free(self):
        overlap = REQUIRES_APPROVAL & FREE_ACTIONS
        assert len(overlap) == 0, f"Actions in both REQUIRES_APPROVAL and FREE_ACTIONS: {overlap}"
