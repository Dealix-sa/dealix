import deal_conversation_intelligence as dci


def test_arabic_price_question():
    r = dci.classify('كم السعر؟')
    assert r['intent'] == 'price_question'
    assert r['approval_required'] is True
    assert 'no_final_price_without_scope' in r['risk_flags']
    assert r['live_send'] is False
    assert r['final_commitment'] is False


def test_arabic_proposal_request():
    r = dci.classify('ارسل العرض')
    assert r['intent'] == 'proposal_request'
    assert r['approval_required'] is True
    assert r['next_best_action'] == 'prepare_proposal_folder_queue_for_founder_review'
    assert r['live_send'] is False


def test_arabic_not_interested():
    r = dci.classify('ما نحتاج')
    assert r['intent'] == 'not_interested'
    assert 'nurture' in r['next_best_action'] or 'close' in r['next_best_action']
    assert r['live_send'] is False


def test_arabic_unsubscribe():
    r = dci.classify('وقف التواصل')
    assert r['intent'] == 'unsubscribe'
    assert r['next_best_action'] == 'mark_do_not_contact_immediately'
    assert r['live_send'] is False
    assert r['final_commitment'] is False


def test_english_details_request():
    r = dci.classify('what does it include?')
    assert r['intent'] == 'ask_for_details'
    assert r['live_send'] is False


def test_english_trust_objection():
    r = dci.classify('we need more proof before deciding')
    assert r['objection_type'] == 'trust'
    assert r['live_send'] is False


def test_english_timing_objection():
    r = dci.classify('not now, maybe next quarter')
    assert r['objection_type'] == 'timing'
    assert r['live_send'] is False


def test_english_discount_request():
    r = dci.classify('can you give us a discount?')
    assert r['intent'] == 'discount_request'
    assert r['approval_required'] is True
    assert r['live_send'] is False


def test_legal_terms_flagged():
    r = dci.classify('send us the contract terms')
    assert r['intent'] == 'legal_terms'
    assert r['approval_required'] is True
    assert r['live_send'] is False


def test_discovery_questions_present():
    r = dci.classify('كم السعر؟')
    assert len(r['suggested_discovery_questions']) >= 1


def test_build_payload_no_live_sends():
    payload = dci.build_payload()
    assert payload['summary']['live_sends'] == 0
    assert payload['summary']['final_commitments'] == 0


def test_verify_passes():
    payload = dci.build_payload()
    assert dci.verify(payload) == []


def test_offer_suggested_on_cold_message():
    r = dci.classify('من انتم')
    assert r['suggested_offer'] == 'free_diagnostic'


def test_interested_arabic():
    r = dci.classify('مهتمين')
    assert r['intent'] == 'interested'
    assert r['sentiment'] == 'positive'
