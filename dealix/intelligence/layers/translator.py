"""
Translator — pluggable AR↔EN with dictionary fallback + custom glossary.
مترجم ثنائي اللغة بقاموس قابل للتوسعة.

Real LLM-backed translation is delegated to the LLM gateway when present.
This module guarantees a deterministic fallback so unit tests + offline
ops never depend on network. Dealix-specific business glossary is shipped
inline so brand/product terms translate consistently.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, Literal

from dealix.intelligence.arabic_nlp import arabic_ratio, normalize_arabic

Direction = Literal["ar->en", "en->ar", "auto"]

# Dealix business glossary (extend freely; keys normalized lower).
_GLOSSARY_AR_TO_EN: dict[str, str] = {
    "ديالكس": "Dealix",
    "جواز قرار": "decision passport",
    "حزمة دليل": "proof pack",
    "ورشة عمل": "workshop",
    "تشخيص مجاني": "free diagnostic",
    "اشتراك شهري": "monthly retainer",
    "عميل": "customer",
    "عملاء": "customers",
    "موعد": "meeting",
    "اجتماع": "meeting",
    "اقتراح": "proposal",
    "عرض سعر": "quote",
    "سعر": "price",
    "اسعار": "pricing",
    "ميزانية": "budget",
    "اشتراك": "subscription",
    "قطاع": "sector",
    "السعودية": "Saudi Arabia",
    "الرياض": "Riyadh",
    "جدة": "Jeddah",
    "الدمام": "Dammam",
    "تكامل": "integration",
    "حوكمة": "governance",
    "موافقة": "approval",
    "تنبيه": "alert",
    "إنذار": "alert",
    "نعم": "yes",
    "لا": "no",
    "شكرا": "thank you",
    "مرحبا": "hello",
    "مع السلامة": "goodbye",
    "السلام عليكم": "peace be upon you",
    "وعليكم السلام": "and peace be upon you",
    "تكنولوجيا": "technology",
    "تقنية": "technology",
    "صحة": "healthcare",
    "تعليم": "education",
    "عقارات": "real estate",
    "تجزئة": "retail",
    "بنوك": "banks",
    "حكومي": "government",
}

_GLOSSARY_EN_TO_AR = {v.lower(): k for k, v in _GLOSSARY_AR_TO_EN.items()}

_WORD_RE = re.compile(r"\b\w+\b|[^\w\s]", re.UNICODE)


@dataclass(frozen=True)
class TranslationResult:
    text: str
    source: Literal["ar", "en", "unknown"]
    target: Literal["ar", "en"]
    backend: str  # "glossary" | "llm:<name>"
    confidence: float  # 0..1 fraction of tokens covered by glossary


LLMTranslateFn = Callable[[str, str, str], str]  # (text, src, tgt) -> str


class Translator:
    """Glossary-first translator with optional LLM upgrade."""

    def __init__(
        self,
        *,
        custom_glossary: dict[str, str] | None = None,
        llm_translate: LLMTranslateFn | None = None,
    ) -> None:
        self._ar_en = dict(_GLOSSARY_AR_TO_EN)
        self._en_ar = dict(_GLOSSARY_EN_TO_AR)
        if custom_glossary:
            for src, tgt in custom_glossary.items():
                s = normalize_arabic(src.lower())
                t = tgt
                # heuristically detect direction by character set of src
                if arabic_ratio(src) >= 0.3:
                    self._ar_en[s] = t
                    self._en_ar[t.lower()] = src
                else:
                    self._en_ar[s] = t
                    self._ar_en[normalize_arabic(t.lower())] = src
        self._llm = llm_translate

    # ── Public ─────────────────────────────────────────────────────
    def detect_language(self, text: str) -> Literal["ar", "en", "unknown"]:
        if not text:
            return "unknown"
        ratio = arabic_ratio(text)
        if ratio >= 0.3:
            return "ar"
        latin = sum(1 for c in text if c.isalpha() and c.isascii())
        if latin / max(len(text), 1) >= 0.2:
            return "en"
        return "unknown"

    def translate(self, text: str, *, direction: Direction = "auto") -> TranslationResult:
        if not text or not text.strip():
            return TranslationResult("", "unknown", "en", "glossary", 0.0)
        src = self.detect_language(text) if direction == "auto" else (
            "ar" if direction.startswith("ar") else "en"
        )
        tgt: Literal["ar", "en"]
        if direction == "ar->en":
            tgt = "en"
        elif direction == "en->ar":
            tgt = "ar"
        else:
            tgt = "en" if src == "ar" else "ar"
        # Try LLM first if provided.
        if self._llm is not None:
            try:
                out = self._llm(text, src or "auto", tgt)
                if out and out.strip():
                    return TranslationResult(out.strip(), src, tgt, "llm", 1.0)
            except Exception:  # pragma: no cover
                pass
        return self._glossary_translate(text, src, tgt)

    # ── Internals ──────────────────────────────────────────────────
    def _glossary_translate(
        self,
        text: str,
        src: Literal["ar", "en", "unknown"],
        tgt: Literal["ar", "en"],
    ) -> TranslationResult:
        gloss = self._ar_en if src == "ar" else self._en_ar
        tokens = _WORD_RE.findall(text)
        if not tokens:
            return TranslationResult(text, src, tgt, "glossary", 0.0)
        out: list[str] = []
        hits = 0
        for tok in tokens:
            key = normalize_arabic(tok.lower()) if src == "ar" else tok.lower()
            if key in gloss:
                hits += 1
                out.append(gloss[key])
            else:
                out.append(tok)
        confidence = hits / max(len(tokens), 1)
        return TranslationResult(_join_tokens(out), src, tgt, "glossary", round(confidence, 3))


def _join_tokens(tokens: list[str]) -> str:
    out: list[str] = []
    for tok in tokens:
        if out and tok and tok[0].isalnum():
            out.append(" ")
        elif out and not tok[0].isalnum() and out[-1] == " ":
            out.pop()
        out.append(tok)
    return "".join(out).strip()
