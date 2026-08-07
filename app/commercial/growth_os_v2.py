from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

REPORT_DIR = Path('reports/commercial/growth_os')

SAFE_DEFAULTS = {
    'EXTERNAL_SEND_ENABLED': False,
    'EMAIL_SEND_ENABLED': False,
    'WHATSAPP_SEND_ENABLED': False,
    'WHATSAPP_ALLOW_LIVE_SEND': False,
    'SMS_SEND_ENABLED': False,
    'CALENDAR_WRITE_ENABLED': False,
    'PROPOSAL_FINALIZATION_ENABLED': False,
    'OUTBOUND_MODE': 'draft_only',
}
FIT_SECTORS = {'clinics', 'logistics', 'training', 'real_estate', 'b2b_services', 'agencies', 'saas', 'industrial'}
SAUDI_CITIES = {'riyadh', 'jeddah', 'dammam', 'khobar', 'makkah', 'madinah'}
OPT_OUT_TERMS = ('unsubscribe', 'stop', 'إيقاف', 'لا ترسل', 'إلغاء')

@dataclass
class SafetyDecision:
    allowed: bool
    reason: str
    required_approvals: list[str]
    blocked_by: list[str]
    audit_level: str = 'L2'

@dataclass
class CommercialAccount:
    account_id: str
    company_name: str
    sector: str
    city: str
    website: str = ''
    source_url: str = ''
    source_type: str = 'client_provided'
    verification_status: str = 'unverified'
    contactability_status: str = 'unknown'
    public_email: str = ''
    whatsapp: str = ''
    whatsapp_opt_in: bool = False
    phone: str = ''
    linkedin_url: str = ''
    pain_hypothesis: str = ''
    icp_score: int = 0
    recommended_motion: str = 'sales'
    recommended_product: str = 'Commercial Growth OS'
    owner: str = 'founder_or_sales_owner'
    risk_level: str = 'medium'
    opt_out: bool = False

@dataclass
class GrowthCard:
    card_id: str
    account_id: str
    company_name: str
    motion: str
    recommended_channel: str
    draft_message_ar: str
    draft_message_en: str
    buttons: list[dict[str, str]]
    owner_decision: str
    approval_required: bool
    send_status: str
    next_action: str
    risk_level: str
    source_url: str

@dataclass
class ReplyClassification:
    reply_id: str
    card_id: str
    reply_type: str
    sentiment: str
    intent: str
    recommended_action: str
    risk_level: str

@dataclass
class NegotiationDraft:
    negotiation_id: str
    card_id: str
    objection_type: str
    allowed_response: str
    forbidden_commitments: list[str]
    scope_adjustment_options: list[str]
    approval_required: bool

@dataclass
class BookingOption:
    booking_id: str
    card_id: str
    duration_minutes: int
    timezone: str
    suggested_slots: list[str]
    agenda: list[str]
    attendees: list[str]
    preparation_notes: list[str]
    calendar_write_enabled: bool
    booking_status: str

@dataclass
class ProposalBrief:
    proposal_id: str
    card_id: str
    package_name: str
    scope: list[str]
    deliverables: list[str]
    timeline: str
    pricing_range_sar: str
    out_of_scope: list[str]
    acceptance_criteria: list[str]
    final_price_allowed: bool
    approval_required: bool
    status: str

@dataclass
class FollowUpTask:
    task_id: str
    card_id: str
    due_in_days: int
    channel: str
    owner: str
    draft_note: str
    status: str

def _flag(name: str) -> bool:
    return os.getenv(name, 'false').lower() in {'1', 'true', 'yes', 'on'}

def default_accounts() -> list[dict[str, Any]]:
    return [
        {'account_id':'acct-clinic-001','company_name':'عيادة تجريبية متعددة الفروع','sector':'clinics','city':'Riyadh','website':'https://example-clinic.com','source_url':'https://example-clinic.com/contact','public_email':'ops@example-clinic.com','whatsapp':'+966500000001','whatsapp_opt_in':True,'pain_hypothesis':'استفسارات واتساب تحتاج متابعة منظمة.','recommended_motion':'sales','recommended_product':'WhatsApp / Inbox Follow-up OS'},
        {'account_id':'acct-logistics-001','company_name':'شركة لوجستية تجريبية','sector':'logistics','city':'Jeddah','website':'https://example-logistics.com','source_url':'https://example-logistics.com/partners','public_email':'partnerships@example-logistics.com','linkedin_url':'https://linkedin.com/company/example-logistics','pain_hypothesis':'فرص شراكات وتوزيع تحتاج متابعة.','recommended_motion':'partnership','recommended_product':'Partnership Growth Sprint'},
        {'account_id':'acct-training-001','company_name':'مركز تدريب تجريبي','sector':'training','city':'Dammam','website':'https://example-training.com','source_url':'https://example-training.com/programs','public_email':'sales@example-training.com','pain_hypothesis':'عروض التدريب تحتاج متابعة قبل الإغلاق.','recommended_motion':'proposal_push','recommended_product':'Growth Card Sprint'},
    ]

