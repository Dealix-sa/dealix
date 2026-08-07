from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPORT_DIR = Path('reports/leadership/x5')

@dataclass
class X5Action:
    action_id: str
    lane: str
    owner: str
    title: str
    priority: int
    status: str = 'ready_for_review'
    approval_required: bool = True
    auto_execute: bool = False


def _now() -> str:
    return datetime.now(UTC).isoformat()


def build_actions() -> list[X5Action]:
    return [
        X5Action('x5-001', 'ceo', 'CEO', 'approve top priorities', 95),
        X5Action('x5-002', 'sales', 'Sales Director', 'review commercial queue', 92),
        X5Action('x5-003', 'growth', 'Growth Director', 'review growth experiment', 86),
        X5Action('x5-004', 'partners', 'Partnerships Director', 'review partner brief', 84),
        X5Action('x5-005', 'marketing', 'Marketing Director', 'review proof content', 82),
        X5Action('x5-006', 'trust', 'Trust Owner', 'review safety queue', 90),
        X5Action('x5-007', 'pricing', 'Pricing Owner', 'review pricing range', 87),
    ]


def build_payload() -> dict[str, Any]:
    actions = sorted(build_actions(), key=lambda item: item.priority, reverse=True)
    inbox = [
        {'approval_id': 'approval-' + action.action_id, 'action_id': action.action_id, 'owner': action.owner, 'status': 'pending'}
        for action in actions
    ]
    audit = [
        {'event_id': 'audit-' + action.action_id, 'action_id': action.action_id, 'event': 'prepared_for_review', 'created_at': _now()}
        for action in actions
    ]
    summary = {
        'actions': len(actions),
        'approval_items': len(inbox),
        'audit_events': len(audit),
        'auto_execute': len([a for a in actions if a.auto_execute]),
    }
    return {'generated_at': _now(), 'summary': summary, 'actions': [asdict(a) for a in actions], 'approval_inbox': inbox, 'audit': audit}


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    (REPORT_DIR / 'latest.md').write_text('# X5 Action Registry\n\n' + '\n'.join(f'- {k}: `{v}`' for k, v in payload['summary'].items()) + '\n', encoding='utf-8')


def verify_payload(payload: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if payload['summary']['auto_execute'] != 0:
        failures.append('auto_execute must be zero')
    if payload['summary']['approval_items'] != payload['summary']['actions']:
        failures.append('approval inbox mismatch')
    return failures


def run_x5() -> dict[str, Any]:
    payload = build_payload()
    write_reports(payload)
    return payload
