from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

REPORT_DIR = Path('reports/commercial/deal_conversation_intelligence')

INTENT_MAP: dict[str, list[str]] = {
    'price_question': ['كم السعر', 'كم التكلفة', 'كم الرسوم', 'what is the price', 'how much', 'pricing', 'سعر', 'تكلفة'],
    'proposal_request': ['ارسل العرض', 'نبغى عرض', 'send proposal', 'نريد عرض', 'send the offer', 'proposal'],
    'meeting_request': ['نبغى اجتماع', 'موعد', 'lets meet', 'meeting', 'call', 'اتصال', 'نتحدث'],
    'ask_for_details': ['وش يشمل', 'تفاصيل', 'more details', 'what does it include', 'كيف يشتغل', 'how does it work'],
    'discount_request': ['خصم', 'تخفيض', 'discount', 'reduce price', 'lower price', 'مو كامل السعر'],
    'price_objection': ['غالي', 'ميزانية محدودة', 'too expensive', 'budget'],
    'timing_objection': ['مو الحين', 'بعدين', 'not now', 'next quarter', 'later', 'الربع القادم', 'انتهى الميزانية'],
    'trust_objection': ['مجربين', 'كيف نثق', 'proof', 'case study', 'examples', 'اثبت', 'شواهد', 'ما عندكم تجربة'],
    'procurement_request': ['مشتريات', 'procurement', 'vendor registration', 'تسجيل مورد', 'رقم الضريبة'],
    'legal_terms': ['شروط', 'عقد', 'contract', 'terms', 'legal', 'مسؤولية', 'ضمان', 'guarantee'],
    'not_interested': ['ما نحتاج', 'لا شكرا', 'not interested', 'no thanks', 'مو محتاجين', 'ما يناسبنا'],
    'unsubscribe': ['وقف التواصل', 'لا تتصل', 'stop contact', 'unsubscribe', 'remove me', 'اوقف', 'لا تراسلني'],
    'interested': ['مهتمين', 'يبدو جيد', 'sounds good', 'interested', 'tell me more', 'اخبرني اكثر', 'نعم'],
}

STAGE_SIGNALS: dict[str, list[str]] = {
    'cold': ['من انتم', 'who are you', 'ما هو dealix', 'ما هو ديلكس'],
    'aware': ['شفت', 'سمعت', 'I heard', 'someone mentioned', 'رأيت'],
    'interested': ['مهتمين', 'interested', 'يبدو جيد', 'tell me more'],
    'discovery': ['تفاصيل', 'details', 'يشمل', 'include', 'كيف', 'how'],
    'proposal': ['ارسل العرض', 'proposal', 'عرض رسمي', 'official offer'],
    'negotiation': ['خصم', 'discount', 'تفاوض', 'negotiate', 'غالي', 'expensive'],
    'procurement': ['مشتريات', 'procurement', 'تسجيل', 'register'],
    'closed_won': ['موافق', 'agreed', 'proceed', 'تعاملنا', 'let\'s go'],
    'closed_lost': ['ما نحتاج', 'not interested', 'decided on another', 'اخترنا غيركم'],
    'renewal': ['تجديد', 'renew', 'extend', 'continue', 'استمرار'],
    'expansion': ['توسيع', 'expand', 'add more', 'more services', 'خدمات اضافية'],
}

OBJECTION_MAP: dict[str, list[str]] = {
    'price': ['غالي', 'ميزانية', 'expensive', 'budget', 'تكلفة عالية'],
    'timing': ['مو الحين', 'not now', 'later', 'بعدين', 'الربع'],
    'trust': ['اثبت', 'proof', 'مجربين', 'case study', 'ما عندكم', 'شواهد'],
    'authority': ['ما عندي صلاحية', 'not my decision', 'management', 'الإدارة', 'مدير'],
    'details': ['تفاصيل', 'not clear', 'need more info', 'غير واضح'],
    'competition': ['عندنا', 'we already have', 'اخترنا', 'competitor', 'بديل'],
    'scope': ['واسع', 'too much', 'not all', 'بس جزء', 'partial'],
    'legal': ['عقد', 'terms', 'contract', 'شروط', 'مسؤولية'],
}

DISCOVERY_QUESTIONS: dict[str, list[str]] = {
    'price_objection': [
        'ما هو الميزانية المتاحة لهذا النوع من الحلول؟',
        'هل الميزانية محددة للسنة أو للمشروع؟',
        'ما هو التأثير المالي للمشكلة الحالية على العمل؟',
    ],
    'timing_objection': [
        'متى يكون التوقيت المناسب؟',
        'ما الذي يجب أن يحدث أولاً قبل البدء؟',
        'هل هناك حدث قادم يؤثر على القرار؟',
    ],
    'trust_objection': [
        'ما هو الدليل الذي سيقنعكم بالمضي قدماً؟',
        'هل تريدون التحدث مع عملاء سابقين؟',
        'ما هي النتيجة التي ستثبت لكم أن النظام يعمل؟',
    ],
    'not_interested': [
        'ما هو التحدي الأكبر الذي تواجهونه الآن؟',
        'هل هناك شيء محدد لم يناسبكم في ما عرضناه؟',
    ],
    'ask_for_details': [
        'ما هو القسم أو العملية التي تهتمون بتحسينها أولاً؟',
        'من هم الأشخاص المعنيون بهذا القرار؟',
        'ما هو التوقع للنتائج في أول 30 يوم؟',
    ],
    'default': [
        'ما هو أكبر تحدٍّ تواجهونه الآن في المبيعات أو الخدمة؟',
        'من يملك قرار هذا الموضوع؟',
        'ما هو الهدف الرئيسي للربع القادم؟',
        'كيف تقيسون النجاح حالياً؟',
    ],
}


