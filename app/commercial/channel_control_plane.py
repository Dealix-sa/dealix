from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.commercial.growth_os_v2 import (
    CommercialAccount,
    GrowthCard,
    can_send_email,
    can_send_whatsapp,
    load_accounts,
    run_growth_os,
    score_account,
    validate_sources,
)

REPORT_DIR = Path('reports/commercial/channel_control')
ALLOWED_CHANNELS = {'email', 'whatsapp', 'linkedin_manual', 'phone', 'website_form', 'partner_referral'}

@dataclass
class ChannelAction:
    action_id: str
    card_id: str
    account_id: str
    company_name: str
    channel: str
    action_type: str
    payload: dict[str, Any]
    status: str
    owner_decision: str
    approval_required: bool
    safety_allowed: bool
    blocked_by: list[str]
    next_action: str
    audit_level: str
    created_at: str

@dataclass
class HumanApprovalCard:
    approval_id: str
    action_id: str
    title: str
    summary: str
    buttons: list[dict[str, str]]
    required_role: str
    decision_status: str

@dataclass
class ChannelAuditEvent:
    event_id: str
    action_id: str
    channel: str
    event_type: str
    detail: str
    created_at: str


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _card_text(card: GrowthCard, account: CommercialAccount) -> str:
    if card.recommended_channel == 'email':
        return card.draft_message_en if account.public_email and account.public_email.endswith('.com') else card.draft_message_ar
    return card.draft_message_ar


def whatsapp_payload(card: GrowthCard, account: CommercialAccount) -> dict[str, Any]:
    return {
        'type': 'interactive',
        'interactive': {
            'type': 'button',
            'body': {'text': card.draft_message_ar[:1024]},
            'action': {'buttons': [
                {'type': 'reply', 'reply': {'id': f"wa:{card.card_id}:approve", 'title': 'مهتم'}},
                {'type': 'reply', 'reply': {'id': f"wa:{card.card_id}:details", 'title': 'التفاصيل'}},
                {'type': 'reply', 'reply': {'id': f"wa:{card.card_id}:stop", 'title': 'إيقاف'}},
            ]},
        },
        'to': account.whatsapp,
        'mode': 'draft_payload_only',
        'requires_opt_in': True,
    }


def email_payload(card: GrowthCard, account: CommercialAccount) -> dict[str, Any]:
    return {
        'to': account.public_email,
        'subject': f'Dealix Commercial Growth OS — {account.company_name}',
        'body': _card_text(card, account),
        'includes_opt_out': True,
        'mode': 'draft_payload_only',
    }


def linkedin_payload(card: GrowthCard, account: CommercialAccount) -> dict[str, Any]:
    return {
        'profile_url': account.linkedin_url,
        'manual_task': True,
        'message_draft': card.draft_message_ar,
        'mode': 'manual_assisted_only',
        'no_auto_dm': True,
    }


def phone_payload(card: GrowthCard, account: CommercialAccount) -> dict[str, Any]:
    return {
        'phone': account.phone,
        'manual_task': True,
        'call_script_ar': 'ابدأ بفهم الهدف التجاري، ثم اسأل عن القناة الأكثر ألمًا، ثم اعرض Sprint صغير بدون وعود مضمونة.',
        'mode': 'manual_call_task',
    }


def website_form_payload(card: GrowthCard, account: CommercialAccount) -> dict[str, Any]:
    return {
        'url': account.source_url or account.website,
        'manual_task': True,
        'message_draft': card.draft_message_ar,
        'mode': 'manual_form_submission',
    }


def partner_payload(card: GrowthCard, account: CommercialAccount) -> dict[str, Any]:
    return {
        'partner_email': account.public_email,
        'partner_url': account.source_url,
        'partnership_angle': 'co-sell, referral, or operational growth partnership',
        'message_draft': card.draft_message_ar,
        'mode': 'partnership_draft_only',
    }


def build_payload(card: GrowthCard, account: CommercialAccount) -> dict[str, Any]:
    channel = card.recommended_channel if card.recommended_channel in ALLOWED_CHANNELS else 'email'
    if channel == 'whatsapp':
        return whatsapp_payload(card, account)
    if channel == 'email':
        return email_payload(card, account)
    if channel == 'linkedin_manual':
        return linkedin_payload(card, account)
    if channel == 'phone':
        return phone_payload(card, account)
    if channel == 'partner_referral':
        return partner_payload(card, account)
    return website_form_payload(card, account)


