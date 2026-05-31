"""Churn Prevention Operations — risk scoring and intervention management.

Endpoints:
  GET  /api/v1/churn-prevention/dashboard         — churn risk overview
  GET  /api/v1/churn-prevention/at-risk            — critical + high risk clients
  GET  /api/v1/churn-prevention/signals-analysis   — aggregate signal analysis
  GET  /api/v1/churn-prevention/{client_id}        — single client full detail
  POST /api/v1/churn-prevention/{client_id}/log-intervention  — log an intervention
  POST /api/v1/churn-prevention/{client_id}/send-proof-pack   — trigger proof pack delivery

All endpoints:
  - Require admin auth (X-Admin-API-Key)
  - Return governance_decision field
  - Bilingual ar/en labels
  - Mutating actions: APPROVAL_FIRST
  - Read-only actions: ALLOW_WITH_REVIEW
"""

from __future__ import annotations

import uuid
from collections import Counter
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from core.logging import get_logger

_log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/churn-prevention",
    tags=["churn-prevention-ops"],
    dependencies=[Depends(require_admin_key)],
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_GOV_READ = "ALLOW_WITH_REVIEW"
_GOV_MUTATE = "APPROVAL_FIRST"

VALID_INTERVENTION_TYPES = frozenset({
    "executive_checkin",
    "proof_pack_delivery",
    "contract_review",
    "discount_offer",
    "feature_demo",
    "escalation",
})

VALID_OUTCOMES = frozenset({"positive", "neutral", "negative"})

VALID_DELIVERY_CHANNELS = frozenset({"email", "in_person"})

# Churn risk weight factors
_WEIGHT_HEALTH_SCORE = 0.30       # inverse: lower health = higher risk
_WEIGHT_DAYS_SINCE_CHECKIN = 0.10
_WEIGHT_MISSED_CHECKINS = 0.20
_WEIGHT_NPS_SCORE = 0.20          # inverse: lower NPS = higher risk
_WEIGHT_CONTRACT_DAYS = 0.20      # inverse: fewer days remaining = higher risk

# Risk band thresholds
_BAND_CRITICAL_MIN = 70
_BAND_HIGH_MIN = 50
_BAND_MEDIUM_MIN = 30

# ---------------------------------------------------------------------------
# Demo at-risk clients (ARC-001 through ARC-007)
# Distribution: 2 critical, 2 high, 2 medium, 1 low
# ---------------------------------------------------------------------------

