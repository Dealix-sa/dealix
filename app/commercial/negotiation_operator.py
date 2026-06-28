from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any

RESTRICTED_COMMITMENTS = {
    'final_price',
    'discount_approval',
    'legal_terms_acceptance',
    'contract_signature',
    'payment_commitment',
    'refund_commitment',
    'guaranteed_roi',
    'guaranteed_revenue',
    'delivery_date_commitment_without_capacity_check',
}

OBJECTION_PLAYBOOK = {
    'price_objection': {
        'allowed_strategy': 'offer a smaller pilot, phased scope, diagnostic sprint, or proof-first sprint without approving discount',
        'draft_ar': 'أتفهم نقطة السعر. بدل ما نبدأ بنطاق كبير، نقدر نبدأ بتشخيص أو Sprint صغير يثبت القيمة التشغيلية أولًا، ثم نقرر التوسع بناءً على النتائج الفعلية.',
        'next_action': 'prepare_smaller_scope_or_diagnostic',
    },
    'not_now': {
        'allowed_strategy': 'move to nurture with a clear future review date and low-pressure value follow-up',
        'draft_ar': 'مفهوم. أقترح نخليها متابعة خفيفة في وقت مناسب، وأرسل لكم ملخص عملي يوضح أين ممكن تضيع الفرص أو المتابعات عندكم بدون أي التزام الآن.',
        'next_action': 'schedule_nurture_followup',
    },
    'send_details': {
        'allowed_strategy': 'send non-binding proposal brief with scope, range, out-of-scope, and approval_required flag',
        'draft_ar': 'أكيد. أرسل لكم ملخص واضح يشمل النطاق، المخرجات، المتطلبات، والخيارات المناسبة كبداية، ويكون العرض النهائي بعد مراجعة واعتماد التفاصيل.',
        'next_action': 'generate_proposal_brief',
    },
    'meeting_request': {
        'allowed_strategy': 'generate three booking options and an agenda; calendar write requires approval',
        'draft_ar': 'ممتاز. أقترح اجتماع قصير نراجع فيه الوضع الحالي، القنوات، والمتابعات، ونطلع بأول workflow عملي نبدأ به.',
        'next_action': 'generate_booking_options',
    },
    'contract_request': {
        'allowed_strategy': 'prepare contract review handoff; do not accept legal terms automatically',
        'draft_ar': 'نقدر نجهز ملخص النطاق والمخرجات للبدء بمراجعة العقد، لكن أي شروط قانونية أو التزامات نهائية تمر بمراجعة واعتماد صريح قبل القبول.',
        'next_action': 'legal_review_handoff',
    },
    'partnership_interest': {
        'allowed_strategy': 'propose partner discovery and value-exchange model without revenue-share commitment',
        'draft_ar': 'ممتاز. خلونا نبدأ بجلسة شراكة نفهم فيها نموذج التعاون، الجمهور المستهدف، والقيمة المتبادلة، وبعدها نجهز تصور غير ملزم للشراكة.',
        'next_action': 'generate_partnership_brief',
    },
    'unsubscribe': {
        'allowed_strategy': 'stop outreach and add to suppression list',
        'draft_ar': 'تم، سنوقف التواصل حسب طلبكم.',
        'next_action': 'suppress_contact',
    },
    'unknown': {
        'allowed_strategy': 'ask one clarifying question and keep human review required',
        'draft_ar': 'حتى أساعدكم بدقة، هل المقصود معرفة التفاصيل، الأسعار التقريبية، أو تحديد موعد قصير للمراجعة؟',
        'next_action': 'request_human_review',
    },
}

@dataclass
class NegotiationInput:
    account_id: str
    company_name: str
    reply_type: str
    message: str
    current_offer: str
    pricing_range_sar: str
    risk_level: str = 'medium'
    owner: str = 'sami'

@dataclass
class NegotiationPlan:
    negotiation_id: str
    account_id: str
    company_name: str
    reply_type: str
    allowed_strategy: str
    draft_response_ar: str
    recommended_next_action: str
    forbidden_commitments: list[str]
    approval_required: bool
    can_send_without_review: bool
    risk_level: str
    audit_reason: str
    created_at: str