def _safety_for(card: GrowthCard, account: CommercialAccount) -> tuple[bool, list[str], str]:
    action = {'status': 'approved' if card.owner_decision == 'send' else card.send_status, 'owner_decision': card.owner_decision}
    if card.recommended_channel == 'whatsapp':
        decision = can_send_whatsapp(action, account, {})
        return decision.allowed, decision.blocked_by, decision.audit_level
    if card.recommended_channel == 'email':
        decision = can_send_email(action, account, {})
        return decision.allowed, decision.blocked_by, decision.audit_level
    if card.recommended_channel == 'linkedin_manual':
        return False, ['manual_only_no_auto_dm'], 'L3'
    if card.recommended_channel == 'phone':
        return False, ['manual_call_required'], 'L2'
    if card.recommended_channel in {'website_form', 'partner_referral'}:
        return False, ['manual_or_partner_review_required'], 'L2'
    return False, ['unknown_channel'], 'L2'


def build_channel_actions(snapshot: dict[str, Any]) -> list[ChannelAction]:
    accounts = {x['account_id']: CommercialAccount(**x) for x in snapshot['accounts']}
    actions: list[ChannelAction] = []
    for raw in snapshot['cards']:
        card = GrowthCard(**raw)
        account = accounts[card.account_id]
        allowed, blocked, audit_level = _safety_for(card, account)
        actions.append(ChannelAction(
            action_id=f"act-{card.card_id}-{card.recommended_channel}",
            card_id=card.card_id,
            account_id=card.account_id,
            company_name=card.company_name,
            channel=card.recommended_channel,
            action_type='send_or_manual_task',
            payload=build_payload(card, account),
            status='ready_for_human_review' if card.send_status == 'draft_only' else card.send_status,
            owner_decision='review',
            approval_required=True,
            safety_allowed=allowed,
            blocked_by=blocked,
            next_action='approve_edit_skip_book_or_assign_owner',
            audit_level=audit_level,
            created_at=_now(),
        ))
    return actions


def build_approval_cards(actions: list[ChannelAction]) -> list[HumanApprovalCard]:
    approvals = []
    for action in actions:
        approvals.append(HumanApprovalCard(
            approval_id=f"approve-{action.action_id}",
            action_id=action.action_id,
            title=f"{action.channel} action for {action.company_name}",
            summary=f"Review {action.channel} payload, risks={','.join(action.blocked_by) or 'none'}, next={action.next_action}",
            buttons=[
                {'id': f"{action.action_id}:approve", 'title': 'اعتماد'},
                {'id': f"{action.action_id}:edit", 'title': 'تعديل'},
                {'id': f"{action.action_id}:skip", 'title': 'تخطي'},
            ],
            required_role='founder_or_sales_owner',
            decision_status='pending',
        ))
    return approvals


def build_audit(actions: list[ChannelAction]) -> list[ChannelAuditEvent]:
    events = []
    for action in actions:
        events.append(ChannelAuditEvent(
            event_id=f"audit-{action.action_id}",
            action_id=action.action_id,
            channel=action.channel,
            event_type='action_prepared_not_sent',
            detail='Prepared payload/task with human approval required and safe defaults enforced.',
            created_at=action.created_at,
        ))
    return events


def run_channel_control_plane() -> dict[str, Any]:
    snapshot = run_growth_os()
    actions = build_channel_actions(snapshot)
    approvals = build_approval_cards(actions)
    audit = build_audit(actions)
    payload = {
        'generated_at': _now(),
        'summary': {
            'actions': len(actions),
            'approval_cards': len(approvals),
            'audit_events': len(audit),
            'live_sends': 0,
            'manual_linkedin_tasks': len([a for a in actions if a.channel == 'linkedin_manual']),
            'whatsapp_payloads': len([a for a in actions if a.channel == 'whatsapp']),
            'email_payloads': len([a for a in actions if a.channel == 'email']),
        },
        'actions': [asdict(a) for a in actions],
        'approval_cards': [asdict(a) for a in approvals],
        'audit': [asdict(e) for e in audit],
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    (REPORT_DIR / 'latest.md').write_text('# Dealix Commercial Channel Control Plane\n\n' + '\n'.join([f"- {k}: `{v}`" for k, v in payload['summary'].items()]) + '\n', encoding='utf-8')
    return payload


def verify_channel_control(payload: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if payload['summary']['live_sends'] != 0:
        failures.append('live sends must remain zero by default')
    for action in payload['actions']:
        if action['channel'] == 'whatsapp' and not action['payload'].get('requires_opt_in'):
            failures.append(f"{action['action_id']} whatsapp missing opt-in flag")
        if action['channel'] == 'linkedin_manual' and not action['payload'].get('no_auto_dm'):
            failures.append(f"{action['action_id']} linkedin must be manual only")
        if action['approval_required'] is not True:
            failures.append(f"{action['action_id']} must require approval")
    for card in payload['approval_cards']:
        if len(card['buttons']) > 3:
            failures.append(f"{card['approval_id']} has too many approval buttons")
    return failures
