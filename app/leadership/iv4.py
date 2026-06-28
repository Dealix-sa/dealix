from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.commercial.growth_os_v2 import run_growth_os
from app.commercial.negotiation_operator import demo_negotiation_day
from app.leadership.dx3 import build_payload as build_dx3_payload

REPORT_DIR = Path('reports/leadership/iv4')


def build_payload() -> dict[str, Any]:
    dx3 = build_dx3_payload()
    growth = run_growth_os()
    negotiation = demo_negotiation_day()
    growth_summary = growth.get('summary', {})
    negotiation_summary = negotiation.get('summary', {})
    top_items = dx3.get('top_items', [])
    command_queue = []
    for idx, item in enumerate(top_items[:5], 1):
        command_queue.append({
            'id': f'iv4-command-{idx}',
            'lane': item['lane'],
            'owner': item['owner'],
            'title': item['title'],
            'why_now': item['why_now'],
            'next_step': item['next_step'],
            'source': 'dx3',
            'score': item['score'],
            'approval_required': True,
            'auto_execute': False,
        })
    command_queue.append({
        'id': 'iv4-commercial-review',
        'lane': 'sales',
        'owner': 'Sales Director',
        'title': 'review commercial growth cards',
        'why_now': 'commercial growth engine produced daily sales material',
        'next_step': 'review_growth_cards_and_proposals',
        'source': 'commercial_growth_os',
        'score': 89,
        'approval_required': True,
        'auto_execute': False,
    })
    command_queue.append({
        'id': 'iv4-negotiation-review',
        'lane': 'sales',
        'owner': 'Sales Director',
        'title': 'review negotiation plans',
        'why_now': 'negotiation plans include sensitive replies and must stay reviewed',
        'next_step': 'review_negotiation_plans',
        'source': 'negotiation_operator',
        'score': 93,
        'approval_required': True,
        'auto_execute': False,
    })
    summary = {
        'dx3_items': dx3['summary']['items'],
        'growth_cards': growth_summary.get('cards', 0),
        'proposal_briefs': growth_summary.get('proposals', 0),
        'negotiation_plans': negotiation_summary.get('plans', 0),
        'command_queue': len(command_queue),
        'approval_required': len([x for x in command_queue if x['approval_required']]),
        'auto_execute': len([x for x in command_queue if x['auto_execute']]),
        'external_sends': 0,
        'final_commitments': 0,
    }
    return {
        'summary': summary,
        'command_queue': command_queue,
        'dx3': dx3,
        'growth': {'summary': growth_summary},
        'negotiation': {'summary': negotiation_summary},
    }


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Dealix IV4 Integration Layer', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Command Queue')
    for item in payload['command_queue']:
        lines.append(f"- **{item['lane']}** — {item['title']} → `{item['next_step']}`")
    (REPORT_DIR / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify_payload(payload: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if payload['summary']['auto_execute'] != 0:
        failures.append('auto_execute must stay zero')
    if payload['summary']['external_sends'] != 0:
        failures.append('external_sends must stay zero')
    if payload['summary']['final_commitments'] != 0:
        failures.append('final_commitments must stay zero')
    if payload['summary']['command_queue'] < 7:
        failures.append('command_queue must include dx3 and commercial actions')
    if payload['summary']['approval_required'] != payload['summary']['command_queue']:
        failures.append('all command items must require approval')
    if payload['summary']['growth_cards'] <= 0:
        failures.append('growth cards must be present')
    if payload['summary']['negotiation_plans'] <= 0:
        failures.append('negotiation plans must be present')
    return failures


def run_iv4() -> dict[str, Any]:
    payload = build_payload()
    write_reports(payload)
    return payload
