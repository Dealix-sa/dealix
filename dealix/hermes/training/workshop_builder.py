"""Workshop builder — a deterministic outline + price band.

Every workshop has the same shape: outline + outcomes + downstream offer.
The downstream offer is mandatory — training is a sales motion, not a
charity.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Workshop:
    workshop_id: str
    title: str
    audience: str
    duration_hours: float
    outline: list[str]
    learning_outcomes: list[str]
    floor_price_sar: float
    ceiling_price_sar: float
    downstream_offer: str  # the offer we expect to sell after


_LIBRARY: dict[str, Workshop] = {
    "ai_for_founders": Workshop(
        workshop_id="ai_for_founders",
        title="AI for Founders — استخدام مسؤول وقرارات أسرع",
        audience="Saudi founders",
        duration_hours=3.0,
        outline=[
            "كيف يضيع المؤسس وقته؟",
            "متى نستخدم Agent ومتى لا نستخدم؟",
            "حوكمة استخدام AI: registry + permissions + approvals",
            "تمرين: بناء عقيدة قرارك الأسبوعية",
        ],
        learning_outcomes=[
            "تحديد ٣ مهمات قابلة للأتمتة بأمان",
            "بناء قائمة قرارات أسبوعية موثّقة",
            "فهم متى يطلب AI موافقة بشرية",
        ],
        floor_price_sar=3000,
        ceiling_price_sar=15000,
        downstream_offer="Founder OS Setup",
    ),
    "ai_governance_for_managers": Workshop(
        workshop_id="ai_governance_for_managers",
        title="حوكمة AI للمديرين — صلاحيات، موافقات، أدلة",
        audience="Operations & risk managers",
        duration_hours=4.0,
        outline=[
            "ما هي عقيدة الحوكمة الأمريكية/الدولية (NIST AI RMF / ISO 42001) باختصار؟",
            "Agent Registry وTool Registry — لماذا الإلزام؟",
            "تصميم Approval Workflow بدون شلل تشغيلي",
            "بناء Evidence Pack جاهز للتدقيق",
        ],
        learning_outcomes=[
            "كتابة سياسة استخدام AI داخلية",
            "بناء permission matrix لفريقهم",
            "تصميم Approval flow أوّلي",
        ],
        floor_price_sar=15000,
        ceiling_price_sar=75000,
        downstream_offer="AI Trust Kit",
    ),
}


def get(workshop_id: str) -> Workshop | None:
    return _LIBRARY.get(workshop_id)


def all_workshops() -> list[Workshop]:
    return list(_LIBRARY.values())


__all__ = ["Workshop", "get", "all_workshops"]
