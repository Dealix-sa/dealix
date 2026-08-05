"""
Section 51 — Sovereignty.

Dealix ≠ تطبيق. Dealix = Control Plane.
The sovereignty order is the *single* rule that every other layer must respect:

    Sami > Internal > Customer > Partner > Agent > Tool

`SOVEREIGNTY_ORDER` is the canonical list (lowest index = highest authority).
`SovereigntyTier.outranks` is the only function any policy should use to
compare two identities — never compare strings directly.
"""

from __future__ import annotations

from enum import StrEnum


class SovereigntyTier(StrEnum):
    """The six tiers of sovereignty. Lower index = higher authority."""

    SAMI = "sami"
    INTERNAL = "internal"
    CUSTOMER = "customer"
    PARTNER = "partner"
    AGENT = "agent"
    TOOL = "tool"

    @property
    def rank(self) -> int:
        return SOVEREIGNTY_ORDER.index(self)

    def outranks(self, other: SovereigntyTier) -> bool:
        """True if this tier sits strictly above `other`."""
        return self.rank < other.rank

    def at_least(self, other: SovereigntyTier) -> bool:
        """True if this tier is at or above `other`."""
        return self.rank <= other.rank


SOVEREIGNTY_ORDER: tuple[SovereigntyTier, ...] = (
    SovereigntyTier.SAMI,
    SovereigntyTier.INTERNAL,
    SovereigntyTier.CUSTOMER,
    SovereigntyTier.PARTNER,
    SovereigntyTier.AGENT,
    SovereigntyTier.TOOL,
)


def assert_sovereignty(actor: SovereigntyTier, required: SovereigntyTier) -> None:
    """Raise PermissionError unless `actor` sits at or above `required`."""
    if not actor.at_least(required):
        raise PermissionError(
            f"Sovereignty violation: {actor.value} cannot act at level "
            f"{required.value}. Order is: "
            + " > ".join(t.value for t in SOVEREIGNTY_ORDER)
        )
