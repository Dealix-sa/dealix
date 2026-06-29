def build_strategy(readout=None):
    readout = readout or {'intent': 'unknown', 'deal_stage': 'cold'}
    stage = readout.get('deal_stage', 'cold')
    score = 40
    if stage in ['interested', 'discovery']:
        score += 20
    if stage in ['proposal', 'negotiation']:
        score += 30
    band = 'low' if score < 45 else 'medium' if score < 70 else 'high'
    return {'deal_score': score, 'close_probability_band': band, 'best_offer': 'Growth Command Sprint', 'pricing_range': 'reviewed range', 'next_best_action': readout.get('next_best_action', 'ask question'), 'proof_to_show': 'daily command report', 'approval_gates': ['share', 'price', 'terms'], 'live_sends': 0, 'final_commitments': 0}


def build_payload():
    return {'summary': {'strategies': 1, 'live_sends': 0, 'final_commitments': 0}, 'strategy': build_strategy({'deal_stage': 'proposal', 'next_best_action': 'prepare folder'})}


def verify(payload):
    s = payload['strategy']
    return [] if s['live_sends'] == 0 and s['final_commitments'] == 0 else ['unsafe']


def main():
    payload = build_payload(); errors = verify(payload)
    print('DEAL_STRATEGY_READY=' + ('0' if errors else '1'))
    print(payload['summary'])


if __name__ == '__main__':
    main()
