from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPORT_DIR = Path('reports/leadership/cmd_v2')

LANES = [
    'ceo',
    'growth',
    'sales_negotiation',
    'partnerships',
    'marketing',
    'trust_pricing',
    'whatsapp_routing',
    'command_room_ui',
]

OWNERS = {
    'ceo': 'CEO',
    'growth': 'Growth Director',
    'sales_negotiation': 'Sales Director',
    'partnerships': 'Partnerships Director',
    'marketing': 'Marketing Director',
    'trust_pricing': 'Trust and Pricing Owner',
    'whatsapp_routing': 'Operations Owner',
    'command_room_ui': 'Product Owner',
}

@dataclass
class CmdAction:
    action_id: str
    lane: str
    owner: str
    title: str
    objective: str
    channel: str
    target: str
    recommendation: str
    next_action: str
    metric: str
    risk: str
    approval_required: bool = True
    external_send: bool = False
    final_commitment: bool = False

@dataclass
class CmdCard:
    card_id: str
    lane: str
    owner: str
    title: str
    summary: str
    actions: list[str]
    buttons: list[dict[str, str]]
    approval_required: bool = True
    external_send: bool = False


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _action(lane: str, idx: int, title: str, objective: str, channel: str, target: str, recommendation: str, next_action: str, metric: str, risk: str = 'medium') -> CmdAction:
    return CmdAction(
        action_id=f'{lane}-{idx:02d}',
        lane=lane,
        owner=OWNERS[lane],
        title=title,
        objective=objective,
        channel=channel,
        target=target,
        recommendation=recommendation,
        next_action=next_action,
        metric=metric,
        risk=risk,
    )


def lane_actions() -> dict[str, list[CmdAction]]:
    return {
        'ceo': [
            _action('ceo', 1, 'Top company decision', 'Choose the highest leverage move today.', 'summary_card', 'all lanes', 'Approve only the top three decisions.', 'approve_top_decisions', 'decisions approved'),
            _action('ceo', 2, 'Escalation review', 'Review sensitive commercial items.', 'dashboard', 'risk queue', 'Approve, edit, or defer sensitive items.', 'review_escalations', 'escalations resolved', 'high'),
        ],
        'growth': [
            _action('growth', 1, 'Sector growth experiment', 'Run one focused acquisition test.', 'email_draft', 'clinics or B2B services', 'Prepare a small batch and measure replies.', 'prepare_growth_experiment', 'qualified replies'),
            _action('growth', 2, 'Reactivation loop', 'Recover stale opportunities.', 'email_draft', 'stale prospects', 'Prepare low pressure follow-up drafts.', 'prepare_reactivation_loop', 'reactivated leads'),
        ],
        'sales_negotiation': [
            _action('sales_negotiation', 1, 'Open proposal push', 'Move open proposals to the next step.', 'email_draft', 'open proposals', 'Prepare a non-binding proposal push.', 'prepare_proposal_push', 'proposal movement'),
            _action('sales_negotiation', 2, 'Objection desk', 'Handle price and timing objections.', 'review_card', 'hot replies', 'Offer smaller scope or diagnostic option.', 'prepare_objection_response', 'objections handled', 'high'),
        ],
        'partnerships': [
            _action('partnerships', 1, 'Referral partner brief', 'Create a partnership path with B2B firms.', 'partner_brief', 'B2B services', 'Prepare mutual value brief.', 'prepare_referral_brief', 'partner meetings'),
            _action('partnerships', 2, 'Integration discovery', 'Explore CRM or ecosystem partnerships.', 'manual_linkedin', 'CRM partners', 'Prepare discovery note only.', 'prepare_integration_discovery', 'discovery calls'),
        ],
        'marketing': [
            _action('marketing', 1, 'Founder content', 'Explain Dealix as an operating system.', 'manual_linkedin', 'Saudi founders', 'Draft a founder post with proof language.', 'draft_founder_post', 'content shipped'),
            _action('marketing', 2, 'Proof asset', 'Convert daily operation into a proof asset.', 'dashboard', 'prospects and clients', 'Use only verified operational output.', 'prepare_proof_asset', 'proof assets'),
        ],
        'trust_pricing': [
            _action('trust_pricing', 1, 'Safety and claims gate', 'Review risky claims and channel actions.', 'audit', 'all outbound drafts', 'Block unsupported claims and risky actions.', 'review_safety_gates', 'risks blocked', 'high'),
            _action('trust_pricing', 2, 'Pricing range gate', 'Protect margin and scope clarity.', 'dashboard', 'proposal queue', 'Use ranges and scope until approval.', 'review_pricing_ranges', 'pricing decisions', 'high'),
        ],
        'whatsapp_routing': [
            _action('whatsapp_routing', 1, 'Role cards', 'Prepare role-specific decision cards.', 'whatsapp_payload', 'leaders', 'Generate cards for review only.', 'generate_role_cards', 'cards prepared'),
        ],
        'command_room_ui': [
            _action('command_room_ui', 1, 'UI snapshot', 'Prepare frontend snapshot for command room.', 'snapshot', 'apps web', 'Generate JSON and TypeScript snapshot.', 'generate_ui_snapshot', 'snapshot generated'),
        ],
    }


