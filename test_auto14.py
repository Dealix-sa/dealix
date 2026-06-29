import auto14


def test_auto14_builds_execution_layer():
    payload = auto14.build_payload()
    assert payload['summary']['safe_auto_tasks'] == 10
    assert payload['summary']['approval_gates'] == 6
    assert payload['summary']['artifacts'] >= 8
    assert payload['summary']['client_required_items'] == 4


def test_auto14_runs_safe_work_but_blocks_sensitive_actions():
    payload = auto14.build_payload()
    assert payload['summary']['live_sends'] == 0
    assert payload['summary']['final_commitments'] == 0
    for item in payload['auto_runs']:
        assert item['auto_run'] is True
        assert item['status'] == 'done'
    for gate in payload['approval_gates']:
        assert gate['auto_run'] is False
        assert gate['status'] == 'approval_required'


def test_auto14_has_client_and_company_delegation():
    payload = auto14.build_payload()
    assert len(payload['client_side']['what_dealix_does_for_client']) == 6
    assert len(payload['company_side']['what_system_does_for_founder']) == 5
    assert auto14.verify(payload) == []
