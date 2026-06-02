"""WhatsApp Client OS — template loader.

Loads the bilingual message library from ``templates.yaml`` once (cached),
with an embedded fallback so the layer never hard-fails if the file is
missing. Templates are canned, option-driven replies — not LLM output.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

_TEMPLATES_PATH = Path(__file__).resolve().parent / "templates.yaml"

# Minimal fallback if the YAML is unreadable — keeps the front door working.
_FALLBACK: dict[str, dict[str, str]] = {
    "welcome": {
        "ar": "أهلًا، أنا مساعد Dealix. اختر: 1) فحص 2) متابعة 3) خدمات 5) دعم 6) اقترح علي",
        "en": "Hi, I'm the Dealix assistant. Pick: 1) Scan 2) Follow-up 3) Services 5) Support 6) Recommend",
    },
    "unknown_fallback": {
        "ar": "ما وصلتني الفكرة. اختر رقم من القائمة أو اكتب: اقترح علي.",
        "en": "I didn't get that. Pick a menu number or type: recommend for me.",
    },
}


@lru_cache(maxsize=1)
def _load() -> dict[str, Any]:
    try:
        import yaml  # local import — optional dependency, already in requirements

        data = yaml.safe_load(_TEMPLATES_PATH.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return dict(_FALLBACK)


def t(key: str, lang: str = "ar") -> str:
    """Return template ``key`` in ``lang`` (ar|en), falling back gracefully."""
    entry = _load().get(key) or _FALLBACK.get(key, {})
    if isinstance(entry, dict):
        return str(entry.get(lang, entry.get("ar", ""))).strip()
    return str(entry).strip()


def keys() -> list[str]:
    return sorted(_load().keys())


__all__ = ["keys", "t"]
