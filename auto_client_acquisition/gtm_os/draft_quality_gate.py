"""Draft quality gate — the executable Compliance/Quality Gate for outreach.

Turns the Market Production OS doctrine into a pass/fail check. A draft only
enters the founder approval queue when it passes *every* line:

  - governance: composes ``governance_os.policy_check_draft`` so scraping,
    cold-WhatsApp, LinkedIn-automation, and guaranteed/fake claims are blocked
    by the same primitives the rest of the repo uses.
  - compliance: unsubscribe present, evidence level present, not suppressed.
  - deliverability: no fake Re:/Fwd: prefix, no spammy subject.
  - quality: personalization >= P1, offer matched to the catalog, risk != high,
    body non-empty.

This module never sends, charges, or scrapes. A passing draft is marked
``governance_decision = "approval_required"`` — it is *ready for a human*, never
auto-allowed. Failing drafts are ``"BLOCK"`` (rewrite before re-queue).
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.governance_os import policy_check_draft
from auto_client_acquisition.gtm_os.offer_catalog import is_catalog_offer
from auto_client_acquisition.gtm_os.outreach_draft import EVIDENCE_LEVELS, OutreachDraft

# Subject patterns that wreck deliverability / mislead recipients (CAN-SPAM).
_SPAM_SUBJECT_PATTERNS: tuple[str, ...] = (
    "100% free",
    "free money",
    "$$$",
    "!!!",
    "act now",
    "limited time only",
    "you are a winner",
    "winner!",
    "click here now",
    "risk-free",
    "double your",
    "اضغط هنا الآن",
    "اربح الآن",
    "عرض ينتهي اليوم",
    "مجانا 100%",
    "مجاناً 100%",
)
_FAKE_REPLY_PREFIXES: tuple[str, ...] = (
    "re:",
    "re :",
    "fw:",
    "fwd:",
    "fwd :",
    "رد:",
    "رد :",
    "إعادة توجيه",
)
_CAPS_WORD_RE = re.compile(r"\b[A-Z]{3,}\b")


class GateIssue(BaseModel):
    """One blocking finding with a bilingual reason."""

    model_config = ConfigDict(extra="forbid")

    code: str
    category: str  # doctrine | compliance | deliverability | quality
    ar: str
    en: str


class GateResult(BaseModel):
    """Outcome of validating a single draft. Carries a governance decision."""

    model_config = ConfigDict(extra="forbid")

    draft_id: str
    passed: bool
    verdict: str  # "pass" | "fail"
    governance_decision: str  # "approval_required" (pass) | "BLOCK" (fail)
    issues: list[GateIssue] = Field(default_factory=list)
    checked_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    @property
    def codes(self) -> tuple[str, ...]:
        return tuple(i.code for i in self.issues)


def _subject_problem(subject: str) -> GateIssue | None:
    s = subject.strip()
    low = s.lower()
    for pref in _FAKE_REPLY_PREFIXES:
        if low.startswith(pref):
            return GateIssue(
                code="fake_reply_prefix",
                category="deliverability",
                ar="عنوان يبدأ بـ Re:/Fwd: في رسالة باردة — تضليل ممنوع.",
                en="Subject starts with Re:/Fwd: on a cold message — misleading, forbidden.",
            )
    for pat in _SPAM_SUBJECT_PATTERNS:
        if pat in low:
            return GateIssue(
                code="misleading_subject",
                category="deliverability",
                ar=f"عنوان يحوي نمط سبام يضر بالتسليم: «{pat}».",
                en=f"Subject contains a spammy pattern that hurts deliverability: '{pat}'.",
            )
    if len(_CAPS_WORD_RE.findall(s)) >= 3:
        return GateIssue(
            code="misleading_subject",
            category="deliverability",
            ar="عنوان فيه إفراط بالأحرف الكبيرة (نمط سبام).",
            en="Subject over-uses ALL-CAPS words (spam pattern).",
        )
    return None


def validate_outreach_draft(
    draft: OutreachDraft | dict,
    *,
    suppression_refs: Iterable[str] | None = None,
    require_offer_in_catalog: bool = True,
) -> GateResult:
    """Validate one draft against the full doctrine. Pure, side-effect free."""
    if isinstance(draft, dict):
        draft = OutreachDraft.model_validate(draft)
    suppressed = set(suppression_refs or ())
    issues: list[GateIssue] = []

    # 1) Doctrine — reuse the canonical draft policy check on all copy.
    policy = policy_check_draft(draft.combined_text())
    if not policy.allowed:
        for code in policy.issues:
            issues.append(
                GateIssue(
                    code=f"governance:{code}",
                    category="doctrine",
                    ar="مخالفة عقيدة في نص المسودة — تُحجب حتى التصحيح.",
                    en="Doctrine violation in draft copy — blocked until fixed.",
                )
            )

    # 2) Compliance — CAN-SPAM unsubscribe + evidence provenance + suppression.
    if not draft.unsubscribe_included:
        issues.append(
            GateIssue(
                code="missing_unsubscribe",
                category="compliance",
                ar="لا يوجد رابط إلغاء اشتراك — مخالف لـ CAN-SPAM.",
                en="No unsubscribe/opt-out present — violates CAN-SPAM.",
            )
        )
    if draft.evidence_level not in EVIDENCE_LEVELS:
        issues.append(
            GateIssue(
                code="missing_evidence_level",
                category="compliance",
                ar="مستوى الأدلة (L0–L5) غير محدد — كل ادعاء يحتاج مصدرًا.",
                en="Evidence level (L0–L5) is missing — every claim needs provenance.",
            )
        )
    if draft.recipient_ref and draft.recipient_ref in suppressed:
        issues.append(
            GateIssue(
                code="suppression_hit",
                category="compliance",
                ar="المستلم في قائمة الكبح (إلغاء/شكوى) — لا يُتواصَل معه.",
                en="Recipient is on the suppression list — must not be contacted.",
            )
        )

    # 3) Deliverability — subject hygiene.
    subj = _subject_problem(draft.subject)
    if subj is not None:
        issues.append(subj)

    # 4) Quality — personalization, offer match, risk, body.
    if draft.personalization_tier == "P0":
        issues.append(
            GateIssue(
                code="personalization_below_p1",
                category="quality",
                ar="التخصيص أقل من P1 (رسالة عامة) — لا تدخل قائمة الموافقة.",
                en="Personalization below P1 (generic) — must not enter the approval queue.",
            )
        )
    offer_ok = draft.offer_matched and bool(draft.offer)
    if require_offer_in_catalog:
        offer_ok = offer_ok and is_catalog_offer(draft.offer)
    if not offer_ok:
        issues.append(
            GateIssue(
                code="offer_not_matched",
                category="quality",
                ar="العرض غير مطابق لكتالوج العروض المعتمد.",
                en="Offer is not matched to the approved offer catalog.",
            )
        )
    if draft.risk_level == "high":
        issues.append(
            GateIssue(
                code="risk_high",
                category="quality",
                ar="مستوى المخاطرة مرتفع — يحتاج إعادة صياغة قبل الموافقة.",
                en="Risk level is high — needs rewrite before approval.",
            )
        )
    if not (draft.body_ar.strip() or draft.body_en.strip()):
        issues.append(
            GateIssue(
                code="empty_body",
                category="quality",
                ar="نص الرسالة فارغ.",
                en="Message body is empty.",
            )
        )

    # 5) Defensive — never let a draft claim a sent/queued state without approval.
    if draft.send_status in {"queued", "sent"} and draft.approval_status != "approved":
        issues.append(
            GateIssue(
                code="send_without_approval",
                category="doctrine",
                ar="حالة إرسال بدون موافقة المؤسس — ممنوع.",
                en="Send/queued state without founder approval — forbidden.",
            )
        )

    passed = not issues
    return GateResult(
        draft_id=draft.draft_id,
        passed=passed,
        verdict="pass" if passed else "fail",
        governance_decision="approval_required" if passed else "BLOCK",
        issues=issues,
    )


def summarize_gate_results(results: Iterable[GateResult]) -> dict[str, object]:
    """Aggregate a batch of gate results for the daily production report."""
    results = list(results)
    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]
    reason_counts: dict[str, int] = {}
    for r in failed:
        for code in r.codes:
            reason_counts[code] = reason_counts.get(code, 0) + 1
    return {
        "total": len(results),
        "passed": len(passed),
        "failed": len(failed),
        "approval_ready_ids": [r.draft_id for r in passed],
        "blocked_ids": [r.draft_id for r in failed],
        "top_failure_reasons": dict(
            sorted(reason_counts.items(), key=lambda kv: kv[1], reverse=True)
        ),
        "generated_at": datetime.now(UTC).isoformat(),
    }


__all__ = [
    "GateIssue",
    "GateResult",
    "summarize_gate_results",
    "validate_outreach_draft",
]
