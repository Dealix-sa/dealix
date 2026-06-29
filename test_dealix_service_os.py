import json
from pathlib import Path

import run_dealix_service_os as sos
import deal_conversation_intelligence as dci


def test_all_layers_ready():
    payload = sos.run_all()
    status = payload['status']
    assert status['RCMAX_READY'] == 1
    assert status['AUTO14_READY'] == 1
    assert status['CLIENT_OPS_MAX_READY'] == 1
    assert status['CONVERSATION_INTELLIGENCE_READY'] == 1
    assert status['DEAL_STRATEGY_READY'] == 1
    assert status['CLIENT_AUTOPILOT_READY'] == 1
    assert status['DEALIX_SERVICE_OS_READY'] == 1


def test_no_live_sends():
    payload = sos.run_all()
    assert payload['status']['LIVE_SENDS'] == 0


def test_no_final_commitments():
    payload = sos.run_all()
    assert payload['status']['FINAL_COMMITMENTS'] == 0


def test_all_approval_gates_present():
    payload = sos.run_all()
    assert payload['csa_summary']['approval_queue_items'] >= 1


def test_reports_are_created():
    payload = sos.run_all()
    sos.write_reports(payload)
    assert Path('reports/commercial/service_os/latest.json').exists()
    assert Path('reports/commercial/service_os/latest.md').exists()


def test_arabic_message_classification():
    cases = [
        ('كم السعر؟', 'price_question'),
        ('ارسل العرض', 'proposal_request'),
        ('ما نحتاج', 'not_interested'),
        ('وقف التواصل', 'unsubscribe'),
        ('مهتمين', 'interested'),
    ]
    for message, expected_intent in cases:
        r = dci.classify(message)
        assert r['intent'] == expected_intent, f'{message!r} → expected {expected_intent}, got {r["intent"]}'
        assert r['live_send'] is False
        assert r['final_commitment'] is False


def test_english_message_classification():
    cases = [
        ('we need more proof before deciding', 'trust'),
        ('not now, maybe next quarter', 'timing'),
        ('can you give us a discount?', 'discount_request'),
    ]
    for message, expected in cases:
        r = dci.classify(message)
        if expected in ('trust', 'timing'):
            assert r['objection_type'] == expected, f'{message!r} objection: {r["objection_type"]}'
        else:
            assert r['intent'] == expected or r['objection_type'] == 'price', f'{message!r} intent: {r["intent"]}'
        assert r['live_send'] is False


def test_proposal_folder_exists():
    import client_service_autopilot as csa
    payload = csa.build_payload()
    assert payload['proposal_folder']


def test_proof_report_template_exists():
    import client_ops_max
    payload = client_ops_max.build_payload()
    assert payload['proof_report_template']
    assert 'sections' in payload['proof_report_template']


def test_renewal_plan_exists():
    import client_ops_max
    payload = client_ops_max.build_payload()
    assert payload['renewal_brief']
    assert 'options' in payload['renewal_brief']


def test_daily_delivery_exists():
    import client_ops_max
    payload = client_ops_max.build_payload()
    assert len(payload['daily_delivery']) >= 7


def test_weekly_review_exists():
    import client_service_autopilot as csa
    payload = csa.build_payload()
    assert payload['weekly_review_pack']
    assert len(payload['weekly_review_pack']['sections']) >= 5


def test_no_errors_across_all_modules():
    payload = sos.run_all()
    all_errors = [e for errs in payload['errors'].values() for e in errs]
    assert all_errors == [], f'Errors found: {all_errors}'
