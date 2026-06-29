import client_service_autopilot as csa


def test_pack_contains_all_required_sections():
    payload = csa.build_payload()
    required = [
        'client_workspace', 'intake_pack', 'conversation_readout', 'deal_strategy',
        'proposal_folder', 'daily_delivery_plan', 'weekly_review_pack',
        'proof_report_template', 'approval_queue', 'renewal_plan',
    ]
    for section in required:
        assert section in payload, f'missing section: {section}'


def test_auto_prepared_items_at_least_10():
    payload = csa.build_payload()
    assert payload['summary']['auto_prepared_items'] >= 10


def test_approval_queue_includes_sensitive_items():
    payload = csa.build_payload()
    queue_actions = [item['action'] for item in payload['approval_queue']]
    assert 'external_email_send' in queue_actions
    assert 'whatsapp_send' in queue_actions
    assert 'final_price_commitment' in queue_actions


def test_live_sends_zero():
    payload = csa.build_payload()
    assert payload['summary']['live_sends'] == 0


def test_final_commitments_zero():
    payload = csa.build_payload()
    assert payload['summary']['final_commitments'] == 0


def test_proof_report_exists():
    payload = csa.build_payload()
    assert payload['proof_report_template']


def test_renewal_plan_exists():
    payload = csa.build_payload()
    assert payload['renewal_plan']
    assert payload['renewal_plan']['approval_required'] is True


def test_strategy_next_best_action():
    payload = csa.build_payload()
    assert payload['deal_strategy']['next_best_action']


def test_approval_queue_never_auto_run():
    payload = csa.build_payload()
    for item in payload['approval_queue']:
        assert item['auto_run'] is False


def test_verify_passes():
    payload = csa.build_payload()
    assert csa.verify(payload) == []


def test_daily_delivery_plan_no_live_send():
    payload = csa.build_payload()
    assert payload['daily_delivery_plan']['live_send'] is False