_CLIENTS: dict[str, dict[str, Any]] = {
    "ARC-001": {
        "client_id": "ARC-001",
        "company_ar": "شركة الخدمات اللوجستية السريعة",
        "company_en": "Rapid Logistics Services Co.",
        "tier": "enterprise",
        "health_score": 18,
        "days_since_last_checkin": 65,
        "consecutive_missed_checkins": 4,
        "nps_score": 2,
        "contract_days_remaining": 12,
        "monthly_value_sar": 4_999,
        "churn_signals": [
            "Health score critically low",
            "No contact in over 60 days",
            "Four consecutive missed checkins",
            "NPS at minimum threshold",
            "Contract expiring in under two weeks",
        ],
        "last_contact_ar": "منذ 65 يوماً",
        "last_contact_en": "65 days ago",
    },
    "ARC-002": {
        "client_id": "ARC-002",
        "company_ar": "مجموعة التصنيع الصناعي المتقدم",
        "company_en": "Advanced Industrial Manufacturing Group",
        "tier": "professional",
        "health_score": 22,
        "days_since_last_checkin": 48,
        "consecutive_missed_checkins": 3,
        "nps_score": 3,
        "contract_days_remaining": 18,
        "monthly_value_sar": 3_999,
        "churn_signals": [
            "Health score below critical threshold",
            "Engagement dropped sharply over last 30 days",
            "Three consecutive missed checkins",
            "NPS score trending downward",
            "Contract renewal not yet confirmed",
        ],
        "last_contact_ar": "منذ 48 يوماً",
        "last_contact_en": "48 days ago",
    },
    "ARC-003": {
        "client_id": "ARC-003",
        "company_ar": "شركة التجزئة الرقمية الموحدة",
        "company_en": "Unified Digital Retail Co.",
        "tier": "professional",
        "health_score": 40,
        "days_since_last_checkin": 32,
        "consecutive_missed_checkins": 2,
        "nps_score": 5,
        "contract_days_remaining": 35,
        "monthly_value_sar": 3_999,
        "churn_signals": [
            "Health score in lower range",
            "Two consecutive missed checkins",
            "NPS score below satisfaction benchmark",
            "Limited engagement with delivered outputs",
        ],
        "last_contact_ar": "منذ 32 يوماً",
        "last_contact_en": "32 days ago",
    },
    "ARC-004": {
        "client_id": "ARC-004",
        "company_ar": "أكاديمية التطوير المهني",
        "company_en": "Professional Development Academy",
        "tier": "essential",
        "health_score": 48,
        "days_since_last_checkin": 28,
        "consecutive_missed_checkins": 2,
        "nps_score": 6,
        "contract_days_remaining": 42,
        "monthly_value_sar": 2_999,
        "churn_signals": [
            "Health score slightly below average",
            "Two missed checkins in current cycle",
            "Feature adoption lower than expected",
        ],
        "last_contact_ar": "منذ 28 يوماً",
        "last_contact_en": "28 days ago",
    },
    "ARC-005": {
        "client_id": "ARC-005",
        "company_ar": "شركة الرعاية الصحية المتكاملة",
        "company_en": "Integrated Healthcare Co.",
        "tier": "enterprise",
        "health_score": 55,
        "days_since_last_checkin": 20,
        "consecutive_missed_checkins": 1,
        "nps_score": 6,
        "contract_days_remaining": 55,
        "monthly_value_sar": 4_999,
        "churn_signals": [
            "One missed checkin this period",
            "Below-average NPS relative to sector",
        ],
        "last_contact_ar": "منذ 20 يوماً",
        "last_contact_en": "20 days ago",
    },
    "ARC-006": {
        "client_id": "ARC-006",
        "company_ar": "مجموعة الخدمات المالية الإقليمية",
        "company_en": "Regional Financial Services Group",
        "tier": "professional",
        "health_score": 62,
        "days_since_last_checkin": 14,
        "consecutive_missed_checkins": 1,
        "nps_score": 7,
        "contract_days_remaining": 60,
        "monthly_value_sar": 3_999,
        "churn_signals": [
            "One missed checkin this period",
            "Contract renewal conversation not initiated",
        ],
        "last_contact_ar": "منذ 14 يوماً",
        "last_contact_en": "14 days ago",
    },
    "ARC-007": {
        "client_id": "ARC-007",
        "company_ar": "شركة التقنية والابتكار السعودية",
        "company_en": "Saudi Technology and Innovation Co.",
        "tier": "enterprise",
        "health_score": 82,
        "days_since_last_checkin": 7,
        "consecutive_missed_checkins": 0,
        "nps_score": 9,
        "contract_days_remaining": 180,
        "monthly_value_sar": 4_999,
        "churn_signals": [
            "Minor delay in last deliverable review",
        ],
        "last_contact_ar": "منذ 7 أيام",
        "last_contact_en": "7 days ago",
    },
}

# In-memory intervention log
_INTERVENTIONS: list[dict[str, Any]] = []

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now_iso() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.now(UTC).isoformat()


def _compute_risk_score(client: dict[str, Any]) -> tuple[float, str]:
    """Compute churn risk score (0-100) and risk band from client factors.

    Higher score means higher churn risk. Factors:
      - health_score (inverse, 30% weight): lower health drives higher risk.
      - days_since_last_checkin (10% weight): capped at 90 days.
      - consecutive_missed_checkins (20% weight): capped at 5.
      - nps_score (inverse, 20% weight): scale 1-10, inverted.
      - contract_days_remaining (inverse, 20% weight): capped at 180 days.

    Returns (score, band) where band is one of:
      'critical' (>=70), 'high' (50-69), 'medium' (30-49), 'low' (<30).
    """
    health = float(client.get("health_score", 50))
    days_checkin = float(client.get("days_since_last_checkin", 0))
    missed = float(client.get("consecutive_missed_checkins", 0))
    nps = float(client.get("nps_score", 5))
    contract_days = float(client.get("contract_days_remaining", 90))

    # Normalise each factor to 0-100 contribution range
    # health_score inverse: 0 health = 100 risk, 100 health = 0 risk
    health_risk = (100.0 - health)

    # days_since_last_checkin: 0 days = 0 risk, 90+ days = 100 risk
    checkin_risk = min(days_checkin / 90.0, 1.0) * 100.0

    # consecutive_missed_checkins: 0 = 0 risk, 5+ = 100 risk
    missed_risk = min(missed / 5.0, 1.0) * 100.0

    # nps_score inverse: scale 1-10; nps=1 = 100 risk, nps=10 = 0 risk
    nps_risk = ((10.0 - nps) / 9.0) * 100.0

    # contract_days_remaining inverse: 0 days = 100 risk, 180+ days = 0 risk
    contract_risk = (1.0 - min(contract_days / 180.0, 1.0)) * 100.0

    score = (
        health_risk * _WEIGHT_HEALTH_SCORE
        + checkin_risk * _WEIGHT_DAYS_SINCE_CHECKIN
        + missed_risk * _WEIGHT_MISSED_CHECKINS
        + nps_risk * _WEIGHT_NPS_SCORE
        + contract_risk * _WEIGHT_CONTRACT_DAYS
    )
    score = round(min(max(score, 0.0), 100.0), 2)

    if score >= _BAND_CRITICAL_MIN:
        band = "critical"
    elif score >= _BAND_HIGH_MIN:
        band = "high"
    elif score >= _BAND_MEDIUM_MIN:
        band = "medium"
    else:
        band = "low"

    return score, band