def load_accounts(path: str = 'data/commercial/accounts.sample.json') -> list[CommercialAccount]:
    p = Path(path)
    raw = json.loads(p.read_text(encoding='utf-8')) if p.exists() else default_accounts()
    return [CommercialAccount(**x) for x in raw]

def validate_sources(accounts: list[CommercialAccount]) -> list[dict[str, str]]:
    risks = []
    for a in accounts:
        if a.opt_out:
            a.contactability_status = 'blocked_opt_out'; a.risk_level = 'high'; risks.append({'account_id': a.account_id, 'risk': 'opt_out'})
        if not a.source_url:
            a.verification_status = 'unverified'; a.contactability_status = 'blocked_missing_source'; a.risk_level = 'high'; risks.append({'account_id': a.account_id, 'risk': 'missing_source_url'})
        else:
            a.verification_status = 'source_recorded'
    return risks

def score_account(a: CommercialAccount) -> CommercialAccount:
    s = 20
    if a.sector.lower() in FIT_SECTORS: s += 25
    if a.city.lower() in SAUDI_CITIES: s += 15
    if a.source_url: s += 15
    if a.public_email or a.whatsapp or a.linkedin_url or a.phone: s += 10
    if a.pain_hypothesis: s += 15
    if a.opt_out: s -= 60
    a.icp_score = max(0, min(100, s))
    a.risk_level = 'low' if a.icp_score >= 70 and a.source_url and not a.opt_out else 'high' if a.icp_score < 50 or not a.source_url or a.opt_out else 'medium'
    return a

def select_channel(a: CommercialAccount) -> str:
    if a.opt_out: return 'website_form'
    if a.recommended_motion == 'partnership': return 'partner_referral' if a.public_email else 'linkedin_manual'
    if a.whatsapp and a.whatsapp_opt_in: return 'whatsapp'
    if a.public_email: return 'email'
    if a.linkedin_url: return 'linkedin_manual'
    if a.phone: return 'phone'
    return 'website_form'

def _message(a: CommercialAccount, lang: str) -> str:
    if lang == 'en':
        return f"Hello {a.company_name},\n\nDealix turns sales, partnerships, replies, meetings, proposals, and follow-ups into a daily command room. Suggested start: {a.recommended_product}. Reply STOP to opt out."
    return f"مرحبًا فريق {a.company_name}،\n\nDealix يرتب المبيعات والشراكات والمتابعات في غرفة قيادة يومية: من نكلم، ماذا نرسل، متى نحجز، وماذا نعرض. المدخل المقترح: {a.recommended_product}. للوقف ردوا إيقاف."

def build_cards(accounts: list[CommercialAccount]) -> list[GrowthCard]:
    cards = []
    for i, a in enumerate(accounts, 1):
        cid = f'cg-{i:04d}'
        status = 'blocked_opt_out' if a.opt_out else 'blocked_missing_source' if not a.source_url else 'draft_only'
        cards.append(GrowthCard(cid, a.account_id, a.company_name, a.recommended_motion, select_channel(a), _message(a,'ar'), _message(a,'en'), [{'id':f'card:{cid}:approve','title':'اعتماد'},{'id':f'card:{cid}:edit','title':'تعديل'},{'id':f'card:{cid}:skip','title':'تخطي'}], 'review', True, status, 'review_approve_edit_skip_or_book_call', a.risk_level, a.source_url))
    return cards

def load_replies(path: str = 'data/commercial/replies.sample.json') -> list[dict[str, str]]:
    p = Path(path)
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else [{'reply_id':'r1','card_id':'cg-0001','text':'مهتم أرسل التفاصيل'},{'reply_id':'r2','card_id':'cg-0002','text':'السعر عالي ونحتاج شراكة'},{'reply_id':'r3','card_id':'cg-0003','text':'خلها بعدين'}]

