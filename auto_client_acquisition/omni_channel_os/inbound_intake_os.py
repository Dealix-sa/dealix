"""Inbound Intake OS — processes website form submissions into qualified leads."""
from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.omni_channel_os.schemas import (
    InboundLead,
    Language,
    LeadCapture,
)

log = logging.getLogger(__name__)
_NO_AUTO_SEND = False  # inbound automation is permitted

INTAKE_QUESTIONS_AR = [
    {
        "field": "company_type",
        "q": "ما نوع الشركة؟",
        "options": ["شركة محلية", "شركة دولية", "مكتب مهني", "جهة حكومية", "أخرى"],
    },
    {
        "field": "workflow_interest",
        "q": "أي workflow تريد تحسينه؟",
        "options": [
            "تقارير ومتابعة داخلية",
            "صيانة/بلاغات/SLA",
            "مستندات ومعرفة داخلية",
            "مبيعات ومتابعة عملاء",
            "خدمة عملاء",
            "غير ذلك",
        ],
    },
    {
        "field": "has_data",
        "q": "هل عندكم ملفات أو API نبدأ منها؟",
        "options": ["نعم، عندنا ملفات", "نعم، عندنا API", "لا، بدنا نجهز", "غير متأكد"],
    },
    {
        "field": "primary_goal",
        "q": "ما الهدف الرئيسي؟",
        "options": [
            "تقليل الوقت اليدوي",
            "تحسين الدقة والجودة",
            "تسريع التقارير",
            "خدمة عملاء أسرع",
            "تقليل التكلفة",
        ],
    },
    {
        "field": "preferred_format",
        "q": "هل تفضلون Audit أو Pilot؟",
        "options": ["Audit مجاني (7 أيام)", "Pilot مدفوع (30 يوم)", "استشارة أولاً"],
    },
    {
        "field": "language",
        "q": "اللغة المفضلة؟",
        "options": ["العربية", "English", "كلاهما"],
    },
    {
        "field": "meeting_time",
        "q": "موعد مناسب للتواصل؟",
        "options": [
            "هذا الأسبوع",
            "الأسبوع القادم",
            "خلال شهر",
            "أنتظر للتواصل بنفسي",
        ],
    },
]

INTAKE_QUESTIONS_EN = [
    {
        "field": "company_type",
        "q": "What type of company?",
        "options": [
            "Local company",
            "International company",
            "Professional office",
            "Government-related",
            "Other",
        ],
    },
    {
        "field": "workflow_interest",
        "q": "Which workflow do you want to improve?",
        "options": [
            "Internal reports and tracking",
            "Maintenance/tickets/SLA",
            "Documents and knowledge management",
            "Sales and client follow-up",
            "Customer service",
            "Other",
        ],
    },
    {
        "field": "has_data",
        "q": "Do you have files or an API to start from?",
        "options": [
            "Yes, we have files",
            "Yes, we have an API",
            "No, we need to set that up",
            "Not sure",
        ],
    },
    {
        "field": "primary_goal",
        "q": "What is your primary goal?",
        "options": [
            "Reduce manual time",
            "Improve accuracy and quality",
            "Speed up reporting",
            "Faster customer service",
            "Reduce costs",
        ],
    },
    {
        "field": "preferred_format",
        "q": "Do you prefer an Audit or Pilot?",
        "options": ["Free Audit (7 days)", "Paid Pilot (30 days)", "Consultation first"],
    },
    {
        "field": "language",
        "q": "Preferred language?",
        "options": ["Arabic", "English", "Both"],
    },
    {
        "field": "meeting_time",
        "q": "When is a good time to connect?",
        "options": [
            "This week",
            "Next week",
            "Within a month",
            "I will reach out myself",
        ],
    },
]

# Qualification weights per form field value
_COMPANY_TYPE_SCORES: dict[str, float] = {
    "شركة محلية": 20.0,
    "local company": 20.0,
    "شركة دولية": 25.0,
    "international company": 25.0,
    "مكتب مهني": 20.0,
    "professional office": 20.0,
    "جهة حكومية": 15.0,
    "government-related": 15.0,
}

_HAS_DATA_SCORES: dict[str, float] = {
    "نعم، عندنا ملفات": 20.0,
    "yes, we have files": 20.0,
    "نعم، عندنا api": 25.0,
    "yes, we have an api": 25.0,
    "لا، بدنا نجهز": 10.0,
    "no, we need to set that up": 10.0,
}

_GOAL_SCORES: dict[str, float] = {
    "تقليل الوقت اليدوي": 15.0,
    "reduce manual time": 15.0,
    "تحسين الدقة والجودة": 12.0,
    "improve accuracy and quality": 12.0,
    "تسريع التقارير": 12.0,
    "speed up reporting": 12.0,
    "خدمة عملاء أسرع": 10.0,
    "faster customer service": 10.0,
    "تقليل التكلفة": 10.0,
    "reduce costs": 10.0,
}

_FORMAT_SCORES: dict[str, float] = {
    "audit مجاني (7 أيام)": 15.0,
    "free audit (7 days)": 15.0,
    "pilot مدفوع (30 يوم)": 25.0,
    "paid pilot (30 days)": 25.0,
    "استشارة أولاً": 10.0,
    "consultation first": 10.0,
}

