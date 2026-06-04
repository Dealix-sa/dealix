"""Shared helpers for Dealix V5 commercial scripts. Pure stdlib, no network."""
from __future__ import annotations

import datetime as _dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = ROOT / "outputs" / "commercial_launch"

# Forced safety flags — present on EVERY draft. The system never sends.
SAFETY_FLAGS = {
    "send_allowed": False,
    "external_send_blocked": True,
    "requires_founder_approval": True,
    "no_auto_send": True,
}

VERTICALS = {
    "facilities_management": {
        "title": "Facilities Management & Maintenance",
        "ar": "إدارة المرافق والصيانة",
        "pain": "manual work-order triage and SLA reporting",
        "pain_ar": "فرز أوامر العمل والتقارير اليدوية",
        "trigger": "won a new multi-site contract",
        "persona": "Operations Director",
        "city": "Riyadh",
    },
    "contracting_project_controls": {
        "title": "Contracting & Project Controls",
        "ar": "المقاولات وضبط المشاريع",
        "pain": "manual progress and cost reporting",
        "pain_ar": "تقارير التقدم والتكلفة اليدوية",
        "trigger": "awarded a large new project",
        "persona": "Projects Director",
        "city": "Jeddah",
    },
    "real_estate_property_ops": {
        "title": "Real Estate & Property Operations",
        "ar": "العقارات وعمليات الأملاك",
        "pain": "tenant request handling and owner reporting",
        "pain_ar": "معالجة طلبات المستأجرين وتقارير الملاك",
        "trigger": "grew the managed portfolio",
        "persona": "Property Operations Manager",
        "city": "Dammam",
    },
    "legal_professional_services": {
        "title": "Legal & Professional Services",
        "ar": "الخدمات القانونية والمهنية",
        "pain": "manual intake and matter status reporting",
        "pain_ar": "الاستقبال اليدوي وتقارير حالة القضايا",
        "trigger": "caseload is growing",
        "persona": "Managing Partner",
        "city": "Riyadh",
    },
    "consulting_training_b2b": {
        "title": "Consulting, Training & B2B Services",
        "ar": "الاستشارات والتدريب وخدمات الأعمال",
        "pain": "proposal turnaround and pipeline consistency",
        "pain_ar": "سرعة العروض واتساق خط الأنابيب",
        "trigger": "scaling the delivery team",
        "persona": "Managing Director",
        "city": "Riyadh",
    },
}

OFFER_STAGES = [
    ("AI Workflow Audit", "499–2,500 SAR"),
    ("Paid Pilot", "5,000–25,000 SAR"),
    ("Department OS", "25,000–150,000 SAR"),
    ("Monthly Retainer", "3,000–25,000 SAR/month"),
    ("Enterprise Custom OS", "150,000+ SAR"),
]

CHANNEL_MIX = {
    "cold_email": 175,
    "follow_up": 100,
    "linkedin_manual": 75,
    "website_form": 50,
}

# Phrases that must NEVER appear in a compliant draft.
BANNED_PHRASES = [
    "guaranteed roi", "guaranteed revenue", "100% roi", "we will double",
    "auto-send", "automated sending", "scraped", "bought your email",
    "no opt-out", "guaranteed results",
]


def today() -> str:
    return _dt.date.today().isoformat()


def out_dir(date: str | None = None) -> Path:
    d = OUTPUTS / (date or today())
    d.mkdir(parents=True, exist_ok=True)
    return d
