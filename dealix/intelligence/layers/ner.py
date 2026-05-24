"""
NER — bilingual rule + dictionary based named-entity recognition.
استخراج الكيانات بالعربية والإنجليزية بطريقة قواعدية + قاموسية.

Entity types:
    PERSON, ORG, LOCATION, MONEY, PHONE, EMAIL, URL, DATE, PERCENT,
    SECTOR, PRODUCT, COMMERCIAL_REGISTER (CR), VAT_NUMBER

Designed for Saudi B2B context — knows SAR amounts, Saudi phone formats,
سعودية / المملكة العربية السعودية, and the most common sector terms.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from dealix.intelligence.arabic_nlp import normalize_arabic


@dataclass(frozen=True)
class Entity:
    text: str
    label: str
    start: int
    end: int
    score: float = 1.0


# ── Regex patterns (compiled once) ───────────────────────────────────
_RE_EMAIL = re.compile(r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b")
_RE_URL = re.compile(r"\bhttps?://[^\s)>\]]+", re.IGNORECASE)
_RE_PHONE_SA = re.compile(
    r"(?:\+?966|0)\s?5\d{1}\s?\d{3}\s?\d{4}"
)
_RE_PHONE_GENERIC = re.compile(r"\+?\d{1,3}[\s\-]?\d{2,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}")
_RE_MONEY = re.compile(
    r"(?:(?:SAR|ر\.?س|ريال|USD|\$|EUR|€)\s?[\d,]+(?:\.\d+)?(?:\s?(?:[KMB]|الف|ألف|مليون|مليار))?)"
    r"|"
    r"(?:[\d,]+(?:\.\d+)?\s?(?:SAR|ر\.?س|ريال|USD|\$|EUR|€|الف|ألف|مليون|مليار))",
    re.IGNORECASE,
)
_RE_PERCENT = re.compile(r"\b\d+(?:\.\d+)?\s?%|\b\d+(?:\.\d+)?\s?بالمائة|\b\d+(?:\.\d+)?\s?بالمئة")
_RE_VAT = re.compile(r"\b3\d{14}\b")  # Saudi 15-digit VAT TIN starts with 3
_RE_CR = re.compile(r"\b(?:CR|C\.R\.|سجل تجاري|س\.ت\.?|رقم السجل)[\s:#-]*\d{7,12}\b", re.IGNORECASE)
_RE_DATE = re.compile(
    r"\b(?:\d{1,2}[\-/]\d{1,2}[\-/]\d{2,4})\b"
    r"|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{1,2},?\s\d{2,4}\b"
    r"|\b(?:يناير|فبراير|مارس|ابريل|أبريل|مايو|يونيو|يوليو|اغسطس|أغسطس|سبتمبر|اكتوبر|أكتوبر|نوفمبر|ديسمبر)"
    r"\s\d{1,2},?\s?\d{2,4}\b"
)

# ── Gazeteers ────────────────────────────────────────────────────────
_LOCATIONS_AR = {
    "الرياض", "جدة", "جده", "الدمام", "الخبر", "مكة", "المدينة", "تبوك", "الطائف",
    "ابها", "أبها", "بريدة", "حائل", "نجران", "جازان", "ينبع", "الجبيل", "القصيم",
    "السعودية", "المملكة العربية السعودية", "الخليج", "الإمارات", "قطر", "البحرين", "الكويت", "عمان",
}
_LOCATIONS_EN = {
    "riyadh", "jeddah", "dammam", "khobar", "mecca", "medina", "tabuk", "taif",
    "abha", "buraydah", "hail", "najran", "jazan", "yanbu", "jubail", "qassim",
    "saudi arabia", "saudi", "ksa", "gulf", "uae", "qatar", "bahrain", "kuwait", "oman",
}
_SECTORS_AR = {
    "تقنية", "تكنولوجيا", "عقارات", "بناء", "مقاولات", "صحة", "تعليم",
    "تجزئة", "ضيافة", "مطاعم", "لوجستيات", "نقل", "تأمين", "بنوك", "مالية",
    "حكومي", "حكومة", "تصنيع", "تجارة", "اعلام", "إعلام", "ترفيه", "سياحة",
}
_SECTORS_EN = {
    "technology", "tech", "real estate", "construction", "healthcare", "health",
    "education", "retail", "hospitality", "logistics", "transport", "insurance",
    "banking", "finance", "government", "manufacturing", "trade", "media",
    "entertainment", "tourism", "saas", "fintech", "edtech",
}
_ORG_SUFFIXES = {
    "شركة", "مؤسسة", "مجموعة", "بنك", "وكالة",
    "company", "co.", "co", "corp", "corp.", "inc", "inc.", "ltd",
    "llc", "group", "bank", "agency", "labs", "tech", "solutions",
}


class NERTagger:
    """Bilingual rule + dictionary NER tagger."""

    def __init__(self) -> None:
        self._locations = self._build_lower_set(_LOCATIONS_AR, _LOCATIONS_EN)
        self._sectors = self._build_lower_set(_SECTORS_AR, _SECTORS_EN)
        self._org_suffixes = {s.lower() for s in _ORG_SUFFIXES}

    @staticmethod
    def _build_lower_set(*sets: Iterable[str]) -> set[str]:
        out: set[str] = set()
        for s in sets:
            for v in s:
                out.add(v.lower())
                out.add(normalize_arabic(v.lower()))
        return out

    # ── Public API ────────────────────────────────────────────────
    def tag(self, text: str) -> list[Entity]:
        if not text:
            return []
        entities: list[Entity] = []
        self._extract_regex(text, _RE_EMAIL, "EMAIL", entities)
        self._extract_regex(text, _RE_URL, "URL", entities)
        self._extract_regex(text, _RE_PHONE_SA, "PHONE", entities, score=0.95)
        self._extract_regex(text, _RE_PHONE_GENERIC, "PHONE", entities, score=0.7)
        self._extract_regex(text, _RE_MONEY, "MONEY", entities)
        self._extract_regex(text, _RE_PERCENT, "PERCENT", entities)
        self._extract_regex(text, _RE_VAT, "VAT_NUMBER", entities)
        self._extract_regex(text, _RE_CR, "COMMERCIAL_REGISTER", entities)
        self._extract_regex(text, _RE_DATE, "DATE", entities)
        self._extract_gazeteer(text, entities)
        self._extract_orgs(text, entities)
        return self._dedupe(entities)

    def tag_grouped(self, text: str) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for e in self.tag(text):
            out.setdefault(e.label, []).append(e.text)
        return out

    # ── Internals ─────────────────────────────────────────────────
    @staticmethod
    def _extract_regex(
        text: str,
        pattern: re.Pattern[str],
        label: str,
        out: list[Entity],
        *,
        score: float = 0.99,
    ) -> None:
        for m in pattern.finditer(text):
            out.append(Entity(m.group(0).strip(), label, m.start(), m.end(), score))

    def _extract_gazeteer(self, text: str, out: list[Entity]) -> None:
        lower = text.lower()
        norm = normalize_arabic(lower)
        for vocab, label in ((self._locations, "LOCATION"), (self._sectors, "SECTOR")):
            for term in vocab:
                if not term or len(term) < 3:
                    continue
                # Find all occurrences (overlap allowed for short terms).
                start = 0
                hay = lower if any("a" <= c <= "z" for c in term) else norm
                while True:
                    idx = hay.find(term, start)
                    if idx < 0:
                        break
                    # word boundary guard for Latin tokens
                    if any("a" <= c <= "z" for c in term):
                        before = idx == 0 or not lower[idx - 1].isalnum()
                        after = idx + len(term) == len(lower) or not lower[idx + len(term)].isalnum()
                        if not (before and after):
                            start = idx + 1
                            continue
                    out.append(
                        Entity(
                            text=text[idx : idx + len(term)],
                            label=label,
                            start=idx,
                            end=idx + len(term),
                            score=0.8,
                        )
                    )
                    start = idx + len(term)

    def _extract_orgs(self, text: str, out: list[Entity]) -> None:
        # Naive: a capitalized word/phrase followed by an org suffix.
        tokens = text.split()
        i = 0
        while i < len(tokens):
            t = tokens[i].strip(",.;:()[]")
            tl = t.lower()
            if tl in self._org_suffixes and i > 0:
                # Look back 1-3 tokens.
                start = max(0, i - 3)
                phrase = " ".join(tokens[start : i + 1]).strip(",.;:()[]")
                idx = text.find(phrase)
                if idx >= 0:
                    out.append(Entity(phrase, "ORG", idx, idx + len(phrase), 0.65))
            i += 1

    @staticmethod
    def _dedupe(entities: list[Entity]) -> list[Entity]:
        entities.sort(key=lambda e: (e.start, -e.score))
        result: list[Entity] = []
        last_end = -1
        for e in entities:
            if e.start >= last_end:
                result.append(e)
                last_end = e.end
            else:
                # Overlap — keep the one with higher score
                prev = result[-1]
                if e.score > prev.score:
                    result[-1] = e
                    last_end = e.end
        return result
