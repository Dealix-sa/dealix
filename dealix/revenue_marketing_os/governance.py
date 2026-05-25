"""
Growth Governance — what marketing can and cannot do without approval.

This module is intentionally simple: a set of named hard-gates and
two pure functions that turn an action request into either an
``allowed=True`` decision or an ``allowed=False`` reason. The HTTP
layer is responsible for invoking them — there is no auto-action.

Forbidden, always:
  - guaranteed-result claims
  - using an unapproved case study
  - naming a customer without consent
  - using customer data inside public content
  - claiming a partnership that does not exist
  - promising "full compliance"

Requires explicit approval:
  - paid ads
  - publishing a case study
  - mentioning revenue numbers
  - offering a discount
  - sending a partnership message
  - publishing an enterprise page
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_scraping": True,
    "no_cold_outreach_automation": True,
    "no_paid_spend_without_attribution": True,
    "no_claim_without_trust_check": True,
    "no_unapproved_case_study": True,
    "no_named_customer_without_consent": True,
    "no_revenue_numbers_in_public_without_approval": True,
    "no_guaranteed_results_claim": True,
    "no_full_compliance_promise": True,
    "no_unverified_revenue_counted": True,
}

FORBIDDEN_PHRASES: tuple[str, ...] = (
    "guaranteed results",
    "guarantee results",
    "نضمن النتائج",
    "full compliance",
    "fully compliant",
    "متوافق بالكامل",
    "official partner of",
    "شريك رسمي لـ",
)

APPROVAL_REQUIRED_ACTIONS: frozenset[str] = frozenset(
    {
        "publish_case_study",
        "publish_enterprise_page",
        "send_partnership_outreach",
        "launch_paid_campaign",
        "publish_revenue_numbers",
        "offer_discount",
        "publish_named_customer",
    }
)


@dataclass(frozen=True)
class GovernanceDecision:
    allowed: bool
    reason_ar: str = ""
    reason_en: str = ""
    requires_approval: bool = False
    triggered_gates: tuple[str, ...] = ()


def check_claim(text: str) -> GovernanceDecision:
    """
    Trust-check a draft message body. Returns ``allowed=False`` if
    any forbidden phrase is present. Used by message and content
    workflows before approval.
    """
    if not text:
        return GovernanceDecision(allowed=True)
    lowered = text.lower()
    triggered: list[str] = []
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lowered:
            triggered.append(phrase)
    if triggered:
        return GovernanceDecision(
            allowed=False,
            reason_ar="ادعاء ممنوع وفق سجل No-Overclaim.",
            reason_en=f"Forbidden claim detected: {', '.join(triggered)}.",
            requires_approval=True,
            triggered_gates=("no_claim_without_trust_check",),
        )
    return GovernanceDecision(allowed=True)


def check_action(action: str, *, has_approval: bool = False) -> GovernanceDecision:
    """
    Marketing action gate. Approval-required actions are blocked
    unless ``has_approval`` is True.
    """
    if action in APPROVAL_REQUIRED_ACTIONS and not has_approval:
        return GovernanceDecision(
            allowed=False,
            reason_ar="هذا الإجراء يحتاج موافقة المؤسس قبل التنفيذ.",
            reason_en="This action requires founder approval.",
            requires_approval=True,
            triggered_gates=("approval_required",),
        )
    return GovernanceDecision(allowed=True)


def check_revenue(
    *, status: str, payment_verified: bool, invoice_verified: bool, agreement_signed: bool
) -> GovernanceDecision:
    """Reject revenue counting if no real proof exists."""
    real_statuses = {"paid", "retainer_active", "renewed", "expanded"}
    if status in real_statuses and not (payment_verified or invoice_verified):
        return GovernanceDecision(
            allowed=False,
            reason_ar="لا يُحتسب الدخل بدون إثبات دفع أو فاتورة.",
            reason_en="Cannot count revenue without payment or invoice proof.",
            triggered_gates=("no_unverified_revenue_counted",),
        )
    if status == "invoiced" and not invoice_verified:
        return GovernanceDecision(
            allowed=False,
            reason_ar="حالة الفاتورة تتطلب تحقق الفاتورة.",
            reason_en="Invoiced status requires invoice verification.",
            triggered_gates=("no_unverified_revenue_counted",),
        )
    if status == "committed" and not agreement_signed:
        return GovernanceDecision(
            allowed=False,
            reason_ar="الالتزام يتطلب اتفاقية موقعة.",
            reason_en="Committed status requires a signed agreement.",
            triggered_gates=("no_unverified_revenue_counted",),
        )
    return GovernanceDecision(allowed=True)


def scan_assets(asset_texts: Iterable[str]) -> list[GovernanceDecision]:
    """Batch check across multiple draft texts (LinkedIn posts, etc.)."""
    return [check_claim(t) for t in asset_texts]
