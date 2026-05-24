"""Guardrails — pre-execution content checks.

These are deterministic, fast, and have no model calls. They run on every
draft message *before* the sovereignty gate. A failed guardrail blocks the
action; the orchestrator records a `RISK_BLOCKED` outcome.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


_FORBIDDEN_CLAIM_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, re.IGNORECASE)
    for p in (
        r"\b(?:guarantee[d]?|guaranteed)\s+(?:results|roi|revenue|leads)\b",
        r"\b(?:partnered|in partnership)\s+with\b",
        r"\b(?:certified|accredited)\s+by\s+(?:saudi|kingdom|nca|sdaia)\b",
        r"\b\d+x\s+(?:return|roi|growth)\s+guaranteed\b",
    )
)

_PII_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p)
    for p in (
        # Saudi national ID (10 digits starting 1 or 2)
        r"\b[12]\d{9}\b",
        # IBAN-like
        r"\bSA\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b",
    )
)


@dataclass(slots=True)
class GuardrailFinding:
    rule_id: str
    severity: str  # info | warn | block
    summary: str
    span: tuple[int, int] | None = None


def scan_overclaim(text: str) -> list[GuardrailFinding]:
    findings: list[GuardrailFinding] = []
    for pat in _FORBIDDEN_CLAIM_PATTERNS:
        for m in pat.finditer(text):
            findings.append(
                GuardrailFinding(
                    rule_id="overclaim",
                    severity="block",
                    summary=f"unverified claim: {m.group(0)!r}",
                    span=m.span(),
                )
            )
    return findings


def scan_pii(text: str) -> list[GuardrailFinding]:
    findings: list[GuardrailFinding] = []
    for pat in _PII_PATTERNS:
        for m in pat.finditer(text):
            findings.append(
                GuardrailFinding(
                    rule_id="pii",
                    severity="block",
                    summary="PII detected in outbound text",
                    span=m.span(),
                )
            )
    return findings


def scan_cold_channel_request(channel: str, opted_in: bool) -> list[GuardrailFinding]:
    if channel.lower() in {"whatsapp", "sms"} and not opted_in:
        return [
            GuardrailFinding(
                rule_id="no_cold_channel",
                severity="block",
                summary=f"cold {channel} requires explicit opt-in",
            )
        ]
    return []


def run_all(text: str, *, channel: str = "email", opted_in: bool = True) -> list[GuardrailFinding]:
    findings: list[GuardrailFinding] = []
    findings.extend(scan_overclaim(text))
    findings.extend(scan_pii(text))
    findings.extend(scan_cold_channel_request(channel, opted_in))
    return findings


def is_blocked(findings: Iterable[GuardrailFinding]) -> bool:
    return any(f.severity == "block" for f in findings)


__all__ = [
    "GuardrailFinding",
    "scan_overclaim",
    "scan_pii",
    "scan_cold_channel_request",
    "run_all",
    "is_blocked",
]
