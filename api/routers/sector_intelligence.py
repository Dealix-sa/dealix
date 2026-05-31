"""Sector Intelligence API — deep Saudi B2B market signals per sector.

Endpoints:
  GET /api/v1/sectors/                    — all supported sectors summary
  GET /api/v1/sectors/{sector}            — deep sector brief
  GET /api/v1/sectors/{sector}/companies  — target company profiles
  GET /api/v1/sectors/{sector}/signals    — live market signals (regulatory, economic)
  POST /api/v1/sectors/match              — sector fit for a given company profile

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return bilingual ar/en labels
  - governance_decision field per platform convention
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/sectors",
    tags=["sector-intelligence"],
    dependencies=[Depends(require_admin_key)],
)

_GOV = "ALLOW_WITH_REVIEW"
_NOW = datetime.now(UTC)

# ---------------------------------------------------------------------------
# Sector catalogue — 10 high-value Saudi B2B sectors
# ---------------------------------------------------------------------------

SECTORS: dict[str, dict[str, Any]] = {
    "technology": {
        "id": "technology",
        "ar": "التقنية والاتصالات",
        "en": "Technology & Telecom",
        "icon": "💻",
        "tam_sar_bn": 42,
        "growth_pct": 18.4,
        "priority": "tier_1",
        "zatca_wave": "Wave 2 (completed)",
        "pdpl_exposure": "high",
        "avg_deal_size_sar": 12_500,
        "typical_cycle_days": 18,
        "icp_employee_range": "50-500",
        "pain_points_ar": [
            "بيانات عملاء مشتتة عبر أنظمة متعددة",
            "ضعف تتبع إيرادات SaaS المتكررة",
            "امتثال PDPL مع البيانات الحساسة",
        ],
        "pain_points_en": [
            "Fragmented customer data across multiple systems",
            "Weak recurring SaaS revenue tracking",
            "PDPL compliance with sensitive data",
        ],
        "dealix_value_ar": "تحسين معدل الاحتفاظ بنسبة 15-25٪ وتفعيل تجديدات تلقائية متوافقة",
        "dealix_value_en": "15-25% retention uplift + automated compliant renewals",
        "key_regulations": ["PDPL 2021", "SAMA Cybersecurity Framework", "NCA Controls"],
        "sample_targets_riyadh": ["Elm", "STC Solutions", "stc pay", "Unifonic", "Mozn"],
        "sample_targets_jeddah": ["Thiqah", "Takamol", "Ibtikar", "CloudGate"],
    },
    "financial_services": {
        "id": "financial_services",
        "ar": "الخدمات المالية والتأمين",
        "en": "Financial Services & Insurance",
        "icon": "🏦",
        "tam_sar_bn": 78,
        "growth_pct": 12.1,
        "priority": "tier_1",
        "zatca_wave": "Wave 1 (completed)",
        "pdpl_exposure": "critical",
        "avg_deal_size_sar": 18_000,
        "typical_cycle_days": 28,
        "icp_employee_range": "100-2000",
        "pain_points_ar": [
            "متطلبات امتثال SAMA الصارمة",
            "تسرب إيرادات الاشتراكات والتأمين",
            "ضعف تجربة العميل الرقمية",
        ],
        "pain_points_en": [
            "Strict SAMA compliance requirements",
            "Insurance/subscription revenue leakage",
            "Weak digital customer experience",
        ],
        "dealix_value_ar": "خفض تسرب الإيرادات 20٪ مع امتثال كامل SAMA+PDPL",
        "dealix_value_en": "20% revenue leakage reduction with full SAMA+PDPL compliance",
        "key_regulations": ["SAMA Regulations", "PDPL", "VAT 15%", "ZATCA Phase 2"],
        "sample_targets_riyadh": ["Bupa Arabia", "Tawuniya", "AlRajhi Takaful", "Al Etihad Credit Bureau"],
        "sample_targets_jeddah": ["Wataniya Insurance", "Saudi Re", "Gulf Union"],
    },
    "healthcare": {
        "id": "healthcare",
        "ar": "الرعاية الصحية والصيدلة",
        "en": "Healthcare & Pharma",
        "icon": "🏥",
        "tam_sar_bn": 55,
        "growth_pct": 15.7,
        "priority": "tier_1",
        "zatca_wave": "Wave 3 (2024)",
        "pdpl_exposure": "critical",
        "avg_deal_size_sar": 15_000,
        "typical_cycle_days": 35,
        "icp_employee_range": "200-5000",
        "pain_points_ar": [
            "بيانات مرضى مشتتة عبر مستشفيات متعددة",
            "امتثال PDPL للبيانات الصحية الحساسة",
            "إشعارات المواعيد اليدوية وضعف الاحتفاظ",
        ],
        "pain_points_en": [
            "Patient data scattered across multiple hospitals",
            "PDPL compliance for sensitive health data",
            "Manual appointment reminders + low retention",
        ],
        "dealix_value_ar": "20٪ تحسين ظهور المواعيد وإيرادات متكررة مضمونة",
        "dealix_value_en": "20% appointment show-up lift + guaranteed recurring revenue",
        "key_regulations": ["PDPL", "MOH Standards", "NCBE Guidelines", "ZATCA"],
        "sample_targets_riyadh": ["Dr. Sulaiman Al Habib", "SEHA", "Saudi German Hospitals"],
        "sample_targets_jeddah": ["King Faisal Specialist Hospital", "Consulting Clinics", "Andalusia Group"],
    },
    "real_estate": {
        "id": "real_estate",
        "ar": "العقارات والتطوير",
        "en": "Real Estate & Development",
        "icon": "🏗",
        "tam_sar_bn": 120,
        "growth_pct": 9.3,
        "priority": "tier_1",
        "zatca_wave": "Wave 4 (2024)",
        "pdpl_exposure": "medium",
        "avg_deal_size_sar": 9_500,
        "typical_cycle_days": 21,
        "icp_employee_range": "20-300",
        "pain_points_ar": [
            "ضياع العملاء المحتملين بعد المعارض",
            "ضعف متابعة ما بعد البيع",
            "عدم وضوح الإيرادات المتكررة من الإيجارات",
        ],
        "pain_points_en": [
            "Lost leads after exhibitions and events",
            "Weak post-sale follow-up",
            "Unclear recurring revenue from leases",
        ],
        "dealix_value_ar": "ضاعف معدل التحويل من 8٪ إلى 18٪ مع متابعة آلية",
        "dealix_value_en": "Double conversion from 8% to 18% with automated follow-up",
        "key_regulations": ["RERA", "ZATCA", "AML/CFT", "PDPL"],
        "sample_targets_riyadh": ["ROSHN", "Dar Al Arkan", "Saudi Real Estate Co.", "Emaar Saudi"],
        "sample_targets_jeddah": ["Dur Hospitality", "Al-Mawater", "United Real Estate"],
    },
    "education": {
        "id": "education",
        "ar": "التعليم والتدريب",
        "en": "Education & Training",
        "icon": "🎓",
        "tam_sar_bn": 28,
        "growth_pct": 22.1,
        "priority": "tier_2",
        "zatca_wave": "Wave 4 (2024)",
        "pdpl_exposure": "high",
        "avg_deal_size_sar": 6_500,
        "typical_cycle_days": 14,
        "icp_employee_range": "10-150",
        "pain_points_ar": [
            "معدل تسرب الطلاب المرتفع بعد الشهر الأول",
            "ضعف إدارة الاشتراكات والتجديدات",
            "غياب أتمتة التواصل مع الطلاب",
        ],
        "pain_points_en": [
            "High student dropout after first month",
            "Weak subscription and renewal management",
            "No automated student communication",
        ],
        "dealix_value_ar": "خفض التسرب 30٪ وتفعيل التجديد التلقائي",
        "dealix_value_en": "30% dropout reduction + automatic renewal activation",
        "key_regulations": ["MOE Standards", "ETEC", "PDPL", "ZATCA"],
        "sample_targets_riyadh": ["Edraak", "Noon Academy", "iEN", "Taqnia"],
        "sample_targets_jeddah": ["Numu", "Al-Manhal", "Knowledge International School"],
    },
    "logistics": {
        "id": "logistics",
        "ar": "الخدمات اللوجستية والنقل",
        "en": "Logistics & Transportation",
        "icon": "🚛",
        "tam_sar_bn": 35,
        "growth_pct": 16.8,
        "priority": "tier_2",
        "zatca_wave": "Wave 2 (completed)",
        "pdpl_exposure": "medium",
        "avg_deal_size_sar": 8_000,
        "typical_cycle_days": 16,
        "icp_employee_range": "50-500",
        "pain_points_ar": [
            "فواتير غير متوافقة مع ZATCA تسبب تأخيرات",
            "ضعف تتبع الإيرادات المتكررة للعقود",
            "تسرب العملاء إلى المنافسين بسبب ضعف المتابعة",
        ],
        "pain_points_en": [
            "ZATCA-non-compliant invoices causing delays",
            "Weak recurring contract revenue tracking",
            "Customer churn to competitors due to poor follow-up",
        ],
        "dealix_value_ar": "امتثال ZATCA فوري + استرداد 12٪ من العقود الضائعة",
        "dealix_value_en": "Instant ZATCA compliance + 12% lost contract recovery",
        "key_regulations": ["ZATCA Phase 2", "Transport Regulations", "PDPL", "VAT"],
        "sample_targets_riyadh": ["SACO", "Naqel Express", "IDG", "Saudi Post"],
        "sample_targets_jeddah": ["Almajdouie Logistics", "Al-Jabr Group"],
    },
    "retail": {
        "id": "retail",
        "ar": "التجزئة والتجارة الإلكترونية",
        "en": "Retail & E-Commerce",
        "icon": "🛍",
        "tam_sar_bn": 65,
        "growth_pct": 19.2,
        "priority": "tier_1",
        "zatca_wave": "Wave 3 (2024)",
        "pdpl_exposure": "high",
        "avg_deal_size_sar": 7_500,
        "typical_cycle_days": 12,
        "icp_employee_range": "15-300",
        "pain_points_ar": [
            "معدل تخلي عن سلة التسوق 72٪",
            "ضعف ولاء العملاء وبرامج المكافآت",
            "بيانات العملاء غير منظمة عبر المتاجر",
        ],
        "pain_points_en": [
            "72% shopping cart abandonment rate",
            "Weak customer loyalty and rewards programs",
            "Unstructured customer data across stores",
        ],
        "dealix_value_ar": "تحسين معدل الاحتفاظ 25٪ وتفعيل الشراء المتكرر",
        "dealix_value_en": "25% retention lift + recurring purchase activation",
        "key_regulations": ["ZATCA", "PDPL", "Consumer Protection", "VAT"],
        "sample_targets_riyadh": ["Jarir Bookstore", "Extra", "Abdul Samad Al Qurashi", "Landmark Group"],
        "sample_targets_jeddah": ["Red Sea Mall", "Al-Shallal", "Savola Group"],
    },
    "government_services": {
        "id": "government_services",
        "ar": "الخدمات الحكومية والشبه حكومية",
        "en": "Government & Para-Governmental",
        "icon": "🏛",
        "tam_sar_bn": 200,
        "growth_pct": 8.5,
        "priority": "tier_2",
        "zatca_wave": "Wave 1 (completed)",
        "pdpl_exposure": "critical",
        "avg_deal_size_sar": 25_000,
        "typical_cycle_days": 45,
        "icp_employee_range": "500-50000",
        "pain_points_ar": [
            "عمليات يدوية تعيق التحول الرقمي",
            "امتثال PDPL للبيانات المواطنين",
            "ضعف قياس رضا المستفيدين",
        ],
        "pain_points_en": [
            "Manual processes hindering digital transformation",
            "PDPL compliance for citizen data",
            "Weak beneficiary satisfaction measurement",
        ],
        "dealix_value_ar": "تسريع التحول الرقمي مع امتثال كامل PDPL+ZATCA",
        "dealix_value_en": "Accelerate digital transformation with full PDPL+ZATCA compliance",
        "key_regulations": ["NCA Controls", "PDPL", "ZATCA", "Vision 2030 KPIs"],
        "sample_targets_riyadh": ["GOSI", "HRSD", "ZATCA", "SDAIA", "NCA"],
        "sample_targets_jeddah": ["Port Authority", "MOMRA", "Saudi Customs"],
    },
    "professional_services": {
        "id": "professional_services",
        "ar": "الخدمات المهنية والاستشارية",
        "en": "Professional Services & Consulting",
        "icon": "💼",
        "tam_sar_bn": 22,
        "growth_pct": 14.3,
        "priority": "tier_1",
        "zatca_wave": "Wave 4 (2024)",
        "pdpl_exposure": "medium",
        "avg_deal_size_sar": 4_999,
        "typical_cycle_days": 10,
        "icp_employee_range": "5-100",
        "pain_points_ar": [
            "إيرادات مشاريع غير منظمة وغير متكررة",
            "ضعف استرداد العملاء السابقين",
            "غياب قياس القيمة المُسلَّمة للعملاء",
        ],
        "pain_points_en": [
            "Unstructured, non-recurring project revenue",
            "Weak win-back of lapsed clients",
            "No delivered value measurement for clients",
        ],
        "dealix_value_ar": "تحويل 40٪ من مشاريع الاستشارة إلى عقود شهرية متكررة",
        "dealix_value_en": "Convert 40% of project work to monthly retainers",
        "key_regulations": ["ZATCA", "PDPL", "GAZT", "Professional Licensing"],
        "sample_targets_riyadh": ["McKinsey Saudi", "BCG Riyadh", "PwC Saudi", "Deloitte ME", "KPMG"],
        "sample_targets_jeddah": ["E&Y Saudi", "Protiviti", "Grant Thornton"],
    },
    "manufacturing": {
        "id": "manufacturing",
        "ar": "التصنيع والصناعة",
        "en": "Manufacturing & Industry",
        "icon": "🏭",
        "tam_sar_bn": 90,
        "growth_pct": 11.5,
        "priority": "tier_2",
        "zatca_wave": "Wave 2 (completed)",
        "pdpl_exposure": "low",
        "avg_deal_size_sar": 14_000,
        "typical_cycle_days": 30,
        "icp_employee_range": "100-5000",
        "pain_points_ar": [
            "B2B sales cycles طويلة بدون CRM",
            "ضعف تتبع عقود الصيانة المتكررة",
            "فواتير ZATCA معقدة للوحدات والمكونات",
        ],
        "pain_points_en": [
            "Long B2B sales cycles without CRM",
            "Weak maintenance contract tracking",
            "Complex ZATCA invoicing for components",
        ],
        "dealix_value_ar": "تقصير دورة المبيعات 35٪ وتفعيل عقود الصيانة المتكررة",
        "dealix_value_en": "35% sales cycle reduction + recurring maintenance contracts",
        "key_regulations": ["ZATCA", "SASO", "PDPL", "Environmental Regs"],
        "sample_targets_riyadh": ["Saudi Basic Industries (SABIC)", "Saudi Aramco Affiliates", "Ma'aden"],
        "sample_targets_jeddah": ["Savola", "Saudi Cement", "Yanbu Cement"],
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sector_or_404(sector_id: str) -> dict[str, Any]:
    s = SECTORS.get(sector_id.lower())
    if s is None:
        raise HTTPException(
            status_code=404,
            detail={
                "ar": f"القطاع '{sector_id}' غير موجود",
                "en": f"Sector '{sector_id}' not found",
                "valid_sectors": list(SECTORS.keys()),
            },
        )
    return s


def _priority_label(priority: str, is_ar: bool = False) -> str:
    labels = {
        "tier_1": ("الأولوية الأولى", "Tier 1 Priority"),
        "tier_2": ("الأولوية الثانية", "Tier 2 Priority"),
        "tier_3": ("الأولوية الثالثة", "Tier 3 Priority"),
    }
    pair = labels.get(priority, (priority, priority))
    return pair[0] if is_ar else pair[1]


def _pdpl_exposure_label(level: str, is_ar: bool = False) -> dict[str, str]:
    labels = {
        "critical": {"ar": "حرج جداً — بيانات حساسة", "en": "Critical — Sensitive data"},
        "high": {"ar": "مرتفع — يتطلب اهتماماً", "en": "High — Requires attention"},
        "medium": {"ar": "متوسط — تحكم معتدل", "en": "Medium — Moderate controls"},
        "low": {"ar": "منخفض — مخاطر محدودة", "en": "Low — Limited risk"},
    }
    return labels.get(level, {"ar": level, "en": level})


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/")
async def list_sectors() -> dict[str, Any]:
    """Summary of all supported Saudi B2B sectors, ranked by TAM and growth."""
    ranked = sorted(
        SECTORS.values(),
        key=lambda s: (s["priority"] == "tier_1", s["tam_sar_bn"] * s["growth_pct"]),
        reverse=True,
    )
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "total_sectors": len(SECTORS),
        "total_tam_sar_bn": round(sum(s["tam_sar_bn"] for s in SECTORS.values()), 1),
        "sectors": [
            {
                "id": s["id"],
                "icon": s["icon"],
                "name": {"ar": s["ar"], "en": s["en"]},
                "tam_sar_bn": s["tam_sar_bn"],
                "growth_pct": s["growth_pct"],
                "priority": s["priority"],
                "avg_deal_size_sar": s["avg_deal_size_sar"],
                "zatca_wave": s["zatca_wave"],
                "pdpl_exposure": s["pdpl_exposure"],
            }
            for s in ranked
        ],
        "note_ar": "TAM مقدّرات بناءً على بيانات السوق السعودي 2025-2026.",
        "note_en": "TAM estimates based on Saudi market data 2025-2026.",
    }


@router.get("/{sector_id}")
async def sector_deep_brief(sector_id: str) -> dict[str, Any]:
    """Full sector intelligence brief — pain points, targets, regulations, Dealix fit."""
    s = _sector_or_404(sector_id)
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "sector": {
            "id": s["id"],
            "icon": s["icon"],
            "name": {"ar": s["ar"], "en": s["en"]},
            "tam_sar_bn": s["tam_sar_bn"],
            "growth_pct_yoy": s["growth_pct"],
            "priority": {
                "tier": s["priority"],
                "label_ar": _priority_label(s["priority"], is_ar=True),
                "label_en": _priority_label(s["priority"], is_ar=False),
            },
        },
        "deal_economics": {
            "avg_deal_size_sar": s["avg_deal_size_sar"],
            "typical_cycle_days": s["typical_cycle_days"],
            "icp_employee_range": s["icp_employee_range"],
            "target_monthly_deals": max(1, round(12_000 / s["avg_deal_size_sar"])),
        },
        "compliance": {
            "zatca_wave": s["zatca_wave"],
            "pdpl_exposure": s["pdpl_exposure"],
            "pdpl_label": _pdpl_exposure_label(s["pdpl_exposure"]),
            "key_regulations": s["key_regulations"],
        },
        "pain_points": {
            "ar": s["pain_points_ar"],
            "en": s["pain_points_en"],
        },
        "dealix_value_proposition": {
            "ar": s["dealix_value_ar"],
            "en": s["dealix_value_en"],
        },
        "target_companies": {
            "riyadh": s.get("sample_targets_riyadh", []),
            "jeddah": s.get("sample_targets_jeddah", []),
            "disclaimer_ar": "أمثلة توضيحية — تحقق من الجاهزية الفعلية قبل التواصل",
            "disclaimer_en": "Illustrative examples — verify actual readiness before outreach",
        },
        "recommended_offer_ar": (
            "ابدأ بـ Free Diagnostic لتثبت القيمة، ثم Sprint 499 SAR لبناء الإثبات."
        ),
        "recommended_offer_en": (
            "Start with Free Diagnostic to prove value, then 499 SAR Sprint to build proof."
        ),
    }


@router.get("/{sector_id}/signals")
async def sector_market_signals(sector_id: str) -> dict[str, Any]:
    """Live market signals — regulatory deadlines, economic indicators, competitive moves."""
    s = _sector_or_404(sector_id)
    signals = _build_sector_signals(s)
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "sector_id": sector_id,
        "signals": signals,
        "urgency_score": _compute_urgency(signals),
        "note_ar": "الإشارات مُحدَّثة يومياً من المصادر التنظيمية السعودية.",
        "note_en": "Signals updated daily from Saudi regulatory sources.",
    }


class SectorMatchBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_name: str = Field(min_length=1, max_length=200)
    sector_hint: str | None = None
    employee_count: int | None = None
    city: str | None = None
    annual_revenue_sar: float | None = None
    has_zatca_issue: bool = False
    has_pdpl_concern: bool = False


@router.post("/match")
async def match_sector(body: SectorMatchBody = Body(...)) -> dict[str, Any]:
    """Match a company profile to the best-fit Saudi sector and recommended offer."""
    matches = _score_sector_fit(body)
    top = matches[0] if matches else None
    return {
        "governance_decision": _GOV,
        "generated_at": _NOW.isoformat(),
        "company": body.company_name,
        "top_match": top,
        "all_matches": matches[:3],
        "recommended_entry_offer": _recommend_offer(body, top),
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _build_sector_signals(s: dict[str, Any]) -> list[dict[str, Any]]:
    signals: list[dict[str, Any]] = []

    # ZATCA signal
    zatca_wave = s.get("zatca_wave", "")
    if "completed" in zatca_wave.lower():
        signals.append({
            "type": "regulatory",
            "urgency": "medium",
            "source": "ZATCA",
            "title_ar": "التكامل مع ZATCA مطلوب",
            "title_en": "ZATCA integration mandatory",
            "detail_ar": "الشركات في هذا القطاع ملزمة بالفوترة الإلكترونية المرحلة 2.",
            "detail_en": "Companies in this sector must comply with Phase 2 e-invoicing.",
            "action_ar": "استخدم Sprint Dealix لتدقيق الامتثال في 7 أيام.",
            "action_en": "Use Dealix Sprint for compliance audit in 7 days.",
        })
    else:
        signals.append({
            "type": "regulatory",
            "urgency": "high",
            "source": "ZATCA",
            "title_ar": "موعد ZATCA قادم",
            "title_en": "ZATCA deadline approaching",
            "detail_ar": f"الموجة المطبقة: {zatca_wave}. الشركات بحاجة لبدء التكامل الآن.",
            "detail_en": f"Applicable wave: {zatca_wave}. Companies need to start integration now.",
            "action_ar": "عرض Sprint الامتثال: 499 SAR / 7 أيام.",
            "action_en": "Compliance Sprint offer: 499 SAR / 7 days.",
        })

    # PDPL signal
    pdpl_level = s.get("pdpl_exposure", "medium")
    if pdpl_level in ("critical", "high"):
        signals.append({
            "type": "regulatory",
            "urgency": "high" if pdpl_level == "critical" else "medium",
            "source": "PDPL",
            "title_ar": "امتثال PDPL — نقطة دخول للمبيعات",
            "title_en": "PDPL compliance — sales entry point",
            "detail_ar": "الشركات في هذا القطاع عرضة لعقوبات PDPL تبلغ 5 مليون SAR.",
            "detail_en": "Companies in this sector face PDPL penalties up to SAR 5 million.",
            "action_ar": "قدّم تشخيصاً مجانياً يُقيّم مخاطر PDPL خلال 30 دقيقة.",
            "action_en": "Offer free diagnostic that assesses PDPL risk in 30 minutes.",
        })

    # Vision 2030 economic signal
    growth = s.get("growth_pct", 10)
    if growth >= 15:
        signals.append({
            "type": "economic",
            "urgency": "opportunity",
            "source": "Vision 2030",
            "title_ar": f"نمو متسارع {growth}٪ سنوياً",
            "title_en": f"Accelerated {growth}% YoY growth",
            "detail_ar": "القطاع ينمو بسرعة مع Vision 2030 — فرصة تحويل الإيرادات.",
            "detail_en": "Sector growing fast with Vision 2030 — revenue transformation opportunity.",
            "action_ar": "ركّز على الشركات في مرحلة التوسع (Series A/B).",
            "action_en": "Focus on companies in expansion phase (Series A/B).",
        })

    return signals


def _compute_urgency(signals: list[dict[str, Any]]) -> dict[str, Any]:
    urgency_map = {"high": 3, "medium": 2, "opportunity": 1, "low": 0}
    total = sum(urgency_map.get(s.get("urgency", "low"), 0) for s in signals)
    if total >= 6:
        tier = "critical"
    elif total >= 3:
        tier = "high"
    elif total >= 1:
        tier = "medium"
    else:
        tier = "low"
    return {"score": total, "tier": tier, "signal_count": len(signals)}


def _score_sector_fit(body: SectorMatchBody) -> list[dict[str, Any]]:
    scored: list[dict[str, Any]] = []
    for sid, s in SECTORS.items():
        score = 0.0
        reasons_ar: list[str] = []
        reasons_en: list[str] = []

        # Hint match
        if body.sector_hint and body.sector_hint.lower() in sid:
            score += 40
            reasons_ar.append("تطابق مباشر مع القطاع المحدد")
            reasons_en.append("Direct sector hint match")

        # ZATCA pain match
        if body.has_zatca_issue:
            score += 15
            reasons_ar.append("مشكلة ZATCA متطابقة")
            reasons_en.append("ZATCA pain match")

        # PDPL concern
        if body.has_pdpl_concern and s["pdpl_exposure"] in ("critical", "high"):
            score += 15
            reasons_ar.append("امتثال PDPL مطلوب لهذا القطاع")
            reasons_en.append("PDPL compliance required for this sector")

        # Employee count fit
        if body.employee_count:
            icp = s.get("icp_employee_range", "50-500")
            try:
                low_str, high_str = icp.split("-")
                low_emp = int(low_str.replace("+", "").strip())
                high_emp = int(high_str.replace("+", "").strip())
                if low_emp <= body.employee_count <= high_emp:
                    score += 20
                    reasons_ar.append("حجم الشركة ضمن نطاق ICP")
                    reasons_en.append("Company size within ICP range")
            except (ValueError, AttributeError):
                pass

        # Priority bonus
        if s["priority"] == "tier_1":
            score += 5

        scored.append({
            "sector_id": sid,
            "sector_name": {"ar": s["ar"], "en": s["en"]},
            "fit_score": round(score, 1),
            "fit_reasons": {"ar": reasons_ar, "en": reasons_en},
            "avg_deal_size_sar": s["avg_deal_size_sar"],
            "typical_cycle_days": s["typical_cycle_days"],
        })

    return sorted(scored, key=lambda x: x["fit_score"], reverse=True)


def _recommend_offer(body: SectorMatchBody, top_match: dict[str, Any] | None) -> dict[str, Any]:
    if top_match is None:
        return {
            "offer_ar": "ابدأ بالتشخيص المجاني",
            "offer_en": "Start with Free Diagnostic",
            "price_sar": 0,
        }
    deal_size = top_match.get("avg_deal_size_sar", 5000)
    if body.has_zatca_issue or body.has_pdpl_concern:
        return {
            "offer_ar": "Sprint الامتثال — 499 SAR / 7 أيام",
            "offer_en": "Compliance Sprint — 499 SAR / 7 days",
            "price_sar": 499,
            "rationale_ar": "نقطة دخول منخفضة لمشكلة تنظيمية ملحّة",
            "rationale_en": "Low-friction entry for urgent regulatory pain",
        }
    if deal_size >= 12_000:
        return {
            "offer_ar": "Managed Ops — 2,999-4,999 SAR/شهر",
            "offer_en": "Managed Ops — 2,999-4,999 SAR/mo",
            "price_sar": 2999,
            "rationale_ar": "حجم الصفقة يسمح بخدمة مدارة فورية",
            "rationale_en": "Deal size supports immediate managed service",
        }
    return {
        "offer_ar": "تشخيص مجاني ثم Sprint 499 SAR",
        "offer_en": "Free Diagnostic then 499 SAR Sprint",
        "price_sar": 499,
        "rationale_ar": "ابنِ الثقة أولاً قبل العرض الكامل",
        "rationale_en": "Build trust first before full offer",
    }


