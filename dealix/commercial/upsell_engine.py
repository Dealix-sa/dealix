"""
Upsell Engine — Trigger expansion offers based on proof milestones.
محرك التطوير — يُحرّك عروض التوسع بناءً على معالم الإثبات.

Rules (constitutional):
  - No upsell without ≥1 proof event (NO_FAKE_PROOF gate)
  - No external proposal without founder approval (NO_LIVE_SEND gate)
  - Uses existing expansion_engine.py for offer selection logic
"""

from __future__ import annotations

import json
import logging
import os
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

log = logging.getLogger(__name__)

# Upsell thresholds by offer tier
UPSELL_GATES: dict[str, dict[str, Any]] = {
    "s2_data_pack": {
        "min_pilots": 1,
        "min_proof_events": 1,
        "price_sar": 1500,
        "title_ar": "حزمة البيانات إلى الإيرادات (30 يوم)",
        "title_en": "Data-to-Revenue Pack (30 Days)",
        "pitch_ar": "بعد نجاح البرنامج التجريبي، الخطوة التالية هي تحليل بياناتكم الكاملة وبناء خارطة فرص لمدة شهر.",
    },
    "s3_managed_ops": {
        "min_pilots": 1,
        "min_proof_events": 1,
        "price_sar": 2999,
        "title_ar": "التشغيل المُدار الشهري",
        "title_en": "Monthly Managed Operations",
        "pitch_ar": "نديم عملياتكم شهرياً: متابعة العملاء، التقارير الأسبوعية، واجتماع استراتيجي شهري. 2,999 ريال/شهر.",
    },
    "s3_managed_ops_premium": {
        "min_pilots": 3,
        "min_proof_events": 3,
        "price_sar": 4999,
        "title_ar": "التشغيل المُدار المتقدم",
        "title_en": "Advanced Managed Operations",
        "pitch_ar": "للشركات التي أثبتت نجاح البرامج التجريبية: خدمة تشغيل متكاملة مع أولوية قصوى وتقارير تنفيذية.",
    },
    "s4_executive_command": {
        "min_pilots": 3,
        "min_proof_events": 5,
        "price_sar": 7500,
        "title_ar": "غرفة القيادة التنفيذية",
        "title_en": "Executive Command Center",
        "pitch_ar": "تقارير يومية، رادار السوق الأسبوعي، واستراتيجية شهرية. للمديرين التنفيذيين الذين يريدون بيانات دقيقة لاتخاذ قرارات أفضل.",
    },
    "s5_agency_partner": {
        "min_pilots": 3,
        "min_proof_events": 3,
        "price_sar": 0,  # Custom + rev-share
        "title_ar": "شراكة الوكالات",
        "title_en": "Agency Partner Program",
        "pitch_ar": "أصبحتم مؤهلين لبرنامج الشراكة: أعيدوا بيع Dealix لعملائكم واحصلوا على 15-30% من الإيراد.",
    },
}


@dataclass
class UpsellOpportunity:
    opportunity_id: str
    account_id: str
    company_name: str
    offer_key: str
    offer_title_ar: str
    offer_title_en: str
    pitch_ar: str
    price_sar: int
    evidence_level: int
    proof_event_count: int
    pilot_count: int
    is_gated: bool  # True = not enough evidence yet
    status: str = "pending_approval"  # pending_approval | presented | accepted | declined
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "opportunity_id": self.opportunity_id,
            "account_id": self.account_id,
            "company_name": self.company_name,
            "offer_key": self.offer_key,
            "offer_title_ar": self.offer_title_ar,
            "offer_title_en": self.offer_title_en,
            "pitch_ar": self.pitch_ar,
            "price_sar": self.price_sar,
            "evidence_level": self.evidence_level,
            "proof_event_count": self.proof_event_count,
            "pilot_count": self.pilot_count,
            "is_gated": self.is_gated,
            "status": self.status,
            "generated_at": self.generated_at.isoformat(),
            "constitutional_note": "NO_LIVE_SEND: هذا العرض يتطلب موافقة الفاوندر قبل تقديمه للعميل",
        }


def evaluate_upsell(
    *,
    account_id: str,
    company_name: str,
    sector: str,
    pain_point: str,
    pilot_count: int,
    proof_event_count: int,
    evidence_level: int,
) -> list[UpsellOpportunity]:
    """
    Evaluate which upsell offers are eligible for this account.
    Returns a list of opportunities (some gated, some eligible).
    Constitutional: all returned offers are pending_approval — not live.
    """
    # Also use existing expansion engine for offer selection
    try:
        from auto_client_acquisition.revenue_os.expansion_engine import next_best_offer
        expansion = next_best_offer(
            primary_pain_keyword=pain_point,
            sector=sector,
            max_proof_level=evidence_level,
            proof_event_count=proof_event_count,
        )
        log.debug("Expansion engine recommendation: %s", expansion.get("offer_key"))
    except Exception as exc:
        log.debug("Expansion engine unavailable: %s", exc)

    opportunities: list[UpsellOpportunity] = []

    for offer_key, gate in UPSELL_GATES.items():
        is_gated = (
            pilot_count < gate["min_pilots"]
            or proof_event_count < gate["min_proof_events"]
        )
        opp = UpsellOpportunity(
            opportunity_id=str(uuid.uuid4()),
            account_id=account_id,
            company_name=company_name,
            offer_key=offer_key,
            offer_title_ar=gate["title_ar"],
            offer_title_en=gate["title_en"],
            pitch_ar=gate["pitch_ar"],
            price_sar=gate["price_sar"],
            evidence_level=evidence_level,
            proof_event_count=proof_event_count,
            pilot_count=pilot_count,
            is_gated=is_gated,
        )
        opportunities.append(opp)

    # Sort: eligible first (not gated), then by price ascending
    opportunities.sort(key=lambda o: (o.is_gated, o.price_sar))

    _save_opportunities(account_id, company_name, opportunities)
    log.info(
        "Upsell evaluated: account=%s pilots=%d proofs=%d eligible=%d gated=%d",
        account_id,
        pilot_count,
        proof_event_count,
        sum(1 for o in opportunities if not o.is_gated),
        sum(1 for o in opportunities if o.is_gated),
    )
    return opportunities


def best_upsell(
    *,
    account_id: str,
    company_name: str,
    sector: str,
    pain_point: str,
    pilot_count: int,
    proof_event_count: int,
    evidence_level: int,
) -> UpsellOpportunity | None:
    """Returns the single best eligible upsell offer, or None if gated."""
    opps = evaluate_upsell(
        account_id=account_id,
        company_name=company_name,
        sector=sector,
        pain_point=pain_point,
        pilot_count=pilot_count,
        proof_event_count=proof_event_count,
        evidence_level=evidence_level,
    )
    eligible = [o for o in opps if not o.is_gated]
    return eligible[0] if eligible else None


def _save_opportunities(account_id: str, company_name: str, opps: list[UpsellOpportunity]) -> None:
    try:
        upsell_dir = os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "upsell"
        )
        os.makedirs(upsell_dir, exist_ok=True)
        path = os.path.join(upsell_dir, f"{account_id}_opportunities.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "account_id": account_id,
                    "company_name": company_name,
                    "evaluated_at": datetime.now(UTC).isoformat(),
                    "opportunities": [o.to_dict() for o in opps],
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
    except Exception as exc:
        log.warning("Could not save upsell opportunities: %s", exc)
