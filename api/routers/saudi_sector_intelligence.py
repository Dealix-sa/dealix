"""Saudi sector intelligence — decision-makers, procurement cycles, compliance,
and sector-specific pain points for Saudi B2B selling.

Endpoints:
  GET  /api/v1/sector-intelligence/sectors                   — all 8 sectors (summary)
  GET  /api/v1/sector-intelligence/sectors/{sector_id}       — full sector profile
  GET  /api/v1/sector-intelligence/procurement-thresholds    — SAR procurement rules
  GET  /api/v1/sector-intelligence/decision-makers/{sector_id} — DM titles + approach
  GET  /api/v1/sector-intelligence/compliance-map            — compliance x sector matrix

All GET endpoints return governance_decision: ALLOW_WITH_REVIEW.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/v1/sector-intelligence", tags=["Analytics"])

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_WRITE = "APPROVAL_FIRST"

# ---------------------------------------------------------------------------
# Sector profiles
# ---------------------------------------------------------------------------

_SECTOR_PROFILES: dict[str, dict[str, Any]] = {
    "banking_finance": {
        "name_en": "Banking, Islamic Finance & FinTech",
        "name_ar": "البنوك والتمويل الإسلامي والتقنية المالية",
        "market_size_sar_billion": 320,
        "decision_maker_titles_en": [
            "Chief Financial Officer",
            "Chief Technology Officer",
            "Head of Digital Transformation",
            "Chief Risk Officer",
        ],
        "decision_maker_titles_ar": [
            "الرئيس التنفيذي للشؤون المالية",
            "الرئيس التنفيذي للتقنية",
            "رئيس التحول الرقمي",
            "رئيس إدارة المخاطر",
        ],
        "procurement_cycle_en": (
            "Regulated tender process for all technology spend above SAR 500K; "
            "SAMA pre-approval required for core banking systems. "
            "Pilot or proof-of-concept can be run under SAR 100K direct purchase."
        ),
        "key_pain_points_en": [
            "Strict SAMA audit and reporting cycles consuming significant manual effort",
            "Legacy core banking systems creating data silos that block revenue analytics",
            "PDPL compliance for customer financial data with cross-border data-transfer risks",
        ],
        "key_pain_points_ar": [
            "دورات تدقيق وإبلاغ صارمة من ساما تستهلك جهدًا يدويًا كبيرًا",
            "أنظمة مصرفية قديمة تُشكّل صوامع بيانات تعيق تحليلات الإيرادات",
            "الامتثال لنظام حماية البيانات الشخصية لبيانات العملاء المالية مع مخاطر النقل العابر للحدود",
        ],
        "compliance_requirements_en": [
            "SAMA Open Banking Framework and Cybersecurity Framework",
            "ZATCA Phase 2 e-invoicing mandatory since 2023",
            "PDPL — financial PII classified as sensitive data requiring explicit consent",
        ],
        "vision_2030_programs_en": [
            "Financial Sector Development Program (FSDP)",
            "Fintech Saudi initiative under SAMA",
        ],
        "top_companies_examples": [
            "Al Rajhi Bank",
            "Saudi National Bank",
            "stc pay",
            "Riyad Bank",
        ],
        "dealix_entry_point_en": (
            "CFO intro via ZATCA compliance angle — frame Dealix as a compliance cost "
            "reduction tool before expanding to revenue intelligence."
        ),
    },
    "healthcare": {
        "name_en": "Healthcare, Hospitals & Health Tech",
        "name_ar": "الرعاية الصحية والمستشفيات وتقنية الصحة",
        "market_size_sar_billion": 160,
        "decision_maker_titles_en": [
            "Chief Medical Information Officer",
            "Director of Digital Health",
            "Head of Operations",
            "Chief Financial Officer",
        ],
        "decision_maker_titles_ar": [
            "كبير مسؤولي المعلومات الطبية",
            "مدير الصحة الرقمية",
            "رئيس العمليات",
            "الرئيس التنفيذي للشؤون المالية",
        ],
        "procurement_cycle_en": (
            "MOH-affiliated hospitals follow government tender rules (SAR 500K threshold). "
            "Private hospital groups can procure directly up to SAR 200K per department. "
            "NPHIES integration projects require MOH vendor pre-qualification."
        ),
        "key_pain_points_en": [
            "NPHIES integration complexity delaying revenue collection from insurers",
            "Patient data scattered across disconnected EMR and scheduling systems",
            "Regulatory reporting to MOH consuming clinical staff time weekly",
        ],
        "key_pain_points_ar": [
            "تعقيد تكامل نظام نفيس يُأخر تحصيل الإيرادات من شركات التأمين",
            "بيانات المرضى مبعثرة عبر أنظمة السجلات الطبية الإلكترونية وحجز المواعيد المنفصلة",
            "التقارير التنظيمية لوزارة الصحة تستهلك وقت الكوادر الطبية أسبوعيًا",
        ],
        "compliance_requirements_en": [
            "NPHIES (National Platform for Health Information Exchange) integration",
            "PDPL — health data classified as sensitive requiring heightened protection",
            "ZATCA e-invoicing for insurance reimbursement billing",
        ],
        "vision_2030_programs_en": [
            "Vision 2030 Health Sector Transformation Program",
            "National Telemedicine Initiative",
        ],
        "top_companies_examples": [
            "Dr. Sulaiman Al Habib Medical Group",
            "Saudi German Hospitals",
            "Andalusia Healthcare",
            "Sehhaty (MOH digital platform)",
        ],
        "dealix_entry_point_en": (
            "Head of Digital Health or CMIO via NPHIES compliance and revenue "
            "leakage framing — show insurer reimbursement reconciliation value first."
        ),
    },
    "logistics_supply_chain": {
        "name_en": "Logistics, Freight & Supply Chain",
        "name_ar": "اللوجستيات والشحن وسلسلة التوريد",
        "market_size_sar_billion": 95,
        "decision_maker_titles_en": [
            "Chief Operations Officer",
            "Head of Supply Chain",
            "Director of Fleet Management",
            "Chief Financial Officer",
        ],
        "decision_maker_titles_ar": [
            "الرئيس التنفيذي للعمليات",
            "رئيس سلسلة التوريد",
            "مدير إدارة الأسطول",
            "الرئيس التنفيذي للشؤون المالية",
        ],
        "procurement_cycle_en": (
            "Large 3PL contracts tendered annually; spot logistics purchased directly. "
            "NEOM and giga-project supply contracts follow government procurement rules "
            "with SAR 500K open-tender threshold."
        ),
        "key_pain_points_en": [
            "ZATCA-non-compliant invoices causing payment delays from corporate clients",
            "Lack of real-time revenue visibility across freight legs and depots",
            "Driver and fleet cost overruns eroding contract margins",
        ],
        "key_pain_points_ar": [
            "الفواتير غير المتوافقة مع زكاة تُسبب تأخيرات دفع من العملاء المؤسسيين",
            "غياب الرؤية الآنية للإيرادات عبر مراحل الشحن والمستودعات",
            "تجاوزات تكاليف السائقين والأسطول تُقلص هوامش العقود",
        ],
        "compliance_requirements_en": [
            "ZATCA Phase 2 e-invoicing — high non-compliance fine risk for freight invoices",
            "Nitaqat Saudization requirements for driver and warehouse roles",
            "Transport General Authority (TGA) licensing and route compliance",
        ],
        "vision_2030_programs_en": [
            "National Transport and Logistics Strategy (NTLS)",
            "NEOM and Red Sea Project supply chain development",
        ],
        "top_companies_examples": [
            "Naqel Express",
            "Aramex Saudi Arabia",
            "Saudi Post (SPL)",
            "Almajdouie Logistics",
        ],
        "dealix_entry_point_en": (
            "COO or Head of Supply Chain via ZATCA compliance risk angle — "
            "quantify the fine exposure before presenting revenue analytics."
        ),
    },
    "real_estate": {
        "name_en": "Real Estate, PropTech & Development",
        "name_ar": "العقارات وتقنية العقارات والتطوير",
        "market_size_sar_billion": 280,
        "decision_maker_titles_en": [
            "Chief Executive Officer",
            "Head of Sales and Leasing",
            "Chief Financial Officer",
            "Director of Digital Transformation",
        ],
        "decision_maker_titles_ar": [
            "الرئيس التنفيذي",
            "رئيس المبيعات والتأجير",
            "الرئيس التنفيذي للشؤون المالية",
            "مدير التحول الرقمي",
        ],
        "procurement_cycle_en": (
            "Private developers procure technology directly up to SAR 500K. "
            "ROSHN and quasi-governmental developers follow government tender rules. "
            "Decision cycle typically 45–90 days for CRM or analytics platforms."
        ),
        "key_pain_points_en": [
            "Lost leads after property exhibitions with no systematic follow-up pipeline",
            "Recurring rental revenue difficult to forecast due to fragmented lease data",
            "RERA compliance reporting for off-plan sales consuming management time",
        ],
        "key_pain_points_ar": [
            "فقدان العملاء المحتملين بعد معارض العقارات دون خط متابعة منهجي",
            "صعوبة التنبؤ بإيرادات الإيجار المتكررة بسبب بيانات عقود الإيجار المبعثرة",
            "تقارير الامتثال لهيئة العقار عن المبيعات على الخارطة تستهلك وقت الإدارة",
        ],
        "compliance_requirements_en": [
            "RERA (Real Estate General Authority) off-plan sales disclosure rules",
            "ZATCA e-invoicing for rental and sale transactions",
            "AML/CFT due diligence for high-value property transactions",
        ],
        "vision_2030_programs_en": [
            "ROSHN and Housing Program (increase home ownership to 70%)",
            "Giga-projects: NEOM, Red Sea Project, Diriyah Gate",
        ],
        "top_companies_examples": [
            "ROSHN Group",
            "Dar Al Arkan",
            "Emaar The Economic City",
            "Saudi Real Estate Company",
        ],
        "dealix_entry_point_en": (
            "Head of Sales or CEO via lead conversion and post-exhibition pipeline angle — "
            "show how many leads are lost without systematic follow-up."
        ),
    },
    "retail_ecommerce": {
        "name_en": "Retail, FMCG & E-Commerce",
        "name_ar": "التجزئة والسلع الاستهلاكية سريعة الدوران والتجارة الإلكترونية",
        "market_size_sar_billion": 175,
        "decision_maker_titles_en": [
            "Chief Marketing Officer",
            "Head of E-Commerce",
            "Chief Financial Officer",
            "Director of Customer Experience",
        ],
        "decision_maker_titles_ar": [
            "الرئيس التنفيذي للتسويق",
            "رئيس التجارة الإلكترونية",
            "الرئيس التنفيذي للشؤون المالية",
            "مدير تجربة العملاء",
        ],
        "procurement_cycle_en": (
            "Retail chains procure SaaS tools directly through IT or marketing budget. "
            "Decisions under SAR 100K typically approved at director level within 30 days. "
            "Annual platform contracts negotiated in Q4 for following year budget."
        ),
        "key_pain_points_en": [
            "High cart abandonment and weak repeat purchase rates eroding LTV",
            "Disconnected offline and online customer data making personalization impossible",
            "ZATCA compliance for mixed e-commerce and in-store VAT invoicing",
        ],
        "key_pain_points_ar": [
            "معدل التخلي عن سلة التسوق المرتفع وضعف معدلات الشراء المتكرر يُقلصان القيمة مدى الحياة",
            "انفصال بيانات العملاء عبر القنوات الرقمية والمادية يجعل التخصيص مستحيلًا",
            "الامتثال لزكاة في الفوترة الضريبية المختلطة بين التجارة الإلكترونية والمتاجر الفعلية",
        ],
        "compliance_requirements_en": [
            "ZATCA Phase 2 e-invoicing for all B2C and B2B transactions",
            "PDPL — customer behavioural and purchase data requires consent management",
            "Consumer Protection Authority (CPA) digital commerce regulations",
        ],
        "vision_2030_programs_en": [
            "National E-Commerce Strategy targeting SAR 150B in e-commerce sales",
            "Saudi Export Development Authority (SEDA) cross-border commerce support",
        ],
        "top_companies_examples": [
            "Tamimi Markets",
            "Danube",
            "Noon (Saudi operations)",
            "Extra (eXtra Stores)",
        ],
        "dealix_entry_point_en": (
            "CMO or Head of E-Commerce via customer retention and LTV angle — "
            "present cart abandonment recovery ROI before broader analytics."
        ),
    },
    "government_quasi_gov": {
        "name_en": "Government, Quasi-Governmental & Giga-Projects",
        "name_ar": "الجهات الحكومية وشبه الحكومية والمشاريع العملاقة",
        "market_size_sar_billion": 600,
        "decision_maker_titles_en": [
            "Deputy Minister for Digital Transformation",
            "Chief Digital Officer",
            "Head of Procurement and Contracts",
            "Director of Strategy and Performance",
        ],
        "decision_maker_titles_ar": [
            "نائب الوزير للتحول الرقمي",
            "الرئيس التنفيذي الرقمي",
            "رئيس المشتريات والعقود",
            "مدير الاستراتيجية والأداء",
        ],
        "procurement_cycle_en": (
            "All government spend above SAR 500K requires open tender via Etimad platform. "
            "Aramco and SABIC follow their own procurement portals with SAR 100K direct limit. "
            "Vendor pre-qualification required; decision cycle 90–180 days."
        ),
        "key_pain_points_en": [
            "Manual KPI and performance reporting to oversight bodies consuming analyst time",
            "NCA cybersecurity compliance gaps creating audit exposure",
            "Difficulty demonstrating Vision 2030 program ROI to leadership",
        ],
        "key_pain_points_ar": [
            "تقارير مؤشرات الأداء اليدوية للجهات الرقابية تستهلك وقت المحللين",
            "فجوات الامتثال الأمني للهيئة الوطنية للأمن السيبراني تخلق مخاطر تدقيق",
            "صعوبة إظهار عائد الاستثمار في برامج رؤية 2030 للقيادة",
        ],
        "compliance_requirements_en": [
            "NCA Essential Cybersecurity Controls (ECC) mandatory for all government systems",
            "PDPL — citizen data classified as sensitive with strict processing rules",
            "ZATCA integration mandatory; government entities exempt from VAT but must issue",
        ],
        "vision_2030_programs_en": [
            "Digital Government Authority (DGA) transformation mandate",
            "NEOM, Red Sea Project, Diriyah Gate Authority giga-projects",
        ],
        "top_companies_examples": [
            "Saudi Aramco",
            "SABIC",
            "NEOM Company",
            "Public Investment Fund (PIF) portfolio entities",
        ],
        "dealix_entry_point_en": (
            "Strategy or Digital Transformation office via Vision 2030 KPI reporting angle — "
            "position as a performance intelligence tool tied to national program metrics."
        ),
    },
    "education_edtech": {
        "name_en": "Education, EdTech & Human Capital",
        "name_ar": "التعليم وتقنية التعليم ورأس المال البشري",
        "market_size_sar_billion": 55,
        "decision_maker_titles_en": [
            "Vice Rector for Digital Transformation",
            "Director of Institutional Research",
            "Chief Financial Officer",
            "Head of Student Experience",
        ],
        "decision_maker_titles_ar": [
            "نائب المدير للتحول الرقمي",
            "مدير البحث المؤسسي",
            "الرئيس التنفيذي للشؤون المالية",
            "رئيس تجربة الطلاب",
        ],
        "procurement_cycle_en": (
            "Public universities follow MOE and government tender rules above SAR 500K. "
            "Private universities and EdTech companies procure directly. "
            "Academic year budget cycles set in Q1; decisions typically confirmed before Ramadan."
        ),
        "key_pain_points_en": [
            "High student dropout in online programs undermining revenue and accreditation KPIs",
            "Fragmented student data across LMS, CRM, and finance systems blocking retention analytics",
            "Nitaqat compliance tracking for Saudi faculty ratios consuming HR bandwidth",
        ],
        "key_pain_points_ar": [
            "معدل التسرب المرتفع في برامج التعلم عن بُعد يُقوّض الإيرادات ومؤشرات الاعتماد",
            "بيانات الطلاب المبعثرة عبر نظام إدارة التعلم وإدارة علاقات العملاء والمالية تعيق تحليلات الاستبقاء",
            "تتبع الامتثال لنطاقات نسب أعضاء هيئة التدريس السعوديين يستهلك موارد الموارد البشرية",
        ],
        "compliance_requirements_en": [
            "NCAAA (National Commission for Academic Accreditation) reporting requirements",
            "PDPL — student data including academic records classified as sensitive",
            "Nitaqat Saudization quotas for academic and administrative staff",
        ],
        "vision_2030_programs_en": [
            "Human Capital Development Program (HCDP)",
            "Misk Foundation and national talent development initiatives",
        ],
        "top_companies_examples": [
            "Noon Academy",
            "Edraak (Arab learning platform)",
            "King Abdulaziz University",
            "Saudi Electronic University",
        ],
        "dealix_entry_point_en": (
            "VP of Digital Transformation or Director of Institutional Research via "
            "student retention and accreditation KPI reporting angle."
        ),
    },
    "manufacturing_industrial": {
        "name_en": "Manufacturing, Petrochemicals & Industrial",
        "name_ar": "التصنيع والبتروكيماويات والصناعة",
        "market_size_sar_billion": 220,
        "decision_maker_titles_en": [
            "Chief Operations Officer",
            "Head of Procurement and Supply Chain",
            "Chief Financial Officer",
            "Director of Business Development",
        ],
        "decision_maker_titles_ar": [
            "الرئيس التنفيذي للعمليات",
            "رئيس المشتريات وسلسلة التوريد",
            "الرئيس التنفيذي للشؤون المالية",
            "مدير تطوير الأعمال",
        ],
        "procurement_cycle_en": (
            "Large manufacturers follow internal procurement portals with SAR 100K direct limit. "
            "SABIC supply chain partners follow SABIC vendor management system rules. "
            "Industrial projects require SASO product certification and local content compliance."
        ),
        "key_pain_points_en": [
            "Long B2B sales cycles without a CRM causing deal slippage and revenue uncertainty",
            "Complex ZATCA invoicing for multi-component products and service contracts",
            "Local content (Vision 2030) reporting to IKTVA consuming finance team capacity",
        ],
        "key_pain_points_ar": [
            "دورات مبيعات B2B طويلة دون نظام إدارة علاقات عملاء تُسبب تسرب الصفقات وعدم اليقين بالإيرادات",
            "فوترة زكاة معقدة للمنتجات متعددة المكونات وعقود الخدمة",
            "تقارير المحتوى المحلي لبرنامج إكثار تستهلك طاقة الفريق المالي",
        ],
        "compliance_requirements_en": [
            "ZATCA Phase 2 e-invoicing for all industrial B2B transactions",
            "SASO (Saudi Standards, Metrology and Quality Organization) product standards",
            "IKTVA (In-Kingdom Total Value Add) local content reporting for Aramco supply chain",
        ],
        "vision_2030_programs_en": [
            "National Industrial Development and Logistics Program (NIDLP)",
            "Saudi Vision 2030 local content and IKTVA targets",
        ],
        "top_companies_examples": [
            "SABIC",
            "Saudi Aramco Industrial Services",
            "Ma'aden",
            "Saudi Ceramics",
        ],
        "dealix_entry_point_en": (
            "COO or CFO via ZATCA invoice complexity and local content reporting angle — "
            "frame Dealix as compliance cost reduction before presenting sales analytics."
        ),
    },
}

# ---------------------------------------------------------------------------
# Procurement thresholds
# ---------------------------------------------------------------------------

_PROCUREMENT_THRESHOLDS: dict[str, dict[str, Any]] = {
    "direct_purchase": {
        "threshold_label_en": "Direct Purchase",
        "threshold_label_ar": "الشراء المباشر",
        "max_sar": 100_000,
        "min_sar": 0,
        "description_en": (
            "No tender required. Single-supplier engagement allowed. "
            "Approval typically at department director level."
        ),
        "description_ar": (
            "لا يُشترط طرح عطاء. يُسمح بالتعامل مع مورد واحد. "
            "الموافقة عادةً على مستوى مدير الإدارة."
        ),
        "dealix_implication_en": (
            "Sprint (SAR 499) and Data Pack (SAR 1,500) fall here — "
            "champion can approve without procurement committee involvement. "
            "Keep initial offer under SAR 100K to stay in this zone."
        ),
    },
    "limited_competition": {
        "threshold_label_en": "Limited Competition",
        "threshold_label_ar": "المنافسة المحدودة",
        "max_sar": 500_000,
        "min_sar": 100_001,
        "description_en": (
            "Three or more competitive quotes required. "
            "Procurement committee review needed. Cycle typically 30–60 days."
        ),
        "description_ar": (
            "يُشترط الحصول على ثلاثة عروض تنافسية على الأقل. "
            "يتطلب مراجعة لجنة المشتريات. الدورة عادةً 30–60 يومًا."
        ),
        "dealix_implication_en": (
            "Managed Ops (SAR 2,999–4,999/mo = SAR 36K–60K/yr) may require 3 quotes. "
            "Position proof-of-concept under SAR 100K to bypass this threshold, "
            "then convert to annual retainer once value is demonstrated."
        ),
    },
    "open_tender": {
        "threshold_label_en": "Open Tender",
        "threshold_label_ar": "المناقصة المفتوحة",
        "max_sar": None,
        "min_sar": 500_001,
        "description_en": (
            "Full public or restricted tender process required via Etimad or internal portal. "
            "Vendor pre-qualification needed. Cycle typically 90–180 days. "
            "Decision at VP or C-suite level."
        ),
        "description_ar": (
            "يُشترط إجراء مناقصة عامة أو مقيدة كاملة عبر منصة اعتماد أو البوابة الداخلية. "
            "يُشترط التأهيل المسبق للموردين. الدورة عادةً 90–180 يومًا. "
            "القرار على مستوى نائب الرئيس أو الإدارة العليا."
        ),
        "dealix_implication_en": (
            "Custom AI projects (SAR 5K–25K/mo = SAR 60K–300K/yr) can cross this threshold. "
            "Ensure Etimad pre-registration and ZATCA vendor compliance before submitting bids. "
            "Reference clients and case studies are essential at this level."
        ),
    },
}

# ---------------------------------------------------------------------------
# Pure helpers
# ---------------------------------------------------------------------------


def _sector_or_404(sector_id: str) -> dict[str, Any]:
    profile = _SECTOR_PROFILES.get(sector_id)
    if profile is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error_en": f"Sector '{sector_id}' not found.",
                "error_ar": f"القطاع '{sector_id}' غير موجود.",
                "valid_sector_ids": list(_SECTOR_PROFILES.keys()),
            },
        )
    return profile


def _build_compliance_row(sector_id: str, profile: dict[str, Any]) -> dict[str, Any]:
    reqs = profile["compliance_requirements_en"]
    flags = {
        "zatca": any("ZATCA" in r for r in reqs),
        "sama": any("SAMA" in r for r in reqs),
        "nca": any("NCA" in r for r in reqs),
        "nitaqat": any("Nitaqat" in r for r in reqs),
        "pdpl": any("PDPL" in r for r in reqs),
        "iktva": any("IKTVA" in r for r in reqs),
        "ncaaa": any("NCAAA" in r for r in reqs),
        "rera": any("RERA" in r for r in reqs),
    }
    return {
        "sector_id": sector_id,
        "sector_name_en": profile["name_en"],
        "sector_name_ar": profile["name_ar"],
        **flags,
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/sectors")
async def list_sectors() -> dict[str, Any]:
    """Return summary of all 8 Saudi B2B sectors — name, market size, and entry point."""
    summary = [
        {
            "sector_id": sid,
            "name_en": p["name_en"],
            "name_ar": p["name_ar"],
            "market_size_sar_billion": p["market_size_sar_billion"],
            "dealix_entry_point_en": p["dealix_entry_point_en"],
        }
        for sid, p in _SECTOR_PROFILES.items()
    ]
    return {
        "governance_decision": _GOV_READ,
        "total_sectors": len(summary),
        "sectors": summary,
    }


@router.get("/sectors/{sector_id}")
async def get_sector(sector_id: str) -> dict[str, Any]:
    """Return the full profile for a single sector. 404 if sector_id is unknown."""
    profile = _sector_or_404(sector_id)
    return {
        "governance_decision": _GOV_READ,
        "sector_id": sector_id,
        **profile,
    }


@router.get("/procurement-thresholds")
async def get_procurement_thresholds() -> dict[str, Any]:
    """Return Saudi government and corporate procurement threshold rules."""
    return {
        "governance_decision": _GOV_READ,
        "currency": "SAR",
        "note_en": (
            "Thresholds apply to most Saudi government and quasi-governmental entities. "
            "Private companies may apply different internal limits."
        ),
        "note_ar": (
            "تنطبق الحدود على معظم الجهات الحكومية وشبه الحكومية السعودية. "
            "قد تطبق الشركات الخاصة حدودًا داخلية مختلفة."
        ),
        "thresholds": _PROCUREMENT_THRESHOLDS,
    }


@router.get("/decision-makers/{sector_id}")
async def get_decision_makers(sector_id: str) -> dict[str, Any]:
    """Return decision-maker titles and recommended approach for one sector."""
    profile = _sector_or_404(sector_id)
    return {
        "governance_decision": _GOV_READ,
        "sector_id": sector_id,
        "sector_name_en": profile["name_en"],
        "sector_name_ar": profile["name_ar"],
        "decision_maker_titles_en": profile["decision_maker_titles_en"],
        "decision_maker_titles_ar": profile["decision_maker_titles_ar"],
        "dealix_entry_point_en": profile["dealix_entry_point_en"],
        "procurement_cycle_en": profile["procurement_cycle_en"],
        "note_en": (
            "Titles are typical for mid-to-large Saudi organisations in this sector. "
            "Smaller companies may concentrate these roles in fewer individuals."
        ),
        "note_ar": (
            "المسميات الوظيفية نموذجية للمنظمات السعودية المتوسطة والكبيرة في هذا القطاع. "
            "قد تُجمع الشركات الصغيرة هذه الأدوار في عدد أقل من الأفراد."
        ),
    }


@router.get("/compliance-map")
async def get_compliance_map() -> dict[str, Any]:
    """Return a matrix showing which compliance frameworks apply to each sector."""
    compliance_matrix = [
        _build_compliance_row(sid, profile)
        for sid, profile in _SECTOR_PROFILES.items()
    ]
    frameworks = {
        "zatca": {
            "name_en": "ZATCA Phase 2 e-invoicing",
            "name_ar": "الفوترة الإلكترونية المرحلة الثانية من زكاة",
        },
        "sama": {
            "name_en": "SAMA regulations (banking and FinTech)",
            "name_ar": "لوائح ساما (البنوك والتقنية المالية)",
        },
        "nca": {
            "name_en": "NCA Essential Cybersecurity Controls (ECC)",
            "name_ar": "ضوابط الأمن السيبراني الأساسية للهيئة الوطنية",
        },
        "nitaqat": {
            "name_en": "Nitaqat Saudization Program",
            "name_ar": "برنامج نطاقات للسعودة",
        },
        "pdpl": {
            "name_en": "Personal Data Protection Law (PDPL)",
            "name_ar": "نظام حماية البيانات الشخصية",
        },
        "iktva": {
            "name_en": "IKTVA local content reporting (Aramco supply chain)",
            "name_ar": "تقارير المحتوى المحلي لإكثار (سلسلة توريد أرامكو)",
        },
        "ncaaa": {
            "name_en": "NCAAA accreditation reporting",
            "name_ar": "متطلبات اعتماد الهيئة الوطنية للتقويم والاعتماد الأكاديمي",
        },
        "rera": {
            "name_en": "RERA real estate regulations",
            "name_ar": "لوائح الهيئة العامة للعقار",
        },
    }
    return {
        "governance_decision": _GOV_READ,
        "framework_legend": frameworks,
        "compliance_matrix": compliance_matrix,
        "note_en": (
            "True = compliance framework is explicitly required for this sector. "
            "False = not a primary requirement but may still apply situationally."
        ),
        "note_ar": (
            "صحيح = إطار الامتثال مطلوب صراحةً لهذا القطاع. "
            "خطأ = ليس متطلبًا أساسيًا لكن قد ينطبق في حالات معينة."
        ),
    }
