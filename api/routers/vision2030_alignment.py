"""Vision 2030 Alignment — Saudi-market strategic narrative builder.

Public read-only endpoints (no auth required — lead-gen tool).
All narratives carry a mandatory draft disclaimer and must be reviewed
before external use.

Prefix: /api/v1/vision2030
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/vision2030",
    tags=["Analytics"],
)

# ---------------------------------------------------------------------------
# Mandatory disclaimer
# ---------------------------------------------------------------------------

_DISCLAIMER_AR = (
    "هذه رواية تقديرية — راجعها قبل الإرسال"
)
_DISCLAIMER_EN = (
    "This is a draft narrative — review before sending"
)

# ---------------------------------------------------------------------------
# Static data: Vision 2030 pillars
# ---------------------------------------------------------------------------

_PILLARS: list[dict[str, Any]] = [
    {
        "pillar_id": "thriving_economy",
        "name_ar": "اقتصاد مزدهر",
        "name_en": "Thriving Economy",
        "ai_relevance_score": 92,
        "dealix_solutions": [
            "AI-driven revenue operations",
            "Automated sales pipeline",
            "Productivity measurement tooling",
            "B2B lead qualification engine",
        ],
    },
    {
        "pillar_id": "vibrant_society",
        "name_ar": "مجتمع حيوي",
        "name_en": "Vibrant Society",
        "ai_relevance_score": 78,
        "dealix_solutions": [
            "AI-powered customer experience scoring",
            "Service quality monitoring",
            "Client health dashboards",
            "Multilingual support workflows",
        ],
    },
    {
        "pillar_id": "ambitious_nation",
        "name_ar": "وطن طموح",
        "name_en": "Ambitious Nation",
        "ai_relevance_score": 85,
        "dealix_solutions": [
            "Data sovereignty controls",
            "Saudi-first localisation layer",
            "Local talent upskilling modules",
            "PDPL-compliant data processing",
        ],
    },
]

_PILLAR_NAMES_BY_ID: dict[str, str] = {
    p["pillar_id"]: p["name_en"] for p in _PILLARS
}

# ---------------------------------------------------------------------------
# Static data: sector alignment profiles
# ---------------------------------------------------------------------------

_SECTOR_ALIGNMENT: dict[str, dict[str, Any]] = {
    "b2b_saas": {
        "overall_alignment_score": 90,
        "aligned_pillars": ["Thriving Economy", "Ambitious Nation"],
        "vision2030_programs": [
            "Saudi Digital Academy",
            "CITC AI Strategy",
            "NTP 2025",
        ],
        "narrative_ar": (
            "يمكن أن يُسهم اعتماد الذكاء الاصطناعي في قطاع البرمجيات السحابية في تسريع "
            "التحول الرقمي للمنشآت السعودية وفق أهداف رؤية 2030. "
            "ويمكن لمنصات B2B أن تدعم أهداف NTP 2025 من خلال تحسين الكفاءة التشغيلية "
            "وتمكين الكوادر الوطنية من إتقان أدوات الذكاء الاصطناعي. "
            "يمكن أن يُعزز ذلك القدرة التنافسية للاقتصاد الرقمي السعودي على المستوى الإقليمي."
        ),
        "narrative_en": (
            "AI adoption in the cloud software sector can accelerate digital transformation "
            "across Saudi enterprises in line with Vision 2030 targets. "
            "B2B platforms can support NTP 2025 objectives by improving operational efficiency "
            "and equipping national talent with AI skills. "
            "This may strengthen the competitiveness of the Saudi digital economy regionally."
        ),
    },
    "agency": {
        "overall_alignment_score": 72,
        "aligned_pillars": ["Thriving Economy", "Vibrant Society"],
        "vision2030_programs": [
            "Saudi Digital Academy",
            "CITC AI Strategy",
        ],
        "narrative_ar": (
            "يمكن لوكالات التسويق والاستشارات التي تعتمد الذكاء الاصطناعي أن تُسهم في "
            "رفع مستوى جودة الخدمات المقدمة للعملاء السعوديين. "
            "يمكن أن تدعم هذه الوكالات ركيزة المجتمع الحيوي من خلال تحسين تجربة العميل "
            "وتقديم محتوى ذو صلة باللغة العربية. "
            "يمكن أن يُقلص اعتماد الذكاء الاصطناعي الفجوة في الكفاءة التشغيلية."
        ),
        "narrative_en": (
            "Marketing and consulting agencies that adopt AI can contribute to raising "
            "the quality of services delivered to Saudi clients. "
            "These agencies can support the Vibrant Society pillar by improving customer "
            "experience and delivering Arabic-language content. "
            "AI adoption may reduce the operational efficiency gap across the sector."
        ),
    },
    "healthcare_clinic": {
        "overall_alignment_score": 88,
        "aligned_pillars": ["Vibrant Society", "Ambitious Nation"],
        "vision2030_programs": [
            "Saudi Vision Health Sector Transformation",
            "CITC AI Strategy",
            "NTP 2025",
        ],
        "narrative_ar": (
            "يمكن للعيادات الصحية التي تعتمد الذكاء الاصطناعي أن تُسهم بشكل مباشر في "
            "تحقيق أهداف تحسين الرعاية الصحية ضمن ركيزة المجتمع الحيوي لرؤية 2030. "
            "يمكن أن تُمكّن أدوات الذكاء الاصطناعي من تحسين إدارة المرضى وتقليل أوقات "
            "الانتظار مع الحفاظ على الامتثال التنظيمي. "
            "يمكن أن تدعم هذه الحلول استدامة المنظومة الصحية الوطنية."
        ),
        "narrative_en": (
            "Healthcare clinics adopting AI can directly contribute to the health improvement "
            "targets under Vision 2030's Vibrant Society pillar. "
            "AI tools can improve patient management and reduce waiting times while "
            "maintaining regulatory compliance. "
            "These solutions may support the long-term sustainability of the national "
            "health system."
        ),
    },
    "real_estate": {
        "overall_alignment_score": 85,
        "aligned_pillars": ["Thriving Economy", "Ambitious Nation"],
        "vision2030_programs": [
            "NEOM",
            "Qiddiya",
            "NTP 2025",
            "CITC AI Strategy",
        ],
        "narrative_ar": (
            "يمكن لقطاع العقارات السعودي الذي يعتمد الذكاء الاصطناعي أن يُسهم في دعم "
            "المشاريع الوطنية الكبرى كنيوم وقدية من خلال تحسين كفاءة إدارة الأصول. "
            "يمكن أن تُعزز أدوات الذكاء الاصطناعي شفافية السوق العقاري وتُسرّع دورة "
            "المبيعات لدعم الاقتصاد المزدهر. "
            "يمكن أن يُقلل ذلك من الاعتماد على الخبرات الخارجية ويُعزز الكوادر الوطنية."
        ),
        "narrative_en": (
            "The Saudi real estate sector adopting AI can contribute to major national "
            "projects such as NEOM and Qiddiya by improving asset management efficiency. "
            "AI tools can enhance market transparency and accelerate the sales cycle "
            "to support the Thriving Economy pillar. "
            "This may reduce dependency on external expertise and strengthen national talent."
        ),
    },
    "logistics": {
        "overall_alignment_score": 83,
        "aligned_pillars": ["Thriving Economy", "Ambitious Nation"],
        "vision2030_programs": [
            "National Transport and Logistics Strategy",
            "NTP 2025",
            "CITC AI Strategy",
        ],
        "narrative_ar": (
            "يمكن لشركات اللوجستيات التي تعتمد الذكاء الاصطناعي أن تدعم استراتيجية "
            "النقل والخدمات اللوجستية الوطنية وأهداف الاقتصاد المزدهر لرؤية 2030. "
            "يمكن أن تُحسّن أدوات تحسين المسارات وإدارة الأسطول كفاءة التشغيل وتقليل "
            "التكاليف. "
            "يمكن أن يُعزز ذلك مكانة المملكة العربية السعودية مركزاً لوجستياً إقليمياً."
        ),
        "narrative_en": (
            "Logistics companies adopting AI can support the National Transport and "
            "Logistics Strategy and the Thriving Economy objectives of Vision 2030. "
            "Route optimisation and fleet management tools can improve operational "
            "efficiency and reduce costs. "
            "This may strengthen Saudi Arabia's position as a regional logistics hub."
        ),
    },
    "fintech": {
        "overall_alignment_score": 91,
        "aligned_pillars": ["Thriving Economy", "Ambitious Nation"],
        "vision2030_programs": [
            "Saudi Fintech Strategy",
            "SAMA Digital Banking Framework",
            "CITC AI Strategy",
            "NTP 2025",
        ],
        "narrative_ar": (
            "يمكن للشركات التقنية المالية التي تعتمد الذكاء الاصطناعي أن تُسرّع تحقيق "
            "أهداف الاستراتيجية الوطنية للتقنية المالية ضمن رؤية 2030. "
            "يمكن أن تُحسّن حلول الذكاء الاصطناعي الامتثال التنظيمي وتكشف عن فرص "
            "الإيرادات وتُعزز الأمن المالي. "
            "يمكن أن يدعم ذلك هدف رفع نسبة المعاملات الرقمية وتعميق الشمول المالي."
        ),
        "narrative_en": (
            "Fintech companies adopting AI can accelerate the National Fintech Strategy "
            "objectives within Vision 2030. "
            "AI solutions can improve regulatory compliance, uncover revenue opportunities, "
            "and strengthen financial security. "
            "This may support the goal of increasing digital transactions and deepening "
            "financial inclusion."
        ),
    },
    "engineering": {
        "overall_alignment_score": 80,
        "aligned_pillars": ["Thriving Economy", "Ambitious Nation"],
        "vision2030_programs": [
            "NEOM",
            "NTP 2025",
            "Saudi Contractors Authority Digitalisation",
        ],
        "narrative_ar": (
            "يمكن لشركات الهندسة والمقاولات التي تعتمد الذكاء الاصطناعي أن تُسهم في "
            "إنجاز المشاريع الوطنية الكبرى بكفاءة أعلى وكلفة أقل. "
            "يمكن أن تُحسّن أدوات إدارة المشاريع بالذكاء الاصطناعي دقة التخطيط وتقليل "
            "التأخيرات وضبط الميزانيات. "
            "يمكن أن يُعزز ذلك قدرة القطاع على تلبية الطلب المتسارع في ظل رؤية 2030."
        ),
        "narrative_en": (
            "Engineering and contracting firms adopting AI can contribute to completing "
            "major national projects with greater efficiency and lower cost. "
            "AI-powered project management tools can improve planning accuracy, reduce "
            "delays, and control budgets. "
            "This may strengthen the sector's capacity to meet accelerating demand "
            "under Vision 2030."
        ),
    },
}

_KNOWN_SECTORS = set(_SECTOR_ALIGNMENT.keys())

# ---------------------------------------------------------------------------
# Pydantic request model
# ---------------------------------------------------------------------------


class GenerateNarrativeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sector: str = Field(..., min_length=2, max_length=64)
    company_name: str = Field(..., min_length=1, max_length=120)
    use_case: str = Field(..., min_length=2, max_length=256)


# ---------------------------------------------------------------------------
# Business logic (pure Python — no LLM)
# ---------------------------------------------------------------------------


def list_pillars() -> dict[str, Any]:
    """Return the three Vision 2030 pillars with AI-relevance metadata."""
    return {
        "pillars": _PILLARS,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


def get_sector_alignment(sector: str) -> dict[str, Any]:
    """Return Vision 2030 alignment data for the given sector.

    Raises KeyError when sector is unknown.
    """
    data = _SECTOR_ALIGNMENT.get(sector)
    if data is None:
        raise KeyError(sector)
    return {
        **data,
        "sector": sector,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


def generate_narrative(
    sector: str,
    company_name: str,
    use_case: str,
) -> dict[str, Any]:
    """Generate a tailored Vision 2030 alignment narrative for a company.

    Falls back to a generic narrative when the sector is not in the
    known-sectors catalogue.  No LLM calls are made.
    All output carries the mandatory draft disclaimer.
    """
    profile = _SECTOR_ALIGNMENT.get(sector)

    if profile is not None:
        base_score = profile["overall_alignment_score"]
        key_pillars = profile["aligned_pillars"]
        base_ar = profile["narrative_ar"]
        base_en = profile["narrative_en"]
    else:
        # Graceful fallback for unknown sectors
        base_score = 65
        key_pillars = ["Thriving Economy"]
        base_ar = (
            "يمكن أن يُسهم اعتماد الذكاء الاصطناعي في هذا القطاع في دعم أهداف "
            "رؤية 2030 التحويلية."
        )
        base_en = (
            "AI adoption in this sector can contribute to the transformational "
            "goals of Vision 2030."
        )

    # Compose company-specific narrative (no guaranteed-outcome language)
    narrative_ar = (
        f"يمكن أن تُسهم {company_name} من خلال تطبيق {use_case} في دعم أهداف "
        f"رؤية 2030. "
        + base_ar
    )
    narrative_en = (
        f"{company_name} can potentially contribute to Vision 2030 objectives "
        f"by applying {use_case}. "
        + base_en
    )

    return {
        "company_name": company_name,
        "sector": sector,
        "use_case": use_case,
        "narrative_ar": narrative_ar,
        "narrative_en": narrative_en,
        "alignment_score": base_score,
        "key_pillars": key_pillars,
        "disclaimer_ar": _DISCLAIMER_AR,
        "disclaimer_en": _DISCLAIMER_EN,
        "governance_decision": "ALLOW_WITH_REVIEW",
    }


# ---------------------------------------------------------------------------
# Router endpoints
# ---------------------------------------------------------------------------


@router.get("/pillars")
def pillars_endpoint() -> dict[str, Any]:
    """List Vision 2030 pillars and their AI-adoption relevance scores."""
    return list_pillars()


@router.get("/sector-alignment/{sector}")
def sector_alignment_endpoint(sector: str) -> dict[str, Any]:
    """Return how a given sector's AI adoption aligns with Vision 2030.

    Returns 404 for unknown sectors.
    """
    try:
        return get_sector_alignment(sector)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail={
                "error": f"Sector '{sector}' not found.",
                "available_sectors": sorted(_KNOWN_SECTORS),
                "governance_decision": "ALLOW",
            },
        )


@router.post("/generate-narrative")
def generate_narrative_endpoint(body: GenerateNarrativeRequest) -> dict[str, Any]:
    """Generate a tailored Vision 2030 alignment narrative for a specific company.

    No LLM calls are made.  All output must be reviewed before external use.
    """
    return generate_narrative(
        sector=body.sector,
        company_name=body.company_name,
        use_case=body.use_case,
    )
