"""WhatsApp Client OS — Permission OS.

Graduated permission ladder (L0-L5) plus the hard rule that **secrets are
never collected in WhatsApp text**. Any integration that needs an API key,
token, or credential is routed to the Secure Client Portal; if a client
pastes secret-looking material into the chat, it must be redacted and the
client guided to the portal instead.

This module is deterministic (regex + table lookups). It does not call an
LLM and never persists raw secret material.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from auto_client_acquisition.whatsapp_client_os.schemas import (
    PermissionLevel,
    permission_rank,
)

# --- Level descriptions (bilingual) ----------------------------------------

PERMISSION_LEVELS: dict[str, dict[str, str]] = {
    PermissionLevel.L0_CHAT_ONLY.value: {
        "ar": "محادثة فقط — بدون أي صلاحيات.",
        "en": "Chat only — no permissions.",
    },
    PermissionLevel.L1_CLIENT_UPLOAD.value: {
        "ar": "رفع ملف أو رابط من العميل.",
        "en": "Client-provided file or link upload.",
    },
    PermissionLevel.L2_CRM_READ.value: {
        "ar": "قراءة فقط من CRM أو جدول (عبر البوابة الآمنة).",
        "en": "Read-only from CRM or sheet (via secure portal).",
    },
    PermissionLevel.L3_CREATE_DRAFTS.value: {
        "ar": "إنشاء مسودات ومهام داخلية.",
        "en": "Create internal drafts and tasks.",
    },
    PermissionLevel.L4_SEND_AFTER_APPROVAL.value: {
        "ar": "إرسال بعد موافقة صريحة على كل نوع.",
        "en": "Send after explicit per-type approval.",
    },
    PermissionLevel.L5_SENSITIVE.value: {
        "ar": "دفع وعقود وبيانات حساسة — لا يتم عبر واتساب.",
        "en": "Payment, contracts, sensitive data — never over WhatsApp.",
    },
}

# Action -> minimum level required.
_ACTION_REQUIRED_LEVEL: dict[str, PermissionLevel] = {
    "chat": PermissionLevel.L0_CHAT_ONLY,
    "upload_file": PermissionLevel.L1_CLIENT_UPLOAD,
    "read_crm": PermissionLevel.L2_CRM_READ,
    "create_draft": PermissionLevel.L3_CREATE_DRAFTS,
    "send_after_approval": PermissionLevel.L4_SEND_AFTER_APPROVAL,
    "payment": PermissionLevel.L5_SENSITIVE,
    "sign_contract": PermissionLevel.L5_SENSITIVE,
    "sensitive_data": PermissionLevel.L5_SENSITIVE,
}

# Actions that may only be granted through the Secure Client Portal, never by
# a WhatsApp reply (anything touching external systems or secrets).
_PORTAL_ONLY_ACTIONS = frozenset(
    {"read_crm", "send_after_approval", "payment", "sign_contract", "sensitive_data"}
)

# --- Secret material detection ---------------------------------------------
# Patterns that strongly indicate a credential/secret was pasted into chat.
_SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bsk-[A-Za-z0-9]{16,}\b"),  # OpenAI-style
    re.compile(r"\b(?:pat|ghp|gho|ghs)_[A-Za-z0-9]{16,}\b"),  # token prefixes
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),  # Slack
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),  # AWS access key id
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]{20,}\b", re.IGNORECASE),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{6,}\b"),  # JWT
    re.compile(r"\b[A-Za-z0-9_-]{32,}\b"),  # long opaque token
    re.compile(r"\b(?:\d[ -]?){13,19}\b"),  # card-like number
)

# Cues that an integration is being discussed (so we proactively offer the
# portal instead of ever asking for a key in text).
_INTEGRATION_CUES: tuple[re.Pattern[str], ...] = (
    re.compile(r"hubspot|salesforce|zoho|pipedrive|crm", re.IGNORECASE),
    re.compile(r"api\s*key|apikey|access\s*token|client\s*secret|webhook\s*secret", re.IGNORECASE),
    re.compile(r"ربط|تكامل|أربط|اربط|مفتاح|توكن|صلاحي", re.IGNORECASE),
)


@dataclass(frozen=True, slots=True)
class SecretGuardResult:
    contains_secret: bool
    mentions_integration: bool
    reason_ar: str
    reason_en: str

    @property
    def route_to_portal(self) -> bool:
        return self.contains_secret or self.mentions_integration


def looks_like_secret(text: str) -> bool:
    """True when text contains credential/secret-looking material."""
    if not text:
        return False
    return any(p.search(text) for p in _SECRET_PATTERNS)


def mentions_integration(text: str) -> bool:
    """True when the message discusses connecting an external system."""
    if not text:
        return False
    return any(p.search(text) for p in _INTEGRATION_CUES)


def secret_guard(text: str) -> SecretGuardResult:
    """Classify a message for secret material / integration intent.

    The brain uses this to: (a) never echo or persist secret material, and
    (b) route any integration to the Secure Client Portal rather than asking
    for credentials in WhatsApp text.
    """
    has_secret = looks_like_secret(text)
    has_integration = mentions_integration(text)
    if has_secret:
        return SecretGuardResult(
            contains_secret=True,
            mentions_integration=has_integration,
            reason_ar="لأمانك لا نستقبل المفاتيح أو الأسرار هنا؛ استخدم البوابة الآمنة.",
            reason_en="For your safety we never accept keys or secrets here; use the secure portal.",
        )
    if has_integration:
        return SecretGuardResult(
            contains_secret=False,
            mentions_integration=True,
            reason_ar="الربط يتم عبر البوابة الآمنة، وليس برسالة واتساب.",
            reason_en="Integrations are done via the secure portal, not a WhatsApp message.",
        )
    return SecretGuardResult(False, False, "", "")


def required_level_for(action: str) -> PermissionLevel:
    return _ACTION_REQUIRED_LEVEL.get(action, PermissionLevel.L5_SENSITIVE)


def can_perform(current_level: PermissionLevel | str, action: str) -> bool:
    """Whether the current granted level is sufficient for an action."""
    needed = required_level_for(action)
    return permission_rank(current_level) >= permission_rank(needed)


def requires_secure_portal(action: str) -> bool:
    """True when an action may only be authorized through the portal."""
    return action in _PORTAL_ONLY_ACTIONS


def describe_level(level: PermissionLevel | str, lang: str = "ar") -> str:
    value = level.value if isinstance(level, PermissionLevel) else str(level)
    entry = PERMISSION_LEVELS.get(value, {})
    return entry.get(lang, entry.get("ar", value))


__all__ = [
    "PERMISSION_LEVELS",
    "SecretGuardResult",
    "can_perform",
    "describe_level",
    "looks_like_secret",
    "mentions_integration",
    "required_level_for",
    "requires_secure_portal",
    "secret_guard",
]
