"""
TrustSignals — proof markers attached to claims and offers, required for
AI-search visibility and external scaling. Every claim that goes out
must point to at least one trust signal or evidence record.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class TrustSignalKind(StrEnum):
    CASE_STUDY = "case_study"
    CUSTOMER_QUOTE = "customer_quote"
    VERIFIED_OUTCOME = "verified_outcome"
    EVIDENCE_PACK = "evidence_pack"
    SECURITY_POSTURE = "security_posture"
    AI_GOVERNANCE_CONTENT = "ai_governance_content"
    PARTNER_TESTIMONIAL = "partner_testimonial"
    REVIEW_PROFILE = "review_profile"
    PUBLIC_METHODOLOGY = "public_methodology"


@dataclass
class TrustSignal:
    signal_id: str
    kind: TrustSignalKind
    subject: str
    url: str | None = None
    captured_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


class TrustSignalLedger:
    def __init__(self) -> None:
        self._signals: dict[str, TrustSignal] = {}
        self._by_subject: dict[str, list[str]] = {}

    def record(self, signal: TrustSignal) -> None:
        self._signals[signal.signal_id] = signal
        self._by_subject.setdefault(signal.subject, []).append(signal.signal_id)

    def for_subject(self, subject: str) -> list[TrustSignal]:
        return [self._signals[i] for i in self._by_subject.get(subject, [])]

    def has_minimum(self, subject: str, *, minimum: int = 1) -> bool:
        return len(self._by_subject.get(subject, [])) >= minimum

    def check_claim(self, subject: str, *, minimum: int = 1) -> tuple[bool, str]:
        present = len(self._by_subject.get(subject, []))
        if present < minimum:
            return False, f"claim about {subject!r} needs at least {minimum} trust signal(s); has {present}"
        return True, "ok"
