def read_message(message):
    t = message.lower()
    if 'price' in t or 'cost' in t or 'سعر' in t:
        intent = 'price_question'; stage = 'interested'; action = 'prepare range and questions'; approval = True; risk = ['scope_review_needed']
    elif 'proposal' in t or 'offer' in t or 'عرض' in t:
        intent = 'proposal_request'; stage = 'proposal'; action = 'prepare proposal folder'; approval = True; risk = ['review_before_share']
    elif 'meeting' in t or 'call' in t or 'موعد' in t:
        intent = 'meeting_request'; stage = 'discovery'; action = 'prepare meeting brief'; approval = True; risk = ['review_invite']
    elif 'proof' in t or 'اثبات' in t:
        intent = 'trust_objection'; stage = 'discovery'; action = 'prepare proof plan'; approval = False; risk = ['avoid_guarantees']
    elif 'stop' in t or 'وقف' in t:
        intent = 'opt_out'; stage = 'closed_lost'; action = 'mark opt out'; approval = False; risk = ['do_not_contact']
    elif 'not interested' in t or 'ما نحتاج' in t:
        intent = 'not_interested'; stage = 'closed_lost'; action = 'close politely'; approval = False; risk = []
    else:
        intent = 'unknown'; stage = 'cold'; action = 'ask clarifying question'; approval = False; risk = []
    return {'message': message, 'intent': intent, 'deal_stage': stage, 'next_best_action': action, 'approval_required': approval, 'risk_flags': risk, 'suggested_offer': 'Growth Command Sprint', 'suggested_discovery_questions': ['Which channel matters?', 'Who owns follow up?', 'What proof matters?'], 'live_sends': 0, 'final_commitments': 0}


def build_payload():
    cases = [read_message(x) for x in ['كم السعر', 'send proposal', 'meeting please', 'proof first', 'stop']]
    return {'summary': {'cases': len(cases), 'live_sends': 0, 'final_commitments': 0}, 'cases': cases}


def verify(payload):
    return [] if payload['summary']['live_sends'] == 0 and payload['summary']['final_commitments'] == 0 else ['unsafe']


def main():
    payload = build_payload(); errors = verify(payload)
    print('CONVERSATION_INTELLIGENCE_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
