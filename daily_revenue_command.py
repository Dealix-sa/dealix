from __future__ import annotations

import json
from pathlib import Path

import dealix_gtm_launch_kit
import dealix_revenue_machine

REPORT = Path('reports/commercial/daily_revenue_command')

FLOW = ['intake', 'map workflow', 'assign owners', 'build queue', 'prepare drafts', 'review gates', 'deliver proof', 'next plan']
OUTPUTS = ['workflow map', 'owner map', 'action queue', 'proof report', 'next plan']


def build_payload():
    launch = dealix_gtm_launch_kit.build_payload()
    revenue = dealix_revenue_machine.build_payload()
    top = revenue['top_accounts'][0]
    command = {
        'account': top['account']['name'],
        'sector': top['account']['sector'],
        'offer': top['offer']['name'],
        'pain': top['account']['pain'],
        'today_kpi': 'prepare one reviewed proposal folder and book one operating review',
        'proof': 'daily command report',
        'next_step': 'run discovery and prepare a proof-first sprint',
        'review_required': True,
        'live': 0,
    }
    summary = {
        'target_companies': launch['summary']['target_companies'],
        'top_score': top['score'],
        'flow_steps': len(FLOW),
        'client_outputs': len(OUTPUTS),
        'first_10_companies': 10,
        'live': 0,
    }
    return {
        'summary': summary,
        'command': command,
        'service_flow': FLOW,
        'client_outputs': OUTPUTS,
        'first_10_companies': launch['company_plan'][:10],
    }


def write_reports(payload):
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# Daily Revenue Command', '']
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
    if len(payload['service_flow']) != 8:
        errors.append('service flow must have 8 steps')
    if len(payload['client_outputs']) != 5:
        errors.append('client outputs must have 5 items')
    if len(payload['first_10_companies']) != 10:
        errors.append('first 10 companies missing')
    return errors


def main():
    payload = build_payload()
    write_reports(payload)
    errors = verify(payload)
    print('DAILY_REVENUE_COMMAND_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
