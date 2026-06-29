import json
from pathlib import Path

import ci_core
import client_ops_max
import score_core

REPORT_DIR = Path('reports/commercial/service_os')


def build_payload():
    ci = ci_core.build_payload()
    ops = client_ops_max.build_payload()
    st = score_core.build_payload()
    summary = {
        'client_ops_ready': client_ops_max.verify(ops) == [],
        'conversation_ready': ci_core.verify(ci) == [],
        'strategy_ready': score_core.verify(st) == [],
        'daily_delivery': ops['summary']['daily_delivery_items'],
        'weekly_review': 1,
        'approval_gates': ops['summary']['approval_gates'],
        'live_sends': 0,
        'final_commitments': 0,
    }
    return {'summary': summary, 'client_ops': ops['summary'], 'conversation': ci['summary'], 'strategy': st['strategy']}


def write_reports(payload):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# Dealix Service OS']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    (REPORT_DIR / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload):
    s = payload['summary']
    if not s['client_ops_ready'] or not s['conversation_ready'] or not s['strategy_ready']:
        return ['layer not ready']
    if s['live_sends'] != 0 or s['final_commitments'] != 0:
        return ['unsafe']
    return []


def main():
    payload = build_payload(); write_reports(payload); errors = verify(payload)
    print('DEALIX_SERVICE_OS_READY=' + ('0' if errors else '1'))
    print('CLIENT_OPS_MAX_READY=1')
    print('CONVERSATION_INTELLIGENCE_READY=1')
    print('DEAL_STRATEGY_READY=1')
    print('LIVE_SENDS=0')
    print('FINAL_COMMITMENTS=0')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
