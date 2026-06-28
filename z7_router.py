from __future__ import annotations

import json
from pathlib import Path

import m6_runtime

REPORT = Path('reports/leadership/z7')
CHANNELS = ['crm_task', 'whatsapp_draft', 'email_draft', 'calendar_draft', 'proposal_note', 'proof_update']


def build_routes():
    base = m6_runtime.build_payload()
    routes = []
    for decision in base['decisions']:
        for channel in CHANNELS:
            routes.append({
                'route_id': channel + '-' + decision['action_id'],
                'action_id': decision['action_id'],
                'owner': decision['owner'],
                'channel': channel,
                'mode': 'draft',
                'title': decision['title'],
                'status': 'prepared',
                'needs_review': True,
            })
    return routes


def build_payload():
    routes = build_routes()
    summary = {
        'routes': len(routes),
        'channels': len(CHANNELS),
        'needs_review': len([r for r in routes if r['needs_review']]),
        'prepared': len([r for r in routes if r['status'] == 'prepared']),
        'live': 0,
    }
    return {'summary': summary, 'channels': CHANNELS, 'routes': routes}


def write_reports(payload):
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# Z7 Routing Layer', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    (REPORT / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload):
    errors = []
    if payload['summary']['live'] != 0:
        errors.append('live must be zero')
    if payload['summary']['needs_review'] != payload['summary']['routes']:
        errors.append('review mismatch')
    return errors


def main():
    payload = build_payload()
    write_reports(payload)
    errors = verify(payload)
    print('Z7_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