def _now() -> str:
    return datetime.now(UTC).isoformat()


def classify_reply(message: str) -> str:
    text = message.lower()
    if any(x in text for x in ['غالي', 'السعر', 'price', 'expensive', 'budget']):
        return 'price_objection'
    if any(x in text for x in ['ارسل', 'التفاصيل', 'details', 'proposal']):
        return 'send_details'
    if any(x in text for x in ['موعد', 'اجتماع', 'meeting', 'call']):
        return 'meeting_request'
    if any(x in text for x in ['عقد', 'contract', 'terms']):
        return 'contract_request'
    if any(x in text for x in ['شراكة', 'partner', 'partnership']):
        return 'partnership_interest'
    if any(x in text for x in ['ليس الآن', 'بعد', 'not now', 'later']):
        return 'not_now'
    if any(x in text for x in ['إيقاف', 'الغاء', 'إلغاء', 'stop', 'unsubscribe']):
        return 'unsubscribe'
    return 'unknown'


def build_negotiation_plan(item: NegotiationInput) -> NegotiationPlan:
    reply_type = item.reply_type if item.reply_type in OBJECTION_PLAYBOOK else classify_reply(item.message)
    rule = OBJECTION_PLAYBOOK.get(reply_type, OBJECTION_PLAYBOOK['unknown'])
    restricted = sorted(RESTRICTED_COMMITMENTS)
    approval_required = reply_type not in {'unsubscribe'}
    risk_level = 'high' if reply_type in {'contract_request', 'price_objection', 'partnership_interest'} else item.risk_level
    return NegotiationPlan(
        negotiation_id=f"neg-{item.account_id}-{reply_type}",
        account_id=item.account_id,
        company_name=item.company_name,
        reply_type=reply_type,
        allowed_strategy=rule['allowed_strategy'],
        draft_response_ar=rule['draft_ar'],
        recommended_next_action=rule['next_action'],
        forbidden_commitments=restricted,
        approval_required=approval_required,
        can_send_without_review=False,
        risk_level=risk_level,
        audit_reason='Negotiation operator can suggest language and next actions, but cannot approve price, discount, legal terms, guarantees, or final commitments.',
        created_at=_now(),
    )


def demo_negotiation_day() -> dict[str, Any]:
    inputs = [
        NegotiationInput('dealix-001', 'Dealix Internal Prospect', 'price_objection', 'السعر عالي شوي، هل فيه خصم؟', '7-Day Growth Operator Sprint', '5000-12000'),
        NegotiationInput('clinic-001', 'Sample Clinic', 'meeting_request', 'نحتاج اجتماع نفهم الخدمة', 'WhatsApp Inbox Follow-up OS', '5000-12000'),
        NegotiationInput('partner-001', 'Sample Partner', 'partnership_interest', 'ممكن شراكة؟', 'Partner Growth OS', '15000-35000'),
    ]
    plans = [build_negotiation_plan(item) for item in inputs]
    return {
        'generated_at': _now(),
        'summary': {
            'plans': len(plans),
            'approval_required': len([p for p in plans if p.approval_required]),
            'live_commitments': 0,
            'can_send_without_review': len([p for p in plans if p.can_send_without_review]),
        },
        'plans': [asdict(p) for p in plans],
    }


def verify_negotiation_payload(payload: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if payload['summary']['live_commitments'] != 0:
        failures.append('live commitments must remain zero')
    if payload['summary']['can_send_without_review'] != 0:
        failures.append('all negotiation drafts require review by default')
    for plan in payload['plans']:
        forbidden = set(plan['forbidden_commitments'])
        if not RESTRICTED_COMMITMENTS.issubset(forbidden):
            failures.append(f"{plan['negotiation_id']} missing restricted commitments")
        if plan['reply_type'] != 'unsubscribe' and not plan['approval_required']:
            failures.append(f"{plan['negotiation_id']} must require approval")
    return failures
