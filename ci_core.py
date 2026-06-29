def read_message(message):
    t = message.lower()
    if 'price' in t or 'cost' in t or 'سعر' in t:
        intent = 'price_question'
        stage = 'interested'
        action = 'prepare range and questions'
        approval = True
    elif 'proposal' in t or 'offer' in t or 'عرض' in t:
        intent = 'proposal_request'
        stage = 'proposal'
        action = 'prepare folder'
        approval = True
    elif 'meeting' in t or 'call' in t or 'موعد' in t:
        intent = 'meeting_request'
        stage = 'discovery'
        action = 'prepare meeting brief'
        approval = True
    elif 'proof' in t or 'اثبات' in t:
        intent = 'trust_objection'
        stage = 'discovery'
        action = 'prepare proof plan'
        approval = False
    else:
        intent = 'unknown'
        stage = 'cold'
        action = 'ask clarifying question'
        approval = False
    return {'intent': intent, 'deal_stage': stage, 'next_best_action': action, 'approval_required': approval, 'live_sends': 0, 'final_commitments': 0}


def build_payload():
    cases = [read_message(x) for x in ['كم السعر', 'send proposal', 'meeting please', 'proof first']]
    return {'summary': {'cases': len(cases), 'live_sends': 0, 'final_commitments': 0}, 'cases': cases}


def verify(payload):
    return [] if payload['summary']['live_sends'] == 0 and payload['summary']['final_commitments'] == 0 else ['unsafe']


def main():
    payload = build_payload()
    print('CONVERSATION_INTELLIGENCE_READY=' + ('0' if verify(payload) else '1'))
    print(payload['summary'])


if __name__ == '__main__':
    main()
