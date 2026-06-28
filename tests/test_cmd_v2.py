from app.leadership.cmd_v2 import LANES, build_payload, verify_payload


def test_cmd_v2_has_all_lanes():
    payload = build_payload()
    assert set(LANES).issubset(set(payload['lanes'].keys()))
    assert payload['summary']['lanes'] == 8


def test_cmd_v2_outputs_actions_for_every_lane():
    payload = build_payload()
    for lane in LANES:
        assert payload['lanes'][lane]
    assert payload['summary']['actions'] >= 12
    assert payload['summary']['decision_cards'] == 8


def test_cmd_v2_is_review_first():
    payload = build_payload()
    assert payload['summary']['external_sends'] == 0
    assert payload['summary']['final_commitments'] == 0
    assert payload['summary']['approval_required'] == payload['summary']['actions']
    assert verify_payload(payload) == []


def test_cmd_v2_cards_are_button_limited():
    payload = build_payload()
    for card in payload['decision_cards']:
        assert len(card['buttons']) <= 3
        assert card['approval_required'] is True
        assert card['external_send'] is False
