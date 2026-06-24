import os


def test_saas_outbound_defaults_safe(monkeypatch):
    for name in [
        "EXTERNAL_SEND_ENABLED",
        "EMAIL_SEND_ENABLED",
        "WHATSAPP_SEND_ENABLED",
        "WHATSAPP_ALLOW_LIVE_SEND",
        "SMS_SEND_ENABLED",
    ]:
        monkeypatch.setenv(name, "false")
    monkeypatch.setenv("OUTBOUND_MODE", "draft_only")

    assert os.getenv("EXTERNAL_SEND_ENABLED") == "false"
    assert os.getenv("WHATSAPP_ALLOW_LIVE_SEND") == "false"
    assert os.getenv("OUTBOUND_MODE") == "draft_only"