def _client_or_404(client_id: str) -> dict[str, Any]:
    """Return client record or raise HTTP 404."""
    record = _CLIENTS.get(client_id.upper())
    if record is None:
        raise HTTPException(
            status_code=404,
            detail={
                "ar": f"العميل '{client_id}' غير موجود",
                "en": f"Client '{client_id}' not found",
            },
        )
    return record


def _enrich_client(record: dict[str, Any]) -> dict[str, Any]:
    """Return client dict with computed risk_score and risk_band appended."""
    score, band = _compute_risk_score(record)
    return {**record, "risk_score": score, "risk_band": band}


def _intervention_label(intervention_type: str) -> tuple[str, str]:
    """Return (label_ar, label_en) for an intervention type."""
    labels: dict[str, tuple[str, str]] = {
        "executive_checkin": ("متابعة تنفيذية", "Executive Check-in"),
        "proof_pack_delivery": ("تسليم Proof Pack", "Proof Pack Delivery"),
        "contract_review": ("مراجعة العقد", "Contract Review"),
        "discount_offer": ("عرض خصم", "Discount Offer"),
        "feature_demo": ("عرض توضيحي للميزات", "Feature Demo"),
        "escalation": ("تصعيد", "Escalation"),
    }
    return labels.get(intervention_type, (intervention_type, intervention_type))


# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------


class LogInterventionBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intervention_type: str = Field(
        description=(
            "One of: executive_checkin, proof_pack_delivery, contract_review, "
            "discount_offer, feature_demo, escalation"
        ),
    )
    notes: str = Field(min_length=10, max_length=2000)
    outcome: str = Field(
        description="One of: positive, neutral, negative",
    )
    next_review_days: int = Field(ge=1, le=90)


class SendProofPackBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    notes: str = Field(min_length=5, max_length=2000)
    delivery_channel: str = Field(
        description="One of: email, in_person. WhatsApp is not permitted.",
    )


# ---------------------------------------------------------------------------
# Endpoints — fixed paths first, then parameterised
# ---------------------------------------------------------------------------


@router.get("/dashboard")
async def get_dashboard() -> dict[str, Any]:
    """Churn risk overview across all monitored clients."""
    enriched = [_enrich_client(r) for r in _CLIENTS.values()]
    enriched.sort(key=lambda c: c["risk_score"], reverse=True)

    total = len(enriched)
    critical_count = sum(1 for c in enriched if c["risk_band"] == "critical")
    high_count = sum(1 for c in enriched if c["risk_band"] == "high")
    medium_count = sum(1 for c in enriched if c["risk_band"] == "medium")
    low_count = sum(1 for c in enriched if c["risk_band"] == "low")

    at_risk_mrr = sum(
        c["monthly_value_sar"]
        for c in enriched
        if c["risk_band"] in ("critical", "high")
    )
    avg_risk = round(sum(c["risk_score"] for c in enriched) / total, 2) if total else 0.0

    _log.info("churn_dashboard_fetched", total_monitored=total, critical=critical_count)

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "total_monitored": total,
        "critical_count": critical_count,
        "high_count": high_count,
        "medium_count": medium_count,
        "low_count": low_count,
        "total_at_risk_mrr_sar": at_risk_mrr,
        "avg_risk_score": avg_risk,
        "action_ar": "راجع العملاء ذوي المخاطر العالية وابدأ التدخل الفوري",
        "action_en": "Review high-risk clients and initiate immediate intervention",
        "clients": enriched,
    }


