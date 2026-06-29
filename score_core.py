def build_strategy(readout=None):
    readout = readout or {'intent': 'unknown', 'deal_stage': 'cold'}
    stage = readout.get('deal_stage', 'cold')
    intent = readout.get('intent', 'unknown')
    score = 35
    if stage in ['interested', 'discovery']:
        score += 20
    if stage in ['proposal', 'negotiation']:
        score += 30
    if intent in ['proposal_request', 'meeting_request']:
        score += 15
    if intent in ['not_interested', 'opt_out']:
        score -= 25
    band = 'low' if score < 45 else 'medium' if score < 70 else 'high' if score < 90 else 'very_high'
    return {'deal_score': score, 'close_probability_band': band, 'best_offer': 'Growth Command Sprint', 'pricing_range': 'reviewed range', 'next_best_action': readout.get('next_best_action', 'ask question'), 'proof_to_show': 'daily command report', 'approval_gates': ['external share', 'final quote', 'terms'], 'do_not_do': ['no guaranteed result', 'no final quote without scope'], 'live_sends': 0, 'final_commitments': 0}


def build_payload():
    return {'summary': {'strategies': 1, 'live_sends': 0, 'final_commitments': 0}, 'strategy': build_strategy({'intent': 'proposal_request', 'deal_stage': 'proposal', 'next_best_action': 'prepare proposal folder'})}


def verify(payload):
    s = payload['strategy']
    return [] if s['live_sends'] == 0 and s['final_commitments'] == 0 and s['next_best_action'] else ['unsafe']


def main():
    payload = build_payload(); errors = verify(payload)
    print('DEAL_STRATEGY_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
