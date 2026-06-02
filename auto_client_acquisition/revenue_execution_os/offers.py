"""Canonical commercial offer ladder for the Revenue Execution OS.

Single source of truth for the five-rung ladder (plus the slow-track
enterprise rung). Prices mirror the doctrine in ``.claude/agents/dealix-pm.md``
and must not be invented elsewhere.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Offer:
    """A single rung on the commercial ladder.

    All amounts are in SAR. ``one_time_*`` is the setup / one-off range;
    ``monthly_*`` is the recurring range (0 when the rung is one-off only).
    """

    rung: int
    key: str
    name_ar: str
    name_en: str
    one_time_min: float
    one_time_max: float
    monthly_min: float
    monthly_max: float
    purpose_ar: str
    purpose_en: str

    @property
    def recurring(self) -> bool:
        return self.monthly_max > 0

    def to_dict(self) -> dict[str, object]:
        return {
            "rung": self.rung,
            "key": self.key,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "one_time_min": self.one_time_min,
            "one_time_max": self.one_time_max,
            "monthly_min": self.monthly_min,
            "monthly_max": self.monthly_max,
            "recurring": self.recurring,
            "price_label_ar": price_label(self, "ar"),
            "price_label_en": price_label(self, "en"),
            "purpose_ar": self.purpose_ar,
            "purpose_en": self.purpose_en,
        }


# Rung 99 is the slow-track enterprise offer (kept off the main 0-4 ladder).
ENTERPRISE_RUNG = 99

OFFER_LADDER: tuple[Offer, ...] = (
    Offer(
        rung=0,
        key="free_diagnostic",
        name_ar="تشخيص عمليات الذكاء الاصطناعي المجاني",
        name_en="Free AI Ops Diagnostic",
        one_time_min=0,
        one_time_max=0,
        monthly_min=0,
        monthly_max=0,
        purpose_ar="دخول سريع وبناء الثقة قبل أي التزام مالي",
        purpose_en="Fast, no-cost entry that builds trust before any commitment",
    ),
    Offer(
        rung=1,
        key="revenue_sprint",
        name_ar="سبرنت ذكاء الإيراد (٧ أيام)",
        name_en="7-Day Revenue Intelligence Sprint",
        one_time_min=499,
        one_time_max=499,
        monthly_min=0,
        monthly_max=0,
        purpose_ar="أول التزام مدفوع صغير يثبت القيمة بسرعة",
        purpose_en="First small paid commitment that proves value quickly",
    ),
    Offer(
        rung=2,
        key="data_revenue_pack",
        name_ar="حزمة البيانات إلى الإيراد",
        name_en="Data-to-Revenue Pack",
        one_time_min=1500,
        one_time_max=1500,
        monthly_min=0,
        monthly_max=0,
        purpose_ar="تحويل بيانات العميل إلى قوائم وأولويات قابلة للتنفيذ",
        purpose_en="Turn the customer's data into actionable lists and priorities",
    ),
    Offer(
        rung=3,
        key="managed_revenue_ops",
        name_ar="عمليات الإيراد المُدارة",
        name_en="Managed Revenue Ops",
        one_time_min=0,
        one_time_max=0,
        monthly_min=2999,
        monthly_max=4999,
        purpose_ar="تشغيل وتحسين مستمر — أساس الإيراد المتكرر",
        purpose_en="Ongoing run + optimize — the recurring-revenue core",
    ),
    Offer(
        rung=4,
        key="custom_ai_setup",
        name_ar="إعداد خدمة ذكاء اصطناعي مخصّصة",
        name_en="Custom AI Service Setup",
        one_time_min=5000,
        one_time_max=25000,
        monthly_min=1000,
        monthly_max=1000,
        purpose_ar="نظام مخصّص لعميل لديه عمليات فعلية",
        purpose_en="A bespoke system for a customer with real operations",
    ),
    Offer(
        rung=ENTERPRISE_RUNG,
        key="ai_governance_review",
        name_ar="مراجعة حوكمة الذكاء الاصطناعي (مسار بطيء)",
        name_en="AI Governance Review (slow track)",
        one_time_min=25000,
        one_time_max=50000,
        monthly_min=0,
        monthly_max=0,
        purpose_ar="مراجعة مؤسسية للجهات الأكبر — مسار بطيء",
        purpose_en="Institutional review for larger entities — slow track",
    ),
)

_BY_KEY: dict[str, Offer] = {o.key: o for o in OFFER_LADDER}
_BY_RUNG: dict[int, Offer] = {o.rung: o for o in OFFER_LADDER}

LADDER_KEYS: tuple[str, ...] = tuple(o.key for o in OFFER_LADDER)


def _fmt(amount: float) -> str:
    # All ladder amounts are whole SAR figures; format with thousands separator.
    return f"{amount:,.0f}"


def price_label(offer: Offer, lang: str = "ar") -> str:
    """Human-readable price label in SAR for the given language."""
    unit = "ريال" if lang == "ar" else "SAR"
    per_month = "/شهر" if lang == "ar" else "/mo"
    if offer.one_time_max == 0 and offer.monthly_max == 0:
        return "مجاني" if lang == "ar" else "Free"
    parts: list[str] = []
    if offer.one_time_max > 0:
        if offer.one_time_min == offer.one_time_max:
            parts.append(f"{_fmt(offer.one_time_min)} {unit}")
        else:
            parts.append(f"{_fmt(offer.one_time_min)}–{_fmt(offer.one_time_max)} {unit}")
    if offer.monthly_max > 0:
        if offer.monthly_min == offer.monthly_max:
            parts.append(f"{_fmt(offer.monthly_min)} {unit}{per_month}")
        else:
            parts.append(f"{_fmt(offer.monthly_min)}–{_fmt(offer.monthly_max)} {unit}{per_month}")
    return " + ".join(parts)


def offer_by_key(key: str) -> Offer:
    """Return the offer for ``key`` or raise ``KeyError``."""
    return _BY_KEY[key]


def offer_for_rung(rung: int) -> Offer:
    """Return the offer for ``rung`` or raise ``KeyError``."""
    return _BY_RUNG[rung]


def next_offer(key: str) -> Offer | None:
    """The next rung up the ladder (renewal/upsell path), or ``None`` at the top.

    The enterprise rung (99) is a slow-track terminal — it has no next rung.
    """
    current = _BY_KEY.get(key)
    if current is None or current.rung == ENTERPRISE_RUNG:
        return None
    higher = sorted(
        (o for o in OFFER_LADDER if 0 <= o.rung < ENTERPRISE_RUNG and o.rung > current.rung),
        key=lambda o: o.rung,
    )
    return higher[0] if higher else _BY_RUNG.get(ENTERPRISE_RUNG)


def ladder_as_dicts() -> list[dict[str, object]]:
    """Serializable view of the full ladder (for API / reports)."""
    return [o.to_dict() for o in OFFER_LADDER]


__all__ = [
    "ENTERPRISE_RUNG",
    "LADDER_KEYS",
    "OFFER_LADDER",
    "Offer",
    "ladder_as_dicts",
    "next_offer",
    "offer_by_key",
    "offer_for_rung",
    "price_label",
]