def _normalize(text: str) -> str:
    return text.lower().strip()


def _detect_intent(text: str) -> str:
    t = _normalize(text)
    for intent, keywords in INTENT_MAP.items():
        if any(kw.lower() in t for kw in keywords):
            return intent
    return 'unknown'


def _detect_stage(text: str, intent: str) -> str:
    t = _normalize(text)
    for stage, signals in STAGE_SIGNALS.items():
        if any(s.lower() in t for s in signals):
            return stage
    stage_from_intent = {
        'price_question': 'interested',
        'proposal_request': 'proposal',
        'meeting_request': 'discovery',
        'ask_for_details': 'discovery',
        'price_objection': 'negotiation',
        'timing_objection': 'interested',
        'trust_objection': 'interested',
        'procurement_request': 'procurement',
        'legal_terms': 'negotiation',
        'discount_request': 'negotiation',
        'not_interested': 'closed_lost',
        'unsubscribe': 'closed_lost',
        'interested': 'interested',
    }
    return stage_from_intent.get(intent, 'aware')


def _detect_objection(text: str, intent: str) -> str:
    t = _normalize(text)
    for objection, keywords in OBJECTION_MAP.items():
        if any(kw.lower() in t for kw in keywords):
            return objection
    intent_to_objection = {
        'price_objection': 'price',
        'timing_objection': 'timing',
        'trust_objection': 'trust',
        'legal_terms': 'legal',
        'discount_request': 'price',
    }
    return intent_to_objection.get(intent, 'none')


def _detect_sentiment(text: str, intent: str) -> str:
    positive = ['جيد', 'ممتاز', 'نعم', 'موافق', 'مهتم', 'good', 'great', 'yes', 'interested', 'agreed']
    negative = ['لا', 'غالي', 'ما نحتاج', 'no', 'expensive', 'not interested', 'stop']
    t = _normalize(text)
    pos = sum(1 for w in positive if w.lower() in t)
    neg = sum(1 for w in negative if w.lower() in t)
    if intent in ('not_interested', 'unsubscribe', 'price_objection', 'timing_objection', 'trust_objection'):
        return 'negative'
    if intent in ('interested', 'meeting_request', 'proposal_request'):
        return 'positive'
    if pos > neg:
        return 'positive'
    if neg > pos:
        return 'negative'
    return 'neutral'


def _detect_urgency(text: str, intent: str) -> str:
    urgent = ['الحين', 'فوري', 'urgent', 'asap', 'immediately', 'اليوم', 'today', 'هذا الاسبوع', 'this week']
    low = ['بعدين', 'later', 'الربع القادم', 'next year', 'مو الحين']
    t = _normalize(text)
    if any(u.lower() in t for u in urgent):
        return 'high'
    if any(l.lower() in t for l in low):
        return 'low'
    if intent in ('meeting_request', 'proposal_request'):
        return 'medium'
    return 'low'


def _missing_info(intent: str, text: str) -> list[str]:
    missing = []
    t = _normalize(text)
    if intent in ('price_question', 'proposal_request', 'discount_request'):
        if 'scope' not in t and 'نطاق' not in t:
            missing.append('scope_not_defined')
        if 'budget' not in t and 'ميزانية' not in t:
            missing.append('budget_unknown')
    if intent in ('meeting_request', 'proposal_request'):
        if 'owner' not in t and 'مسؤول' not in t and 'قرار' not in t:
            missing.append('decision_maker_unknown')
    if intent == 'ask_for_details':
        missing.append('specific_area_of_interest_unclear')
    return missing


def _response_angle(intent: str, stage: str, objection: str) -> str:
    if intent == 'price_question':
        return 'share_pricing_range_with_scope_caveat'
    if intent == 'proposal_request':
        return 'prepare_proposal_folder_for_review'
    if intent == 'meeting_request':
        return 'confirm_discovery_call_and_send_agenda_draft'
    if intent == 'ask_for_details':
        return 'send_one_page_offer_and_case_highlight'
    if objection == 'price':
        return 'anchor_value_before_price_reframe_scope'
    if objection == 'timing':
        return 'discover_trigger_and_set_future_touchpoint'
    if objection == 'trust':
        return 'share_proof_pack_and_propose_pilot'
    if intent == 'not_interested':
        return 'polite_close_or_low_touch_nurture'
    if intent == 'unsubscribe':
        return 'mark_do_not_contact_and_comply'
    return 'ask_discovery_question'


