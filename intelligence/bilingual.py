"""Bilingual AR/EN output layer for Dealix Operating System.

Every OS output is bilingual by default. If Arabic content is not yet authored,
ar_available is set to False so callers never get silently English-only content.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel

LanguageCode = Literal["en", "ar", "both"]


class BilingualText(BaseModel):
    en: str | None = None
    ar: str | None = None
    ar_available: bool = True


class BilingualBlock(BaseModel):
    title: BilingualText
    body: BilingualText
    bullets: list[BilingualText] = []


class BilingualRenderer:
    GOVERNANCE_NOTE = BilingualText(
        en="Draft — requires approval before external use",
        ar="مسودة — تتطلب موافقة قبل الاستخدام الخارجي",
    )

    @staticmethod
    def bt(en: str, ar: str) -> BilingualText:
        return BilingualText(en=en, ar=ar)

    @staticmethod
    def maybe(en: str, ar: str | None = None) -> BilingualText:
        if ar:
            return BilingualText(en=en, ar=ar, ar_available=True)
        return BilingualText(en=en, ar=None, ar_available=False)

    @staticmethod
    def filter_text(text: BilingualText, lang: LanguageCode) -> dict[str, Any]:
        result: dict[str, Any] = {"ar_available": text.ar_available}
        if lang in ("en", "both"):
            result["en"] = text.en
        if lang in ("ar", "both"):
            result["ar"] = text.ar
        return result

    @staticmethod
    def filter_block(block: BilingualBlock, lang: LanguageCode) -> dict[str, Any]:
        return {
            "title": BilingualRenderer.filter_text(block.title, lang),
            "body": BilingualRenderer.filter_text(block.body, lang),
            "bullets": [BilingualRenderer.filter_text(b, lang) for b in block.bullets],
        }

    @staticmethod
    def wrap(payload: dict[str, Any], lang: LanguageCode = "both") -> dict[str, Any]:
        """Inject governance note and keep payload structure."""
        return {
            **payload,
            "governance_note": BilingualRenderer.filter_text(
                BilingualRenderer.GOVERNANCE_NOTE, lang
            ),
            "lang": lang,
        }


# FastAPI dependency
async def get_lang(lang: LanguageCode = "both") -> LanguageCode:
    return lang
