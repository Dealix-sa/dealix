from __future__ import annotations

import json
from pathlib import Path

import dealix_gtm_launch_kit
import dealix_revenue_machine

REPORT = Path('reports/commercial/q13')


def build_payload():
    gtm = dealix_gtm_launch_kit.build_payload()
    revenue = dealix_revenue_machine.build_payload()
    top = revenue['top_accounts'][0]
    command = {
        'account': top['account']['name'],
        'sector': top['account']['sector'],
        'offer': top['offer']['name'],
        'pain': top['account']['pain'],
        'today_kpi': 'prepare one reviewed proposal folder and book one operating review',
        'proof': 'daily command report',
        'next_step': 'run discovery and prepare proof-first sprint',
        'review_required': True,
        'live': 0,
    }
    service_flow = [
        'collect intake',
        'map current follow-up flow',
        'assign owners',
        'build command queue',
        'prepare draft routes',
        'review approvals',
        'deliver proof report',
        'prepare next-week plan',
    ]
    client_outputs = ['flow map', 'owner map', 'action queue', 'proof report', 'next-week plan']
    summary = {
        'target_companies': gtm['summary']['target_companies'],
        'top_score': top['score'],
        'service_steps': len(service_flow),
        'client_outputs': len(client_outputs),
        'first_10_companies': 10,
        'live': 0,
    }
    return {
        'summary': summary,
        'command': command,
        'service_flow': service_flow,
        'client_outputs': client_outputs,
        'first_10_companies': gtm['company_plan'][:10],
    }


def write_reports(payload):
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# Q13 Founder Daily Command', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Today')
    lines.append(f"- Account: {payload['command']['account']}")
    lines.append(f"- Offer: {payload['command']['offer']}")
    lines.append(f"- KPI: {payload['command']['today_kpi']}")
    (REPORT / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload):
    errors = []
    if payload['summary']['live'] != 0 or payload['command']['live'] != 0:
        errors.append('live must be zero')
    if len(payload['service_flow']) < 8:
        errors.append('service flow incomplete')
    if len(payload['first_10_companies']) != 10:
        errors.append('first 10 companies missing')
    if not payload['command']['account'] or not payload['command']['offer']:
        errors.append('command incomplete')
    return errors


def main():
    payload = build_payload()
    write_reports(payload)
    errors = verify(payload)
    print('Q13_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
