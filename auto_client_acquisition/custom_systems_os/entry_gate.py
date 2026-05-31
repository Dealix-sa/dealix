"""Custom Systems OS — governed entry gate.

Encodes the doctrine rule "no customization / no white-label before 3 paid
pilots" as runtime logic (not just documentation). Pure, no I/O. The
capability is always delivered founder-assisted; the bilingual disclosure is
returned so no caller can present it as a fully-managed/white-label service.
"""

from __future__ import annotations

from auto_client_acquisition.custom_systems_os.schemas import CustomSystemEntryDecision

# Doctrine: a custom system build unlocks only after >= 3 paid pilots.
MIN_PAID_PILOTS = 3

DELIVERY_MODE = "founder_assisted"

DISCLOSURE_AR = (
    "تسليم بقيادة المؤسس / شبه-مؤتمت: الأدوات جاهزة لكن التسليم يتطلّب تشغيلاً "
    "وموافقةً يدويةً من المؤسس. لا إرسال خارجي مؤتمت، ولا white-label كامل، "
    "ولا وعود بالنتائج. القيمة التقديرية ليست قيمة مُتحقَّقة."
)
DISCLOSURE_EN = (
    "Founder-assisted / semi-automated delivery: tooling is ready, but delivery "
    "requires manual founder operation and approval. No automated external send, "
    "no full white-label, no outcome promises. Estimated value is not Verified value."
)


def check_entry(
    *,
    paid_pilots_completed: int,
    signed_proof_packs: int = 0,
    workflow_owner_present: bool = False,
) -> CustomSystemEntryDecision:
    """Decide whether a custom-system engagement may begin.

    Blocks until the doctrine entry conditions are met. ``delivery_mode`` is
    always ``founder_assisted`` and the bilingual disclosure is always
    populated so the gate cannot be repackaged as a managed/white-label tier.
    """
    blocked: list[str] = []
    if int(paid_pilots_completed) < MIN_PAID_PILOTS:
        blocked.append("no_customization_before_3_paid_pilots")
    if not workflow_owner_present:
        blocked.append("workflow_owner_missing")

    return CustomSystemEntryDecision(
        allowed=not blocked,
        blocked_reasons=tuple(blocked),
        delivery_mode=DELIVERY_MODE,
        disclosure_ar=DISCLOSURE_AR,
        disclosure_en=DISCLOSURE_EN,
    )


__all__ = [
    "DELIVERY_MODE",
    "DISCLOSURE_AR",
    "DISCLOSURE_EN",
    "MIN_PAID_PILOTS",
    "check_entry",
]
