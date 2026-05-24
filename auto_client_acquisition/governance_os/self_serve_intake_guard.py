"""Self-Serve Intake Guard — Phase 1 (autonomous lead-to-cash).

Composite guard that runs on every self-serve form submission BEFORE any
Source Passport is created or any Moyasar invoice is requested.

Composes the existing primitives:
  - forbidden_actions.is_channel_forbidden
  - claim_safety.audit_claim_safety
  - lawful_basis.LawfulBasis

Returns a structured verdict with bilingual reasons (AR/EN) suitable for
HTTP 422 responses. Never raises — callers decide whether to refuse the
submission or queue it for human review.

Doctrine references (non-negotiables enforced):
  #1 No cold WhatsApp / channel automation (forbidden_actions)
  #4 No guaranteed sales claims (claim_safety)
  #5 No fake proof (claim_safety)
  #10 Source Passport / PDPL lawful basis required (lawful_basis)
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.governance_os.claim_safety import (
    ClaimSafetyResult,
    audit_claim_safety,
)
from auto_client_acquisition.governance_os.forbidden_actions import is_channel_forbidden
from auto_client_acquisition.governance_os.lawful_basis import LawfulBasis


@dataclass(frozen=True, slots=True)
class IntakeVerdict:
    """Outcome of a self-serve intake check."""

    allow: bool
    violation_codes: tuple[str, ...]
    reasons_ar: tuple[str, ...]
    reasons_en: tuple[str, ...]
    claim_safety: ClaimSafetyResult

    def to_dict(self) -> dict[str, object]:
        return {
            "allow": self.allow,
            "violation_codes": list(self.violation_codes),
            "reasons": {
                "ar": list(self.reasons_ar),
                "en": list(self.reasons_en),
            },
            "claim_safety_issues": list(self.claim_safety.issues),
            "claim_safety_decision": self.claim_safety.suggested_decision.value,
        }


_REASONS: dict[str, tuple[str, str]] = {
    "lawful_basis_missing": (
        "أساس قانوني مفقود — PDPL يتطلّب موافقة صريحة أو عقد قبل المعالجة.",
        "Lawful basis missing — PDPL requires explicit consent or contract.",
    ),
    "consent_not_given": (
        "لم يُسجَّل قبول صريح من المستخدم — يتطلب checkbox مفعّل.",
        "Explicit consent not recorded — checkbox must be active.",
    ),
    "channel_pattern_forbidden": (
        "النص يحتوي نمط قناة ممنوع (cold WhatsApp / blast / linkedin automation).",
        "Submission contains a forbidden channel pattern.",
    ),
    "claim_safety_blocked": (
        "النص يحتوي وعداً مضموناً أو إثباتاً مزيفاً — تم الحجب.",
        "Text contains guaranteed claim or fake proof — blocked.",
    ),
    "claim_safety_draft_only": (
        "النص فيه عبارات تحتاج مراجعة بشرية قبل أي إرسال.",
        "Text contains language requiring human review before send.",
    ),
    "source_passport_id_missing": (
        "Source Passport مطلوب — لا معالجة بدونه (Non-Negotiable #10).",
        "Source Passport required — no processing without it (Non-Negotiable #10).",
    ),
    "offer_id_invalid": (
        "Offer غير معروف — يجب اختياره من القائمة الرسمية.",
        "Unknown offer — must be selected from the official catalog.",
    ),
}

# The 5 productized offers — single source of truth for routing.
ALLOWED_OFFER_IDS = (
    "diagnostic_free",
    "sprint_499",
    "data_pack_1500",
    "managed_ops_retainer",
    "custom_ai",
)

# Offers that are eligible for full auto-approve (low risk, ≤ 1,500 SAR).
AUTO_APPROVE_OFFERS = (
    "diagnostic_free",
    "sprint_499",
    "data_pack_1500",
)


def evaluate_intake(
    *,
    offer_id: str,
    source_passport_id: str | None,
    lawful_basis: LawfulBasis | str | None,
    consent_given: bool,
    free_text: str = "",
) -> IntakeVerdict:
    """
    Evaluate a self-serve intake payload against the doctrine.

    Returns IntakeVerdict.allow=True only when:
      - offer_id is in ALLOWED_OFFER_IDS
      - source_passport_id is non-empty (Non-Negotiable #10)
      - lawful_basis is set AND consent_given (when basis==CONSENT)
      - no forbidden channel pattern in free_text
      - claim_safety returns ALLOW (not BLOCK, not DRAFT_ONLY)
    """
    codes: list[str] = []

    if offer_id not in ALLOWED_OFFER_IDS:
        codes.append("offer_id_invalid")

    if not source_passport_id:
        codes.append("source_passport_id_missing")

    # Normalize lawful basis.
    if isinstance(lawful_basis, str):
        try:
            lawful_basis = LawfulBasis(lawful_basis)
        except ValueError:
            lawful_basis = None

    if lawful_basis is None:
        codes.append("lawful_basis_missing")
    elif lawful_basis == LawfulBasis.CONSENT and not consent_given:
        codes.append("consent_not_given")

    if free_text and is_channel_forbidden(free_text):
        codes.append("channel_pattern_forbidden")

    claim_result = audit_claim_safety(free_text) if free_text else audit_claim_safety("")

    # Map claim_safety verdict into the intake codes.
    decision = claim_result.suggested_decision.value
    if decision == "BLOCK":
        codes.append("claim_safety_blocked")
    elif decision == "DRAFT_ONLY":
        codes.append("claim_safety_draft_only")

    # Deduplicate while preserving order.
    unique_codes = tuple(dict.fromkeys(codes))
    reasons_ar = tuple(_REASONS[c][0] for c in unique_codes if c in _REASONS)
    reasons_en = tuple(_REASONS[c][1] for c in unique_codes if c in _REASONS)

    return IntakeVerdict(
        allow=not unique_codes,
        violation_codes=unique_codes,
        reasons_ar=reasons_ar,
        reasons_en=reasons_en,
        claim_safety=claim_result,
    )


def is_auto_approve_offer(offer_id: str) -> bool:
    """Phase 1 fast-path: ≤ 1,500 SAR offers skip founder approval queue."""
    return offer_id in AUTO_APPROVE_OFFERS


__all__ = [
    "ALLOWED_OFFER_IDS",
    "AUTO_APPROVE_OFFERS",
    "IntakeVerdict",
    "evaluate_intake",
    "is_auto_approve_offer",
]
