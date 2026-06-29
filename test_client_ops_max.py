import client_ops_max


def test_client_ops_max_builds_service_delivery_os():
    payload = client_ops_max.build_payload()
    assert payload['summary']['lifecycle_stages'] == 7
    assert payload['summary']['deliverables'] == 9
    assert payload['summary']['daily_delivery_items'] == 7
    assert payload['summary']['sla_rules'] == 4
    assert payload['summary']['value_metrics'] == 5
    assert client_ops_max.verify(payload) == []


def test_client_ops_max_delegates_work_to_dealix():
    payload = client_ops_max.build_payload()
    assert len(payload['client_minimum_input']) == 4
    assert len(payload['dealix_done_for_client']) == 7
    assert payload['workspace']['status'] == 'prepared_for_delivery'
    assert 'proof' in payload['workspace']['workspace_sections']


def test_client_ops_max_blocks_sensitive_actions():
    payload = client_ops_max.build_payload()
    assert payload['summary']['live_sends'] == 0
    assert payload['summary']['final_commitments'] == 0
    for gate in payload['approval_gates']:
        assert gate['auto_run'] is False
        assert gate['status'] == 'approval_required'