_OFFER_LADDER = [
    ("sales_tracking", ["مبيعات ومتابعة عملاء", "sales and client follow-up"]),
    ("maintenance_sla", ["صيانة/بلاغات/sla", "maintenance/tickets/sla"]),
    ("documents_knowledge", ["مستندات ومعرفة داخلية", "documents and knowledge management"]),
    ("reporting_tracking", ["تقارير ومتابعة داخلية", "internal reports and tracking"]),
    ("customer_service", ["خدمة عملاء", "customer service"]),
    ("free_diagnostic", []),  # default fallback
]


class InboundIntakeOS:
    """Processes website intake form submissions into qualified leads."""

    _NO_AUTO_SEND = False  # inbound automation is permitted

    def process_submission(self, submission: dict[str, Any]) -> InboundLead:
        """Process a form submission into a qualified InboundLead."""
        score = self.qualify(submission)
        offer = self.route_offer(submission)

        lang_raw = (submission.get("language") or "ar").lower()
        language = Language.arabic
        if "english" in lang_raw or lang_raw in ("en", "english"):
            language = Language.english
        elif "both" in lang_raw or "كلاهما" in lang_raw:
            language = Language.bilingual

        lead_capture = LeadCapture(
            source="website_intake",
            name=submission.get("name") or "Unknown",
            email=submission.get("email"),
            phone=submission.get("phone"),
            company=submission.get("company"),
            sector=submission.get("sector") or submission.get("workflow_interest"),
            country=submission.get("country") or "KSA",
            language_preference=language,
            raw_form_data=submission,
        )

        inbound_lead = InboundLead(
            lead=lead_capture,
            qualification_score=score,
            offer_route=offer,
        )
        inbound_lead.auto_reply_draft = self.generate_auto_reply(inbound_lead)
        return inbound_lead

    def qualify(self, submission: dict[str, Any]) -> float:
        """Score submission 0-100 based on company_type, has_data, primary_goal, preferred_format."""
        score = 5.0  # baseline for submitting

        ct = (submission.get("company_type") or "").lower()
        score += _COMPANY_TYPE_SCORES.get(ct, 0.0)

        hd = (submission.get("has_data") or "").lower()
        score += _HAS_DATA_SCORES.get(hd, 0.0)

        pg = (submission.get("primary_goal") or "").lower()
        score += _GOAL_SCORES.get(pg, 0.0)

        pf = (submission.get("preferred_format") or "").lower()
        score += _FORMAT_SCORES.get(pf, 0.0)

        # Bonus if contact info is provided
        if submission.get("email"):
            score += 5.0
        if submission.get("phone"):
            score += 5.0
        if submission.get("company"):
            score += 5.0

        return min(100.0, max(0.0, score))

    def route_offer(self, submission: dict[str, Any]) -> str:
        """Map submission answers to the best offer from the 5-rung ladder."""
        interest = (submission.get("workflow_interest") or "").lower()
        for offer_name, keywords in _OFFER_LADDER:
            if any(kw in interest for kw in keywords):
                return offer_name
        return "free_diagnostic"

    def generate_auto_reply(self, lead: InboundLead) -> str:
        """Generate an automatic welcome reply based on qualification score."""
        lang = lead.lead.language_preference
        name = lead.lead.name
        offer = lead.offer_route
        score = lead.qualification_score

        if lang == Language.arabic:
            if score >= 60:
                return (
                    f"السلام عليكم {name}،\n"
                    f"وصلنا طلبكم وسعداء باهتمامكم.\n"
                    f"بناءً على إجاباتكم، يبدو أن {offer} مناسب لاحتياجاتكم.\n"
                    "سنتواصل معكم قريباً لتحديد موعد مناسب.\n"
                    "مع التحية،\nSami | Dealix"
                )
            return (
                f"السلام عليكم {name}،\n"
                "وصلنا طلبكم، شكراً لاهتمامكم بـ Dealix.\n"
                "سنرسل لكم نبذة مختصرة تناسب نشاطكم خلال فترة وجيزة.\n"
                "مع التحية،\nSami | Dealix"
            )
        if score >= 60:
            return (
                f"Hi {name},\n"
                f"We received your submission. Based on your answers, {offer} looks like a strong fit.\n"
                "We will reach out shortly to schedule a call.\n"
                "Best regards,\nSami | Dealix"
            )
        return (
            f"Hi {name},\n"
            "Thank you for your interest in Dealix.\n"
            "We will send you a brief overview relevant to your business shortly.\n"
            "Best regards,\nSami | Dealix"
        )

    def create_call_brief(self, lead: InboundLead) -> dict[str, Any]:
        """Create a call brief for the discovery call."""
        return {
            "name": lead.lead.name,
            "company": lead.lead.company,
            "email": lead.lead.email,
            "phone": lead.lead.phone,
            "sector": lead.lead.sector,
            "country": lead.lead.country,
            "language": lead.lead.language_preference.value,
            "qualification_score": round(lead.qualification_score, 1),
            "offer_route": lead.offer_route,
            "key_points": [
                f"Sector: {lead.lead.sector or 'unknown'}",
                f"Offer fit: {lead.offer_route}",
                f"Score: {round(lead.qualification_score, 1)}",
            ],
            "form_answers": lead.lead.raw_form_data,
        }

    def get_intake_form(self, language: str = "ar") -> list[dict]:
        """Return the intake questions in the specified language."""
        if language in ("en", "english"):
            return INTAKE_QUESTIONS_EN
        return INTAKE_QUESTIONS_AR


__all__ = [
    "INTAKE_QUESTIONS_AR",
    "INTAKE_QUESTIONS_EN",
    "InboundIntakeOS",
]
