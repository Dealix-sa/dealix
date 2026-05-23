"""
Risk prioritizer.

Wraps the control-plane RiskEngine output into a stable sort that the
weekly review and the CEO brief both rely on.
"""
from __future__ import annotations

from typing import Iterable

from control_plane.risk_engine import RiskItem


_PRIORITY = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


def prioritize_risks(risks: Iterable[RiskItem]) -> list[RiskItem]:
    return sorted(risks, key=lambda r: (_PRIORITY.get(r.severity, 9), r.code))
