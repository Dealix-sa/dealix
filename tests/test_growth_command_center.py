import json
from pathlib import Path


def test_growth_command_center_stack_defaults_are_safe():
    data = json.loads(Path("data/commercial/growth_command_center_stack.json").read_text(encoding="utf-8"))
    defaults = data["safety_defaults"]
    assert defaults["EXTERNAL_SEND_ENABLED"] is False
    assert defaults["EMAIL_SEND_ENABLED"] is False
    assert defaults["WHATSAPP_SEND_ENABLED"] is False
    assert defaults["WHATSAPP_ALLOW_LIVE_SEND"] is False
    assert defaults["SMS_SEND_ENABLED"] is False
    assert defaults["OUTBOUND_MODE"] == "draft_only"


def test_growth_command_center_has_core_services():
    data = json.loads(Path("data/commercial/growth_command_center_stack.json").read_text(encoding="utf-8"))
    names = {service["name"] for service in data["service_stack"]}
    assert "Revenue Command Room OS" in names
    assert "Company Brain OS" in names
    assert "AI Sales Agent OS" in names
    assert "Client Delivery OS" in names
    assert "AI Trust and Governance OS" in names


def test_growth_command_center_generator_exists():
    assert Path("scripts/commercial/generate_growth_command_center.py").exists()
