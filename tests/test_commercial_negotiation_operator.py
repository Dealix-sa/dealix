from app.commercial.negotiation_operator import (
    RESTRICTED_COMMITMENTS,
    NegotiationInput,
    build_negotiation_plan,
    classify_reply,
    demo_negotiation_day,
    verify_negotiation_payload,
)


def test_classifies_price_objection():
    assert classify_reply('السعر عالي شوي') == 'price_objection'


def test_negotiation_cannot_make_final_commitments():
    plan = build_negotiation_plan(NegotiationInput(
        account_id='a1',
        company_name='Client',
        reply_type='price_objection',
        message='هل فيه خصم؟',
        current_offer='Growth Sprint',
        pricing_range_sar='5000-12000',
    ))
    assert plan.can_send_without_review is False
    assert plan.approval_required is True
    assert set(RESTRICTED_COMMITMENTS).issubset(set(plan.forbidden_commitments))
    assert 'guaranteed_roi' in plan.forbidden_commitments
    assert 'discount_approval' in plan.forbidden_commitments


def test_contract_request_is_high_risk_and_reviewed():
    plan = build_negotiation_plan(NegotiationInput(
        account_id='a2',
        company_name='Client',
        reply_type='contract_request',
        message='ارسل العقد',
        current_offer='Company Brain Sprint',
        pricing_range_sar='15000-35000',
    ))
    assert plan.risk_level == 'high'
    assert plan.recommended_next_action == 'legal_review_handoff'
    assert plan.approval_required is True


def test_demo_payload_is_safe_by_default():
    payload = demo_negotiation_day()
    assert payload['summary']['live_commitments'] == 0
    assert payload['summary']['can_send_without_review'] == 0
    assert verify_negotiation_payload(payload) == []
