"""Sovereignty levels — the doctrine."""

from __future__ import annotations

# Re-export the canonical enum from the kernel so callers can import
# from either path without circular dependencies.
from dealix.hermes.kernel.schemas import SovereigntyLevel


_AUTONOMOUS = {SovereigntyLevel.S0_AUTO_SAFE, SovereigntyLevel.S1_INTERNAL}
_HUMAN_REQUIRED = {
    SovereigntyLevel.S2_SAMI_APPROVAL,
    SovereigntyLevel.S3_SOVEREIGN_MEMO,
    SovereigntyLevel.S4_SOVEREIGN_ONLY,
    SovereigntyLevel.S5_NEVER_AUTONOMOUS,
}
_MEMO_REQUIRED = {
    SovereigntyLevel.S3_SOVEREIGN_MEMO,
    SovereigntyLevel.S4_SOVEREIGN_ONLY,
}


def is_autonomous(level: SovereigntyLevel) -> bool:
    return level in _AUTONOMOUS


def requires_human(level: SovereigntyLevel) -> bool:
    return level in _HUMAN_REQUIRED


def requires_memo(level: SovereigntyLevel) -> bool:
    return level in _MEMO_REQUIRED


def is_never_autonomous(level: SovereigntyLevel) -> bool:
    return level == SovereigntyLevel.S5_NEVER_AUTONOMOUS


__all__ = [
    "SovereigntyLevel",
    "is_autonomous",
    "is_never_autonomous",
    "requires_human",
    "requires_memo",
]
