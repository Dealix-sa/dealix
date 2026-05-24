"""خادم الثقة — content guardrails.

Pure regex / keyword detectors that flag risky payloads BEFORE they hit
external systems. Each guardrail is a `Guardrail` Protocol implementation
that returns a GuardrailResult.

Included detectors:
  * NoOverclaimGuardrail
  * NoSensitiveDataGuardrail
  * NoUnauthorizedPricingGuardrail
  * NoFalsePartnershipGuardrail
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum
from typing import Any, Protocol, runtime_checkable


class GuardrailSeverity(StrEnum):
    INFO = "info"
    WARN = "warn"
    BLOCK = "block"


@dataclass
class GuardrailResult:
    guardrail: str
    passed: bool
    severity: GuardrailSeverity
    findings: list[str] = field(default_factory=list)
    detail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "guardrail": self.guardrail,
            "passed": self.passed,
            "severity": self.severity.value,
            "findings": list(self.findings),
            "detail": self.detail,
        }


@runtime_checkable
class Guardrail(Protocol):
    """Contract every guardrail honours."""

    name: str

    def check(self, payload: dict[str, Any]) -> GuardrailResult: ...


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────


def _extract_text(payload: dict[str, Any]) -> str:
    """Collect text-ish fields into one searchable blob."""
    if "text" in payload and isinstance(payload["text"], str):
        return payload["text"]
    parts: list[str] = []
    for key in ("body", "title", "content", "summary", "rationale", "subject"):
        val = payload.get(key)
        if isinstance(val, str):
            parts.append(val)
    if "fields" in payload and isinstance(payload["fields"], dict):
        for v in payload["fields"].values():
            if isinstance(v, str):
                parts.append(v)
    return "\n".join(parts)


# ─────────────────────────────────────────────────────────────
# No-overclaim guardrail
# ─────────────────────────────────────────────────────────────


_OVERCLAIM_PATTERNS: tuple[str, ...] = (
    r"\bguarantee[ds]?\b",
    r"\b100\s?%\b",
    r"\bbest in saudi\b",
    r"\bbest in the kingdom\b",
    r"\bfirst in mena\b",
    r"\bnumber one in\b",
    r"\bworld[-\s]?class\b",
    r"\bunbeatable\b",
    r"\bnever fails?\b",
)

_OVERCLAIM_RE = re.compile("|".join(_OVERCLAIM_PATTERNS), re.IGNORECASE)


class NoOverclaimGuardrail:
    """Flags marketing overclaims when no evidence_ref is present."""

    name = "no_overclaim"

    def check(self, payload: dict[str, Any]) -> GuardrailResult:
        text = _extract_text(payload)
        evidence_ref = payload.get("evidence_ref") or payload.get("evidence_refs")
        matches = [m.group(0) for m in _OVERCLAIM_RE.finditer(text)]
        if not matches:
            return GuardrailResult(self.name, True, GuardrailSeverity.INFO)
        if evidence_ref:
            return GuardrailResult(
                self.name,
                True,
                GuardrailSeverity.WARN,
                findings=matches,
                detail="overclaim phrasing present but evidence reference supplied",
            )
        return GuardrailResult(
            self.name,
            False,
            GuardrailSeverity.BLOCK,
            findings=matches,
            detail="overclaim phrasing without evidence reference",
        )


# ─────────────────────────────────────────────────────────────
# No sensitive data guardrail
# ─────────────────────────────────────────────────────────────


_SA_NATIONAL_ID_RE = re.compile(r"\b[12]\d{9}\b")
_IBAN_RE = re.compile(r"\bSA\d{2}[A-Z0-9]{18,22}\b", re.IGNORECASE)
_EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")


class NoSensitiveDataGuardrail:
    """Flags SA national IDs, IBANs and non-whitelisted emails."""

    name = "no_sensitive_data"

    def __init__(self, whitelisted_email_domains: set[str] | None = None) -> None:
        self._whitelist = {d.lower() for d in (whitelisted_email_domains or set())}

    def check(self, payload: dict[str, Any]) -> GuardrailResult:
        text = _extract_text(payload)
        findings: list[str] = []
        if hit := _SA_NATIONAL_ID_RE.search(text):
            findings.append(f"sa_national_id:{hit.group(0)}")
        if hit := _IBAN_RE.search(text):
            findings.append(f"iban:{hit.group(0)}")
        for m in _EMAIL_RE.finditer(text):
            email = m.group(0)
            domain = email.rsplit("@", 1)[-1].lower()
            if domain not in self._whitelist:
                findings.append(f"email:{email}")
        if not findings:
            return GuardrailResult(self.name, True, GuardrailSeverity.INFO)
        return GuardrailResult(
            self.name,
            False,
            GuardrailSeverity.BLOCK,
            findings=findings,
            detail="sensitive data detected in outbound payload",
        )


# ─────────────────────────────────────────────────────────────
# No unauthorized pricing
# ─────────────────────────────────────────────────────────────


_PRICE_RE = re.compile(
    r"(?:SAR|ر\.س|﷼|\$|USD|AED|EUR)\s?(\d[\d,]*\.?\d*)|"
    r"(\d[\d,]*\.?\d*)\s?(?:SAR|ر\.س|﷼|\$|USD|AED|EUR)",
    re.IGNORECASE,
)


class NoUnauthorizedPricingGuardrail:
    """Flags currency amounts > threshold without approval_ref."""

    name = "no_unauthorized_pricing"

    def __init__(self, threshold_sar: Decimal | int = 25_000) -> None:
        self._threshold = Decimal(str(threshold_sar))

    def check(self, payload: dict[str, Any]) -> GuardrailResult:
        text = _extract_text(payload)
        amounts: list[Decimal] = []
        for match in _PRICE_RE.finditer(text):
            raw = match.group(1) or match.group(2)
            if raw is None:
                continue
            cleaned = raw.replace(",", "")
            try:
                amounts.append(Decimal(cleaned))
            except Exception:  # pragma: no cover - defensive
                continue
        over = [a for a in amounts if a > self._threshold]
        if not over:
            return GuardrailResult(self.name, True, GuardrailSeverity.INFO)
        if payload.get("approval_ref"):
            return GuardrailResult(
                self.name,
                True,
                GuardrailSeverity.WARN,
                findings=[str(a) for a in over],
                detail="high-value pricing carries approval_ref",
            )
        return GuardrailResult(
            self.name,
            False,
            GuardrailSeverity.BLOCK,
            findings=[str(a) for a in over],
            detail=f"amount over {self._threshold} SAR without approval_ref",
        )


# ─────────────────────────────────────────────────────────────
# No false partnership claims
# ─────────────────────────────────────────────────────────────


_PARTNER_CLAIM_RE = re.compile(
    r"(?i:\bpartner(?:ed|ship|ing)?\s+(?:with|of)\s+)"
    r"([A-Z][A-Za-z0-9&\-]{1,30}(?:\s[A-Z][A-Za-z0-9&\-]{1,30}){0,4})",
)


class NoFalsePartnershipGuardrail:
    """Flags 'partner with X' claims when X is not in the registry."""

    name = "no_false_partnership"

    def __init__(self, registered_partners: set[str] | None = None) -> None:
        self._registered = {p.strip().lower() for p in (registered_partners or set())}

    def check(self, payload: dict[str, Any]) -> GuardrailResult:
        text = _extract_text(payload)
        findings: list[str] = []
        for match in _PARTNER_CLAIM_RE.finditer(text):
            name = match.group(1).strip()
            if name.lower() not in self._registered:
                findings.append(name)
        if not findings:
            return GuardrailResult(self.name, True, GuardrailSeverity.INFO)
        return GuardrailResult(
            self.name,
            False,
            GuardrailSeverity.BLOCK,
            findings=findings,
            detail="partnership claim references entity missing from registry",
        )


# ─────────────────────────────────────────────────────────────
# Chain
# ─────────────────────────────────────────────────────────────


class GuardrailChain:
    """Run an ordered list of Guardrails over a payload."""

    def __init__(self, guardrails: list[Guardrail] | None = None) -> None:
        self._guardrails: list[Guardrail] = list(
            guardrails
            or [
                NoOverclaimGuardrail(),
                NoSensitiveDataGuardrail(),
                NoUnauthorizedPricingGuardrail(),
                NoFalsePartnershipGuardrail(),
            ]
        )

    def add(self, guardrail: Guardrail) -> None:
        self._guardrails.append(guardrail)

    def run_all(self, payload: dict[str, Any]) -> list[GuardrailResult]:
        return [g.check(payload) for g in self._guardrails]

    @staticmethod
    def passed(results: list[GuardrailResult]) -> bool:
        return all(r.passed for r in results)


__all__ = [
    "Guardrail",
    "GuardrailChain",
    "GuardrailResult",
    "GuardrailSeverity",
    "NoFalsePartnershipGuardrail",
    "NoOverclaimGuardrail",
    "NoSensitiveDataGuardrail",
    "NoUnauthorizedPricingGuardrail",
]
