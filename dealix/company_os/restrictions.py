"""Canonical Company OS restrictions.

The foundation must remain safe under CI and local runs even when future
connectors are added.
"""

BLOCKED_ACTIONS = {
    "send_email",
    "send_whatsapp",
    "send_sms",
    "post_linkedin",
    "post_x",
    "capture_payment",
    "merge_pr",
    "modify_production",
    "print_env",
    "scrape_prohibited_source",
}

PROHIBITED_CLAIMS = {
    "guaranteed revenue",
    "guaranteed roi",
    "guaranteed b2g win",
    "government access",
    "fake proof",
    "fake client",
    "auto-send without approval",
}


def assert_draft_only(mode: str) -> None:
    if mode != "draft-only":
        raise ValueError("Company OS foundation only supports --mode draft-only")


def is_blocked_action(action_type: str) -> bool:
    return action_type.strip().lower() in BLOCKED_ACTIONS
