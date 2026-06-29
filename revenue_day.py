from __future__ import annotations

import json
from pathlib import Path

REPORT_DIR = Path('reports/commercial/revenue_day')


def build_payload():
    command = {
        'account': 'top reviewed account',
        'sector': 'clinics',
        'offer': 'growth command sprint',
        'today_goal': 'prepare one proposal and book one review call',
        'proof': 'daily command report',
        'review_required': True,
        'live': 0,
    }
    service = {
        'inputs': ['channels', 'sample opportunities', 'owners', 'approval rules', 'proof target'],
        'flow': ['intake', 'map workflow', 'assign owners', 'build queue', 'prepare drafts', 'deliver proof', 'next plan'],
        'outputs': ['workflow map', 'owner map', 'action queue', 'proof report', 'next plan'],
    }
    summary = {'target_companies': 30, 'first_10_companies': 10, 'service_steps': 7, 'client_inputs': 5, 'client_outputs': 5, 'live': 0}
    return {'summary': summary, 'command': command, 'service': service}


def write_reports(payload):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    (REPORT_DIR / 'latest.md').write_text('# Revenue Day Command\n\n' + '\n'.join(f'- {k}: `{v}`' for k, v in payload['summary'].items()) + '\n', encoding='utf-8')


def verify(payload):
    return [] if payload['summary']['live'] == 0 and payload['command']['live'] == 0 else ['live must be zero']


def main():
    payload = build_payload()
    write_reports(payload)
    errors = verify(payload)
    print('REVENUE_DAY_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