def classify_reply(r: dict[str, str]) -> ReplyClassification:
    t = r.get('text','').lower(); rid = r.get('reply_id','r'); cid = r.get('card_id','c')
    if any(x in t for x in OPT_OUT_TERMS): return ReplyClassification(rid,cid,'unsubscribe','negative','opt_out','block_and_mark_opt_out','high')
    if 'سعر' in t or 'غالي' in t or 'price' in t: return ReplyClassification(rid,cid,'price_objection','neutral','price_objection','prepare_scope_adjustment','medium')
    if 'شراكة' in t or 'partner' in t: return ReplyClassification(rid,cid,'partnership_interest','positive','partner','prepare_partnership_brief','low')
    if 'موعد' in t or 'meeting' in t or 'call' in t or 'مهتم' in t: return ReplyClassification(rid,cid,'meeting_request','positive','book_meeting','offer_booking_slots','low')
    if 'تفاصيل' in t or 'details' in t: return ReplyClassification(rid,cid,'send_details','positive','proposal','prepare_proposal_brief','low')
    if 'بعدين' in t or 'later' in t: return ReplyClassification(rid,cid,'not_now','neutral','nurture','schedule_follow_up','low')
    return ReplyClassification(rid,cid,'unknown','neutral','unknown','manual_review','medium')

def build_negotiation_draft(r: ReplyClassification) -> NegotiationDraft:
    return NegotiationDraft(f'neg-{r.reply_id}', r.card_id, r.reply_type, 'اقترح نطاق أصغر أو pilot مرحلي بدون خصم أو التزام نهائي.', ['final price','discount approval','legal terms','payment commitment','guaranteed revenue','contract acceptance'], ['smaller pilot','phased scope','diagnostic first','lower retainer tier','proof-first sprint','partner model'], True)

def _slots() -> list[str]:
    d = datetime.now(UTC).replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return [(d + timedelta(days=i)).isoformat() for i in range(3)]

def build_booking_option(c: GrowthCard) -> BookingOption:
    return BookingOption(f'book-{c.card_id}', c.card_id, 25, 'Asia/Riyadh', _slots(), ['فهم الهدف','اختيار workflow','تأكيد البيانات','تحديد next action'], ['client_owner','dealix_operator'], ['راجع المصدر','لا تعد بنتائج مضمونة','جهز مثال'], False, 'draft_slot_options')

def build_proposal_brief(c: GrowthCard) -> ProposalBrief:
    pkg = '14-Day Commercial OS Sprint' if c.motion in {'partnership','proposal_push','renewal'} else '7-Day Growth Card Sprint'
    return ProposalBrief(f'prop-{c.card_id}', c.card_id, pkg, ['account review','ICP scoring','growth cards','reply desk','booking options','proposal briefs','follow-up tasks','command snapshot'], ['latest.json','latest.md','cards','reply plans','proposal brief','proof pack'], '7-14 business days', '5,000-12,000 SAR' if pkg.startswith('7') else '15,000-35,000 SAR', ['live outbound without approval','calendar writes by default','final legal terms','guaranteed revenue'], ['source_url recorded','approval_required true','next_action present','risk_level present','proof report generated'], False, True, 'draft_requires_approval')

def build_followups(c: GrowthCard) -> list[FollowUpTask]:
    return [FollowUpTask(f'fu-{c.card_id}-d{d}', c.card_id, d, c.recommended_channel, 'founder_or_sales_owner', n, 'draft') for d,n in [(1,'تأكيد وصول الرسالة.'),(3,'إرسال قيمة عملية.'),(7,'قرار واضح أو nurture.')]]

def can_send_email(action: dict[str, Any], a: CommercialAccount, rules: dict[str, Any]) -> SafetyDecision:
    if not (_flag('EXTERNAL_SEND_ENABLED') and _flag('EMAIL_SEND_ENABLED') and os.getenv('OUTBOUND_MODE','draft_only') == 'controlled_live'):
        return SafetyDecision(False, 'email live disabled by default', ['owner_approval'], ['safe_default'])
    if a.opt_out: return SafetyDecision(False, 'opt out', [], ['opt_out'], 'L4')
    if action.get('status') != 'approved' or action.get('owner_decision') != 'send': return SafetyDecision(False, 'not approved', ['owner_approval'], ['approval_gate'])
    return SafetyDecision(True, 'approved controlled email', [], [], 'L3')

def can_send_whatsapp(action: dict[str, Any], a: CommercialAccount, rules: dict[str, Any]) -> SafetyDecision:
    if not (_flag('EXTERNAL_SEND_ENABLED') and _flag('WHATSAPP_SEND_ENABLED') and _flag('WHATSAPP_ALLOW_LIVE_SEND') and os.getenv('OUTBOUND_MODE','draft_only') == 'controlled_live'):
        return SafetyDecision(False, 'whatsapp live disabled by default', ['owner_approval','whatsapp_opt_in'], ['safe_default'], 'L4')
    if not a.whatsapp_opt_in: return SafetyDecision(False, 'missing opt-in', ['opt_in'], ['no_opt_in'], 'L4')
    if action.get('status') != 'approved' or action.get('owner_decision') != 'send': return SafetyDecision(False, 'not approved', ['owner_approval'], ['approval_gate'], 'L4')
    return SafetyDecision(True, 'approved controlled whatsapp', [], [], 'L4')

