from app.outbound.policy_gate import can_send_email, can_send_whatsapp


def test_email_blocked_by_default():
    env = {
        "EXTERNAL_SEND_ENABLED": "false",
        "EMAIL_SEND_ENABLED": "false",
        "OUTBOUND_MODE": "draft_only",
    }
    contact = {
        "email": "test@example.com",
        "source_url": "https://example.com",
        "verification_status": "approved_to_send",
        "email_opt_out": False,
    }
    message = {
        "status": "approved",
        "body": "Hello. Unsubscribe anytime.",
    }
    result = can_send_email(contact, message, env)
    assert not result.allowed


def test_email_allowed_only_when_controlled_and_compliant():
    env = {
        "EXTERNAL_SEND_ENABLED": "true",
        "EMAIL_SEND_ENABLED": "true",
        "OUTBOUND_MODE": "controlled_live",
    }
    contact = {
        "email": "test@example.com",
        "source_url": "https://example.com",
        "verification_status": "approved_to_send",
        "email_opt_out": False,
    }
    message = {
        "status": "approved",
        "body": "Hello from Dealix. You can unsubscribe anytime.",
    }
    result = can_send_email(contact, message, env)
    assert result.allowed, result.reasons


def test_email_requires_unsubscribe():
    env = {
        "EXTERNAL_SEND_ENABLED": "true",
        "EMAIL_SEND_ENABLED": "true",
        "OUTBOUND_MODE": "controlled_live",
    }
    contact = {
        "email": "test@example.com",
        "source_url": "https://example.com",
        "verification_status": "approved_to_send",
        "email_opt_out": False,
    }
    message = {
        "status": "approved",
        "body": "Hello from Dealix.",
    }
    result = can_send_email(contact, message, env)
    assert not result.allowed
    assert any("unsubscribe" in r for r in result.reasons)


def test_whatsapp_requires_opt_in_and_template():
    env = {
        "EXTERNAL_SEND_ENABLED": "true",
        "WHATSAPP_SEND_ENABLED": "true",
        "WHATSAPP_ALLOW_LIVE_SEND": "true",
        "OUTBOUND_MODE": "controlled_live",
        "WHATSAPP_SEND_MODE": "template_only",
    }
    contact = {
        "whatsapp": "+966500000000",
        "whatsapp_opt_in": False,
        "whatsapp_opt_out": False,
        "source_url": "https://example.com",
        "verification_status": "approved_to_send",
    }
    message = {
        "status": "approved",
        "template_name": "dealix_intro_ar",
        "body": "السلام عليكم",
    }
    result = can_send_whatsapp(contact, message, env)
    assert not result.allowed
    assert any("opt-in" in r for r in result.reasons)


def test_whatsapp_allowed_when_opted_in_and_template():
    env = {
        "EXTERNAL_SEND_ENABLED": "true",
        "WHATSAPP_SEND_ENABLED": "true",
        "WHATSAPP_ALLOW_LIVE_SEND": "true",
        "OUTBOUND_MODE": "controlled_live",
        "WHATSAPP_SEND_MODE": "template_only",
    }
    contact = {
        "whatsapp": "+966500000000",
        "whatsapp_opt_in": True,
        "whatsapp_opt_out": False,
        "source_url": "https://example.com",
        "verification_status": "approved_to_send",
    }
    message = {
        "status": "approved",
        "template_name": "dealix_intro_ar",
        "body": "السلام عليكم",
    }
    result = can_send_whatsapp(contact, message, env)
    assert result.allowed, result.reasons


def test_blocks_fake_guarantees():
    env = {
        "EXTERNAL_SEND_ENABLED": "true",
        "EMAIL_SEND_ENABLED": "true",
        "OUTBOUND_MODE": "controlled_live",
    }
    contact = {
        "email": "test@example.com",
        "source_url": "https://example.com",
        "verification_status": "approved_to_send",
        "email_opt_out": False,
    }
    message = {
        "status": "approved",
        "body": "نضمن لك 100% نتائج. unsubscribe anytime.",
    }
    result = can_send_email(contact, message, env)
    assert not result.allowed
    assert any("blocked claim" in r for r in result.reasons)
