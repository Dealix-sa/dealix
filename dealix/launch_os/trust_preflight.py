"""Trust preflight gate — checks outbound drafts against 10 policy rules.

All outbound communications (email, phone scripts, LinkedIn, WhatsApp) must
pass this gate before dispatch or approval routing.

Rules enforced:
  R01  No guarantee language (results, ROI, revenue promises)
  R02  No competitor defamation
  R03  No PII exposure (national IDs, phone numbers, emails in body)
  R04  No spam trigger patterns (URGENT, ACT NOW, limited-time pressure)
  R05  WhatsApp channel requires consent_record_ref
  R06  Arabic text must not use informal/inappropriate tone markers
  R07  Claim accuracy — evidence_level must be L2 or above
  R08  Legal entity check — drafted_by must be set
  R09  Pricing within approved range (pricing_status not draft_only for send)
  R10  Enterprise proposals require founder approval flag
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TrustViolation:
    """Single rule violation returned by :func:`run_preflight`.

    Attributes:
        rule_id:     Identifier such as ``"R01"``.
        severity:    ``"block"`` (hard stop) or ``"warn"`` (advisory).
        message_ar:  Arabic explanation.
        message_en:  English explanation.

    Examples:
        >>> v = TrustViolation("R01", "block", "يحظر استخدام لغة الضمان", "Guarantee language is forbidden")
        >>> v.rule_id
        'R01'
    """

    rule_id: str
    severity: str
    message_ar: str
    message_en: str


# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

_GUARANTEE_PATTERNS_EN = re.compile(
    r"\b(guarantee|guaranteed|we promise|promise\b|100%\s+roi|double your|"
    r"triple your|risk.?free results|assured results|certain(ly)? (increase|boost|grow))\b",
    re.IGNORECASE,
)
_GUARANTEE_PATTERNS_AR = re.compile(
    r"(نضمن|مضمون|نكفل|كفالة نتائج|ضمان ربح|ضمان عائد|نوعد|وعد بنتائج)",
)
_DEFAMATION_PATTERNS = re.compile(
    r"\b(competitor|rival|opponent).{0,40}(bad|terrible|fraud|scam|fake|fail|worst|avoid)\b",
    re.IGNORECASE,
)
_PII_PHONE = re.compile(r"(\+966|05)\d{7,9}")
_PII_EMAIL_IN_BODY = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")
_PII_NATIONAL_ID = re.compile(r"\b[12]\d{9}\b")
_SPAM_PATTERNS = re.compile(
    r"\b(URGENT|ACT NOW|LIMITED TIME|EXPIRES|LAST CHANCE|FREE GIFT|CLICK HERE NOW|"
    r"SPECIAL PROMOTION ENDS|فرصة محدودة|العرض ينتهي غداً|عجل)\b",
    re.IGNORECASE,
)
_INFORMAL_AR = re.compile(r"(يا عم|يا صاحبي|برو|هههه|لول)")

# Minimum evidence level (as integer suffix) that allows outbound send.
_MIN_EVIDENCE_LEVEL = 2  # L2

_EVIDENCE_ORDER = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}


def _evidence_int(level: str) -> int:
    return _EVIDENCE_ORDER.get(level, 0)


def _full_text(draft: dict[str, Any]) -> str:
    parts = [
        draft.get("subject", ""),
        draft.get("body", ""),
        draft.get("subject_ar", ""),
        draft.get("subject_en", ""),
        draft.get("body_ar", ""),
        draft.get("body_en", ""),
    ]
    return " ".join(str(p) for p in parts)


def _check_r01_no_guarantee(draft: dict[str, Any]) -> TrustViolation | None:
    text = _full_text(draft)
    if _GUARANTEE_PATTERNS_EN.search(text) or _GUARANTEE_PATTERNS_AR.search(text):
        return TrustViolation(
            rule_id="R01",
            severity="block",
            message_ar="يُحظر استخدام لغة الضمان أو الوعد بنتائج محددة",
            message_en="Guarantee or promised-outcome language is forbidden",
        )
    return None


def _check_r02_no_defamation(draft: dict[str, Any]) -> TrustViolation | None:
    text = _full_text(draft)
    if _DEFAMATION_PATTERNS.search(text):
        return TrustViolation(
            rule_id="R02",
            severity="block",
            message_ar="يُحظر الإساءة إلى المنافسين أو التشهير بهم",
            message_en="Competitor defamation is forbidden",
        )
    return None


def _check_r03_no_pii(draft: dict[str, Any]) -> TrustViolation | None:
    text = _full_text(draft)
    if _PII_PHONE.search(text) or _PII_NATIONAL_ID.search(text):
        return TrustViolation(
            rule_id="R03",
            severity="block",
            message_ar="لا يجوز تضمين أرقام الهواتف أو الهوية الوطنية في جسم الرسالة",
            message_en="Phone numbers or national IDs must not appear in the draft body",
        )
    # Email addresses in body are advisory (may be intentional CTA)
    if _PII_EMAIL_IN_BODY.search(draft.get("body", "") + draft.get("body_ar", "") + draft.get("body_en", "")):
        return TrustViolation(
            rule_id="R03",
            severity="warn",
            message_ar="تحقق من أن البريد الإلكتروني في الجسم مقصود وليس بيانات شخصية مسربة",
            message_en="Email address found in body — confirm this is intentional and not leaked PII",
        )
    return None


def _check_r04_no_spam(draft: dict[str, Any]) -> TrustViolation | None:
    text = _full_text(draft)
    if _SPAM_PATTERNS.search(text):
        return TrustViolation(
            rule_id="R04",
            severity="block",
            message_ar="النص يحتوي على أنماط بريد عشوائي (ضغط وقت، عروض محدودة مبالغ فيها)",
            message_en="Draft contains spam trigger patterns (urgency pressure, aggressive promotions)",
        )
    return None


def _check_r05_whatsapp_consent(draft: dict[str, Any]) -> TrustViolation | None:
    channel = str(draft.get("channel", "")).lower()
    if "whatsapp" not in channel:
        return None
    if not draft.get("consent_record_ref"):
        return TrustViolation(
            rule_id="R05",
            severity="block",
            message_ar="قناة واتساب تستلزم وجود مرجع إذن صريح (consent_record_ref)",
            message_en="WhatsApp channel requires an explicit consent_record_ref before sending",
        )
    return None


def _check_r06_arabic_tone(draft: dict[str, Any]) -> TrustViolation | None:
    ar_text = draft.get("body_ar", "") + draft.get("subject_ar", "") + draft.get("body", "")
    if _INFORMAL_AR.search(ar_text):
        return TrustViolation(
            rule_id="R06",
            severity="warn",
            message_ar="النص العربي يحتوي على مصطلحات غير رسمية؛ يُرجى مراجعة الأسلوب",
            message_en="Arabic text contains informal tone markers; review before sending",
        )
    return None


def _check_r07_evidence_level(draft: dict[str, Any]) -> TrustViolation | None:
    level = str(draft.get("evidence_level", "L0"))
    if _evidence_int(level) < _MIN_EVIDENCE_LEVEL:
        return TrustViolation(
            rule_id="R07",
            severity="block",
            message_ar=f"مستوى الدليل {level} أقل من الحد المطلوب L2 للإرسال الخارجي",
            message_en=f"Evidence level {level} is below the required L2 minimum for outbound",
        )
    return None


def _check_r08_legal_entity(draft: dict[str, Any]) -> TrustViolation | None:
    if not draft.get("drafted_by"):
        return TrustViolation(
            rule_id="R08",
            severity="block",
            message_ar="يجب تحديد المسؤول عن المسودة (drafted_by) قبل الإرسال",
            message_en="drafted_by must be set — draft ownership is required for audit trail",
        )
    return None


def _check_r09_pricing_status(draft: dict[str, Any]) -> TrustViolation | None:
    status = str(draft.get("pricing_status", "draft_only"))
    if status == "draft_only":
        return TrustViolation(
            rule_id="R09",
            severity="block",
            message_ar="لا يمكن إرسال مسودة بحالة السعر (draft_only) — يجب الحصول على موافقة السعر",
            message_en="Draft with pricing_status=draft_only cannot be sent — pricing approval required",
        )
    return None


def _check_r10_enterprise_approval(draft: dict[str, Any]) -> TrustViolation | None:
    status = str(draft.get("pricing_status", ""))
    approval_required = bool(draft.get("approval_required", False))
    if status == "founder_approval_required" and not approval_required:
        return TrustViolation(
            rule_id="R10",
            severity="block",
            message_ar="العروض المؤسسية ذات قيمة عالية تستلزم إشارة موافقة المؤسس (approval_required=true)",
            message_en="Enterprise proposals with founder_approval_required pricing must set approval_required=true",
        )
    return None


_RULES = [
    _check_r01_no_guarantee,
    _check_r02_no_defamation,
    _check_r03_no_pii,
    _check_r04_no_spam,
    _check_r05_whatsapp_consent,
    _check_r06_arabic_tone,
    _check_r07_evidence_level,
    _check_r08_legal_entity,
    _check_r09_pricing_status,
    _check_r10_enterprise_approval,
]


def run_preflight(draft: dict[str, Any]) -> tuple[bool, list[TrustViolation]]:
    """Run all 10 trust rules against an outreach draft dict.

    Args:
        draft: Dict matching the ``outreach_draft.schema.json`` structure or
               the extended :class:`~dealix.launch_os.outreach_factory.OutreachDraft`
               representation.

    Returns:
        A ``(passed, violations)`` tuple where ``passed`` is ``True`` only
        when there are zero ``"block"``-severity violations.

    Examples:
        >>> ok_draft = {
        ...     "channel": "email",
        ...     "body": "We can help you improve your operations.",
        ...     "body_ar": "يمكننا مساعدتك في تحسين عملياتك.",
        ...     "evidence_level": "L3",
        ...     "drafted_by": "founder",
        ...     "pricing_status": "approved_range_required",
        ...     "approval_required": False,
        ... }
        >>> passed, viols = run_preflight(ok_draft)
        >>> passed
        True

        >>> bad_draft = {
        ...     "channel": "email",
        ...     "body": "We guarantee 100% ROI in 30 days.",
        ...     "evidence_level": "L0",
        ...     "drafted_by": "",
        ...     "pricing_status": "draft_only",
        ...     "approval_required": False,
        ... }
        >>> passed2, viols2 = run_preflight(bad_draft)
        >>> passed2
        False
        >>> any(v.rule_id == "R01" for v in viols2)
        True
    """
    violations: list[TrustViolation] = []
    for rule_fn in _RULES:
        result = rule_fn(draft)
        if result is not None:
            violations.append(result)
    passed = all(v.severity != "block" for v in violations)
    return passed, violations


if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=False)
    print(f"Trust preflight doctests: {results.attempted} run, {results.failed} failed")

    sample = {
        "channel": "email",
        "body": "We can help streamline your sales process.",
        "body_ar": "يمكننا مساعدتك في تحسين عملية المبيعات لديك.",
        "evidence_level": "L3",
        "drafted_by": "founder",
        "pricing_status": "approved_range_required",
        "approval_required": False,
    }
    passed, viols = run_preflight(sample)
    print(f"Smoke test passed={passed}, violations={len(viols)}")
