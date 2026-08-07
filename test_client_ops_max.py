import ci_core
import client_ops_max
import run_os16
import score_core


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


def test_conversation_core_reads_arabic_and_english():
    ar = ci_core.read_message('كم السعر')
    en = ci_core.read_message('send proposal')
    assert ar['intent'] == 'price_question'
    assert en['intent'] == 'proposal_request'
    assert ar['live_sends'] == 0
    assert en['final_commitments'] == 0


def test_strategy_core_uses_conversation_readout():
    readout = ci_core.read_message('send proposal')
    strategy = score_core.build_strategy(readout)
    assert strategy['next_best_action']
    assert strategy['close_probability_band'] in ['low', 'medium', 'high', 'very_high']
    assert strategy['live_sends'] == 0
    assert strategy['final_commitments'] == 0


def test_service_os_runner_builds_report_payload():
    payload = run_os16.build_payload()
    assert payload['summary']['client_ops_ready'] is True
    assert payload['summary']['conversation_ready'] is True
    assert payload['summary']['strategy_ready'] is True
    assert payload['summary']['live_sends'] == 0
    assert payload['summary']['final_commitments'] == 0
    assert run_os16.verify(payload) == []
