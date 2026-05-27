"""The S0..S5 sovereignty ladder.

These six levels are referenced everywhere in Hermes. Their meaning is
fixed and must never be redefined without a sovereign memo.

    S0  Auto Safe     — summaries, classification, drafting only.
    S1  Internal      — internal task / draft creation; non-binding.
    S2  Sami Approval — external send, customer-facing artifact.
    S3  Sovereign     — pricing, contracts, enterprise commitments.
                        Memo  Always needs a written rationale.
    S4  Sovereign     — public APIs, marketplace listings, strategy
                        Only   changes. Sami acts; agents only prepare.
    S5  Never         — money movement, signing on Sami's behalf,
                        Autonomous   anything irreversible. Agents must
                                     refuse.
"""

from __future__ import annotations

from enum import IntEnum
from typing import Iterable


class SovereigntyLevel(IntEnum):
    """Ordered ladder. Higher integer = more sovereign weight."""

    S0_AUTO_SAFE = 0
    S1_INTERNAL = 1
    S2_SAMI_APPROVAL = 2
    S3_SOVEREIGN_MEMO = 3
    S4_SOVEREIGN_ONLY = 4
    S5_NEVER_AUTONOMOUS = 5

    @property
    def label(self) -> str:
        return {
            SovereigntyLevel.S0_AUTO_SAFE: "S0 Auto Safe",
            SovereigntyLevel.S1_INTERNAL: "S1 Internal",
            SovereigntyLevel.S2_SAMI_APPROVAL: "S2 Sami Approval",
            SovereigntyLevel.S3_SOVEREIGN_MEMO: "S3 Sovereign Memo",
            SovereigntyLevel.S4_SOVEREIGN_ONLY: "S4 Sovereign Only",
            SovereigntyLevel.S5_NEVER_AUTONOMOUS: "S5 Never Autonomous",
        }[self]

    @property
    def can_auto_execute(self) -> bool:
        return self <= SovereigntyLevel.S1_INTERNAL

    @property
    def needs_approval(self) -> bool:
        return self in {
            SovereigntyLevel.S2_SAMI_APPROVAL,
            SovereigntyLevel.S3_SOVEREIGN_MEMO,
        }

    @property
    def is_sovereign_only(self) -> bool:
        """S4/S5 — agents may prepare but must never execute."""
        return self >= SovereigntyLevel.S4_SOVEREIGN_ONLY

    @classmethod
    def max(cls, levels: Iterable["SovereigntyLevel"]) -> "SovereigntyLevel":
        """Return the strictest level in a set; default S1."""
        items = list(levels)
        if not items:
            return cls.S1_INTERNAL
        return max(items)


__all__ = ["SovereigntyLevel"]
