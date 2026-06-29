from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPORT_DIR = Path('reports/commercial/client_ops_max')

LIFECYCLE_STAGES = [
    'sale_ready',
    'intake',
    'diagnosis',
    'setup',
    'daily_ops',
    'weekly_review',
    'renewal',
]

DELIVERABLES = [
    'client_intake_pack',
    'workflow_diagnosis',
    'owner_map',
    'command_queue',
    'draft_route_pack',
    'daily_proof_note',
    'weekly_proof_report',
    'next_week_action_plan',
    'renewal_or_expansion_brief',
]

DAILY_DELIVERY = [
    'review_open_opportunities',
    'update_command_queue',
    'prepare_draft_routes',
    'record_proof_note',
    'log_owner_activity',
    'flag_blocked_items',
    'update_stage',
]

SLA_RULES = [
    'intake_completed_within_24h',
    'first_proof_note_by_day_2',
    'weekly_review_every_7_days',
    'approval_gates_never_auto_run',
]

VALUE_METRICS = [
    'opportunities_reviewed',
    'owners_assigned',
    'draft_routes_prepared',
    'proof_items_delivered',
    'decisions_recorded',
]

APPROVAL_GATES = [
    'external_send',
    'final_price_commitment',
    'legal_terms_acceptance',
    'contract_signature',
    'guaranteed_revenue_claim',
]


def _intake_pack(account: str, sector: str) -> dict[str, Any]:
    return {
        'account': account,
        'sector': sector,
        'questions': [
            'what channels do you use for client follow-up?',
            'who is the owner of each commercial step?',
            'what is your current close rate?',
            'what proof would convince you the system works?',
            'what is the biggest missed opportunity right now?',
            'what approval rules should we follow?',
        ],
        'data_needed': [
            'sample opportunities (last 30 days)',
            'owner list',
            'current workflow diagram or description',
        ],
        'approval_required': False,
        'auto_send': False,
    }


def _workflow_diagnosis(sector: str) -> dict[str, Any]:
    return {
        'channels_mapped': True,
        'handoffs_identified': True,
        'owners_confirmed': False,
        'missed_follow_ups_scored': True,
        'bottlenecks': ['no daily queue', 'no draft system', 'no proof tracking'],
        'sector': sector,
        'score': 'diagnosis_pending',
    }


def _command_queue(account: str) -> list[dict[str, Any]]:
    return [
        {'action': 'confirm owners', 'owner': 'Founder', 'status': 'pending', 'day': 1},
        {'action': 'map first workflow', 'owner': 'Delivery', 'status': 'pending', 'day': 1},
        {'action': 'review sample opportunities', 'owner': 'Growth', 'status': 'pending', 'day': 1},
        {'action': 'prepare first draft routes', 'owner': 'Sales', 'status': 'pending', 'day': 2},
        {'action': 'record first proof note', 'owner': 'Delivery', 'status': 'pending', 'day': 2},
        {'action': 'client review call', 'owner': 'Founder', 'status': 'pending', 'day': 3},
        {'action': account + ' weekly review', 'owner': 'Founder', 'status': 'pending', 'day': 7},
    ]


def _proof_report_template(account: str) -> dict[str, Any]:
    return {
        'account': account,
        'sections': [
            'baseline_state',
            'opportunities_reviewed',
            'owners_assigned',
            'draft_routes_prepared',
            'decisions_recorded',
            'proof_items',
            'next_plan',
        ],
        'mode': 'template_only',
        'live_sends': 0,
    }


def _renewal_brief(account: str) -> dict[str, Any]:
    return {
        'account': account,
        'trigger': 'day_7_review',
        'options': ['managed_ops_monthly', 'expansion_sprint', 'custom_system'],
        'pricing_range': '2999-25000 SAR',
        'approval_required': True,
        'auto_commit': False,
    }


def _approval_gates() -> list[dict[str, Any]]:
    return [
        {
            'gate': gate,
            'auto_run': False,
            'approval_required': True,
            'reason': 'requires founder review before execution',
        }
        for gate in APPROVAL_GATES
    ]


def build_payload(account: str = 'Demo Account', sector: str = 'Real Estate') -> dict[str, Any]:
    intake = _intake_pack(account, sector)
    diagnosis = _workflow_diagnosis(sector)
    queue = _command_queue(account)
    proof = _proof_report_template(account)
    renewal = _renewal_brief(account)
    gates = _approval_gates()

    summary = {
        'lifecycle_stages': len(LIFECYCLE_STAGES),
        'deliverables': len(DELIVERABLES),
        'daily_delivery_items': len(DAILY_DELIVERY),
        'sla_rules': len(SLA_RULES),
        'value_metrics': len(VALUE_METRICS),
        'approval_gates': len(gates),
        'live_sends': 0,
        'final_commitments': 0,
    }

    return {
        'summary': summary,
        'lifecycle': LIFECYCLE_STAGES,
        'deliverables': DELIVERABLES,
        'daily_delivery': DAILY_DELIVERY,
        'sla_rules': SLA_RULES,
        'value_metrics': VALUE_METRICS,
        'intake_pack': intake,
        'workflow_diagnosis': diagnosis,
        'owner_map': {'owners': ['Founder', 'Growth', 'Sales', 'Delivery', 'Client Owner']},
        'command_queue': queue,
        'draft_route_pack': {'mode': 'draft_only', 'routes': []},
        'proof_report_template': proof,
        'renewal_brief': renewal,
        'approval_gates': gates,
    }


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# Client Ops Max', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Lifecycle Stages')
    for stage in payload['lifecycle']:
        lines.append(f'- {stage}')
    lines.append('\n## Deliverables')
    for d in payload['deliverables']:
        lines.append(f'- {d}')
    lines.append('\n## Approval Gates')
    for gate in payload['approval_gates']:
        lines.append(f"- {gate['gate']} — auto_run: {gate['auto_run']}")
    (REPORT_DIR / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload['summary']['lifecycle_stages'] < 7:
        errors.append('lifecycle must have 7 stages')
    if payload['summary']['deliverables'] < 9:
        errors.append('deliverables must be >= 9')
    if payload['summary']['daily_delivery_items'] < 7:
        errors.append('daily delivery items must be >= 7')
    if payload['summary']['sla_rules'] < 4:
        errors.append('sla rules must be >= 4')
    if payload['summary']['value_metrics'] < 5:
        errors.append('value metrics must be >= 5')
    if payload['summary']['live_sends'] != 0:
        errors.append('live_sends must be zero')
    if payload['summary']['final_commitments'] != 0:
        errors.append('final_commitments must be zero')
    for gate in payload['approval_gates']:
        if gate['auto_run'] is not False:
            errors.append(f"approval gate {gate['gate']} cannot auto_run")
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
