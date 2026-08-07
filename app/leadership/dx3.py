from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPORT_DIR = Path('reports/leadership/dx3')

LANES = ['ceo', 'growth', 'sales', 'partners', 'marketing', 'success', 'delivery', 'trust', 'pricing', 'board']

@dataclass
class Dx3Item:
    id: str
    lane: str
    owner: str
    level: str
    title: str
    why_now: str
    next_step: str
    metric: str
    score: int
    needs_review: bool = True
    auto_execute: bool = False


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _item(lane: str, n: int, owner: str, level: str, title: str, why_now: str, next_step: str, metric: str, score: int) -> Dx3Item:
    return Dx3Item(f'{lane}-{n}', lane, owner, level, title, why_now, next_step, metric, score)


def build_items() -> list[Dx3Item]:
    return [
        _item('ceo', 1, 'CEO', 'strategic', 'pick top company move', 'too many possible directions', 'approve three moves only', 'decision clarity', 95),
        _item('ceo', 2, 'CEO', 'strategic', 'review high risk queue', 'some decisions affect terms or price', 'approve or defer risk items', 'risk reduced', 92),
        _item('growth', 1, 'Growth Director', 'tactical', 'run one sector experiment', 'focused tests create learning', 'prepare clinic segment test', 'qualified replies', 86),
        _item('growth', 2, 'Growth Director', 'tactical', 'reactivate old prospects', 'stale prospects are cheaper than new ones', 'prepare value followups', 'reactivated leads', 78),
        _item('sales', 1, 'Sales Director', 'execution', 'move open proposals', 'open proposals need a next step', 'prepare proposal push cards', 'proposal movement', 88),
        _item('sales', 2, 'Sales Director', 'execution', 'handle objections', 'price and timing objections block deals', 'prepare objection replies', 'objections handled', 91),
        _item('partners', 1, 'Partnerships Director', 'strategic', 'create referral channel', 'partners can reduce acquisition cost', 'prepare partner value brief', 'partner meetings', 84),
        _item('partners', 2, 'Partnerships Director', 'strategic', 'explore ecosystem partner', 'integration channels can compound growth', 'prepare discovery note', 'discovery calls', 74),
        _item('marketing', 1, 'Marketing Director', 'tactical', 'publish founder proof post', 'market needs clear positioning', 'draft founder post', 'content shipped', 81),
        _item('marketing', 2, 'Marketing Director', 'tactical', 'build proof asset', 'proof makes sales easier', 'turn report into proof asset', 'proof assets', 83),
        _item('success', 1, 'Customer Success', 'execution', 'check client health', 'retention depends on visible progress', 'prepare client update', 'client health', 76),
        _item('delivery', 1, 'Delivery Ops', 'execution', 'remove delivery blockers', 'blocked work slows proof', 'request missing input', 'blockers resolved', 80),
        _item('trust', 1, 'Trust Owner', 'control', 'review claims and channels', 'trust protects company reputation', 'review risk gates', 'risks blocked', 90),
        _item('pricing', 1, 'Pricing Owner', 'control', 'review scope and range', 'unclear scope weakens margin', 'review pricing ranges', 'pricing clarity', 87),
        _item('board', 1, 'Board Memo Owner', 'weekly', 'prepare weekly memo', 'leadership needs a single narrative', 'summarize moves risks and proof', 'memo ready', 70),
    ]


def build_payload() -> dict[str, Any]:
    items = build_items()
    top = sorted(items, key=lambda x: x.score, reverse=True)[:7]
    lane_counts = {lane: len([x for x in items if x.lane == lane]) for lane in LANES}
    payload = {
        'generated_at': _now(),
        'summary': {
            'lanes': len(LANES),
            'items': len(items),
            'top_items': len(top),
            'review_required': len([x for x in items if x.needs_review]),
            'auto_execute': len([x for x in items if x.auto_execute]),
            'avg_score': round(sum(x.score for x in items) / len(items), 2),
        },
        'lane_counts': lane_counts,
        'items': [asdict(x) for x in items],
        'top_items': [asdict(x) for x in top],
    }
    return payload


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Dealix DX3 Leadership Expansion', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Top Items')
    for item in payload['top_items']:
        lines.append(f"- **{item['lane']}** — {item['title']} → `{item['next_step']}`")
    (REPORT_DIR / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify_payload(payload: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if payload['summary']['auto_execute'] != 0:
        failures.append('auto_execute must be zero')
    if payload['summary']['review_required'] != payload['summary']['items']:
        failures.append('all items must require review')
    for lane in LANES:
        if payload['lane_counts'].get(lane, 0) <= 0:
            failures.append(f'{lane} missing')
    for item in payload['items']:
        if not item['next_step'] or not item['metric']:
            failures.append(f"{item['id']} missing next step or metric")
        if item['score'] < 0 or item['score'] > 100:
            failures.append(f"{item['id']} invalid score")
    return failures


def run_dx3() -> dict[str, Any]:
    payload = build_payload()
    write_reports(payload)
    return payload