def can_write_calendar(action: dict[str, Any], a: CommercialAccount, rules: dict[str, Any]) -> SafetyDecision:
    if not _flag('CALENDAR_WRITE_ENABLED'): return SafetyDecision(False, 'calendar disabled by default', ['booking_approval'], ['safe_default'])
    return SafetyDecision(action.get('owner_decision') == 'book', 'booking approval required', ['booking_approval'], [] if action.get('owner_decision') == 'book' else ['approval_gate'])

def can_finalize_proposal(action: dict[str, Any], a: CommercialAccount, rules: dict[str, Any]) -> SafetyDecision:
    if not _flag('PROPOSAL_FINALIZATION_ENABLED'): return SafetyDecision(False, 'proposal finalization disabled by default', ['founder_approval'], ['safe_default'], 'L4')
    return SafetyDecision(action.get('final_price_allowed') is True, 'founder approval required', ['founder_approval'], [] if action.get('final_price_allowed') else ['pricing_guard'], 'L4')

def run_growth_os(accounts_path: str = 'data/commercial/accounts.sample.json', replies_path: str = 'data/commercial/replies.sample.json') -> dict[str, Any]:
    accounts = load_accounts(accounts_path); risks = validate_sources(accounts); accounts = [score_account(a) for a in accounts]
    cards = build_cards(accounts); replies = [classify_reply(r) for r in load_replies(replies_path)]
    negotiations = [build_negotiation_draft(r) for r in replies if r.reply_type != 'unsubscribe']
    bookings = [build_booking_option(c) for c in cards if c.send_status == 'draft_only']; proposals = [build_proposal_brief(c) for c in cards]
    followups = [t for c in cards if c.send_status == 'draft_only' for t in build_followups(c)]
    summary = {'accounts':len(accounts),'cards':len(cards),'replies':len(replies),'negotiation_drafts':len(negotiations),'booking_options':len(bookings),'proposal_briefs':len(proposals),'followup_tasks':len(followups),'risks':len(risks),'live_send':False,'calendar_write':False,'proposal_finalization':False}
    snapshot = {'generated_at':datetime.now(UTC).isoformat(),'safe_defaults':SAFE_DEFAULTS,'summary':summary,'accounts':[asdict(a) for a in accounts],'cards':[asdict(c) for c in cards],'replies':[asdict(r) for r in replies],'negotiation_drafts':[asdict(n) for n in negotiations],'booking_options':[asdict(b) for b in bookings],'proposal_briefs':[asdict(p) for p in proposals],'followup_tasks':[asdict(t) for t in followups],'risks':risks,'decision_queue':[{'card_id':c.card_id,'company_name':c.company_name,'decision':c.owner_decision,'risk_level':c.risk_level,'next_action':c.next_action} for c in cards],'next_10_actions':[f'Review {c.card_id} for {c.company_name}: {c.next_action}' for c in cards][:10],'proof_pack':{'no_fake_claims':True,'no_guaranteed_roi':True,'evidence':summary}}
    REPORT_DIR.mkdir(parents=True, exist_ok=True); (REPORT_DIR/'latest.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding='utf-8')
    (REPORT_DIR/'latest.md').write_text('# Dealix Commercial Growth OS v2 Report\n\n' + '\n'.join([f'- {k}: `{v}`' for k,v in summary.items()]) + '\n', encoding='utf-8')
    return snapshot

def verify_snapshot(snapshot: dict[str, Any]) -> list[str]:
    failures = []
    if snapshot['summary']['live_send'] is not False: failures.append('live_send must remain false')
    if snapshot['summary']['calendar_write'] is not False: failures.append('calendar_write must remain false')
    for c in snapshot['cards']:
        if not c.get('owner_decision') or not c.get('next_action'): failures.append(f"{c.get('card_id')} missing decision/next_action")
        if len(c.get('buttons', [])) > 3: failures.append(f"{c.get('card_id')} has too many buttons")
    for p in snapshot['proposal_briefs']:
        if p.get('approval_required') is not True or p.get('final_price_allowed') is not False: failures.append(f"{p.get('proposal_id')} proposal gate failed")
    return failures
