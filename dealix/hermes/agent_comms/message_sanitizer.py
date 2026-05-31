"""
Message sanitizer — strips known prompt-injection patterns and refuses
messages that try to escalate privilege or impersonate the system.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_INJECTION_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"(?i)ignore\s+(all\s+)?previous\s+instructions"), "override_attempt"),
    (re.compile(r"(?i)disregard\s+(all\s+)?(prior|above)\s+instructions"), "override_attempt"),
    (re.compile(r"(?i)you\s+are\s+now\s+a\s+different"), "persona_override"),
    (re.compile(r"(?i)system\s*:\s*"), "system_prompt_spoof"),
    (re.compile(r"(?i)assistant\s*:\s*"), "assistant_role_spoof"),
    (re.compile(r"(?i)act\s+as\s+(an?\s+)?(admin|root|superuser)"), "privilege_escalation"),
    (re.compile(r"(?i)reveal\s+(your|the)\s+(system\s+)?prompt"), "prompt_exfiltration"),
    (
        re.compile(r"(?i)export\s+all\s+\w*\s*(data|records|credentials|customer|user)"),
        "bulk_exfiltration",
    ),
    (re.compile(r"(?i)send\s+to\s+(external|outside|webhook)"), "external_exfiltration"),
    (re.compile(r"(?i)\bcurl\s+https?://"), "outbound_call_attempt"),
    (re.compile(r"<\s*script[^>]*>", re.IGNORECASE), "html_script_injection"),
)

_MAX_LENGTH = 8000


@dataclass
class SanitizationResult:
    safe: bool
    sanitized_text: str
    findings: list[str]


def sanitize_message(text: str) -> SanitizationResult:
    if text is None:
        return SanitizationResult(True, "", [])
    truncated = text[:_MAX_LENGTH]
    findings: list[str] = []
    for pattern, label in _INJECTION_PATTERNS:
        if pattern.search(truncated):
            findings.append(label)
            truncated = pattern.sub("[REDACTED]", truncated)
    # collapse unicode bidi/zero-width tricks
    truncated = re.sub(r"[‪-‮​-‏]", "", truncated)
    return SanitizationResult(
        safe=not findings,
        sanitized_text=truncated,
        findings=findings,
    )
