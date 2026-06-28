from scripts.leadership.run_executive_growth_command_day import ROLES, build_payload, verify


def test_every_leadership_lane_has_a_card():
    payload = build_payload()
    roles = {card['role'] for card in payload['decision_cards']}
    assert set(ROLES).issubset(roles)
    assert payload['summary']['decision_cards'] == len(ROLES)


def test_safety_defaults_remain_review_only():
    payload = build_payload()
    assert payload['summary']['live_sends'] == 0
    assert payload['summary']['live_commitments'] == 0
    assert payload['summary']['approval_required'] == len(ROLES)
    assert verify(payload) == []


def test_cards_have_three_buttons_max_and_need_approval():
    payload = build_payload()
    for card in payload['decision_cards']:
        assert len(card['buttons']) <= 3
        assert card['approval_required'] is True
        assert card['no_live_send'] is True
