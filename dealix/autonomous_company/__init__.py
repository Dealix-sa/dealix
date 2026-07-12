"""Dealix Autonomous Company OS — a self-operating commercial loop.

This package makes Dealix behave like a company that runs itself: it keeps a
durable memory of every deal, decides the next-best action for each account each
cycle, advances the pipeline through the real evidence chain, tracks recognized
revenue and forecast, and produces a single Command Room brief for the founder.

Hard safety line (inherited from the Strategy Execution OS):
    - Every external-facing action is a DRAFT queued for human approval.
    - No message is sent, nothing is published, no customer is charged.
    - Revenue is recognized only on a real `payment_received` event.
    - No fake customers, no fabricated results.
"""

from __future__ import annotations

from .company_os import CycleResult, run_cycle
from .schemas import Deal, DealStage, KPIs

__all__ = ["Deal", "DealStage", "KPIs", "run_cycle", "CycleResult"]
