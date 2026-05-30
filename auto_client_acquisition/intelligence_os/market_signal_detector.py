"""Market Signal Detector — timing-based targeting for Saudi B2B.

Detects budget cycles, trigger events, and competitive signals to
score timing quality of a prospect engagement.
Saudi fiscal year and seasonal patterns are baked in.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class SignalType(StrEnum):
    BUDGET_CYCLE = "budget_cycle"       # Fiscal year budget windows
    TRIGGER_EVENT = "trigger_event"     # Company trigger (hiring, launch, etc.)
    COMPETITIVE = "competitive"         # Competitor vulnerability
    PAIN_ACUTE = "pain_acute"          # Pain recently expressed
    GROWTH_SIGNAL = "growth_signal"    # Company growing fast
    REGULATORY = "regulatory"          # Regulatory change driving urgency


class SaudiFiscalQuarter(StrEnum):
    Q1 = "Q1"   # Jan-Mar
    Q2 = "Q2"   # Apr-Jun (includes Ramadan variability)
    Q3 = "Q3"   # Jul-Sep (summer slowdown)
    Q4 = "Q4"   # Oct-Dec (peak budget allocation)


# Saudi B2B budget calendar — month → (quarter, score, Arabic note)
_SAUDI_BUDGET_WINDOWS: dict[int, tuple[str, int, str]] = {
    1:  ("Q1", 80,  "ميزانيات جديدة مُعتمدة — شهر التحرك"),
    2:  ("Q1", 85,  "إنفاق مبكر على الأولويات — ذروة Q1"),
    3:  ("Q1", 75,  "نهاية Q1 — اتجاه لإغلاق قبل رمضان"),
    4:  ("Q2", 60,  "رمضان المحتمل — قرارات أبطأ"),
    5:  ("Q2", 55,  "ما بعد رمضان — استئناف تدريجي"),
    6:  ("Q2", 70,  "مراجعة منتصف السنة — فرصة جيدة"),
    7:  ("Q3", 45,  "إجازة صيف — قرارات أبطأ"),
    8:  ("Q3", 40,  "ذروة الصيف — أبطأ شهر في السنة"),
    9:  ("Q3", 65,  "عودة بعد الصيف — طاقة وميزانية جديدة"),
    10: ("Q4", 90,  "موسم تخصيص الميزانيات — الأفضل للتواصل"),
    11: ("Q4", 95,  "ذروة إغلاق العقود — أعلى نقطة في السنة"),
    12: ("Q4", 85,  "نهاية السنة — تصفية ميزانيات متبقية"),
}


@dataclass(frozen=True, slots=True)
class MarketSignal:
    """A detected market timing signal."""

    signal_type: SignalType
    strength: int           # 0-100
    trigger_ar: str
    trigger_en: str
    recommended_action_ar: str
    recommended_action_en: str


@dataclass(frozen=True, slots=True)
class TimingScore:
    """Composite timing assessment for a prospect engagement."""

    overall: int                        # 0-100 composite
    budget_cycle_score: int             # 0-100
    trigger_event_score: int            # 0-100
    competitive_pressure_score: int     # 0-100
    fiscal_quarter: SaudiFiscalQuarter
    signals: tuple[MarketSignal, ...]
    timing_verdict_ar: str
    timing_verdict_en: str
    optimal_window_ar: str
    optimal_window_en: str


def _budget_signal(month: int) -> MarketSignal:
    quarter_str, score, note_ar = _SAUDI_BUDGET_WINDOWS.get(month, ("Q2", 60, ""))
    action_ar = (
        "تواصل الآن — موسم الميزانيات مفتوح" if score >= 80
        else ("انتظر قليلاً — الوقت معقول" if score >= 60 else "تأجّل حتى Q4 أو Q1")
    )
    action_en = (
        "Engage now — budget season is open" if score >= 80
        else ("Timing is reasonable" if score >= 60 else "Defer to Q4 or Q1")
    )
    return MarketSignal(
        signal_type=SignalType.BUDGET_CYCLE,
        strength=score,
        trigger_ar=note_ar,
        trigger_en=f"{quarter_str} budget window (month {month})",
        recommended_action_ar=action_ar,
        recommended_action_en=action_en,
    )


def detect_signals(
    account_info: dict[str, Any],
    *,
    current_month: int | None = None,
) -> list[MarketSignal]:
    """Detect market timing signals from account information.

    Args:
        account_info: Dict with optional keys:
            recent_hire (bool), funding_round (bool), pain_expressed_recently (bool),
            competitor_used (bool), regulatory_pressure (bool), growth_rate_pct (int).
        current_month: Override current month (1-12) for testing.

    Returns:
        List of MarketSignal sorted by strength descending.
    """
    month = current_month or datetime.date.today().month
    signals: list[MarketSignal] = [_budget_signal(month)]

    if account_info.get("recent_hire"):
        signals.append(MarketSignal(
            signal_type=SignalType.TRIGGER_EVENT,
            strength=85,
            trigger_ar="توظيف حديث — المؤسسة تنمو وتحتاج أنظمة جديدة",
            trigger_en="Recent hiring — company is growing and needs new systems",
            recommended_action_ar="تواصل خلال أسبوعين — النمو يولّد احتياجاً",
            recommended_action_en="Engage within 2 weeks — growth creates need",
        ))

    if account_info.get("funding_round"):
        signals.append(MarketSignal(
            signal_type=SignalType.GROWTH_SIGNAL,
            strength=90,
            trigger_ar="جولة تمويل حديثة — ميزانية متاحة وتوقعات عالية",
            trigger_en="Recent funding round — budget available, high expectations",
            recommended_action_ar="تواصل فوراً — الميزانية متاحة والحاجة ملحّة",
            recommended_action_en="Engage immediately — budget available and need is urgent",
        ))

    if account_info.get("pain_expressed_recently"):
        signals.append(MarketSignal(
            signal_type=SignalType.PAIN_ACUTE,
            strength=95,
            trigger_ar="الألم معبَّر عنه حديثاً — الاستعداد للشراء عالٍ",
            trigger_en="Pain expressed recently — purchase readiness is high",
            recommended_action_ar="تواصل اليوم — اللحظة الأمثل للتحويل",
            recommended_action_en="Engage today — optimal conversion moment",
        ))

    if account_info.get("competitor_used"):
        signals.append(MarketSignal(
            signal_type=SignalType.COMPETITIVE,
            strength=70,
            trigger_ar="يستخدم منافساً — يمكن مقارنة ميزة الإثبات",
            trigger_en="Using a competitor — can compare proof advantage",
            recommended_action_ar="قدّم مقارنة مباشرة مع دليل ملموس",
            recommended_action_en="Present a direct comparison with tangible proof",
        ))

    if account_info.get("regulatory_pressure"):
        signals.append(MarketSignal(
            signal_type=SignalType.REGULATORY,
            strength=80,
            trigger_ar="ضغط تنظيمي (نظام PDPL / NCA) — يحتاج حلاً سريعاً",
            trigger_en="Regulatory pressure (PDPL/NCA) — needs quick solution",
            recommended_action_ar="عرض الحل التوافقي المدمج — ميزة تنافسية مباشرة",
            recommended_action_en="Offer embedded compliance solution — direct competitive advantage",
        ))

    growth_rate = int(account_info.get("growth_rate_pct", 0))
    if growth_rate >= 20:
        signals.append(MarketSignal(
            signal_type=SignalType.GROWTH_SIGNAL,
            strength=min(100, 60 + growth_rate),
            trigger_ar=f"نمو {growth_rate}% — احتياجات جديدة تتسارع",
            trigger_en=f"{growth_rate}% growth — new needs accelerating",
            recommended_action_ar="تواصل بعرض يدعم التوسع والنمو",
            recommended_action_en="Engage with a growth-supporting offer",
        ))

    return sorted(signals, key=lambda s: s.strength, reverse=True)


def score_timing(
    signals: list[MarketSignal],
    *,
    current_month: int | None = None,
) -> TimingScore:
    """Compute composite timing score from detected signals.

    Weights: 40% budget cycle, 40% trigger events, 20% competitive pressure.
    """
    month = current_month or datetime.date.today().month
    quarter_str, _, _ = _SAUDI_BUDGET_WINDOWS.get(month, ("Q2", 60, ""))
    fiscal_quarter = SaudiFiscalQuarter(quarter_str)

    if not signals:
        return TimingScore(
            overall=30,
            budget_cycle_score=30,
            trigger_event_score=0,
            competitive_pressure_score=0,
            fiscal_quarter=fiscal_quarter,
            signals=(),
            timing_verdict_ar="لا إشارات واضحة — استمر بمتابعة دورية",
            timing_verdict_en="No clear signals — continue periodic follow-up",
            optimal_window_ar="Q4 (أكتوبر-ديسمبر) — موسم الميزانيات",
            optimal_window_en="Q4 (October-December) — budget season",
        )

    budget_score = next(
        (s.strength for s in signals if s.signal_type == SignalType.BUDGET_CYCLE), 50
    )
    trigger_score = max(
        (s.strength for s in signals if s.signal_type in (
            SignalType.TRIGGER_EVENT, SignalType.PAIN_ACUTE, SignalType.GROWTH_SIGNAL
        )),
        default=0,
    )
    competitive_score = max(
        (s.strength for s in signals if s.signal_type in (
            SignalType.COMPETITIVE, SignalType.REGULATORY
        )),
        default=0,
    )

    overall = int(budget_score * 0.4 + trigger_score * 0.4 + competitive_score * 0.2)

    if overall >= 80:
        verdict_ar = "وقت مثالي — تحرّك الآن فوراً"
        verdict_en = "Optimal timing — move now immediately"
    elif overall >= 60:
        verdict_ar = "وقت جيد — تواصل هذا الأسبوع"
        verdict_en = "Good timing — engage this week"
    elif overall >= 40:
        verdict_ar = "وقت معقول — ابدأ المحادثة"
        verdict_en = "Reasonable timing — start the conversation"
    else:
        verdict_ar = "توقيت ضعيف — ارعَ حتى Q4 أو حين يظهر trigger"
        verdict_en = "Weak timing — nurture until Q4 or a trigger appears"

    return TimingScore(
        overall=overall,
        budget_cycle_score=budget_score,
        trigger_event_score=trigger_score,
        competitive_pressure_score=competitive_score,
        fiscal_quarter=fiscal_quarter,
        signals=tuple(signals),
        timing_verdict_ar=verdict_ar,
        timing_verdict_en=verdict_en,
        optimal_window_ar="Q4 (أكتوبر-ديسمبر) — ذروة إغلاق الميزانيات",
        optimal_window_en="Q4 (October-December) — peak budget close season",
    )


__all__ = [
    "MarketSignal",
    "SaudiFiscalQuarter",
    "SignalType",
    "TimingScore",
    "detect_signals",
    "score_timing",
]
