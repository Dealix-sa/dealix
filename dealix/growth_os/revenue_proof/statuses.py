"""Revenue lifecycle statuses."""

from __future__ import annotations

from typing import Final, Literal

RevenueStatus = Literal[
    "influenced",
    "pipeline",
    "proposal_sent",
    "committed",
    "invoiced",
    "paid",
    "retainer_active",
]

REVENUE_STATUSES: Final[tuple[RevenueStatus, ...]] = (
    "influenced",
    "pipeline",
    "proposal_sent",
    "committed",
    "invoiced",
    "paid",
    "retainer_active",
)

# Ordered earlier -> later in the funnel. Used for state-transition checks.
_STATUS_ORDER: Final[dict[RevenueStatus, int]] = {
    s: i for i, s in enumerate(REVENUE_STATUSES)
}


def status_rank(status: RevenueStatus) -> int:
    return _STATUS_ORDER[status]


__all__ = ["REVENUE_STATUSES", "RevenueStatus", "status_rank"]
