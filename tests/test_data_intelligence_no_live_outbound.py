from app.connectors.exa import ExaConnector


def test_data_intelligence_connector_has_no_mutation_methods():
    connector = ExaConnector(api_key="test-key-placeholder")

    for method_name in ["send", "charge", "publish", "create_crm_record"]:
        assert not hasattr(connector, method_name)


def test_dry_run_contract_is_review_first(monkeypatch):
    monkeypatch.delenv("EXA_API_KEY", raising=False)
    connector = ExaConnector()

    payload = connector.dry_run_search("Riyadh B2B operations")

    assert payload["delivery_enabled"] is False
    assert payload["human_review_required"] is True
    assert payload["source_url_required"] is True
