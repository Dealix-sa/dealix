"""خادم Hermes — signal ingestion.

A Signal is the rawest possible observation entering the Hermes kernel.
Signals come from many places (inbound messages, market radar, internal
notes, tenders, etc.) and are routed to a SignalClassifier which decides
whether the signal is monetizable, sensitive, or needs sovereign review.

Classification is deterministic keyword/regex matching only — no LLM call.
That keeps the kernel testable, offline-safe, and free of model surprises.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from dealix.hermes.core.schemas import WorkspaceScope, utcnow


class SignalSource(StrEnum):
    INBOUND_MESSAGE = "inbound_message"
    OUTBOUND_REPLY = "outbound_reply"
    MARKET_RADAR = "market_radar"
    TENDER = "tender"
    COMPETITOR = "competitor"
    NEWS = "news"
    INTERNAL_NOTE = "internal_note"
    PARTNER_REFERRAL = "partner_referral"
    CUSTOMER_HEALTH = "customer_health"
    OBSERVATION = "observation"


class SignalCategory(StrEnum):
    """Where the SignalClassifier routes the signal next."""

    MONEY = "money"
    PARTNER = "partner"
    PRODUCT = "product"
    KNOWLEDGE = "knowledge"
    RISK = "risk"
    NOISE = "noise"


# ─────────────────────────────────────────────────────────────
# The Signal envelope
# ─────────────────────────────────────────────────────────────


def _new_signal_id() -> str:
    return f"sig_{uuid4().hex}"


class Signal(BaseModel):
    """A raw incoming observation."""

    model_config = ConfigDict(extra="forbid")

    signal_id: str = Field(default_factory=_new_signal_id)
    source: SignalSource
    raw_text: str = Field(..., min_length=1, max_length=20_000)
    channel: str = Field(..., min_length=1, max_length=64)
    captured_at: object = Field(default_factory=utcnow)
    metadata: dict[str, str] = Field(default_factory=dict)
    workspace: WorkspaceScope = WorkspaceScope.INTERNAL

    @field_validator("raw_text")
    @classmethod
    def _strip(cls, value: str) -> str:
        return value.strip()


# ─────────────────────────────────────────────────────────────
# Classification output
# ─────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class SignalClassification:
    """Result of running the classifier on a Signal."""

    category: SignalCategory
    monetizable: bool
    sensitive: bool
    repeatable: bool
    needs_sami: bool
    matched_rules: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "category": self.category.value,
            "monetizable": self.monetizable,
            "sensitive": self.sensitive,
            "repeatable": self.repeatable,
            "needs_sami": self.needs_sami,
            "matched_rules": list(self.matched_rules),
        }


# ─────────────────────────────────────────────────────────────
# Heuristic classifier
# ─────────────────────────────────────────────────────────────


# Lowercased keyword sets — Arabic + English variants. We keep them
# as plain tuples so the rules remain inspectable.
_PARTNER_TERMS: tuple[str, ...] = (
    "partner", "partnership", "white label", "white-label", "agency",
    "reseller", "joint venture", "jv", "شراكة", "وكالة", "موزع",
)
_MONEY_TERMS: tuple[str, ...] = (
    "price", "pricing", "invoice", "payment", "quote", "proposal",
    "contract", "purchase order", "po ", "budget", "تسعير", "سعر",
    "فاتورة", "عرض سعر", "دفع",
)
_PRODUCT_TERMS: tuple[str, ...] = (
    "feature request", "new feature", "build a", "we need a", "missing",
    "doesn't support", "wish you had", "ميزة جديدة", "تحسين",
)
_KNOWLEDGE_TERMS: tuple[str, ...] = (
    "how do you", "best practice", "case study", "benchmark", "playbook",
    "tutorial", "كيف", "أفضل ممارسة",
)
_RISK_TERMS: tuple[str, ...] = (
    "lawsuit", "regulator", "complaint", "breach", "downtime", "incident",
    "leak", "fine", "penalty", "شكوى", "اختراق",
)
_SENSITIVE_TERMS: tuple[str, ...] = (
    "confidential", "nda", "pii", "personal data", "ssn", "iban",
    "national id", "customer data", "سري", "بيانات شخصية",
)
_REPEATABLE_TERMS: tuple[str, ...] = (
    "again", "every month", "monthly", "weekly", "recurring", "subscription",
    "retainer", "كل شهر", "اشتراك",
)
_SAMI_TERMS: tuple[str, ...] = (
    "ceo", "founder", "board", "press release", "investor", "regulator",
    "media", "تصريح", "بيان صحفي",
)

# SA national id heuristic (10 digits starting with 1 or 2)
_SA_NATIONAL_ID = re.compile(r"\b[12]\d{9}\b")
# Generic IBAN heuristic
_IBAN = re.compile(r"\bSA\d{2}[A-Z0-9]{18,22}\b", re.IGNORECASE)


def _contains_any(text: str, terms: tuple[str, ...]) -> str | None:
    for term in terms:
        if term in text:
            return term
    return None


class SignalClassifier:
    """Deterministic, keyword-based signal classifier.

    Eight heuristic rules currently implemented:
      1. PARTNER terms → category=PARTNER, monetizable=True
      2. MONEY terms   → category=MONEY,   monetizable=True
      3. PRODUCT terms → category=PRODUCT
      4. KNOWLEDGE     → category=KNOWLEDGE
      5. RISK terms    → category=RISK,    needs_sami=True
      6. SENSITIVE     → sensitive=True
      7. REPEATABLE    → repeatable=True
      8. SAMI-only     → needs_sami=True
      + PII regexes (SA national id / IBAN) → sensitive=True
      + source=TENDER → category=MONEY, needs_sami=True
    """

    def classify(self, signal: Signal) -> SignalClassification:
        text = signal.raw_text.lower()
        matched: list[str] = []

        category = SignalCategory.NOISE
        monetizable = False
        sensitive = False
        repeatable = False
        needs_sami = False

        if hit := _contains_any(text, _PARTNER_TERMS):
            category = SignalCategory.PARTNER
            monetizable = True
            matched.append(f"partner:{hit}")
        if hit := _contains_any(text, _MONEY_TERMS):
            category = SignalCategory.MONEY
            monetizable = True
            matched.append(f"money:{hit}")
        if hit := _contains_any(text, _PRODUCT_TERMS):
            if category == SignalCategory.NOISE:
                category = SignalCategory.PRODUCT
            matched.append(f"product:{hit}")
        if hit := _contains_any(text, _KNOWLEDGE_TERMS):
            if category == SignalCategory.NOISE:
                category = SignalCategory.KNOWLEDGE
            matched.append(f"knowledge:{hit}")
        if hit := _contains_any(text, _RISK_TERMS):
            category = SignalCategory.RISK
            needs_sami = True
            matched.append(f"risk:{hit}")
        if hit := _contains_any(text, _SENSITIVE_TERMS):
            sensitive = True
            matched.append(f"sensitive:{hit}")
        if hit := _contains_any(text, _REPEATABLE_TERMS):
            repeatable = True
            matched.append(f"repeatable:{hit}")
        if hit := _contains_any(text, _SAMI_TERMS):
            needs_sami = True
            matched.append(f"sami:{hit}")

        # PII regexes — escalate sensitivity even with no keyword hit
        if _SA_NATIONAL_ID.search(signal.raw_text):
            sensitive = True
            matched.append("pii:sa_national_id")
        if _IBAN.search(signal.raw_text):
            sensitive = True
            matched.append("pii:iban")

        # Source-based override: tenders are always money + sami
        if signal.source == SignalSource.TENDER:
            category = SignalCategory.MONEY
            monetizable = True
            needs_sami = True
            matched.append("source:tender")

        return SignalClassification(
            category=category,
            monetizable=monetizable,
            sensitive=sensitive,
            repeatable=repeatable,
            needs_sami=needs_sami,
            matched_rules=tuple(matched),
        )


__all__ = [
    "Signal",
    "SignalCategory",
    "SignalClassification",
    "SignalClassifier",
    "SignalSource",
]
