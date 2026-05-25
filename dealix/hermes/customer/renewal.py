"""Renewal tracking."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, ConfigDict


class Renewal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_id: str
    contract_id: str
    renewal_date: str  # ISO date
    expected_value_sar: float
    notified: bool = False


def upcoming_renewals(renewals: list[Renewal], *, within_days: int = 60) -> list[Renewal]:
    horizon = datetime.now(UTC) + timedelta(days=within_days)
    upcoming: list[Renewal] = []
    for r in renewals:
        try:
            date = datetime.fromisoformat(r.renewal_date.replace("Z", "+00:00"))
        except ValueError:
            continue
        if date <= horizon:
            upcoming.append(r)
    return upcoming
