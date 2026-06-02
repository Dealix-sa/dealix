"""Template library loader for the WhatsApp Client OS.

Loads ``data/whatsapp/templates.yaml`` and renders a template by key with
simple ``{var}`` substitution. A small embedded fallback keeps rendering
working if the YAML is missing. Templates are for GOVERNED, consented
conversations — never cold sends.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_DEFAULT_PATH = "data/whatsapp/templates.yaml"

# Canonical template keys (kept in sync with templates.yaml).
TEMPLATE_KEYS: tuple[str, ...] = (
    "welcome",
    "assessment_start",
    "assessment_result",
    "permission_request",
    "missing_input",
    "draft_ready",
    "followup_due",
    "proposal_ready",
    "proof_pack_ready",
    "payment_handoff_ready",
    "onboarding_start",
    "weekly_report",
    "renewal_offer",
    "support_escalation",
)

_FALLBACK: dict[str, str] = {
    "welcome": "أهلًا، أنا مساعد Dealix. اختر الخطوة من القائمة.",
    "assessment_start": "تمام. بسأل أسئلة قصيرة — الخطوة {step} من {total}.",
    "assessment_result": "التوصية: {offer_name_ar}. أول خطوة: {next_action_ar}.",
    "permission_request": "نحتاج صلاحية: {system}. الغرض: {purpose_ar}. لا ترسل المفتاح هنا.",
    "missing_input": "ناقصنا: {input_ar}. ارفعه من الرابط الآمن.",
    "draft_ready": "جاهز Draft للمراجعة: «{draft_ar}». اعتمد / عدّل / ارفض.",
    "followup_due": "تذكير متابعة مع {lead_ar} — تحتاج موافقتك قبل الإرسال.",
    "proposal_ready": "جهّزت عرضًا: {offer_name_ar}. راجع واعتمد أو احجز مكالمة.",
    "proof_pack_ready": "جاهز Proof Pack: {proof_title_ar}. كل رقم معه مستوى دليل.",
    "payment_handoff_ready": "جاهز للدفع الآمن: {offer_name_ar}. عبر رابط آمن بعد موافقتك.",
    "onboarding_start": "أهلًا بك كعميل Dealix. نبدأ بإعداد بسيط.",
    "weekly_report": "تقريرك الأسبوعي: {period_ar}. أهم تحسّن: {improvement_ar}.",
    "renewal_offer": "اكتملت قيمة الشهر. أقترح الاستمرار بناءً على النتائج.",
    "support_escalation": "وصل طلبك للدعم. أخبرني إذا تبغى نصعّده لشخص الآن.",
}


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_WHATSAPP_TEMPLATES_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = _REPO_ROOT / p
    return p


@lru_cache(maxsize=1)
def _load() -> dict[str, dict[str, Any]]:
    path = _path()
    if not path.exists():
        return {k: {"body_ar": v} for k, v in _FALLBACK.items()}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        tpls = data.get("templates") or {}
        if isinstance(tpls, dict) and tpls:
            return tpls
    except Exception:
        pass
    return {k: {"body_ar": v} for k, v in _FALLBACK.items()}


def get_template(key: str) -> str:
    tpl = _load().get(key)
    if tpl and isinstance(tpl, dict) and tpl.get("body_ar"):
        return str(tpl["body_ar"]).strip()
    return _FALLBACK.get(key, "")


def render(key: str, /, **kwargs: Any) -> str:
    """Render a template; missing variables are left as-is (no crash)."""
    body = get_template(key)
    if not body:
        return ""
    try:
        return body.format_map(_SafeDict(kwargs))
    except Exception:
        return body


class _SafeDict(dict):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def available_keys() -> list[str]:
    return sorted(_load().keys())


__all__ = ["TEMPLATE_KEYS", "available_keys", "get_template", "render"]
