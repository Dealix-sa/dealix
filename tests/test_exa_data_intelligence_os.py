from app.connectors.exa import ExaConnector


def test_exa_connector_dry_run_is_safe_by_default(monkeypatch):
    monkeypatch.delenv("EXA_API_KEY", raising=False)
    connector = ExaConnector()

    result = connector.dry_run_search("Riyadh clinics operations")

    assert result["provider"] == "exa"
    assert result["delivery_enabled"] is False
    assert result["human_review_required"] is True
    assert result["source_url_required"] is True
    assert result["mode"] == "dry_run"


def test_exa_connector_reports_configured_when_key_exists(monkeypatch):
    monkeypatch.setenv("EXA_API_KEY", "test-key-placeholder")
    connector = ExaConnector()

    assert connector.configured() is True
    assert connector.can_search_live() is True


def test_exa_live_search_can_be_disabled_even_with_key(monkeypatch):
    monkeypatch.setenv("EXA_API_KEY", "test-key-placeholder")
    monkeypatch.setenv("EXA_ALLOW_LIVE_SEARCH", "false")
    connector = ExaConnector()

    assert connector.configured() is True
    assert connector.can_search_live() is False