def _next_best_action(intent: str, stage: str, objection: str, urgency: str) -> str:
    if intent == 'unsubscribe':
        return 'mark_do_not_contact_immediately'
    if intent == 'not_interested':
        return 'send_polite_close_note_and_add_to_long_nurture'
    if intent == 'proposal_request':
        return 'prepare_proposal_folder_queue_for_founder_review'
    if intent == 'meeting_request':
        return 'draft_meeting_agenda_and_confirm_owner'
    if intent == 'price_question' and stage in ('negotiation', 'proposal'):
        return 'present_scoped_pricing_range_do_not_commit_final'
    if objection == 'trust':
        return 'prepare_proof_pack_and_pilot_proposal'
    if objection == 'price':
        return 'review_scope_then_confirm_value_anchor'
    if stage == 'discovery':
        return 'run_discovery_questions_and_map_owner'
    return 'ask_one_discovery_question_and_listen'


def _approval_required(intent: str, stage: str) -> bool:
    sensitive = {'proposal_request', 'procurement_request', 'legal_terms', 'discount_request', 'price_question'}
    sensitive_stages = {'proposal', 'negotiation', 'procurement'}
    return intent in sensitive or stage in sensitive_stages


def _risk_flags(intent: str, objection: str, missing: list[str]) -> list[str]:
    flags = []
    if intent == 'price_question' and 'scope_not_defined' in missing:
        flags.append('no_final_price_without_scope')
    if intent in ('legal_terms',):
        flags.append('no_legal_commitment_without_review')
    if intent == 'discount_request':
        flags.append('no_discount_without_founder_approval')
    if objection == 'legal':
        flags.append('legal_risk_review_required')
    if 'budget_unknown' in missing:
        flags.append('budget_not_qualified')
    return flags


def _suggested_offer(intent: str, stage: str, urgency: str) -> str:
    if stage in ('cold', 'aware'):
        return 'free_diagnostic'
    if stage == 'interested' and urgency == 'low':
        return 'micro_sprint_499_sar'
    if stage in ('discovery', 'interested') and urgency == 'medium':
        return 'data_pack_1500_sar'
    if stage in ('proposal', 'negotiation'):
        return 'transformation_diagnostic_sprint_7500_25000_sar'
    if stage in ('renewal', 'expansion'):
        return 'managed_ops_2999_4999_sar_monthly'
    return 'free_diagnostic'


def classify(message: str) -> dict[str, Any]:
    intent = _detect_intent(message)
    stage = _detect_stage(message, intent)
    objection = _detect_objection(message, intent)
    sentiment = _detect_sentiment(message, intent)
    urgency = _detect_urgency(message, intent)
    missing = _missing_info(intent, message)
    angle = _response_angle(intent, stage, objection)
    action = _next_best_action(intent, stage, objection, urgency)
    approval = _approval_required(intent, stage)
    flags = _risk_flags(intent, objection, missing)
    offer = _suggested_offer(intent, stage, urgency)
    discovery_qs = DISCOVERY_QUESTIONS.get(intent, DISCOVERY_QUESTIONS['default'])

    return {
        'message': message,
        'intent': intent,
        'deal_stage': stage,
        'sentiment': sentiment,
        'urgency': urgency,
        'objection_type': objection,
        'missing_info': missing,
        'recommended_response_angle': angle,
        'next_best_action': action,
        'approval_required': approval,
        'risk_flags': flags,
        'suggested_offer': offer,
        'suggested_discovery_questions': discovery_qs,
        'live_send': False,
        'final_commitment': False,
    }


def build_payload() -> dict[str, Any]:
    demo_messages = [
        'كم السعر؟',
        'ارسل العرض',
        'ما نحتاج',
        'وقف التواصل',
        'what does it include?',
        'we need more proof before deciding',
        'not now, maybe next quarter',
        'send us the contract terms',
        'can you give us a discount?',
        'we are interested, tell me more',
    ]
    results = [classify(m) for m in demo_messages]
    summary = {
        'messages_classified': len(results),
        'intents_detected': list({r['intent'] for r in results}),
        'live_sends': 0,
        'final_commitments': 0,
        'approval_gates_triggered': sum(1 for r in results if r['approval_required']),
    }
    return {
        'summary': summary,
        'classifications': results,
    }


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
    lines = ['# Deal Conversation Intelligence', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Classifications')
    for r in payload['classifications']:
        lines.append(f"- [{r['intent']}] {r['message'][:50]} → {r['next_best_action']}")
    (REPORT_DIR / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload['summary']['live_sends'] != 0:
        errors.append('live_sends must be zero')
    if payload['summary']['final_commitments'] != 0:
        errors.append('final_commitments must be zero')
    for r in payload['classifications']:
        if r['live_send'] is not False:
            errors.append(f"live_send must be False for: {r['message']}")
        if r['final_commitment'] is not False:
            errors.append(f"final_commitment must be False for: {r['message']}")
    return errors


def main() -> int:
    payload = build_payload()
    write_reports(payload)
    errors = verify(payload)
    print('CONVERSATION_INTELLIGENCE_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