@router.get("/at-risk")
async def get_at_risk_clients(
    risk_band: str | None = Query(default=None, description="Filter by risk_band: critical or high"),
) -> dict[str, Any]:
    """Critical and high risk clients with recommended interventions."""
    at_risk = [
        _enrich_client(r)
        for r in _CLIENTS.values()
        if _compute_risk_score(r)[1] in ("critical", "high")
    ]
    at_risk.sort(key=lambda c: c["risk_score"], reverse=True)

    if risk_band is not None:
        at_risk = [c for c in at_risk if c["risk_band"] == risk_band]

    for client in at_risk:
        if client["risk_band"] == "critical":
            client["recommended_intervention_ar"] = (
                "اتصال تنفيذي عاجل — إشراك المؤسس خلال 24 ساعة"
            )
            client["recommended_intervention_en"] = (
                "Urgent executive check-in — founder engagement within 24 hours"
            )
        else:
            client["recommended_intervention_ar"] = (
                "تسليم Proof Pack محدّث — إثبات القيمة المحققة خلال 48 ساعة"
            )
            client["recommended_intervention_en"] = (
                "Deliver updated Proof Pack — demonstrate achieved value within 48 hours"
            )

    _log.info("churn_at_risk_fetched", count=len(at_risk), filter_band=risk_band)

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "total_at_risk": len(at_risk),
        "clients": at_risk,
    }


@router.get("/signals-analysis")
async def get_signals_analysis() -> dict[str, Any]:
    """Aggregate analysis of churn signals across all monitored clients."""
    all_signals: list[str] = []
    tier_counts: dict[str, int] = {}

    for record in _CLIENTS.values():
        score, band = _compute_risk_score(record)
        all_signals.extend(record.get("churn_signals", []))
        tier = record.get("tier", "unknown")
        tier_counts[tier] = tier_counts.get(tier, 0) + 1

    signal_freq = dict(Counter(all_signals).most_common())
    most_common = max(signal_freq, key=lambda k: signal_freq[k]) if signal_freq else ""

    # At-risk by tier: only clients in critical or high band
    at_risk_by_tier: dict[str, int] = {}
    for record in _CLIENTS.values():
        _, band = _compute_risk_score(record)
        if band in ("critical", "high"):
            tier = record.get("tier", "unknown")
            at_risk_by_tier[tier] = at_risk_by_tier.get(tier, 0) + 1

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "signal_frequency": signal_freq,
        "most_common_signal": most_common,
        "at_risk_by_tier": at_risk_by_tier,
        "recommendations_ar": [
            "أعط الأولوية للعملاء الذين لم يتم التواصل معهم منذ أكثر من 30 يوماً",
            "أرسل Proof Pack محدّثاً للعملاء ذوي درجة NPS المنخفضة",
            "ابدأ محادثات تجديد العقد مبكراً للعملاء المنتهية عقودهم قريباً",
            "نفّذ متابعات تنفيذية للعملاء ذوي درجات الصحة المنخفضة",
        ],
        "recommendations_en": [
            "Prioritise clients with no contact in over 30 days",
            "Send updated Proof Pack to clients with low NPS scores",
            "Start contract renewal conversations early for clients with expiring contracts",
            "Execute executive check-ins for clients with low health scores",
        ],
    }


