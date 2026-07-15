"""
PII redaction — PDPL-aligned detect + mask.
طمس البيانات الشخصية وفق نظام حماية البيانات السعودي (PDPL).

Categories detected:
    EMAIL, PHONE, NATIONAL_ID (SA), IBAN, CARD, IP, MAC, URL, NAME_HINT,
    CR_NUMBER (commercial register), VAT_NUMBER

Redaction strategies:
    "mask"    → keep type, replace value with [EMAIL] etc.
    "hash"    → SHA-256 first 10 chars
    "partial" → first 2 / last 2 chars + middle "***"
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Iterable, Literal

RedactionMode = Literal["mask", "hash", "partial"]


@dataclass(frozen=True)
class PIIMatch:
    category: str
    value: str
    start: int
    end: int
    severity: str  # "low" | "medium" | "high"


# Patterns — compiled once.
_PATTERNS: dict[str, tuple[re.Pattern[str], str]] = {
    "EMAIL": (re.compile(r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b"), "high"),
    "PHONE_SA": (re.compile(r"(?:\+?966|0)\s?5\d\s?\d{3}\s?\d{4}"), "high"),
    "PHONE_GENERIC": (
        re.compile(r"\+?\d{1,3}[\s\-]?\(?\d{2,4}\)?[\s\-]?\d{3,4}[\s\-]?\d{3,4}"),
        "medium",
    ),
    "NATIONAL_ID_SA": (re.compile(r"\b[12]\d{9}\b"), "high"),
    "IBAN": (re.compile(r"\bSA\d{2}\s?(?:\d{4}\s?){5}\b"), "high"),
    "CARD": (re.compile(r"\b(?:\d[ \-]?){13,19}\b"), "high"),
    "IP": (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "low"),
    "IPV6": (re.compile(r"\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b"), "low"),
    "MAC": (re.compile(r"\b(?:[0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}\b"), "low"),
    "URL": (re.compile(r"\bhttps?://[^\s)>\]]+", re.IGNORECASE), "low"),
    "CR_NUMBER": (
        re.compile(r"\b(?:CR|C\.R\.|سجل تجاري|س\.ت\.?|رقم السجل)[\s:#\-]*\d{7,12}\b", re.IGNORECASE),
        "medium",
    ),
    "VAT_NUMBER": (re.compile(r"\b3\d{14}\b"), "medium"),
}

# Name-hint markers — single-word names slip through patterns; require a
# preceding cue word to avoid mass false positives.
_NAME_CUES = (
    r"(?:my name is|i am|i'm|this is|اسمي|انا|أنا|اسم[يى] هو|اسم العميل|اسم المسؤول)"
)
_RE_NAME = re.compile(
    rf"\b{_NAME_CUES}\s+([A-Z][a-zA-Z؀-ۿ]{{1,30}}(?:\s+[A-Z][a-zA-Z؀-ۿ]{{1,30}}){{0,3}})",
    re.IGNORECASE,
)


def _validate_card_luhn(value: str) -> bool:
    digits = [int(c) for c in re.sub(r"\D", "", value)]
    if not 13 <= len(digits) <= 19:
        return False
    checksum = 0
    parity = len(digits) % 2
    for i, d in enumerate(digits):
        if i % 2 == parity:
            d = d * 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0


class PIIRedactor:
    """Detect + redact PII with PDPL-aligned categories."""

    def __init__(
        self,
        *,
        categories: Iterable[str] | None = None,
        keep_emails_for_role: bool = False,
    ) -> None:
        self.categories = set(categories) if categories else set(_PATTERNS) | {"NAME"}
        self.keep_emails_for_role = keep_emails_for_role

    # ── Detection ─────────────────────────────────────────────────
    def detect(self, text: str) -> list[PIIMatch]:
        if not text:
            return []
        out: list[PIIMatch] = []
        for cat, (pattern, severity) in _PATTERNS.items():
            if cat not in self.categories and cat.split("_")[0] not in self.categories:
                continue
            for m in pattern.finditer(text):
                value = m.group(0)
                if cat == "CARD" and not _validate_card_luhn(value):
                    continue
                if cat == "EMAIL" and self.keep_emails_for_role:
                    local = value.split("@", 1)[0].lower()
                    if local in {"info", "sales", "support", "admin", "hello", "contact"}:
                        continue
                out.append(PIIMatch(_canonical_category(cat), value, m.start(), m.end(), severity))
        if "NAME" in self.categories:
            for m in _RE_NAME.finditer(text):
                if not m.group(1):
                    continue
                out.append(
                    PIIMatch(
                        "NAME",
                        m.group(1),
                        m.start(1),
                        m.end(1),
                        "medium",
                    )
                )
        return self._dedupe(out)

    # ── Redaction ─────────────────────────────────────────────────
    def redact(self, text: str, *, mode: RedactionMode = "mask") -> tuple[str, list[PIIMatch]]:
        matches = self.detect(text)
        if not matches:
            return text, []
        # Walk back-to-front so positions remain valid.
        out_text = text
        for m in sorted(matches, key=lambda x: x.start, reverse=True):
            replacement = _format_replacement(m, mode)
            out_text = out_text[: m.start] + replacement + out_text[m.end :]
        return out_text, matches

    def has_pii(self, text: str) -> bool:
        return bool(self.detect(text))

    # ── Internals ─────────────────────────────────────────────────
    @staticmethod
    def _dedupe(matches: list[PIIMatch]) -> list[PIIMatch]:
        matches.sort(key=lambda m: (m.start, -(m.end - m.start)))
        result: list[PIIMatch] = []
        last_end = -1
        for m in matches:
            if m.start >= last_end:
                result.append(m)
                last_end = m.end
        return result


def _canonical_category(cat: str) -> str:
    if cat.startswith("PHONE"):
        return "PHONE"
    if cat == "IPV6":
        return "IP"
    return cat


def _format_replacement(m: PIIMatch, mode: RedactionMode) -> str:
    if mode == "mask":
        return f"[{m.category}]"
    if mode == "hash":
        h = hashlib.sha256(m.value.encode("utf-8")).hexdigest()[:10]
        return f"[{m.category}:{h}]"
    if mode == "partial":
        v = m.value
        if len(v) <= 4:
            return f"[{m.category}]"
        return f"{v[:2]}***{v[-2:]}"
    return f"[{m.category}]"
