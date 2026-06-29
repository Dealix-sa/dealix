from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import auto14
import rcmax

REPORT_DIR = Path('reports/commercial/client_ops_max')

CLIENT_LIFECYCLE = [
    {'stage': 'sale_ready', 'goal': 'prepare reviewed offer and proof-first proposal'},
    {'stage': 'intake', 'goal': 'collect channels, sample opportunities, owners, rules, proof target'},
    {'stage': 'diagnosis', 'goal': 'map current workflow, gaps, owners, and handoffs'},
    {'stage': 'setup', 'goal': 'create command queue, proof template, and working pack'},
    {'stage': 'daily_ops', 'goal': 'prepare actions, drafts, decisions, and proof notes'},
    {'stage': 'weekly_review', 'goal': 'summarize proof, risks, and next actions'},
    {'stage': 'renewal', 'goal': 'recommend next sprint or managed command room'},
]

DELIVERABLES = [
    'client intake pack',
    'workflow diagnosis',
    'owner map',
    'command queue',
    'draft route pack',
    'daily proof note',
    'weekly proof report',
    'next-week action plan',
    'renewal or expansion brief',
]

SLA_RULES = [
    {'name': 'intake_ready', 'target': 'same day after inputs'},
    {'name': 'first_command_queue', 'target': 'within 1 working day'},
    {'name': 'first_proof_note', 'target': 'within 2 working days'},
    {'name': 'weekly_review_pack', 'target': 'every 7 days'},
]

APPROVAL_GATES = [
    'send external message',
    'publish client-facing claim',
    'commit final price',
    'accept legal terms',
    'sign contract',
    'promise revenue result',
]


def _build_workspace(auto_payload: dict[str, Any], rc_payload: dict[str, Any]) -> dict[str, Any]:
    command = rc_payload['command']
    artifacts = auto_payload['artifacts']
    return {
        'client': command['account'],
        'sector': command['sector'],
        'offer': command['offer'],
        'status': 'prepared_for_delivery',
        'workspace_sections': [
            'intake',
            'workflow_map',
            'owners',
            'command_queue',
            'draft_routes',
            'proof',
            'next_plan',
        ],
        'prepared_artifacts': list(artifacts.keys()),
    }


def _build_daily_delivery(auto_payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {'item': 'review intake', 'owner': 'Delivery', 'status': 'ready'},
        {'item': 'update workflow map', 'owner': 'Delivery', 'status': 'ready'},
        {'item': 'prepare action queue', 'owner': 'Ops', 'status': 'ready'},
        {'item': 'prepare draft routes', 'owner': 'Sales', 'status': 'ready'},
        {'item': 'prepare proof note', 'owner': 'Delivery', 'status': 'ready'},
        {'item': 'surface approvals', 'owner': 'Founder', 'status': 'ready'},
        {'item': 'update next plan', 'owner': 'Founder', 'status': 'ready'},
    ]


def _build_value_scorecard() -> dict[str, Any]:
    return {
        'metrics': [
            {'name': 'opportunities_reviewed', 'target': 10},
            {'name': 'owners_assigned', 'target': 3},
            {'name': 'draft_routes_prepared', 'target': 6},
            {'name': 'proof_items_delivered', 'target': 4},
            {'name': 'next_actions_approved', 'target': 3},
        ],
        'client_value_statement': 'Client sees what is happening, who owns it, what is pending, and what proof exists.',
    }


def build_payload() -> dict[str, Any]:
    rc_payload = rcmax.build_payload()
    auto_payload = auto14.build_payload()
    workspace = _build_workspace(auto_payload, rc_payload)
    daily_delivery = _build_daily_delivery(auto_payload)
    scorecard = _build_value_scorecard()
    weekly_review = {
        'sections': ['summary', 'completed work', 'approval gaps', 'proof delivered', 'risks', 'next week plan'],
        'status': 'prepared_template',
    }
    summary = {
        'lifecycle_stages': len(CLIENT_LIFECYCLE),
        'deliverables': len(DELIVERABLES),
        'daily_delivery_items': len(daily_delivery),
        'sla_rules': len(SLA_RULES),
        'approval_gates': len(APPROVAL_GATES),
        'value_metrics': len(scorecard['metrics']),
        'live_sends': 0,
        'final_commitments': 0,
    }
    return {
        'summary': summary,
        'workspace': workspace,
        'lifecycle': CLIENT_LIFECYCLE,
        'deliverables': DELIVERABLES,
        'daily_delivery': daily_delivery,
        'weekly_review': weekly_review,
        'sla_rules': SLA_RULES,
        'approval_gates': [{'gate': gate, 'auto_run': False, 'status': 'approval_required'} for gate in APPROVAL_GATES],
        'value_scorecard': scorecard,
        'client_minimum_input': ['approve sample data use', 'confirm owners', 'review proof', 'approve external actions'],
        'dealix_done_for_client': ['workspace', 'maps', 'queue', 'drafts', 'proof', 'weekly review', 'next plan'],
    }


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# Client Ops Max', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Daily Delivery')
    for item in payload['daily_delivery']:
        lines.append(f"- {item['owner']}: {item['item']} — {item['status']}")
    lines.append('\n## Deliverables')
    for item in payload['deliverables']:
        lines.append(f'- {item}')
    (REPORT_DIR / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload['summary']['live_sends'] != 0:
        errors.append('live sends must stay zero')
    if payload['summary']['final_commitments'] != 0:
        errors.append('final commitments must stay zero')
    if payload['summary']['deliverables'] < 9:
        errors.append('not enough deliverables')
    if payload['summary']['daily_delivery_items'] < 7:
        errors.append('daily delivery incomplete')
    if payload['summary']['approval_gates'] < 6:
        errors.append('approval gates missing')
    for gate in payload['approval_gates']:
        if gate['auto_run'] is not False:
            errors.append('approval gate cannot auto run')
    return errors


def main() -> int:
    payload = build_payload()
    write_reports(payload)
    errors = verify(payload)
    print('CLIENT_OPS_MAX_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