@router.get("/{client_id}")
async def get_client_detail(client_id: str) -> dict[str, Any]:
    """Full churn risk detail for a single client."""
    record = _client_or_404(client_id)
    score, band = _compute_risk_score(record)

    client_interventions = [
        i for i in _INTERVENTIONS if i.get("client_id") == record["client_id"]
    ]

    if band == "critical":
        recommended_actions = [
            {
                "ar": "اتصال تنفيذي عاجل خلال 24 ساعة",
                "en": "Urgent executive check-in within 24 hours",
            },
            {
                "ar": "تقديم Proof Pack مخصص يُظهر القيمة المحققة",
                "en": "Deliver a tailored Proof Pack demonstrating achieved value",
            },
            {
                "ar": "بدء محادثة تجديد العقد مع العرض التشويقي",
                "en": "Initiate contract renewal conversation with retention offer",
            },
        ]
    elif band == "high":
        recommended_actions = [
            {
                "ar": "تسليم Proof Pack محدّث خلال 48 ساعة",
                "en": "Deliver updated Proof Pack within 48 hours",
            },
            {
                "ar": "جدولة مراجعة شهرية عاجلة",
                "en": "Schedule an urgent monthly review",
            },
            {
                "ar": "إجراء تقييم لرضا العميل ومعالجة المخاوف المباشرة",
                "en": "Conduct client satisfaction assessment and address direct concerns",
            },
        ]
    elif band == "medium":
        recommended_actions = [
            {
                "ar": "تواصل استباقي وعرض عرض توضيحي للميزات الجديدة",
                "en": "Proactive outreach with feature demo for new capabilities",
            },
            {
                "ar": "مراجعة تقدم الأهداف المتفق عليها",
                "en": "Review progress against agreed objectives",
            },
            {
                "ar": "مشاركة تقرير القيمة الشهري للتعزيز",
                "en": "Share monthly value report to reinforce delivered outcomes",
            },
        ]
    else:
        recommended_actions = [
            {
                "ar": "المتابعة الدورية وفقاً للجدول المعتاد",
                "en": "Continue periodic follow-up on standard schedule",
            },
            {
                "ar": "استكشاف فرص التوسع والترقية",
                "en": "Explore expansion and upgrade opportunities",
            },
            {
                "ar": "طلب مرجع أو إحالة استناداً إلى الرضا المرتفع",
                "en": "Request reference or referral based on high satisfaction",
            },
        ]

    _log.info(
        "churn_client_detail_fetched",
        client_id=record["client_id"],
        risk_score=score,
        risk_band=band,
    )

    return {
        "governance_decision": _GOV_READ,
        "generated_at": _now_iso(),
        "client_id": record["client_id"],
        "company_ar": record["company_ar"],
        "company_en": record["company_en"],
        "tier": record["tier"],
        "health_score": record["health_score"],
        "days_since_last_checkin": record["days_since_last_checkin"],
        "consecutive_missed_checkins": record["consecutive_missed_checkins"],
        "nps_score": record["nps_score"],
        "contract_days_remaining": record["contract_days_remaining"],
        "monthly_value_sar": record["monthly_value_sar"],
        "churn_signals": record["churn_signals"],
        "last_contact_ar": record["last_contact_ar"],
        "last_contact_en": record["last_contact_en"],
        "risk_score": score,
        "risk_band": band,
        "intervention_history": client_interventions,
        "recommended_actions": recommended_actions,
    }


@router.post("/{client_id}/log-intervention")
async def log_intervention(
    client_id: str, body: LogInterventionBody
) -> dict[str, Any]:
    """Log a churn prevention intervention for a client. Requires APPROVAL_FIRST."""
    record = _client_or_404(client_id)

    if body.intervention_type not in VALID_INTERVENTION_TYPES:
        raise HTTPException(
            status_code=422,
            detail={
                "ar": f"نوع التدخل '{body.intervention_type}' غير صالح",
                "en": f"Invalid intervention_type '{body.intervention_type}'",
                "valid_types": sorted(VALID_INTERVENTION_TYPES),
            },
        )

    if body.outcome not in VALID_OUTCOMES:
        raise HTTPException(
            status_code=422,
            detail={
                "ar": f"النتيجة '{body.outcome}' غير صالحة",
                "en": f"Invalid outcome '{body.outcome}'",
                "valid_outcomes": sorted(VALID_OUTCOMES),
            },
        )

    score, band = _compute_risk_score(record)
    intervention_id = f"CPO-{uuid.uuid4().hex[:8].upper()}"
    timestamp = _now_iso()

    type_label_ar, type_label_en = _intervention_label(body.intervention_type)

    intervention_record = {
        "id": intervention_id,
        "client_id": record["client_id"],
        "intervention_type": body.intervention_type,
        "notes": body.notes,
        "outcome": body.outcome,
        "next_review_days": body.next_review_days,
        "risk_score_at_intervention": score,
        "risk_band_at_intervention": band,
        "logged_at": timestamp,
    }
    _INTERVENTIONS.append(intervention_record)

    if body.outcome == "negative":
        guidance_ar = "النتيجة سلبية — يُوصى بتصعيد فوري إلى المستوى التنفيذي"
        guidance_en = "Negative outcome — immediate escalation to executive level recommended"
    elif body.outcome == "neutral":
        guidance_ar = "النتيجة محايدة — تابع خلال المدة المحددة وراجع العوامل"
        guidance_en = "Neutral outcome — follow up within specified period and review factors"
    else:
        guidance_ar = "النتيجة إيجابية — واصل المتابعة وفق الجدول المتفق عليه"
        guidance_en = "Positive outcome — continue follow-up on agreed schedule"

    _log.info(
        "churn_intervention_logged",
        intervention_id=intervention_id,
        client_id=record["client_id"],
        intervention_type=body.intervention_type,
        outcome=body.outcome,
    )

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": timestamp,
        "status": "intervention_logged_pending_approval",
        "intervention_id": intervention_id,
        "client_id": record["client_id"],
        "company_ar": record["company_ar"],
        "company_en": record["company_en"],
        "intervention_type": body.intervention_type,
        "intervention_type_label_ar": type_label_ar,
        "intervention_type_label_en": type_label_en,
        "outcome": body.outcome,
        "next_review_days": body.next_review_days,
        "risk_score_at_intervention": score,
        "risk_band_at_intervention": band,
        "updated_risk_guidance_ar": guidance_ar,
        "updated_risk_guidance_en": guidance_en,
        "message_ar": "التدخل مُسجَّل — يحتاج موافقة المدير قبل الجدولة الرسمية",
        "message_en": "Intervention logged — requires manager approval before official scheduling",
    }


