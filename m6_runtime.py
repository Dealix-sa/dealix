from __future__ import annotations

import json
from pathlib import Path

REPORT = Path('reports/leadership/m6')

ACTIONS = [
    ('m6-001', 'CEO', 'approve top priorities', 'approved'),
    ('m6-002', 'Sales Director', 'review commercial queue', 'approved'),
    ('m6-003', 'Growth Director', 'review growth experiment', 'approved'),
    ('m6-004', 'Partnerships Director', 'review partner brief', 'needs_edit'),
    ('m6-005', 'Marketing Director', 'review proof content', 'needs_edit'),
    ('m6-006', 'Trust Owner', 'review safety queue', 'skipped'),
    ('m6-007', 'Pricing Owner', 'review pricing range', 'skipped'),
]


def build_payload():
    decisions = []
    for action_id, owner, title, status in ACTIONS:
        decisions.append({
            'decision_id': 'decision-' + action_id,
            'action_id': action_id,
            'owner': owner,
            'title': title,
            'from_status': 'ready_for_review',
            'to_status': status,
        })
    memory = [{'event_id': 'memory-' + d['action_id'], 'action_id': d['action_id'], 'after': d['to_status']} for d in decisions]
    proof = {
        'decisions': len(decisions),
        'approved': len([d for d in decisions if d['to_status'] == 'approved']),
        'needs_edit': len([d for d in decisions if d['to_status'] == 'needs_edit']),
        'skipped': len([d for d in decisions if d['to_status'] == 'skipped']),
        'run_now': 0,
    }
    return {'summary': {'decisions': len(decisions), 'memory_events': len(memory), 'run_now': 0}, 'decisions': decisions, 'memory': memory, 'proof': proof}


def verify(payload):
    errors = []
    if payload['summary']['run_now'] != 0:
        errors.append('run_now must be zero')
    if payload['summary']['decisions'] != payload['summary']['memory_events']:
        errors.append('memory mismatch')
    return errors


def main():
    payload = build_payload()
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    (REPORT / 'latest.md').write_text('# M6 Operating Memory\n\n' + '\n'.join(f'- {k}: `{v}`' for k, v in payload['summary'].items()) + '\n', encoding='utf-8')
    errors = verify(payload)
    print('M6_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
