"""
Sovereign money dashboard — read-only snapshot for Sami.

Pulls from the in-memory outcome/asset stores. No external calls.
"""

from __future__ import annotations

from pydantic import BaseModel

from dealix.hermes.core.assets import default_store as default_asset_store
from dealix.hermes.money.cashflow import CashflowSnapshot, snapshot


class MoneyDashboard(BaseModel):
    cashflow: CashflowSnapshot
    assets_total: int
    pending_approvals: list[str]


def render() -> MoneyDashboard:
    return MoneyDashboard(
        cashflow=snapshot(),
        assets_total=default_asset_store().count(),
        pending_approvals=[],
    )
