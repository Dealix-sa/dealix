"""Sales Operating System.

Pipeline playbooks, deal reviews, battlecards, forecasting, and sales coaching.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Literal

from intelligence.bilingual import BilingualBlock, BilingualRenderer, BilingualText, LanguageCode
from intelligence.negotiation_engine import NegotiationEngine
from intelligence.ops_adapters import BattlecardsAdapter, ForecastingAdapter, validate_sku
from intelligence.revenue_intelligence import Deal, RevenueIntelligenceEngine


@dataclass
class PipelineScript:
    stage: str
    actions: list[BilingualText]
    required_evidence: list[str]
    exit_criteria: list[str]
    max_days_in_stage: int

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "stage": self.stage,
            "actions": [BilingualRenderer.filter_text(a, lang) for a in self.actions],
            "required_evidence": self.required_evidence,
            "exit_criteria": self.exit_criteria,
            "max_days_in_stage": self.max_days_in_stage,
        }


@dataclass
class CoachingInsight:
    area: Literal["discovery", "objection_handling", "closing", "qualification"]
    insight: BilingualText
    recommended_action: BilingualText
    priority: Literal["high", "medium", "low"]

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "area": self.area,
            "insight": BilingualRenderer.filter_text(self.insight, lang),
            "recommended_action": BilingualRenderer.filter_text(self.recommended_action, lang),
            "priority": self.priority,
        }


@dataclass
class DealReview:
    deal_id: str
    company_name: str
    stage: str
    health_score: float
    risk_flags: list[str]
    coaching_insights: list[CoachingInsight]
    next_best_action: BilingualText
    battlecard: dict[str, Any] | None

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "deal_id": self.deal_id,
            "company_name": self.company_name,
            "stage": self.stage,
            "health_score": self.health_score,
            "risk_flags": self.risk_flags,
            "coaching_insights": [c.to_dict(lang) for c in self.coaching_insights],
            "next_best_action": BilingualRenderer.filter_text(self.next_best_action, lang),
            "battlecard": self.battlecard,
        }


class SalesOperatingSystem:
    """End-to-end sales operating system for Dealix."""

    STAGE_NAMES = [
        "lead",
        "qualified",
        "diagnostic_scheduled",
        "proposal_sent",
        "pilot_negotiation",
        "contract_sent",
        "closed_won",
        "closed_lost",
    ]

    def __init__(self) -> None:
        self.negotiation = NegotiationEngine()
        self.battlecards = BattlecardsAdapter()
        self.forecasting = ForecastingAdapter()

    def get_pipeline_playbook(self, lang: LanguageCode = "both") -> dict[str, Any]:
        scripts = [
            PipelineScript(
                stage="lead",
                actions=[
                    BilingualRenderer.bt("Score ICP and enrich company signals", "تقييم ICP وإثراء إشارات الشركة"),
                    BilingualRenderer.bt("Prioritize top 20 by score", "ترتيز أعلى 20 حسب التقييم"),
                ],
                required_evidence=["icp_score", "sector_momentum"],
                exit_criteria=["ICP score >= 50", "City and sector validated"],
                max_days_in_stage=3,
            ),
            PipelineScript(
                stage="qualified",
                actions=[
                    BilingualRenderer.bt("Run discovery call using bilingual script", "إجراء مكالمة استكشاف باستخدام سكريبت ثنائي اللغة"),
                    BilingualRenderer.bt("Document pain, budget, authority, timeline", "توثيق الألم والميزانية والسلطة والجدول الزمني"),
                ],
                required_evidence=["discovery_notes", "stakeholder_map"],
                exit_criteria=["BANT confirmed", "Decision maker identified"],
                max_days_in_stage=7,
            ),
            PipelineScript(
                stage="diagnostic_scheduled",
                actions=[
                    BilingualRenderer.bt("Prepare diagnostic agenda and data requests", "إعداد جدول التشخيص وطلبات البيانات"),
                    BilingualRenderer.bt("Confirm attendance of decision makers", "تأكيد حضور صناع القرار"),
                ],
                required_evidence=["diagnostic_agenda", "attendee_list"],
                exit_criteria=["Diagnostic completed", "Leakage points documented"],
                max_days_in_stage=5,
            ),
            PipelineScript(
                stage="proposal_sent",
                actions=[
                    BilingualRenderer.bt("Schedule proposal review call", "جدولة مكالمة مراجعة العرض"),
                    BilingualRenderer.bt("Prepare objection playbook for price/timing/trust", "إعداد دليل الاعتراضات للسعر/التوقيت/الثقة"),
                ],
                required_evidence=["proposal_sent_timestamp", "proposal_opened"],
                exit_criteria=["Proposal reviewed", "Feedback received"],
                max_days_in_stage=7,
            ),
            PipelineScript(
                stage="pilot_negotiation",
                actions=[
                    BilingualRenderer.bt("Define pilot success metrics", "تحديد مؤشرات نجاح البرنامج التجريبي"),
                    BilingualRenderer.bt("Get SOW and payment approval", "الحصول على الموافقة على بيان نطاق العمل والدفع"),
                ],
                required_evidence=["pilot_sow", "success_metrics"],
                exit_criteria=["Pilot SOW signed", "Payment link sent/confirmed"],
                max_days_in_stage=10,
            ),
            PipelineScript(
                stage="contract_sent",
                actions=[
                    BilingualRenderer.bt("Follow up on contract review", "المتابعة على مراجعة العقد"),
                    BilingualRenderer.bt("Prepare implementation kickoff", "التحضير لانطلاق التنفيذ"),
                ],
                required_evidence=["contract_sent_timestamp", "legal_feedback"],
                exit_criteria=["Contract signed", "Kickoff scheduled"],
                max_days_in_stage=14,
            ),
        ]
        return BilingualRenderer.wrap(
            {"playbook": [s.to_dict(lang) for s in scripts]},
            lang,
        )

    def review_deal(
        self,
        deal: dict[str, Any],
        competitor: str | None = None,
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        deal_id = deal.get("deal_id", "unknown")
        company_name = deal.get("company_name", "unknown")
        stage = deal.get("stage", "lead")
        value_sar = deal.get("value_sar", 0)
        days_in_stage = deal.get("days_in_stage", 0)
        activities_count = deal.get("activities_count", 0)

        health = self._deal_health(stage, days_in_stage, activities_count)
        risk_flags: list[str] = []
        if days_in_stage > 14:
            risk_flags.append(f"Stale: {days_in_stage} days in {stage}")
        if activities_count == 0:
            risk_flags.append("No recorded activity")
        if stage in ("proposal_sent", "pilot_negotiation") and value_sar > 50000:
            risk_flags.append("High-value deal needs executive sponsor")

        insights: list[CoachingInsight] = []
        if stage == "lead":
            insights.append(CoachingInsight(
                area="qualification",
                insight=BilingualRenderer.bt("No discovery completed yet", "لم يكتمل الاستكشاف بعد"),
                recommended_action=BilingualRenderer.bt("Schedule discovery call within 48h", "جدولة مكالمة استكشاف خلال 48 ساعة"),
                priority="high",
            ))
        if stage == "proposal_sent":
            insights.append(CoachingInsight(
                area="closing",
                insight=BilingualRenderer.bt("Proposal sent but no follow-up scheduled", "تم إرسال العرض لكن لا توجد متابعة مجدولة"),
                recommended_action=BilingualRenderer.bt("Book review call and prepare objection playbook", "حجز مكالمة مراجعة وإعداد دليل الاعتراضات"),
                priority="high",
            ))
        if not risk_flags:
            insights.append(CoachingInsight(
                area="discovery",
                insight=BilingualRenderer.bt("Deal is on track", "الصفقة على المسار الصحيح"),
                recommended_action=BilingualRenderer.bt("Advance to next stage", "التقدم إلى المرحلة التالية"),
                priority="low",
            ))

        next_action = BilingualRenderer.bt(
            f"Next: {insights[0].recommended_action.en if insights else 'Continue regular cadence'}",
            f"التالي: {insights[0].recommended_action.ar if insights else 'استمرار الإيقاع المنتظم'}",
        )

        battlecard = None
        if competitor:
            card = self.battlecards.get(competitor)
            battlecard = self.battlecards.to_dict(card)

        review = DealReview(
            deal_id=deal_id,
            company_name=company_name,
            stage=stage,
            health_score=health,
            risk_flags=risk_flags,
            coaching_insights=insights,
            next_best_action=next_action,
            battlecard=battlecard,
        )
        return BilingualRenderer.wrap({"deal_review": review.to_dict(lang)}, lang)

    def _deal_health(self, stage: str, days_in_stage: int, activities_count: int) -> float:
        base = {"lead": 20, "qualified": 40, "diagnostic_scheduled": 55, "proposal_sent": 65, "pilot_negotiation": 75, "contract_sent": 85, "closed_won": 100, "closed_lost": 0}.get(stage, 20)
        if days_in_stage <= 3:
            base += 10
        elif days_in_stage <= 7:
            base += 5
        elif days_in_stage > 14:
            base -= 15
        if activities_count >= 3:
            base += 10
        elif activities_count >= 1:
            base += 5
        return max(0.0, min(100.0, base))

    def batch_review(
        self,
        deals: list[dict[str, Any]],
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        reviews = [self.review_deal(d, lang=lang)["deal_review"] for d in deals]
        return BilingualRenderer.wrap({"reviews": reviews}, lang)

    def coaching_brief(
        self,
        deals: list[dict[str, Any]],
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        insights: list[CoachingInsight] = []
        if not deals:
            insights.append(CoachingInsight(
                area="qualification",
                insight=BilingualRenderer.bt("No active deals to coach", "لا توجد صفقات نشطة للتوجيه"),
                recommended_action=BilingualRenderer.bt("Generate leads first", "توليد العملاء المحتملين أولاً"),
                priority="high",
            ))
        else:
            stale_count = sum(1 for d in deals if d.get("days_in_stage", 0) > 14)
            if stale_count > 0:
                insights.append(CoachingInsight(
                    area="closing",
                    insight=BilingualRenderer.bt(f"{stale_count} deals are stale", f"{stale_count} صفقات راكدة"),
                    recommended_action=BilingualRenderer.bt("Re-activate or close stale deals", "إعادة تفعيل أو إغلاق الصفقات الراكدة"),
                    priority="high",
                ))
            proposal_count = sum(1 for d in deals if d.get("stage") == "proposal_sent")
            if proposal_count > 0:
                insights.append(CoachingInsight(
                    area="objection_handling",
                    insight=BilingualRenderer.bt(f"{proposal_count} proposals awaiting follow-up", f"{proposal_count} عرض في انتظار المتابعة"),
                    recommended_action=BilingualRenderer.bt("Schedule review calls and prepare objections", "جدولة مكالمات مراجعة وإعداد اعتراضات"),
                    priority="medium",
                ))
        return BilingualRenderer.wrap({"insights": [i.to_dict(lang) for i in insights]}, lang)

    def weekly_sales_brief(
        self,
        deals: list[dict[str, Any]],
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        engine = RevenueIntelligenceEngine()
        deal_objs = [
            Deal(
                deal_id=d.get("deal_id", f"deal-{i}"),
                company_name=d.get("company_name", "unknown"),
                stage=d.get("stage", "lead"),
                value_sar=d.get("value_sar", 0),
                created_at=datetime.fromisoformat(d["created_at"]) if "created_at" in d else datetime.now(timezone.utc),
                last_activity_at=datetime.fromisoformat(d["last_activity_at"]) if "last_activity_at" in d else datetime.now(timezone.utc),
                activities_count=d.get("activities_count", 0),
                days_in_stage=d.get("days_in_stage", 0),
            )
            for i, d in enumerate(deals)
        ]
        engine.load_deals(deal_objs)
        intel = engine.analyze()
        forecast = self.forecasting.forecast(deal_objs, period_days=90)
        return BilingualRenderer.wrap(
            {
                "week_of": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "pipeline_health": intel.pipeline_health,
                "total_pipeline_sar": intel.total_pipeline_sar,
                "weighted_pipeline_sar": intel.weighted_pipeline_sar,
                "revenue_at_risk_sar": intel.revenue_at_risk_sar,
                "recommended_actions": intel.recommended_actions,
                "forecast": self.forecasting.to_dict(forecast),
                "coaching": self.coaching_brief(deals, lang)["insights"],
            },
            lang,
        )

    def battlecard_for(self, competitor_key: str, lang: LanguageCode = "both") -> dict[str, Any]:
        card = self.battlecards.get(competitor_key)
        return BilingualRenderer.wrap(
            {"competitor": competitor_key, "battlecard": self.battlecards.to_dict(card)},
            lang,
        )
