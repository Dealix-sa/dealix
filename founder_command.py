from __future__ import annotations

import json
from pathlib import Path

import dealix_gtm_launch_kit
import dealix_revenue_machine

REPORT = Path('reports/commercial/w13')


def build_payload():
    launch = dealix_gtm_launch_kit.build_payload()
    revenue = dealix_revenue_machine.build_payload()
    top = revenue['top_accounts'][0]
    command = {
        'sell_to': top['account']['name'],
        'sector': top['account']['sector'],
        'offer': top['offer']['name'],
        'reason': top['account']['pain'],
        'kpi': 'prepare one reviewed proposal and book one operating review',
        'proof': 'daily command report',
        'review': True,
        'live': 0,
    }
    service = {
        'steps': ['map flow', 'collect inputs', 'build queue', 'prepare drafts', 'review approvals', 'deliver proof', 'expand plan'],
        'inputs': ['channels', 'sample leads', 'owners', 'approval rules'],
        'outputs': ['command report', 'action queue', 'draft routes', 'proof summary'],
    }
    summary = {
        'target_companies': launch['summary']['target_companies'],
        'top_score': top['score'],
        'service_steps': len(service['steps']),
        'inputs': len(service['inputs']),
        'outputs': len(service['outputs']),
        'live': 0,
    }
    return {'summary': summary, 'command': command, 'service': service, 'first_10': launch['company_plan'][:10]}


def write_reports(payload):
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    (REPORT / 'latest.md').write_text('# W13 Founder Command\n\n' + '\n'.join(f'- {k}: `{v}`' for k, v in payload['summary'].items()) + '\n', encoding='utf-8')


def verify(payload):
    errors = []
    if payload['summary']['live'] != 0:
        errors.append('live must be zero')
    if len(payload['first_10']) != 10:
        errors.append('first 10 missing')
    if payload['summary']['service_steps'] < 7:
        errors.append('service flow incomplete')
    return errors


def main():
    payload = build_payload()
    write_reports(payload)
    errors = verify(payload)
    print('W13_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
