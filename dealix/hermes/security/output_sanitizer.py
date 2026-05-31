"""
Output Sanitizer — تنظيف المخرجات قبل التسليم.

يزيل:
    - معرّفات وطنية سعودية (يبدأ بـ 1 أو 2 ثم 9 أرقام).
    - IBAN السعودي SA + 22 رقمًا.
    - بطاقات ائتمان 13-16 رقمًا.
    - عناوين البريد الإلكتروني.
    - الرموز التحكّمية (control chars) وعرض الصفر (zero-width).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Removal:
    kind: str
    original: str
    span: tuple[int, int]


@dataclass
class SanitizedOutput:
    text: str
    removals: list[Removal] = field(default_factory=list)


# Patterns — مرتبّة بالأولويّة (الأكثر تحديدًا أوّلاً).
_SAUDI_ID_RE = re.compile(r"(?<!\d)[12]\d{9}(?!\d)")
_IBAN_SA_RE = re.compile(r"\bSA\d{22}\b")
_CREDIT_CARD_RE = re.compile(r"(?<!\d)(?:\d[ -]?){12,15}\d(?!\d)")
_EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"
)

# Control chars (ما عدا \t \n \r) + zero-width chars.
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_ZERO_WIDTH_RE = re.compile(r"[​-‏‪-‮⁠﻿]")


def _luhn_valid(digits: str) -> bool:
    """Luhn check للحدّ من false positives على أرقام عشوائية."""
    nums = [int(c) for c in digits if c.isdigit()]
    if len(nums) < 13 or len(nums) > 19:
        return False
    checksum = 0
    parity = len(nums) % 2
    for idx, val in enumerate(nums):
        if idx % 2 == parity:
            val *= 2
            if val > 9:
                val -= 9
        checksum += val
    return checksum % 10 == 0


class OutputSanitizer:
    """واجهة موحَّدة لتنظيف المخرجات."""

    def sanitize(self, text: str) -> SanitizedOutput:
        if not isinstance(text, str):
            raise TypeError("text must be str")

        removals: list[Removal] = []
        working = text

        working, ibans = self._apply(working, _IBAN_SA_RE, "iban_sa", "[REDACTED_IBAN]")
        removals.extend(ibans)

        working, saudi_ids = self._apply(
            working, _SAUDI_ID_RE, "saudi_national_id", "[REDACTED_ID]"
        )
        removals.extend(saudi_ids)

        # بطاقات ائتمان — نطبّق Luhn لتقليل الـ false positives.
        working, cards = self._apply_with_predicate(
            working,
            _CREDIT_CARD_RE,
            "credit_card",
            "[REDACTED_CARD]",
            predicate=lambda match_text: _luhn_valid(match_text),
        )
        removals.extend(cards)

        working, emails = self._apply(working, _EMAIL_RE, "email", "[REDACTED_EMAIL]")
        removals.extend(emails)

        # Control + zero-width — تُزال بلا بديل.
        working, controls = self._apply(working, _CONTROL_RE, "control_char", "")
        removals.extend(controls)
        working, zws = self._apply(working, _ZERO_WIDTH_RE, "zero_width", "")
        removals.extend(zws)

        return SanitizedOutput(text=working, removals=removals)

    @staticmethod
    def _apply(
        text: str,
        pattern: re.Pattern[str],
        kind: str,
        replacement: str,
    ) -> tuple[str, list[Removal]]:
        removals: list[Removal] = []
        # نُسجّل المواقع قبل الاستبدال.
        for match in pattern.finditer(text):
            removals.append(
                Removal(kind=kind, original=match.group(0), span=match.span())
            )
        if removals:
            text = pattern.sub(replacement, text)
        return text, removals

    @staticmethod
    def _apply_with_predicate(
        text: str,
        pattern: re.Pattern[str],
        kind: str,
        replacement: str,
        *,
        predicate,
    ) -> tuple[str, list[Removal]]:
        removals: list[Removal] = []
        pieces: list[str] = []
        cursor = 0
        for match in pattern.finditer(text):
            original = match.group(0)
            if predicate(original):
                pieces.append(text[cursor : match.start()])
                pieces.append(replacement)
                removals.append(
                    Removal(kind=kind, original=original, span=match.span())
                )
                cursor = match.end()
        pieces.append(text[cursor:])
        return ("".join(pieces) if removals else text), removals


__all__ = ["OutputSanitizer", "Removal", "SanitizedOutput"]
