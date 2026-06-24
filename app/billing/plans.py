"""Billing plan definitions. No live charge is performed here."""

from __future__ import annotations

PLANS = {
    "diagnostic": {"name": "AI Revenue Diagnostic", "currency": "SAR", "range": "0-1500"},
    "sprint_7_day": {
        "name": "7-Day Revenue Command Room Sprint",
        "currency": "SAR",
        "range": "5000-12000",
    },
    "company_brain_14_day": {
        "name": "14-Day Company Brain Sprint",
        "currency": "SAR",
        "range": "15000-35000",
    },
    "managed_os_monthly": {
        "name": "Monthly Managed OS",
        "currency": "SAR",
        "range": "3000-25000",
    },
    "enterprise_custom": {"name": "Enterprise Custom", "currency": "SAR", "range": "quote-based"},
}


def get_plan(code: str) -> dict:
    if code not in PLANS:
        raise KeyError(f"unknown plan: {code}")
    return PLANS[code]
