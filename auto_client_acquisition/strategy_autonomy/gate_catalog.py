"""Strategic gate catalog — codified CEO decision rules as data.

Turns the narrative targets in ``docs/90_DAY_BUSINESS_EXECUTION_PLAN.md``,
the six rules in ``docs/company/DECISION_RULES.md`` and the decision gates
in ``.claude/agents/dealix-pm.md`` into typed, evaluable :class:`GateRule`
rows. The evaluator (``decision_gates``) consumes this catalog.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from auto_client_acquisition.strategy_autonomy.decision_types import (
    StrategicDecisionType,
)


@dataclass(frozen=True, slots=True)
class GateRule:
    """One codified strategic decision gate.

    ``window_day`` is the day-window after launch when the gate becomes
    due (``None`` means always evaluable). ``metric`` names a field on the
    :class:`StrategicSignalSnapshot`. ``comparator`` is one of
    ``gte`` / ``lte`` / ``eq``.
    """

    gate_id: str
    source: str
    title_ar: str
    title_en: str
    window_day: int | None
    metric: str
    comparator: str
    threshold: float
    on_pass: str
    on_fail: str
    severity: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_SCALE = StrategicDecisionType.SCALE.value
_BUILD = StrategicDecisionType.BUILD.value
_HOLD = StrategicDecisionType.HOLD.value
_KILL = StrategicDecisionType.KILL.value
_RAISE_PRICE = StrategicDecisionType.RAISE_PRICE.value
_OFFER_RETAINER = StrategicDecisionType.OFFER_RETAINER.value
_HIRE = StrategicDecisionType.HIRE.value


STRATEGIC_GATE_CATALOG: tuple[GateRule, ...] = (
    # ── 90-day execution plan targets ───────────────────────────────
    GateRule(
        gate_id="g_revenue_day90_build",
        source="docs/90_DAY_BUSINESS_EXECUTION_PLAN.md",
        title_ar="إيراد تراكمي 40 ألف ريال بيوم 90 يفتح موجة البناء",
        title_en="40K SAR cumulative revenue by day 90 unlocks the build wave",
        window_day=90,
        metric="total_revenue_sar",
        comparator="gte",
        threshold=40000.0,
        on_pass=_BUILD,
        on_fail=_HOLD,
        severity="high",
    ),
    GateRule(
        gate_id="g_retainers_day90_build",
        source=".claude/agents/dealix-pm.md",
        title_ar="3 اشتراكات شهرية فعّالة بيوم 90 شرط لموجة البناء",
        title_en="3 active retainers by day 90 gate the build wave",
        window_day=90,
        metric="retainer_count",
        comparator="gte",
        threshold=3.0,
        on_pass=_BUILD,
        on_fail=_HOLD,
        severity="high",
    ),
    GateRule(
        gate_id="g_revenue_day60_hold",
        source=".claude/agents/dealix-pm.md",
        title_ar="إيراد أقل من 25 ألف ريال بيوم 60 يوقف بناء عروض جديدة",
        title_en="Revenue below 25K SAR by day 60 halts new-offer building",
        window_day=60,
        metric="total_revenue_sar",
        comparator="gte",
        threshold=25000.0,
        on_pass=_SCALE,
        on_fail=_HOLD,
        severity="high",
    ),
    GateRule(
        gate_id="g_mrr_day60_retainer",
        source="docs/90_DAY_BUSINESS_EXECUTION_PLAN.md",
        title_ar="وصول الإيراد الشهري المتكرر لـ 6 آلاف ريال يفتح عرض الاشتراك",
        title_en="MRR reaching 6K SAR unlocks the retainer offer",
        window_day=60,
        metric="mrr_sar",
        comparator="gte",
        threshold=5998.0,
        on_pass=_OFFER_RETAINER,
        on_fail=_HOLD,
        severity="medium",
    ),
    # ── founder-time / hiring gate ──────────────────────────────────
    GateRule(
        gate_id="g_founder_hours_hire",
        source=".claude/agents/dealix-pm.md",
        title_ar="وقت المؤسس فوق 5 ساعات لكل سبرنت بعد العميل الخامس يستدعي توظيفاً",
        title_en="Founder time above 5h/sprint after customer 5 triggers a hire",
        window_day=None,
        metric="founder_hours_per_sprint",
        comparator="lte",
        threshold=5.0,
        on_pass=_HOLD,
        on_fail=_HIRE,
        severity="medium",
    ),
    # ── DECISION_RULES.md — readiness / proof / governance ──────────
    GateRule(
        gate_id="g_proof_score_scale",
        source="docs/company/DECISION_RULES.md",
        title_ar="درجة الإثبات 85 أو أعلى تفتح التوسّع — قاعدة عدم البيع قبل الجاهزية",
        title_en="Proof score >= 85 unlocks scale — do not sell before ready",
        window_day=30,
        metric="proof_score",
        comparator="gte",
        threshold=85.0,
        on_pass=_SCALE,
        on_fail=_HOLD,
        severity="high",
    ),
    GateRule(
        gate_id="g_governance_risk_hold",
        source="docs/company/DECISION_RULES.md",
        title_ar="مؤشر مخاطر الحوكمة فوق 50 يوقف أي قرار توسّع",
        title_en="Governance risk index above 50 halts any scale decision",
        window_day=None,
        metric="governance_risk_index",
        comparator="lte",
        threshold=50.0,
        on_pass=_SCALE,
        on_fail=_HOLD,
        severity="high",
    ),
    GateRule(
        gate_id="g_repeatability_raise_price",
        source="docs/company/DECISION_RULES.md",
        title_ar="تكرار التسليم 3 مرات أو أكثر يفتح اختبار رفع السعر",
        title_en="Delivery repeated 3+ times unlocks a price-raise test",
        window_day=60,
        metric="retainer_count",
        comparator="gte",
        threshold=3.0,
        on_pass=_RAISE_PRICE,
        on_fail=_HOLD,
        severity="medium",
    ),
    GateRule(
        gate_id="g_kill_no_traction_day60",
        source="docs/company/DECISION_RULES.md",
        title_ar="صفر عميل دافع بيوم 60 يطرح إيقاف العرض الحالي للمراجعة",
        title_en="Zero paid customers by day 60 surfaces an offer-kill review",
        window_day=60,
        metric="paid_customers",
        comparator="gte",
        threshold=1.0,
        on_pass=_HOLD,
        on_fail=_KILL,
        severity="high",
    ),
)


def get_gate(gate_id: str) -> GateRule | None:
    """Return a gate rule by id, or None if not in the catalog."""
    for gate in STRATEGIC_GATE_CATALOG:
        if gate.gate_id == gate_id:
            return gate
    return None


def list_gates() -> tuple[GateRule, ...]:
    """Return the full strategic gate catalog."""
    return STRATEGIC_GATE_CATALOG


__all__ = [
    "STRATEGIC_GATE_CATALOG",
    "GateRule",
    "get_gate",
    "list_gates",
]
