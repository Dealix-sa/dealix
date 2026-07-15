"""Safety guard for the Launch Conversation & Negotiation Engine.

The engine is draft-only and approval-first. This guard refuses to run if any
environment flag would allow automatic external sending, live payment capture,
auto-merge, or production mutation. It never enables anything — it only blocks.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

# Flags that MUST be false/absent for the engine to run in draft-only mode.
# Combines the auto-* flags from the master prompt with the canonical Dealix
# outbound-safety flags from CLAUDE.md / .claude/rules/dealix-safety.md.
BLOCKING_FLAGS: tuple[str, ...] = (
    "EXTERNAL_SEND_ENABLED",
    "EMAIL_SEND_ENABLED",
    "WHATSAPP_SEND_ENABLED",
    "WHATSAPP_ALLOW_LIVE_SEND",
    "SMS_SEND_ENABLED",
    "AUTO_WHATSAPP_ENABLED",
    "AUTO_EMAIL_ENABLED",
    "AUTO_LINKEDIN_ENABLED",
    "AUTO_PAYMENT_CAPTURE_ENABLED",
    "AUTO_MERGE_ENABLED",
    "PRODUCTION_MUTATION_ENABLED",
)

# OUTBOUND_MODE must stay draft_only.
REQUIRED_OUTBOUND_MODE = "draft_only"

_TRUTHY = {"1", "true", "yes", "on", "enabled"}


def _is_truthy(value: str | None) -> bool:
    return value is not None and value.strip().lower() in _TRUTHY


@dataclass
class SafetyResult:
    safe: bool
    verdict: str
    violations: list[str] = field(default_factory=list)
    checked_flags: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, object]:
        return {
            "safe": self.safe,
            "verdict": self.verdict,
            "violations": self.violations,
            "checked_flags": self.checked_flags,
        }


def evaluate_environment(env: dict[str, str] | None = None) -> SafetyResult:
    """Return a SafetyResult describing whether draft-only operation is safe."""
    source = env if env is not None else dict(os.environ)
    violations: list[str] = []

    for flag in BLOCKING_FLAGS:
        if _is_truthy(source.get(flag)):
            violations.append(f"{flag} is enabled — external/auto action not allowed")

    outbound_mode = (source.get("OUTBOUND_MODE") or REQUIRED_OUTBOUND_MODE).strip().lower()
    if outbound_mode != REQUIRED_OUTBOUND_MODE:
        violations.append(
            f"OUTBOUND_MODE={outbound_mode!r} — must be {REQUIRED_OUTBOUND_MODE!r}"
        )

    safe = not violations
    verdict = "SAFE_TO_RUN_INTERNAL_DRAFT_ONLY" if safe else "BLOCKED_BY_SAFETY_GUARD"
    return SafetyResult(
        safe=safe,
        verdict=verdict,
        violations=violations,
        checked_flags=list(BLOCKING_FLAGS) + ["OUTBOUND_MODE"],
    )
