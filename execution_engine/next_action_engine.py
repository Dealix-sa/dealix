from __future__ import annotations

"""Pick the single highest-leverage next action from a list of checks."""

from .evidence_checker import EvidenceCheck

# Higher priority first. The first matching prefix wins.
_PRIORITY_ORDER: tuple[str, ...] = (
    "Payment",
    "1 proposal",
    "3 client samples",
    "25 DMs",
    "25 qualified leads",
    "Weekly learning",
    "One system update",
)


def _priority(check: EvidenceCheck) -> int:
    for idx, prefix in enumerate(_PRIORITY_ORDER):
        if check.criterion.startswith(prefix):
            return idx
    return len(_PRIORITY_ORDER)


def compute_next_action(checks: list[EvidenceCheck]) -> str:
    """Return a single one-line directive, or an empty string if all pass."""
    unfulfilled = [c for c in checks if c.status != "pass"]
    if not unfulfilled:
        return "All criteria pass. Run 'dealix advance' to move to the next stage."
    unfulfilled.sort(key=_priority)
    head = unfulfilled[0]
    action = head.next_action or f"Complete: {head.criterion}"
    return f"Next: {action}"
