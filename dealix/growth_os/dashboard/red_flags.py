"""Red-flag detection — the seven patterns that should never go ignored."""

from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from dealix.growth_os.dashboard.metrics import GrowthDashboardSnapshot


class RedFlag(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    severity: str = "warn"  # warn | block
    title_ar: str
    title_en: str
    description_ar: str
    description_en: str
    triggered: bool = False
    evidence: dict[str, float] = Field(default_factory=dict)


RED_FLAG_CATALOG: Final[tuple[RedFlag, ...]] = (
    RedFlag(
        key="no_real_revenue",
        severity="block",
        title_ar="لا يوجد إيراد موثّق",
        title_en="No real revenue",
        description_ar="لم يُسجَّل إيراد موثّق في الفترة",
        description_en="No verified revenue recorded for the period",
    ),
    RedFlag(
        key="pipeline_without_proposals",
        severity="warn",
        title_ar="خط أنابيب بلا عروض",
        title_en="Pipeline without proposals",
        description_ar="قيمة pipeline مرتفعة وعدد العروض المُرسلة منخفض",
        description_en="High pipeline value but few proposals sent",
    ),
    RedFlag(
        key="low_win_rate",
        severity="warn",
        title_ar="معدل فوز منخفض",
        title_en="Low win rate",
        description_ar="معدل فوز أقل من 20%",
        description_en="Win rate below 20%",
    ),
    RedFlag(
        key="margin_collapse",
        severity="block",
        title_ar="انهيار في الهامش",
        title_en="Margin collapse",
        description_ar="متوسط الهامش أقل من 20%",
        description_en="Average margin below 20%",
    ),
    RedFlag(
        key="no_retainer_revenue",
        severity="warn",
        title_ar="لا إيراد متكرر",
        title_en="No retainer revenue",
        description_ar="حصة الـ retainer من الإيراد 0%",
        description_en="Retainer share of revenue is 0%",
    ),
    RedFlag(
        key="vanity_metric_drift",
        severity="block",
        title_ar="انجراف إلى مقاييس فارغة",
        title_en="Vanity-metric drift",
        description_ar="تكررت محاولات احتساب مقاييس فارغة",
        description_en="Repeated attempts to count vanity metrics",
    ),
    RedFlag(
        key="operating_rules_breached",
        severity="block",
        title_ar="انتهاك قواعد التشغيل",
        title_en="Operating rules breached",
        description_ar="تجاوزت انتهاكات قواعد التشغيل العتبة",
        description_en="Operating-rule violations exceeded the threshold",
    ),
)

_CATALOG_BY_KEY: Final[dict[str, RedFlag]] = {f.key: f for f in RED_FLAG_CATALOG}


def _trigger(key: str, evidence: dict[str, float]) -> RedFlag:
    base = _CATALOG_BY_KEY[key]
    return base.model_copy(update={"triggered": True, "evidence": evidence})


def detect_red_flags(snapshot: GrowthDashboardSnapshot) -> list[RedFlag]:
    """Return the list of triggered red flags for the snapshot."""
    flags: list[RedFlag] = []

    if snapshot.real_revenue_usd <= 0:
        flags.append(_trigger("no_real_revenue", {"real_revenue_usd": 0.0}))

    if (
        snapshot.pipeline_value_usd >= 10_000
        and snapshot.proposals_sent <= 1
    ):
        flags.append(
            _trigger(
                "pipeline_without_proposals",
                {
                    "pipeline_value_usd": snapshot.pipeline_value_usd,
                    "proposals_sent": float(snapshot.proposals_sent),
                },
            )
        )

    win_rate = snapshot.win_rate()
    if (snapshot.proposals_won + snapshot.proposals_lost) > 0 and win_rate < 0.20:
        flags.append(_trigger("low_win_rate", {"win_rate": win_rate}))

    if snapshot.avg_margin_pct and snapshot.avg_margin_pct < 0.20:
        flags.append(_trigger("margin_collapse", {"avg_margin_pct": snapshot.avg_margin_pct}))

    if snapshot.real_revenue_usd > 0 and snapshot.retainer_revenue_usd <= 0:
        flags.append(
            _trigger(
                "no_retainer_revenue",
                {"retainer_revenue_usd": snapshot.retainer_revenue_usd},
            )
        )

    if snapshot.vanity_metric_attempts_blocked > 0:
        flags.append(
            _trigger(
                "vanity_metric_drift",
                {
                    "vanity_metric_attempts_blocked": float(
                        snapshot.vanity_metric_attempts_blocked
                    ),
                },
            )
        )

    if snapshot.operating_rule_violations >= 3:
        flags.append(
            _trigger(
                "operating_rules_breached",
                {
                    "operating_rule_violations": float(
                        snapshot.operating_rule_violations
                    ),
                },
            )
        )

    return flags


def catalog() -> list[RedFlag]:
    return list(RED_FLAG_CATALOG)


__all__ = ["RED_FLAG_CATALOG", "RedFlag", "catalog", "detect_red_flags"]
