"""Safety guard for Dealix commercial launch workflows."""

from __future__ import annotations

import os
from dataclasses import dataclass

CANONICAL_FOUNDER_EMAIL = "sami.assiri11@gmail.com"

UNSAFE_ENV_FLAGS = {
    "EXTERNAL_SEND_ENABLED": "true",
    "AUTO_WHATSAPP_ENABLED": "true",
    "AUTO_EMAIL_ENABLED": "true",
    "AUTO_LINKEDIN_ENABLED": "true",
    "AUTO_PAYMENT_CAPTURE_ENABLED": "true",
    "AUTO_MERGE_ENABLED": "true",
    "PRODUCTION_MUTATION_ENABLED": "true",
}

FORBIDDEN_CLAIM_FRAGMENTS = [
    "guaranteed revenue",
    "guarantee revenue",
    "نضمن زيادة الإيرادات",
    "نضمن النتائج",
    "government access",
    "وصول حكومي",
    "closed won",
]


@dataclass(frozen=True)
class SafetyStatus:
    ok: bool
    verdict: str
    violations: list[str]


def detect_env_violations() -> list[str]:
    violations: list[str] = []
    for key, bad_value in UNSAFE_ENV_FLAGS.items():
        if os.getenv(key, "").strip().lower() == bad_value:
            violations.append(f"{key}={bad_value}")
    return violations


def validate_founder_email(email: str) -> SafetyStatus:
    if email == CANONICAL_FOUNDER_EMAIL:
        return SafetyStatus(True, "FOUNDER_EMAIL_OK", [])
    return SafetyStatus(False, "FOUNDER_EMAIL_BLOCKED", [f"unexpected_founder_email={email}"])


def scan_for_forbidden_claims(text: str) -> list[str]:
    lowered = text.lower()
    return [claim for claim in FORBIDDEN_CLAIM_FRAGMENTS if claim.lower() in lowered]


def assert_draft_only_environment() -> SafetyStatus:
    violations = detect_env_violations()
    if violations:
        return SafetyStatus(False, "BLOCKED_BY_SAFETY_GUARD", violations)
    return SafetyStatus(True, "SAFE_TO_RUN_INTERNAL_DRAFT_ONLY", [])


def channel_requires_approval(channel: str) -> bool:
    return channel.strip().lower() in {"email", "whatsapp", "linkedin", "call_script"}
