"""Dealix Autonomous Company Control Plane.

The control plane is the meta-layer above the Company OS. It does not
replace any system (Revenue OS, Delivery OS, Trust OS, Product OS, ...).
It sits above them and answers, every day:

    - What is happening?
    - What needs a decision?
    - What is risky?
    - What is an opportunity?
    - What should we stop?
    - What should we double down on?
    - What evidence backs each call?
    - What is the next decision?

Modules:
    company_state  -- materialise the single source of truth for "company state today"
    action_router  -- classify every proposed action into one of 5 paths
                       (execute / draft / approve / escalate / block)
"""

from control_plane.action_router import (
    ActionPath,
    ActionRouter,
    RoutedAction,
)
from control_plane.company_state import (
    CompanyState,
    DeliveryState,
    LearningState,
    ProductState,
    RevenueState,
    SalesState,
    TrustState,
)

__all__ = [
    "ActionPath",
    "ActionRouter",
    "RoutedAction",
    "CompanyState",
    "DeliveryState",
    "LearningState",
    "ProductState",
    "RevenueState",
    "SalesState",
    "TrustState",
]