@router.post("/{client_id}/send-proof-pack")
async def send_proof_pack(
    client_id: str, body: SendProofPackBody
) -> dict[str, Any]:
    """Trigger proof pack delivery to an at-risk client. Requires APPROVAL_FIRST.

    WhatsApp is explicitly blocked as a delivery channel in compliance with
    the no-unsolicited-outreach doctrine.
    """
    record = _client_or_404(client_id)

    if body.delivery_channel == "whatsapp":
        raise HTTPException(
            status_code=400,
            detail={
                "ar": "واتساب محظور كقناة تسليم — يُخالف سياسة التواصل غير المرغوب فيه",
                "en": (
                    "WhatsApp is not permitted as a delivery channel — "
                    "doctrine: no unsolicited outreach via messaging apps"
                ),
                "doctrine_note": "no_cold_whatsapp",
                "allowed_channels": sorted(VALID_DELIVERY_CHANNELS),
            },
        )

    if body.delivery_channel not in VALID_DELIVERY_CHANNELS:
        raise HTTPException(
            status_code=422,
            detail={
                "ar": f"قناة التسليم '{body.delivery_channel}' غير صالحة",
                "en": f"Invalid delivery_channel '{body.delivery_channel}'",
                "allowed_channels": sorted(VALID_DELIVERY_CHANNELS),
            },
        )

    score, band = _compute_risk_score(record)
    delivery_id = f"PPD-{uuid.uuid4().hex[:8].upper()}"
    timestamp = _now_iso()

    channel_label_ar = "البريد الإلكتروني" if body.delivery_channel == "email" else "لقاء شخصي"
    channel_label_en = "Email" if body.delivery_channel == "email" else "In Person"

    _log.info(
        "churn_proof_pack_queued",
        delivery_id=delivery_id,
        client_id=record["client_id"],
        delivery_channel=body.delivery_channel,
        risk_band=band,
    )

    return {
        "governance_decision": _GOV_MUTATE,
        "generated_at": timestamp,
        "status": "proof_pack_delivery_queued_pending_approval",
        "delivery_id": delivery_id,
        "client_id": record["client_id"],
        "company_ar": record["company_ar"],
        "company_en": record["company_en"],
        "delivery_channel": body.delivery_channel,
        "delivery_channel_label_ar": channel_label_ar,
        "delivery_channel_label_en": channel_label_en,
        "notes": body.notes,
        "risk_score": score,
        "risk_band": band,
        "message_ar": (
            f"تسليم Proof Pack مُصفَّف عبر {channel_label_ar} — "
            "يحتاج موافقة المدير قبل الإرسال"
        ),
        "message_en": (
            f"Proof Pack delivery queued via {channel_label_en} — "
            "requires manager approval before sending"
        ),
    }
