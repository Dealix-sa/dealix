import client_ops_max


def test_lifecycle_has_7_stages():
    payload = client_ops_max.build_payload()
    assert payload['summary']['lifecycle_stages'] >= 7
    assert len(payload['lifecycle']) >= 7


def test_deliverables_at_least_9():
    payload = client_ops_max.build_payload()
    assert payload['summary']['deliverables'] >= 9
    assert len(payload['deliverables']) >= 9


def test_daily_delivery_at_least_7():
    payload = client_ops_max.build_payload()
    assert payload['summary']['daily_delivery_items'] >= 7
    assert len(payload['daily_delivery']) >= 7


def test_sla_rules_at_least_4():
    payload = client_ops_max.build_payload()
    assert payload['summary']['sla_rules'] >= 4


def test_value_metrics_at_least_5():
    payload = client_ops_max.build_payload()
    assert payload['summary']['value_metrics'] >= 5


def test_live_sends_zero():
    payload = client_ops_max.build_payload()
    assert payload['summary']['live_sends'] == 0


def test_final_commitments_zero():
    payload = client_ops_max.build_payload()
    assert payload['summary']['final_commitments'] == 0


def test_approval_gates_cannot_auto_run():
    payload = client_ops_max.build_payload()
    for gate in payload['approval_gates']:
        assert gate['auto_run'] is False


def test_verify_passes():
    payload = client_ops_max.build_payload()
    assert client_ops_max.verify(payload) == []


def test_proof_report_template_exists():
    payload = client_ops_max.build_payload()
    assert payload['proof_report_template']
    assert payload['proof_report_template']['live_sends'] == 0


def test_renewal_brief_requires_approval():
    payload = client_ops_max.build_payload()
    assert payload['renewal_brief']['approval_required'] is True
    assert payload['renewal_brief']['auto_commit'] is False
