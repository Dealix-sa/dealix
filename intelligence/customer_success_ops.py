"""Customer Success Operating System.

Success plans, renewal forecasting, expansion signals, and health dashboards.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

from intelligence.bilingual import BilingualRenderer, BilingualText, LanguageCode
from intelligence.ops_adapters import CSScorecard


@dataclass
class SuccessMilestone:
    name: BilingualText
    due_days: int
    completed: bool
    evidence: list[str]

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "name": BilingualRenderer.filter_text(self.name, lang),
            "due_days": self.due_days,
            "completed": self.completed,
            "evidence": self.evidence,
        }


@dataclass
class SuccessPlan:
    plan_id: str
    customer_id: str
    customer_name: str
    goals: list[BilingualText]
    milestones: list[SuccessMilestone]
    health_score: float
    renewal_date: str | None
    expansion_signals: list[str]
    risk_flags: list[str]

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "goals": [BilingualRenderer.filter_text(g, lang) for g in self.goals],
            "milestones": [m.to_dict(lang) for m in self.milestones],
            "health_score": self.health_score,
            "renewal_date": self.renewal_date,
            "expansion_signals": self.expansion_signals,
            "risk_flags": self.risk_flags,
        }


@dataclass
class RenewalForecast:
    customer_id: str
    customer_name: str
    renewal_date: str
    likelihood_percent: float
    risk_factors: list[str]
    recommended_action: BilingualText

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "renewal_date": self.renewal_date,
            "likelihood_percent": self.likelihood_percent,
            "risk_factors": self.risk_factors,
            "recommended_action": BilingualRenderer.filter_text(self.recommended_action, lang),
        }


@dataclass
class ExpansionSignal:
    customer_id: str
    signal_type: Literal["usage_increase", "feature_request", "referral", "upsell_ask"]
    description: BilingualText
    confidence: float
    recommended_action: BilingualText

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "signal_type": self.signal_type,
            "description": BilingualRenderer.filter_text(self.description, lang),
            "confidence": self.confidence,
            "recommended_action": BilingualRenderer.filter_text(self.recommended_action, lang),
        }


class CustomerSuccessOperatingSystem:
    """Customer success operating system for Dealix accounts."""

    def __init__(self) -> None:
        self.scorecard = CSScorecard()
        self._plans: dict[str, SuccessPlan] = {}

    def create_success_plan(
        self,
        customer_id: str,
        customer_name: str,
        goals_en: list[str],
        goals_ar: list[str],
        package_sku: str,
        renewal_date: str | None = None,
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        plan_id = f"csp-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        goals = [BilingualRenderer.bt(en, ar) for en, ar in zip(goals_en, goals_ar)]
        milestones = [
            SuccessMilestone(
                name=BilingualRenderer.bt("Kick-off call completed", "إكمال مكالمة الانطلاق"),
                due_days=3,
                completed=False,
                evidence=[],
            ),
            SuccessMilestone(
                name=BilingualRenderer.bt("First value milestone delivered", "تسليم أول معلم للقيمة"),
                due_days=14,
                completed=False,
                evidence=[],
            ),
            SuccessMilestone(
                name=BilingualRenderer.bt("Proof pack documented", "توثيق حزمة الإثبات"),
                due_days=30,
                completed=False,
                evidence=[],
            ),
            SuccessMilestone(
                name=BilingualRenderer.bt("Renewal/upsell conversation scheduled", "جدولة محادثة التجديد/الترقية"),
                due_days=60,
                completed=False,
                evidence=[],
            ),
        ]
        plan = SuccessPlan(
            plan_id=plan_id,
            customer_id=customer_id,
            customer_name=customer_name,
            goals=goals,
            milestones=milestones,
            health_score=75.0,
            renewal_date=renewal_date,
            expansion_signals=[],
            risk_flags=[],
        )
        self._plans[plan_id] = plan
        return BilingualRenderer.wrap({"success_plan": plan.to_dict(lang)}, lang)

    def get_success_plan(self, plan_id: str, lang: LanguageCode = "both") -> dict[str, Any]:
        plan = self._plans.get(plan_id)
        if not plan:
            raise ValueError(f"Success plan {plan_id} not found")
        return BilingualRenderer.wrap({"success_plan": plan.to_dict(lang)}, lang)

    def update_milestone(
        self,
        plan_id: str,
        milestone_name_en: str,
        completed: bool,
        evidence: list[str] | None = None,
    ) -> dict[str, Any]:
        plan = self._plans.get(plan_id)
        if not plan:
            raise ValueError(f"Success plan {plan_id} not found")
        for m in plan.milestones:
            if m.name.en == milestone_name_en:
                m.completed = completed
                m.evidence = evidence or []
                break
        else:
            raise ValueError(f"Milestone {milestone_name_en} not found")
        return BilingualRenderer.wrap({"success_plan": plan.to_dict()}, "both")

    def health_dashboard(
        self,
        customers: list[dict[str, Any]],
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        score_inputs = [
            {
                "customer_id": c["customer_id"],
                "customer_name": c["customer_name"],
                "last_activity_days": c.get("last_activity_days", 7),
                "deliverables_completed": c.get("deliverables_completed", 0),
                "deliverables_total": c.get("deliverables_total", 1),
                "payments_on_time": c.get("payments_on_time", 0),
                "payments_total": c.get("payments_total", 0),
                "support_tickets_open": c.get("support_tickets_open", 0),
                "nps_score": c.get("nps_score"),
                "expansion_signals": c.get("expansion_signals", []),
            }
            for c in customers
        ]
        scores = self.scorecard.batch_score(score_inputs)
        return BilingualRenderer.wrap(
            {
                "count": len(scores),
                "average_health": round(sum(s.overall_score for s in scores) / max(len(scores), 1), 1),
                "tier_breakdown": self._tier_breakdown(scores),
                "customers": [
                    {
                        "customer_id": s.customer_id,
                        "customer_name": s.customer_name,
                        "overall_score": s.overall_score,
                        "tier": s.tier.value,
                        "engagement_score": s.engagement_score,
                        "delivery_score": s.delivery_score,
                        "payment_score": s.payment_score,
                        "expansion_score": s.expansion_score,
                        "risk_flags": s.risk_flags,
                        "recommended_actions": s.recommended_actions,
                    }
                    for s in scores
                ],
            },
            lang,
        )

    def _tier_breakdown(self, scores: list[Any]) -> dict[str, int]:
        breakdown: dict[str, int] = {}
        for s in scores:
            breakdown[s.tier.value] = breakdown.get(s.tier.value, 0) + 1
        return breakdown

    def forecast_renewals(
        self,
        customers: list[dict[str, Any]],
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        forecasts: list[RenewalForecast] = []
        for c in customers:
            renewal_date = c.get("renewal_date")
            if not renewal_date:
                continue
            health = c.get("health_score", 50)
            likelihood = min(95.0, max(10.0, health * 0.9))
            risk_factors: list[str] = []
            if health < 60:
                risk_factors.append("Health score below 60")
            if c.get("open_tickets", 0) > 3:
                risk_factors.append("High open ticket count")
            action = (
                BilingualRenderer.bt("Schedule executive business review", "جدولة مراجعة أعمال تنفيذية")
                if risk_factors
                else BilingualRenderer.bt("Prepare renewal proposal", "إعداد عرض التجديد")
            )
            forecasts.append(RenewalForecast(
                customer_id=c["customer_id"],
                customer_name=c["customer_name"],
                renewal_date=renewal_date,
                likelihood_percent=round(likelihood, 1),
                risk_factors=risk_factors,
                recommended_action=action,
            ))
        return BilingualRenderer.wrap(
            {"renewal_forecasts": [f.to_dict(lang) for f in forecasts]},
            lang,
        )

    def detect_expansion_signals(
        self,
        customer_id: str,
        usage_data: dict[str, Any],
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        signals: list[ExpansionSignal] = []
        if usage_data.get("usage_growth_percent", 0) > 30:
            signals.append(ExpansionSignal(
                customer_id=customer_id,
                signal_type="usage_increase",
                description=BilingualRenderer.bt("Usage grew over 30% this month", "نما الاستخدام أكثر من 30% هذا الشهر"),
                confidence=0.8,
                recommended_action=BilingualRenderer.bt("Offer premium tier conversation", "عرض محادثة الباقة المميزة"),
            ))
        if usage_data.get("new_feature_requests", 0) >= 2:
            signals.append(ExpansionSignal(
                customer_id=customer_id,
                signal_type="feature_request",
                description=BilingualRenderer.bt("Multiple feature requests indicate expansion need", "طلبات ميزات متعددة تشير إلى حاجة للتوسع"),
                confidence=0.7,
                recommended_action=BilingualRenderer.bt("Scope expansion SOW", "تحديد بيان نطاق التوسع"),
            ))
        if usage_data.get("referrals", 0) > 0:
            signals.append(ExpansionSignal(
                customer_id=customer_id,
                signal_type="referral",
                description=BilingualRenderer.bt("Customer referred another company", "العميل أحال شركة أخرى"),
                confidence=0.9,
                recommended_action=BilingualRenderer.bt("Activate referral program", "تفعيل برنامج الإحالة"),
            ))
        return BilingualRenderer.wrap(
            {"customer_id": customer_id, "expansion_signals": [s.to_dict(lang) for s in signals]},
            lang,
        )

    def customer_brief(
        self,
        customer_id: str,
        customer_data: dict[str, Any],
        lang: LanguageCode = "both",
    ) -> dict[str, Any]:
        score = self.scorecard.score(**customer_data)
        return BilingualRenderer.wrap(
            {
                "customer_id": customer_id,
                "customer_name": score.customer_name,
                "health_score": score.overall_score,
                "tier": score.tier.value,
                "engagement_score": score.engagement_score,
                "delivery_score": score.delivery_score,
                "payment_score": score.payment_score,
                "expansion_score": score.expansion_score,
                "risk_flags": score.risk_flags,
                "recommended_actions": score.recommended_actions,
            },
            lang,
        )
