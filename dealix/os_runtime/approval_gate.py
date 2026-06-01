"""
Approval Gate
=============
Determines if a given action requires founder approval.
Enforces doctrine non-negotiables — some actions are always blocked.

Doctrine rules enforced here (non-negotiable):
- No cold WhatsApp automation
- No LinkedIn automation
- No scraping
- No guaranteed outcome claims
- All external actions require approval
"""

from typing import Optional

# Actions always blocked — no approval overrides these
NEVER_ALLOWED: set[str] = {
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
}

# Actions that require founder approval before execution
REQUIRES_APPROVAL: set[str] = {
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
    "send_linkedin_message",
    "phone_intro",
    "schedule_call",
}

# Actions that are free (no approval needed)
FREE_ACTIONS: set[str] = {
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
}


def check_approval(action: str, context: Optional[dict] = None) -> dict:
    """
    Check if an action requires founder approval or is blocked.

    Args:
        action: The action name to check.
        context: Optional context dict for additional checks.

    Returns:
        dict with:
            - action: str
            - allowed: bool (False means blocked, not just requires approval)
            - requires_approval: bool
            - auto_execute: bool (True only for free actions)
            - decision: "blocked" | "requires_approval" | "free"
            - reason: str
            - governance_decision: dict
    """
    action_normalized = str(action or "").lower().strip().replace("-", "_").replace(" ", "_")

    # 1. Check never-allowed first (doctrine non-negotiables)
    if action_normalized in NEVER_ALLOWED:
        result = {
            "action": action,
            "allowed": False,
            "requires_approval": False,
            "auto_execute": False,
            "decision": "blocked",
            "reason": f"DOCTRINE VIOLATION: '{action}' is never allowed. This is a non-negotiable rule.",
            "governance_decision": {
                "module": "approval_gate",
                "version": "1.0",
                "action": action,
                "decision": "blocked",
                "doctrine_enforced": True,
                "override_possible": False,
            },
        }
        return result

    # 2. Check requires-approval actions
    if action_normalized in REQUIRES_APPROVAL:
        result = {
            "action": action,
            "allowed": True,
            "requires_approval": True,
            "auto_execute": False,
            "decision": "requires_approval",
            "reason": f"'{action}' requires explicit founder approval before execution.",
            "governance_decision": {
                "module": "approval_gate",
                "version": "1.0",
                "action": action,
                "decision": "requires_approval",
                "doctrine_enforced": True,
                "escalation": "founder_daily_brief",
            },
        }
        return result

    # 3. Check free actions
    if action_normalized in FREE_ACTIONS:
        result = {
            "action": action,
            "allowed": True,
            "requires_approval": False,
            "auto_execute": True,
            "decision": "free",
            "reason": f"'{action}' is a free internal action — no approval needed.",
            "governance_decision": {
                "module": "approval_gate",
                "version": "1.0",
                "action": action,
                "decision": "free",
                "doctrine_enforced": True,
            },
        }
        return result

    # 4. Unknown action — default to requires approval (safe default)
    result = {
        "action": action,
        "allowed": True,
        "requires_approval": True,
        "auto_execute": False,
        "decision": "requires_approval",
        "reason": (
            f"'{action}' is not in the known action list. "
            "Defaulting to requires_approval — add to approval_gate.py if this is a recurring action."
        ),
        "governance_decision": {
            "module": "approval_gate",
            "version": "1.0",
            "action": action,
            "decision": "requires_approval",
            "unknown_action": True,
            "escalation": "founder_daily_brief",
        },
    }
    return result


def is_allowed(action: str) -> bool:
    """Quick boolean check: is this action allowed at all (not blocked)?"""
    return check_approval(action)["allowed"]


def is_free(action: str) -> bool:
    """Quick boolean check: can this action execute without approval?"""
    result = check_approval(action)
    return result["allowed"] and not result["requires_approval"]


def list_blocked_actions() -> list[str]:
    """Return all never-allowed actions."""
    return sorted(NEVER_ALLOWED)


def list_approval_required_actions() -> list[str]:
    """Return all actions requiring founder approval."""
    return sorted(REQUIRES_APPROVAL)


def list_free_actions() -> list[str]:
    """Return all free (no approval) actions."""
    return sorted(FREE_ACTIONS)
