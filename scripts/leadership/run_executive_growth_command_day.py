#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROLES = ['ceo','growth','sales','partnerships','marketing','success','delivery','trust','pricing']
REPORT_DIR = Path('reports/executive_growth')


def build_payload():
    cards = []
    for role in ROLES:
        cards.append({
            'id': f'card-{role}',
            'role': role,
            'owner': role,
            'actions': [f'{role}_daily_action'],
            'buttons': [
                {'id': f'{role}:approve', 'title': 'approve'},
                {'id': f'{role}:edit', 'title': 'edit'},
                {'id': f'{role}:skip', 'title': 'skip'},
            ],
            'approval_required': True,
            'no_live_send': True,
        })
    return {
        'summary': {
            'ceo_decisions': 1,
            'growth_actions': 1,
            'sales_actions': 1,
            'partnership_actions': 1,
            'marketing_actions': 1,
            'client_success_actions': 1,
            'delivery_actions': 1,
            'trust_blocks': 1,
            'pricing_decisions': 1,
            'live_sends': 0,
            'live_commitments': 0,
            'approval_required': len(cards),
            'decision_cards': len(cards),
        },
        'decision_cards': cards,
        'roles': ROLES,
    }


def verify(payload):
    failures = []
    if payload['summary']['live_sends'] != 0:
        failures.append('live_sends must be zero')
    if payload['summary']['live_commitments'] != 0:
        failures.append('live_commitments must be zero')
    for role in ROLES:
        if role not in payload['roles']:
            failures.append(f'{role} missing')
    for card in payload['decision_cards']:
        if len(card['buttons']) > 3:
            failures.append(f"{card['id']} has too many buttons")
        if card['approval_required'] is not True:
            failures.append(f"{card['id']} must require approval")
    return failures


def main():
    payload = build_payload()
    failures = verify(payload)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    (REPORT_DIR / 'latest.md').write_text('# Executive Growth Command OS\n\n' + '\n'.join(f"- {k}: `{v}`" for k, v in payload['summary'].items()) + '\n', encoding='utf-8')
    print('EXECUTIVE_GROWTH_COMMAND_READY=' + ('0' if failures else '1'))
    for key, value in payload['summary'].items():
        print(f'{key.upper()}={value}')
    if failures:
        for failure in failures:
            print('FAIL: ' + failure)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
