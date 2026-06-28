from app.leadership.iv4 import build_payload, verify_payload


def test_iv4_integrates_dx3_growth_and_negotiation():
    payload = build_payload()
    assert payload['summary']['dx3_items'] > 0
    assert payload['summary']['growth_cards'] > 0
    assert payload['summary']['negotiation_plans'] > 0
    assert payload['summary']['command_queue'] >= 7


def test_iv4_is_review_first():
    payload = build_payload()
    assert payload['summary']['auto_execute'] == 0
    assert payload['summary']['external_sends'] == 0
    assert payload['summary']['final_commitments'] == 0
    assert payload['summary']['approval_required'] == payload['summary']['command_queue']
    assert verify_payload(payload) == []


def test_iv4_command_queue_has_operating_fields():
    payload = build_payload()
    for item in payload['command_queue']:
        assert item['lane']
        assert item['owner']
        assert item['title']
        assert item['next_step']
        assert item['source']
        assert item['approval_required'] is True