def decision_cards(actions: list[CmdAction]) -> list[CmdCard]:
    cards: list[CmdCard] = []
    for lane in LANES:
        items = [a for a in actions if a.lane == lane][:3]
        if not items:
            continue
        cards.append(CmdCard(
            card_id=f'cmd-v2-{lane}',
            lane=lane,
            owner=OWNERS[lane],
            title=f'{OWNERS[lane]} daily command',
            summary=' | '.join(a.title for a in items),
            actions=[a.next_action for a in items],
            buttons=[
                {'id': f'{lane}:approve', 'title': 'اعتماد'},
                {'id': f'{lane}:edit', 'title': 'تعديل'},
                {'id': f'{lane}:skip', 'title': 'تخطي'},
            ],
        ))
    return cards


def build_payload() -> dict[str, Any]:
    lanes = lane_actions()
    actions = [a for values in lanes.values() for a in values]
    cards = decision_cards(actions)
    summary = {
        'lanes': len(lanes),
        'actions': len(actions),
        'decision_cards': len(cards),
        'ceo_decisions': len(lanes['ceo']),
        'growth_actions': len(lanes['growth']),
        'sales_negotiation_actions': len(lanes['sales_negotiation']),
        'partnership_actions': len(lanes['partnerships']),
        'marketing_actions': len(lanes['marketing']),
        'trust_pricing_actions': len(lanes['trust_pricing']),
        'whatsapp_routing_actions': len(lanes['whatsapp_routing']),
        'ui_actions': len(lanes['command_room_ui']),
        'approval_required': len([a for a in actions if a.approval_required]),
        'external_sends': len([a for a in actions if a.external_send]),
        'final_commitments': len([a for a in actions if a.final_commitment]),
    }
    return {
        'generated_at': _now(),
        'summary': summary,
        'lanes': {k: [asdict(a) for a in v] for k, v in lanes.items()},
        'decision_cards': [asdict(c) for c in cards],
    }


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Dealix Command v2', '', f"- generated_at: `{payload['generated_at']}`"]
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    (REPORT_DIR / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify_payload(payload: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if payload['summary']['external_sends'] != 0:
        failures.append('external_sends must stay zero')
    if payload['summary']['final_commitments'] != 0:
        failures.append('final_commitments must stay zero')
    for lane in LANES:
        if lane not in payload['lanes'] or not payload['lanes'][lane]:
            failures.append(f'{lane} missing actions')
    for card in payload['decision_cards']:
        if len(card['buttons']) > 3:
            failures.append(f"{card['card_id']} has too many buttons")
        if card['approval_required'] is not True:
            failures.append(f"{card['card_id']} must require approval")
        if card['external_send'] is not False:
            failures.append(f"{card['card_id']} must not be external send")
    return failures


def run_cmd_v2() -> dict[str, Any]:
    payload = build_payload()
    write_reports(payload)
    return payload
