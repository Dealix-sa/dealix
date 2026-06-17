"""Deterministic safety gate for the AI router (V14).

Doctrine-aligned guardrail: no guaranteed-outcome claims, no scraping, no
cold/mass outreach, no auto-send. The scan is a shallow, explainable
substring/regex check — it never calls a model. Both inbound prompts and
generated outputs pass through it.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# Terms that, if requested in a prompt, make the task non-compliant outright.
BANNED_REQUEST_TERMS: tuple[str, ...] = (
    "guarantee",
    "guaranteed",
    "scrape",
    "scraping",
    "cold whatsapp",
    "cold outreach",
    "mass outreach",
    "bulk whatsapp",
    "whatsapp blast",
    "blast",
    "linkedin automation",
    "auto-send",
    "auto send",
    "autosend",
    "نضمن",
    "مضمون",
)

# Claims that must never appear in a generated draft.
BANNED_OUTPUT_TERMS: tuple[str, ...] = (
    "guaranteed",
    "نضمن",
    "مضمون",
    "100% money-back",
    "risk-free",
    "auto-send",
    "autosend",
)

_GUARANTEE_RE = re.compile(r"\bguarantee(d|s)?\b", re.IGNORECASE)


@dataclass
class SafetyResult:
    passed: bool
    reasons: list[str] = field(default_factory=list)


def _scan(text: str, terms: tuple[str, ...]) -> list[str]:
    low = (text or "").lower()
    hits = [t for t in terms if t.lower() in low]
    if _GUARANTEE_RE.search(text or "") and "guarantee" not in hits and "guaranteed" not in hits:
        hits.append("guarantee")
    return hits


def scan_prompt(prompt: str) -> SafetyResult:
    """Refuse prompts that ask for banned behaviour."""
    hits = _scan(prompt, BANNED_REQUEST_TERMS)
    if hits:
        return SafetyResult(False, [f"prompt requests banned behaviour: {', '.join(sorted(set(hits)))}"])
    return SafetyResult(True, [])


def scan_output(text: str) -> SafetyResult:
    """Refuse outputs that contain banned claims."""
    hits = _scan(text, BANNED_OUTPUT_TERMS)
    if hits:
        return SafetyResult(False, [f"output contains banned claim: {', '.join(sorted(set(hits)))}"])
    return SafetyResult(True, [])
