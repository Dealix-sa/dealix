"""
Saudi B2B meeting agenda builder for Dealix sales engagements.

Structures discovery calls, proposal presentations, and QBRs
for Saudi cultural context. All data is static. No LLM calls.

Prefix: /api/v1/meeting-agenda
Tags: Sales
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/meeting-agenda", tags=["Sales"])

# ---------------------------------------------------------------------------
# Meeting type data
# ---------------------------------------------------------------------------

_MEETING_TYPES: dict[str, dict[str, Any]] = {
    "discovery_call": {
        "meeting_type": "discovery_call",
        "name_en": "Discovery Call",
        "name_ar": "مكالمة الاستكشاف",
        "duration_minutes": 45,
        "arabic_protocol_en": (
            "Begin with personal greetings and accept any offer of coffee or dates — "
            "declining is considered impolite. Allow 5–10 minutes of relationship building "
            "before moving to business topics. Do not rush. "
            "The quality of the relationship determines whether they listen to your solution."
        ),
        "agenda_template_en": [
            {"order": 1, "duration_minutes": 10, "item_en": "Greetings and relationship building", "item_ar": "التحيات وبناء العلاقة"},
            {"order": 2, "duration_minutes": 10, "item_en": "Context sharing — their current operations and priorities", "item_ar": "تبادل السياق — عملياتهم الحالية وأولوياتهم"},
            {"order": 3, "duration_minutes": 15, "item_en": "Pain discovery — open-ended questions about bottlenecks and costs", "item_ar": "اكتشاف الألم — أسئلة مفتوحة حول العوائق والتكاليف"},
            {"order": 4, "duration_minutes": 10, "item_en": "Next steps — agree on a specific time-bound follow-up action", "item_ar": "الخطوات التالية — الاتفاق على إجراء متابعة محدد ومقيّد بوقت"},
        ],
        "agenda_template_ar": [
            {"order": 1, "duration_minutes": 10, "item_ar": "التحيات وبناء العلاقة", "item_en": "Greetings and relationship building"},
            {"order": 2, "duration_minutes": 10, "item_ar": "تبادل السياق — العمليات الحالية والأولويات", "item_en": "Context sharing — current operations and priorities"},
            {"order": 3, "duration_minutes": 15, "item_ar": "اكتشاف الألم — أسئلة مفتوحة حول العوائق والتكاليف", "item_en": "Pain discovery — open-ended questions about bottlenecks and costs"},
            {"order": 4, "duration_minutes": 10, "item_ar": "الخطوات التالية — الاتفاق على إجراء متابعة محدد", "item_en": "Next steps — agree on a specific follow-up action"},
        ],
        "avoid_en": [
            "Do not pitch the product in a discovery call — listen first.",
            "Do not skip the rapport phase even under time pressure.",
        ],
        "success_criteria_en": (
            "At the end of the call: you have identified at least one concrete pain point, "
            "confirmed a named decision-maker, and agreed on a specific next step with a date."
        ),
    },
    "proposal_presentation": {
        "meeting_type": "proposal_presentation",
        "name_en": "Proposal Presentation",
        "name_ar": "تقديم العرض التجاري",
        "duration_minutes": 60,
        "arabic_protocol_en": (
            "Send the proposal document 24 hours in advance — do not present it cold. "
            "Open with a recap of the pain they described in their own words. "
            "Use a printed Arabic summary for senior stakeholders who prefer not to read on screen. "
            "Never read slides verbatim."
        ),
        "agenda_template_en": [
            {"order": 1, "duration_minutes": 10, "item_en": "Recap — restate the pain and context from discovery, in their words", "item_ar": "إعادة الصياغة — تكرار الألم والسياق من الاستكشاف بكلماتهم"},
            {"order": 2, "duration_minutes": 20, "item_en": "Present solution — scope, deliverables, and implementation timeline", "item_ar": "تقديم الحل — النطاق، التسليمات، والجدول الزمني للتنفيذ"},
            {"order": 3, "duration_minutes": 15, "item_en": "ROI walk — investment, expected outcomes, and ZATCA/PDPL coverage", "item_ar": "استعراض العائد على الاستثمار — الاستثمار، النتائج المتوقعة، وتغطية زاتكا/PDPL"},
            {"order": 4, "duration_minutes": 10, "item_en": "Q&A — address objections without pressure", "item_ar": "أسئلة وأجوبة — معالجة الاعتراضات بدون ضغط"},
            {"order": 5, "duration_minutes": 5, "item_en": "Close — agree on a decision timeline and next step", "item_ar": "الإغلاق — الاتفاق على جدول زمني للقرار والخطوة التالية"},
        ],
        "agenda_template_ar": [
            {"order": 1, "duration_minutes": 10, "item_ar": "إعادة الصياغة — تكرار الألم والسياق بكلماتهم", "item_en": "Recap — restate pain and context in their words"},
            {"order": 2, "duration_minutes": 20, "item_ar": "تقديم الحل — النطاق، التسليمات، الجدول الزمني", "item_en": "Present solution — scope, deliverables, timeline"},
            {"order": 3, "duration_minutes": 15, "item_ar": "استعراض العائد على الاستثمار والتغطية التنظيمية", "item_en": "ROI walk and regulatory coverage"},
            {"order": 4, "duration_minutes": 10, "item_ar": "أسئلة وأجوبة — معالجة الاعتراضات", "item_en": "Q&A — address objections"},
            {"order": 5, "duration_minutes": 5, "item_ar": "الإغلاق — الاتفاق على الخطوات التالية", "item_en": "Close — agree on next steps"},
        ],
        "avoid_en": [
            "Never present guaranteed ROI percentages — show verified ranges from Proof Pack only.",
            "Do not let the meeting run long — Saudi executives respect punctuality.",
        ],
        "success_criteria_en": (
            "At the end of the meeting: the prospect has acknowledged the scope and investment, "
            "named any remaining concerns, and committed to a decision date."
        ),
    },
    "executive_sponsor_brief": {
        "meeting_type": "executive_sponsor_brief",
        "name_en": "Executive Sponsor Brief",
        "name_ar": "إحاطة الراعي التنفيذي",
        "duration_minutes": 30,
        "arabic_protocol_en": (
            "C-suite executives in Saudi Arabia have extremely limited time. "
            "Prepare a single-page Arabic brief — no more than one page. "
            "Lead with the Vision 2030 angle relevant to their sector. "
            "State the ask in the first 3 minutes. "
            "Do not use jargon. Treat this as a decision meeting, not a discovery meeting."
        ),
        "agenda_template_en": [
            {"order": 1, "duration_minutes": 5, "item_en": "Greetings and brief context on why this meeting matters to their Vision 2030 goals", "item_ar": "تحيات وسياق موجز حول أهمية هذا الاجتماع لأهداف رؤية 2030"},
            {"order": 2, "duration_minutes": 10, "item_en": "Problem statement — the specific gap affecting their organisation, in one-page brief format", "item_ar": "بيان المشكلة — الثغرة المحددة المؤثرة على مؤسستهم، بتنسيق ورقة واحدة"},
            {"order": 3, "duration_minutes": 10, "item_en": "Proposed solution and business case — investment, expected impact, risk mitigation", "item_ar": "الحل المقترح وحالة الأعمال — الاستثمار، الأثر المتوقع، تخفيف المخاطر"},
            {"order": 4, "duration_minutes": 5, "item_en": "Decision ask — clear, specific, time-bound request", "item_ar": "طلب القرار — طلب واضح محدد ومقيّد بوقت"},
        ],
        "agenda_template_ar": [
            {"order": 1, "duration_minutes": 5, "item_ar": "تحيات وسياق موجز حول رؤية 2030", "item_en": "Greetings and Vision 2030 context"},
            {"order": 2, "duration_minutes": 10, "item_ar": "بيان المشكلة — ورقة واحدة", "item_en": "Problem statement — one-page brief"},
            {"order": 3, "duration_minutes": 10, "item_ar": "الحل المقترح وحالة الأعمال", "item_en": "Proposed solution and business case"},
            {"order": 4, "duration_minutes": 5, "item_ar": "طلب القرار — واضح ومحدد", "item_en": "Decision ask — clear and specific"},
        ],
        "avoid_en": [
            "Do not use more than one page of supporting material — executives will not read more.",
            "Do not arrive without a named decision ask — vague requests are not actioned.",
        ],
        "success_criteria_en": (
            "At the end of the brief: the executive has either approved the next step, "
            "delegated to a named owner, or given a clear reason for deferral."
        ),
    },
    "qbr_quarterly_review": {
        "meeting_type": "qbr_quarterly_review",
        "name_en": "Quarterly Business Review (QBR)",
        "name_ar": "مراجعة الأعمال الربع سنوية",
        "duration_minutes": 90,
        "arabic_protocol_en": (
            "QBRs carry significant weight in Saudi business culture — they signal "
            "long-term partnership intent. Always hold the QBR in person if possible. "
            "Bring printed bilingual reports. Allow time for unstructured conversation after the formal agenda. "
            "Senior leadership attendance from Dealix is expected."
        ),
        "agenda_template_en": [
            {"order": 1, "duration_minutes": 30, "item_en": "Results review — documented outcomes from the past quarter with verified data", "item_ar": "مراجعة النتائج — المخرجات الموثقة للربع الماضي مع بيانات موثقة"},
            {"order": 2, "duration_minutes": 20, "item_en": "ROI proof — Proof Pack walkthrough, evidence of measurable change", "item_ar": "إثبات العائد على الاستثمار — استعراض حزمة الإثبات، أدلة التغيير القابل للقياس"},
            {"order": 3, "duration_minutes": 20, "item_en": "Roadmap — next quarter priorities, scope adjustments, and new use cases", "item_ar": "خارطة الطريق — أولويات الربع القادم، تعديلات النطاق، وحالات الاستخدام الجديدة"},
            {"order": 4, "duration_minutes": 20, "item_en": "Upsell and expansion — present new opportunities grounded in observed data", "item_ar": "الترقية والتوسع — تقديم فرص جديدة مبنية على بيانات ملاحظة"},
        ],
        "agenda_template_ar": [
            {"order": 1, "duration_minutes": 30, "item_ar": "مراجعة النتائج — مخرجات موثقة للربع الماضي", "item_en": "Results review — documented outcomes for the past quarter"},
            {"order": 2, "duration_minutes": 20, "item_ar": "إثبات العائد على الاستثمار — حزمة الإثبات", "item_en": "ROI proof — Proof Pack walkthrough"},
            {"order": 3, "duration_minutes": 20, "item_ar": "خارطة الطريق — أولويات الربع القادم", "item_en": "Roadmap — next quarter priorities"},
            {"order": 4, "duration_minutes": 20, "item_ar": "الترقية والتوسع — فرص جديدة بالبيانات", "item_en": "Upsell and expansion — data-grounded opportunities"},
        ],
        "avoid_en": [
            "Do not present projections in a QBR — only verified outcomes from the Proof Pack.",
            "Do not hold a QBR remotely if an in-person option is available.",
        ],
        "success_criteria_en": (
            "At the end of the QBR: the client has acknowledged the documented value, "
            "agreed on the next quarter roadmap, and either renewed, expanded, "
            "or stated a clear reason for not doing so."
        ),
    },
    "renewal_close": {
        "meeting_type": "renewal_close",
        "name_en": "Renewal Close Meeting",
        "name_ar": "اجتماع إغلاق التجديد",
        "duration_minutes": 45,
        "arabic_protocol_en": (
            "Renewal conversations in Saudi B2B require relationship reinforcement, "
            "not hard sell. Lead with gratitude for the partnership. "
            "Reference specific verified outcomes from the engagement before discussing contract terms. "
            "Never pressure on price — frame renewal as continuity of a working relationship."
        ),
        "agenda_template_en": [
            {"order": 1, "duration_minutes": 15, "item_en": "Health review — client satisfaction check, any unresolved concerns", "item_ar": "مراجعة الصحة — فحص رضا العميل، أي مخاوف لم تُحل"},
            {"order": 2, "duration_minutes": 15, "item_en": "Value recap — summarise the top 3 verified outcomes from the engagement", "item_ar": "ملخص القيمة — تلخيص أفضل 3 مخرجات موثقة من المشاركة"},
            {"order": 3, "duration_minutes": 15, "item_en": "Renewal proposal — present terms, any scope adjustments, and pricing in SAR", "item_ar": "مقترح التجديد — تقديم الشروط، أي تعديلات على النطاق، والتسعير بالريال"},
        ],
        "agenda_template_ar": [
            {"order": 1, "duration_minutes": 15, "item_ar": "مراجعة الصحة — رضا العميل والمخاوف القائمة", "item_en": "Health review — satisfaction and outstanding concerns"},
            {"order": 2, "duration_minutes": 15, "item_ar": "ملخص القيمة — أفضل 3 مخرجات موثقة", "item_en": "Value recap — top 3 verified outcomes"},
            {"order": 3, "duration_minutes": 15, "item_ar": "مقترح التجديد — الشروط والتسعير بالريال", "item_en": "Renewal proposal — terms and SAR pricing"},
        ],
        "avoid_en": [
            "Do not use urgency or pressure language around renewal deadlines.",
            "Do not present renewal terms before completing the value recap.",
        ],
        "success_criteria_en": (
            "At the end of the meeting: the client has either signed the renewal, "
            "committed to a review date within 7 days, or stated a specific blocker "
            "that can be addressed."
        ),
    },
}

# ---------------------------------------------------------------------------
# Saudi meeting protocol
# ---------------------------------------------------------------------------

_SAUDI_MEETING_PROTOCOL: dict[str, Any] = {
    "pre_meeting_en": (
        "Send the meeting agenda at least 24 hours in advance in both English and Arabic. "
        "Confirm attendance the day before — no-shows are common without confirmation. "
        "Have all materials prepared in Arabic. "
        "Check the Islamic calendar for any overlapping observances."
    ),
    "pre_meeting_ar": (
        "أرسل جدول الاجتماع قبل 24 ساعة على الأقل باللغتين الإنجليزية والعربية. "
        "أكّد الحضور في اليوم السابق — الغياب بدون تأكيد أمر شائع. "
        "أعدّ جميع المواد باللغة العربية. "
        "تحقق من التقويم الهجري لأي ممارسات دينية متداخلة."
    ),
    "greeting_en": (
        "Wait for the host to initiate the handshake — do not extend your hand first. "
        "Accept any offer of Arabic coffee (qahwa) or dates — declining is impolite. "
        "Allow 5–10 minutes of genuine smalltalk before business; do not rush this phase. "
        "Address attendees by their title (Sheikh, Dr., Eng.) unless invited to use first names."
    ),
    "greeting_ar": (
        "انتظر حتى يبادر المضيف بالمصافحة — لا تمدّ يدك أولاً. "
        "اقبل أي عرض للقهوة العربية (القهوة) أو التمر — الرفض يُعدّ قلة أدب. "
        "اسمح بـ 5–10 دقائق من الحديث العفوي الحقيقي قبل الأعمال؛ لا تتسرع في هذه المرحلة. "
        "خاطب الحاضرين بلقبهم (الشيخ، الدكتور، المهندس) ما لم يُدعوك لاستخدام الأسماء الأولى."
    ),
    "during_en": (
        "Never interrupt while someone is speaking — it is considered disrespectful. "
        "Use honorifics consistently throughout the meeting. "
        "If prayer time falls during the meeting, pause immediately and accommodate it. "
        "Acknowledge Islamic calendar constraints when discussing timelines — "
        "Ramadan and Eid periods require adjusted planning. "
        "Do not make final decisions in the meeting — it is normal for decisions to require "
        "consultation (shura) after the meeting."
    ),
    "during_ar": (
        "لا تقاطع أبداً أثناء حديث شخص ما — يُعدّ ذلك قلة احترام. "
        "استخدم الألقاب الرسمية باستمرار طوال الاجتماع. "
        "إذا حلّ وقت الصلاة خلال الاجتماع، أوقف الاجتماع فوراً ووفّر الوقت اللازم. "
        "اعترف بقيود التقويم الهجري عند مناقشة الجداول الزمنية — "
        "تتطلب فترات رمضان والعيد تخطيطاً معدّلاً. "
        "لا تتوقع قرارات نهائية في الاجتماع — من الطبيعي أن تتطلب القرارات "
        "مشاورة (شورى) بعد الاجتماع."
    ),
    "post_meeting_en": (
        "Send a meeting recap by email within 4 hours of the meeting ending. "
        "A WhatsApp thank-you message is culturally appropriate and appreciated — "
        "but only if the client has already engaged via WhatsApp. "
        "Document all agreed next steps with owners and dates. "
        "Share a bilingual summary if Arabic was the primary meeting language."
    ),
    "post_meeting_ar": (
        "أرسل ملخص الاجتماع بالبريد الإلكتروني في غضون 4 ساعات من انتهاء الاجتماع. "
        "رسالة شكر عبر واتساب مقبولة ثقافياً ومُقدَّرة — "
        "لكن فقط إذا كان العميل قد تفاعل بالفعل عبر واتساب. "
        "وثّق جميع الخطوات التالية المتفق عليها مع أصحابها والتواريخ. "
        "شارك ملخصاً ثنائي اللغة إذا كانت العربية هي اللغة الأساسية في الاجتماع."
    ),
}

# ---------------------------------------------------------------------------
# Pydantic model
# ---------------------------------------------------------------------------


class MeetingAgendaRequest(BaseModel):
    meeting_type: str = Field(
        ..., description="Meeting type ID from GET /types"
    )
    client_name: str = Field(..., max_length=120)
    client_company: str = Field(..., max_length=120)
    client_title: str = Field(..., max_length=80, description="Client's professional title")
    key_topics: list[str] = Field(
        default_factory=list,
        max_length=5,
        description="Up to 5 specific topics to incorporate into the agenda",
    )
    is_ramadan_period: bool = Field(
        default=False,
        description="Set to true if the meeting falls during Ramadan",
    )
    language_preference: str = Field(
        default="en",
        description="Preferred agenda language: 'en' for English, 'ar' for Arabic",
    )


# ---------------------------------------------------------------------------
# Pure-function core
# ---------------------------------------------------------------------------


def _build_agenda(req: MeetingAgendaRequest) -> dict[str, Any]:
    """
    Build a structured meeting agenda based on the request.
    Injects client details and Ramadan context as appropriate.
    """
    meeting = _MEETING_TYPES.get(req.meeting_type)
    if meeting is None:
        raise KeyError(req.meeting_type)

    salutation = f"{req.client_title} {req.client_name}" if req.client_title else req.client_name
    agenda_key = "agenda_template_ar" if req.language_preference == "ar" else "agenda_template_en"
    agenda_items = list(meeting[agenda_key])

    protocol_notes: list[str] = [
        _SAUDI_MEETING_PROTOCOL["pre_meeting_en"],
        _SAUDI_MEETING_PROTOCOL["greeting_en"],
        _SAUDI_MEETING_PROTOCOL["during_en"],
        _SAUDI_MEETING_PROTOCOL["post_meeting_en"],
    ]

    if req.is_ramadan_period:
        protocol_notes.append(
            "RAMADAN NOTE: Business capacity is reduced during fasting hours. "
            "Schedule the meeting after Iftar if possible (post-sunset). "
            "Shorten the agenda where possible — aim for 75% of the standard duration. "
            "Avoid scheduling during the first two days and the last three days of Ramadan."
        )

    if req.key_topics:
        topics_note = (
            f"Specific topics to address for {req.client_company}: "
            + "; ".join(req.key_topics)
        )
        agenda_items = list(agenda_items) + [
            {
                "order": len(agenda_items) + 1,
                "duration_minutes": 0,
                "item_en": topics_note,
                "item_ar": f"موضوعات محددة لـ {req.client_company}: " + "; ".join(req.key_topics),
                "note_en": "Weave these topics into the relevant agenda items above rather than treating as a separate block.",
            }
        ]

    return {
        "meeting_type": req.meeting_type,
        "name_en": meeting["name_en"],
        "name_ar": meeting["name_ar"],
        "client_name": req.client_name,
        "client_company": req.client_company,
        "client_title": req.client_title,
        "salutation": salutation,
        "duration_minutes": meeting["duration_minutes"],
        "is_ramadan_period": req.is_ramadan_period,
        "language_preference": req.language_preference,
        "agenda_items": agenda_items,
        "arabic_protocol_en": meeting["arabic_protocol_en"],
        "protocol_notes": protocol_notes,
        "avoid": meeting["avoid_en"],
        "success_criteria_en": meeting["success_criteria_en"],
        "governance_decision": "ALLOW_WITH_REVIEW",
        "note_en": (
            "This agenda is a structured guide. Adapt it to the actual conversation — "
            "do not follow it rigidly if the client takes the discussion in a productive direction."
        ),
        "note_ar": (
            "هذا الجدول دليل منظم. كيّفه وفق المحادثة الفعلية — "
            "لا تتبعه بصرامة إذا أخذ العميل النقاش في اتجاه منتج."
        ),
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/types", summary="List all meeting types (summary view)")
async def list_meeting_types() -> dict[str, Any]:
    """Return a summary of all available meeting types."""
    summaries = [
        {
            "meeting_type": k,
            "name_en": v["name_en"],
            "name_ar": v["name_ar"],
            "duration_minutes": v["duration_minutes"],
        }
        for k, v in _MEETING_TYPES.items()
    ]
    return {
        "governance_decision": "ALLOW_WITH_REVIEW",
        "total": len(summaries),
        "types": summaries,
    }


@router.get("/types/{meeting_type}", summary="Full detail for a single meeting type")
async def get_meeting_type(meeting_type: str) -> dict[str, Any]:
    """Return the full meeting type template including agenda, protocol, and success criteria."""
    mt = _MEETING_TYPES.get(meeting_type)
    if mt is None:
        available = sorted(_MEETING_TYPES.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Meeting type '{meeting_type}' not found. Available: {available}",
        )
    return {
        "governance_decision": "ALLOW_WITH_REVIEW",
        "meeting_type": mt,
    }


@router.get("/protocol", summary="Saudi B2B meeting protocol guidelines")
async def get_protocol() -> dict[str, Any]:
    """Return the full set of Saudi B2B meeting protocol guidelines."""
    return {
        "governance_decision": "ALLOW_WITH_REVIEW",
        "protocol": _SAUDI_MEETING_PROTOCOL,
        "note_en": (
            "These guidelines apply to all in-person and video meetings with Saudi B2B prospects. "
            "Protocol adherence is a trust signal, not optional etiquette."
        ),
        "note_ar": (
            "تنطبق هذه الإرشادات على جميع الاجتماعات الحضورية وعبر الفيديو مع عملاء B2B السعوديين. "
            "الالتزام بالبروتوكول هو إشارة ثقة، وليس آداباً اختيارية."
        ),
    }


@router.post("/build-agenda", summary="Build a structured meeting agenda")
async def build_agenda(body: MeetingAgendaRequest) -> dict[str, Any]:
    """
    Generate a structured, culturally contextualised meeting agenda
    for the specified meeting type and client details.
    """
    if body.language_preference not in ("en", "ar"):
        raise HTTPException(
            status_code=422,
            detail="language_preference must be 'en' or 'ar'.",
        )
    try:
        result = _build_agenda(body)
    except KeyError:
        available = sorted(_MEETING_TYPES.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Meeting type '{body.meeting_type}' not found. Available: {available}",
        )
    return result
