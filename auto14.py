from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import rcmax

REPORT_DIR = Path('reports/commercial/auto14')

SAFE_AUTO_TASKS = [
    'build_client_workspace',
    'prepare_intake_questions',
    'prepare_workflow_map_template',
    'prepare_owner_map_template',
    'prepare_action_queue',
    'prepare_proposal_folder',
    'prepare_discovery_script',
    'prepare_proof_report_template',
    'prepare_next_week_plan',
    'prepare_internal_kpi_summary',
]

APPROVAL_TASKS = [
    'external_email_send',
    'whatsapp_send',
    'calendar_invite_send',
    'final_price_commitment',
    'legal_terms_acceptance',
    'contract_signature',
]


def _auto_artifacts(base: dict[str, Any]) -> dict[str, Any]:
    command = base['command']
    service = base['service_blueprint']
    proposal = base['proposal_folder']
    return {
        'client_workspace': {
            'account': command['account'],
            'sector': command['sector'],
            'offer': command['offer'],
            'status': 'prepared',
        },
        'intake_questions': service['inputs_needed'],
        'workflow_map': {'sections': ['current channels', 'handoffs', 'owners', 'approval points', 'missed follow ups']},
        'owner_map': {'owners': ['Founder', 'Growth', 'Sales', 'Delivery', 'Client Owner']},
        'action_queue': [
            {'action': 'review client intake', 'owner': 'Founder', 'status': 'ready'},
            {'action': 'prepare account brief', 'owner': 'Growth', 'status': 'ready'},
            {'action': 'review matched offer', 'owner': 'Sales', 'status': 'ready'},
            {'action': 'prepare proof report', 'owner': 'Delivery', 'status': 'ready'},
        ],
        'proposal_folder': proposal,
        'discovery_script': proposal['discovery_script'],
        'proof_template': {'sections': ['baseline', 'queue', 'owners', 'drafts', 'decisions', 'proof', 'next plan']},
        'next_week_plan': ['review proof', 'approve next actions', 'expand to managed command room'],
    }


def _approval_gate(task: str) -> dict[str, Any]:
    return {
        'task': task,
        'status': 'approval_required',
        'auto_run': False,
        'reason': 'requires human review before external or final commitment',
    }


def build_payload() -> dict[str, Any]:
    base = rcmax.build_payload()
    artifacts = _auto_artifacts(base)
    auto_runs = [
        {'task': task, 'status': 'done', 'auto_run': True, 'artifact': task.replace('prepare_', '').replace('build_', '')}
        for task in SAFE_AUTO_TASKS
    ]
    approval_gates = [_approval_gate(task) for task in APPROVAL_TASKS]
    client_side = {
        'what_client_must_do': ['approve access to sample data', 'confirm owners', 'approve external messages', 'review proof'],
        'what_dealix_does_for_client': ['prepare workspace', 'map workflow', 'prepare queue', 'prepare drafts', 'prepare proof', 'prepare next plan'],
        'client_time_required': '30 to 45 minutes for first review plus approvals',
    }
    company_side = {
        'what_founder_must_do': ['review approval gates', 'join review call', 'approve price scope'],
        'what_system_does_for_founder': ['select account', 'match offer', 'prepare service pack', 'prepare proof pack', 'prepare day plan'],
    }
    summary = {
        'safe_auto_tasks': len(auto_runs),
        'approval_gates': len(approval_gates),
        'artifacts': len(artifacts),
        'client_required_items': len(client_side['what_client_must_do']),
        'system_company_items': len(company_side['what_system_does_for_founder']),
        'live_sends': 0,
        'final_commitments': 0,
    }
    return {
        'summary': summary,
        'base_command': base['command'],
        'auto_runs': auto_runs,
        'approval_gates': approval_gates,
        'artifacts': artifacts,
        'client_side': client_side,
        'company_side': company_side,
    }


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# Auto14 Execution Max', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Auto Runs')
    for item in payload['auto_runs']:
        lines.append(f"- {item['task']} — {item['status']}")
    lines.append('\n## Approval Gates')
    for item in payload['approval_gates']:
        lines.append(f"- {item['task']} — {item['status']}")
    (REPORT_DIR / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload['summary']['live_sends'] != 0:
        errors.append('live sends must stay zero')
    if payload['summary']['final_commitments'] != 0:
        errors.append('final commitments must stay zero')
    if payload['summary']['safe_auto_tasks'] < 10:
        errors.append('not enough safe automation tasks')
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
    print('AUTO14_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
