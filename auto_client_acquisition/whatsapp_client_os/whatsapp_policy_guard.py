"""Policy guard for the WhatsApp Client OS.

Wraps the existing platform guardrails (never reimplements them):
- ``channel_policy_gateway`` for the WhatsApp 4-condition customer-outbound rule.
- ``safe_send_gateway.doctrine`` for the non-negotiables.

Adds two WhatsApp-specific protections:
1. SECRETS-IN-CHAT detection — API keys / tokens / passwords must never be
   typed into WhatsApp. We detect them, refuse to store the value, and steer
   the client to a secure portal link.
2. Unsafe-request detection — cold WhatsApp, blasts, scraping and LinkedIn
   automation requested in free text are blocked with a safe alternative.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from auto_client_acquisition.channel_policy_gateway.policy import check_channel_policy
from auto_client_acquisition.channel_policy_gateway.schemas import PolicyDecision
from auto_client_acquisition.safe_send_gateway.doctrine import (
    doctrine_violations_for_revenue_intelligence,
)

# ── Secret / credential patterns (value is NEVER logged or stored) ────────
_SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("openai_key", re.compile(r"\bsk-[A-Za-z0-9_\-]{16,}\b")),
    ("anthropic_key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{16,}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{12,}\b")),
    ("hubspot_pat", re.compile(r"\bpat-[a-z0-9]{2,}-[A-Za-z0-9\-]{8,}\b", re.IGNORECASE)),
    ("bearer_token", re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{16,}\b", re.IGNORECASE)),
    ("generic_long_token", re.compile(r"\b[A-Za-z0-9_\-]{32,}\b")),
    (
        "key_assignment",
        re.compile(
            r"\b(api[_\- ]?key|secret|token|password|كلمة\s*السر|المفتاح)\b\s*[:=]\s*\S{6,}",
            re.IGNORECASE,
        ),
    ),
)

# ── Unsafe-intent patterns in free text (Arabic + English) ───────────────
_UNSAFE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "cold_whatsapp",
        re.compile(
            r"\b(cold\s+whatsapp|cold\s+outreach)\b|واتساب\s+بارد|أرسل\s+لكل\s+الأرقام",
            re.IGNORECASE,
        ),
    ),
    (
        "broadcast_blast",
        re.compile(
            r"\b(broadcast|blast|mass\s+message)\b|رسالة\s+جماعيّ?ة|أرسل\s+للجميع|أرسل\s+لكافة",
            re.IGNORECASE,
        ),
    ),
    ("purchased_list", re.compile(r"\bpurchased\s+list\b|قائمة\s+(مشتراة|مشتراه)", re.IGNORECASE)),
    ("scraping", re.compile(r"\bscrap(e|ing)\b|harvest|اسحب\s+الأرقام|اخترق|اكشط", re.IGNORECASE)),
    (
        "linkedin_automation",
        re.compile(
            r"\blinkedin\s+(automation|bot|auto)\b|أتمتة\s+لينكدإن|بوت\s+لينكدإن", re.IGNORECASE
        ),
    ),
)


@dataclass(frozen=True, slots=True)
class SecretScan:
    found: bool
    kinds: tuple[str, ...] = ()
    refusal_ar: str = ""
    secure_portal_alternative_ar: str = ""


@dataclass(frozen=True, slots=True)
class UnsafeScan:
    blocked: bool
    reasons: tuple[str, ...] = ()
    reason_ar: str = ""
    safe_alternative_ar: str = ""


@dataclass(frozen=True, slots=True)
class GuardResult:
    allowed: bool
    secret_scan: SecretScan
    unsafe_scan: UnsafeScan
    doctrine_violations: tuple[str, ...] = field(default_factory=tuple)


def scan_for_secrets(text: str) -> SecretScan:
    """Detect credentials in client text. The matched VALUE is never returned."""
    if not text:
        return SecretScan(found=False)
    kinds: list[str] = []
    for name, pat in _SECRET_PATTERNS:
        if pat.search(text):
            kinds.append(name)
    if not kinds:
        return SecretScan(found=False)
    return SecretScan(
        found=True,
        kinds=tuple(dict.fromkeys(kinds)),  # de-dup, keep order
        refusal_ar=(
            "لا ترسل المفاتيح أو كلمات السر هنا في واتساب — لأمان بياناتك لا نحفظها في الشات."
        ),
        secure_portal_alternative_ar=(
            "افتح الرابط الآمن لإدخال المفتاح، أو اطلب خطوات الربط اليدوية، أو امنحنا صلاحية قراءة فقط."
        ),
    )


def scan_for_unsafe_request(text: str) -> UnsafeScan:
    """Block cold WhatsApp / blasts / scraping / LinkedIn automation requests."""
    if not text:
        return UnsafeScan(blocked=False)
    reasons: list[str] = []
    for name, pat in _UNSAFE_PATTERNS:
        if pat.search(text):
            reasons.append(name)
    if not reasons:
        return UnsafeScan(blocked=False)
    return UnsafeScan(
        blocked=True,
        reasons=tuple(dict.fromkeys(reasons)),
        reason_ar="ممنوع: واتساب بارد أو إرسال جماعي أو scraping أو أتمتة LinkedIn.",
        safe_alternative_ar="نتواصل فقط مع جهات على علاقة قائمة، بمسودة + موافقة صريحة منك.",
    )


def guard_inbound(text: str) -> GuardResult:
    """Full inbound guard: secrets + unsafe-request + doctrine mapping."""
    secret = scan_for_secrets(text)
    unsafe = scan_for_unsafe_request(text)
    codes, _ = doctrine_violations_for_revenue_intelligence(
        request_cold_whatsapp="cold_whatsapp" in unsafe.reasons
        or "broadcast_blast" in unsafe.reasons,
        request_linkedin_automation="linkedin_automation" in unsafe.reasons,
        request_scraping="scraping" in unsafe.reasons,
        request_bulk_outreach="broadcast_blast" in unsafe.reasons
        or "purchased_list" in unsafe.reasons,
    )
    allowed = not secret.found and not unsafe.blocked
    return GuardResult(
        allowed=allowed,
        secret_scan=secret,
        unsafe_scan=unsafe,
        doctrine_violations=tuple(codes),
    )


def evaluate_outbound(
    *,
    consent_record_exists: bool = False,
    approved_template_or_24h_window: bool = False,
    human_approved: bool = False,
) -> PolicyDecision:
    """Delegate any client-bound WhatsApp send to the canonical channel policy.

    ``live_gate_true`` is intentionally never set here — the Client OS never
    flips the live gate; the best possible outcome is ``approved_manual``.
    """
    return check_channel_policy(
        channel="whatsapp",
        action_kind="send_live",
        consent_record_exists=consent_record_exists,
        approved_template_or_24h_window=approved_template_or_24h_window,
        live_gate_true=False,
        human_approved=human_approved,
    )


__all__ = [
    "GuardResult",
    "SecretScan",
    "UnsafeScan",
    "evaluate_outbound",
    "guard_inbound",
    "scan_for_secrets",
    "scan_for_unsafe_request",
]
