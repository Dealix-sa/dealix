from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import rcmax
import auto14
import client_ops_max
import deal_conversation_intelligence as dci
import deal_strategy_brain as dsb

REPORT_DIR = Path('reports/commercial/client_service_autopilot')

SENSITIVE_ACTIONS = [
    'external_email_send',
    'whatsapp_send',
    'calendar_invite_send',
    'final_price_commitment',
    'legal_terms_acceptance',
    'contract_signature',
    'guaranteed_revenue_claim',
    'public_claim_without_review',
]


def _client_workspace(account: str, sector: str, offer: str) -> dict[str, Any]:
    return {
        'account': account,
        'sector': sector,
        'offer': offer,
        'status': 'active',
        'created': 'today',
        'folders': [
            'intake',
            'diagnosis',
            'command_queue',
            'drafts',
            'proof',
            'weekly_review',
            'renewal',
        ],
    }


def _weekly_review_pack(account: str) -> dict[str, Any]:
    return {
        'account': account,
        'sections': [
            'opportunities_reviewed',
            'owners_confirmed',
            'drafts_prepared',
            'proof_delivered',
            'decisions_recorded',
            'blocked_items',
            'next_week_plan',
        ],
        'cadence': 'every_7_days',
        'approval_required': False,
        'auto_send': False,
    }


def _approval_queue(intel: dict[str, Any], strategy: dict[str, Any]) -> list[dict[str, Any]]:
    queue = []
    for action in SENSITIVE_ACTIONS:
        queue.append({
            'action': action,
            'status': 'pending_approval',
            'auto_run': False,
            'triggered_by': 'system',
        })
    for gate in strategy.get('approval_gates', []):
        if not any(q['action'] == gate for q in queue):
            queue.append({
                'action': gate,
                'status': 'pending_approval',
                'auto_run': False,
                'triggered_by': 'deal_strategy',
            })
    return queue


def build_payload(
    account: str = 'Demo Account',
    sector: str = 'Real Estate',
    message: str = 'كم السعر؟',
) -> dict[str, Any]:
    base_command = rcmax.build_payload()
    auto_pack = auto14.build_payload()
    ops = client_ops_max.build_payload(account, sector)
    intel = dci.classify(message)
    strategy = dsb.build_strategy(account, sector, message)

    workspace = _client_workspace(account, sector, base_command['command']['offer'])
    weekly_review = _weekly_review_pack(account)
    approval_queue = _approval_queue(intel, strategy)

    auto_prepared = [
        'client_workspace',
        'intake_pack',
        'workflow_diagnosis',
        'owner_map',
        'command_queue',
        'draft_route_pack',
        'conversation_readout',
        'deal_strategy',
        'proposal_folder',
        'daily_delivery_plan',
        'weekly_review_pack',
        'proof_report_template',
        'renewal_plan',
    ]

    summary = {
        'auto_prepared_items': len(auto_prepared),
        'approval_queue_items': len(approval_queue),
        'live_sends': 0,
        'final_commitments': 0,
        'lifecycle_stages': ops['summary']['lifecycle_stages'],
        'deliverables': ops['summary']['deliverables'],
    }

    return {
        'summary': summary,
        'client_workspace': workspace,
        'intake_pack': ops['intake_pack'],
        'conversation_readout': intel,
        'deal_strategy': strategy,
        'proposal_folder': auto_pack['artifacts']['proposal_folder'],
        'daily_delivery_plan': {
            'items': ops['daily_delivery'],
            'auto_run': True,
            'live_send': False,
        },
        'weekly_review_pack': weekly_review,
        'proof_report_template': ops['proof_report_template'],
        'approval_queue': approval_queue,
        'renewal_plan': ops['renewal_brief'],
        'auto_prepared': auto_prepared,
        'rcmax_command': base_command['command'],
        'auto14_summary': auto_pack['summary'],
        'ops_summary': ops['summary'],
    }


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
    lines = ['# Client Service Autopilot', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Auto-Prepared Items')
    for item in payload['auto_prepared']:
        lines.append(f'- {item}')
    lines.append('\n## Approval Queue')
    for item in payload['approval_queue']:
        lines.append(f"- {item['action']} — {item['status']}")
    lines.append('\n## Deal Strategy')
    strategy = payload['deal_strategy']
    lines.append(f"- Score: {strategy['deal_score']}")
    lines.append(f"- Probability: {strategy['close_probability_band']}")
    lines.append(f"- Next action: {strategy['next_best_action']}")
    (REPORT_DIR / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_sections = [
        'client_workspace', 'intake_pack', 'conversation_readout', 'deal_strategy',
        'proposal_folder', 'daily_delivery_plan', 'weekly_review_pack',
        'proof_report_template', 'approval_queue', 'renewal_plan',
    ]
    for section in required_sections:
        if section not in payload:
            errors.append(f'missing section: {section}')
    if payload['summary']['auto_prepared_items'] < 10:
        errors.append('auto_prepared_items must be >= 10')
    if payload['summary']['live_sends'] != 0:
        errors.append('live_sends must be zero')
    if payload['summary']['final_commitments'] != 0:
        errors.append('final_commitments must be zero')
    if not payload.get('proof_report_template'):
        errors.append('proof_report_template missing')
    if not payload.get('renewal_plan'):
        errors.append('renewal_plan missing')
    if not payload.get('deal_strategy', {}).get('next_best_action'):
        errors.append('deal_strategy missing next_best_action')
    for item in payload.get('approval_queue', []):
        if item.get('auto_run') is not False:
            errors.append(f"approval item {item['action']} has auto_run=True")
    return errors


def main() -> int:
    payload = build_payload()
    write_reports(payload)
    errors = verify(payload)
    print('CLIENT_AUTOPILOT_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
