import deal_strategy_brain as dsb


def test_strategy_builds_for_price_question():
    s = dsb.build_strategy('Alpha', 'Retail', 'كم السعر؟')
    assert s['deal_score'] >= 0
    assert s['close_probability_band'] in dsb.CLOSE_PROBABILITY_BANDS
    assert s['best_offer']
    assert s['next_best_action']
    assert s['live_sends'] == 0
    assert s['final_commitments'] == 0


def test_approval_gates_present_for_proposal():
    s = dsb.build_strategy('Beta', 'Logistics', 'ارسل العرض')
    assert len(s['approval_gates']) >= 1


def test_strategy_must_ask_questions():
    s = dsb.build_strategy('Gamma', 'Real Estate', 'كم السعر؟')
    assert len(s['must_ask_questions']) >= 1


def test_do_not_do_present():
    s = dsb.build_strategy('Delta', 'Healthcare', 'كم السعر؟')
    assert 'guaranteed_revenue' in s['do_not_do']
    assert 'final_price_without_scope' in s['do_not_do']


def test_proof_to_show_present():
    s = dsb.build_strategy('Epsilon', 'Technology', 'we need more proof')
    assert len(s['proof_to_show']) >= 1


def test_negotiation_position_present():
    s = dsb.build_strategy('Zeta', 'Finance', 'غالي جداً')
    assert s['negotiation_position']['stance']
    assert 'never_do' in s['negotiation_position']


def test_discount_requires_approval():
    s = dsb.build_strategy('Eta', 'Services', 'can you give a discount?')
    assert s['recommended_discount_policy']['discount_requires_approval'] is True
    assert s['recommended_discount_policy']['auto_commit'] is False


def test_build_payload_all_strategies():
    payload = dsb.build_payload()
    assert payload['summary']['strategies_built'] == 5
    assert payload['summary']['live_sends'] == 0
    assert payload['summary']['final_commitments'] == 0


def test_verify_passes():
    payload = dsb.build_payload()
    assert dsb.verify(payload) == []


def test_unsubscribe_gives_do_not_contact():
    s = dsb.build_strategy('Theta', 'Retail', 'وقف التواصل')
    assert 'mark_do_not_contact' in s['next_best_action']
