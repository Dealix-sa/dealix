"""Cashflow brief — a 14-day window of expected inflows.

The brief is a derived view. It does NOT move money. It tells the
founder what's likely to land, what's late, and what's at risk.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta, timezone
from typing import Any


@dataclass
class CashflowLine:
    client_name: str
    offer: str
    amount_sar: float
    expected_at: date
    probability: float
    status: str  # one of: expected, late, at_risk, paid

    def to_dict(self) -> dict[str, Any]:
        return {
            "client_name": self.client_name,
            "offer": self.offer,
            "amount_sar": self.amount_sar,
            "expected_at": self.expected_at.isoformat(),
            "probability": self.probability,
            "status": self.status,
        }


@dataclass
class CashflowBrief:
    horizon_days: int
    generated_at: datetime
    expected_inflow_sar: float
    weighted_inflow_sar: float
    late_total_sar: float
    at_risk_total_sar: float
    lines: list[CashflowLine]

    def to_dict(self) -> dict[str, Any]:
        return {
            "horizon_days": self.horizon_days,
            "generated_at": self.generated_at.isoformat(),
            "expected_inflow_sar": round(self.expected_inflow_sar, 2),
            "weighted_inflow_sar": round(self.weighted_inflow_sar, 2),
            "late_total_sar": round(self.late_total_sar, 2),
            "at_risk_total_sar": round(self.at_risk_total_sar, 2),
            "lines": [line.to_dict() for line in self.lines],
        }


def build_brief(
    items: list[dict[str, Any]], horizon_days: int = 14
) -> CashflowBrief:
    """Build the brief from a list of `{client_name, offer, amount_sar,
    expected_at, probability, status?}` records.
    """
    today = datetime.now(UTC).date()
    horizon = today + timedelta(days=horizon_days)

    lines: list[CashflowLine] = []
    for item in items:
        expected_at = item["expected_at"]
        if isinstance(expected_at, str):
            expected_at = date.fromisoformat(expected_at)
        if expected_at > horizon:
            continue
        status = item.get("status") or _infer_status(
            expected_at, today, item.get("probability", 0.5)
        )
        lines.append(
            CashflowLine(
                client_name=item["client_name"],
                offer=item["offer"],
                amount_sar=float(item["amount_sar"]),
                expected_at=expected_at,
                probability=float(item.get("probability", 0.5)),
                status=status,
            )
        )

    expected = sum(line.amount_sar for line in lines if line.status != "paid")
    weighted = sum(
        line.amount_sar * line.probability
        for line in lines
        if line.status != "paid"
    )
    late = sum(line.amount_sar for line in lines if line.status == "late")
    at_risk = sum(line.amount_sar for line in lines if line.status == "at_risk")

    return CashflowBrief(
        horizon_days=horizon_days,
        generated_at=datetime.now(UTC),
        expected_inflow_sar=expected,
        weighted_inflow_sar=weighted,
        late_total_sar=late,
        at_risk_total_sar=at_risk,
        lines=sorted(lines, key=lambda line: line.expected_at),
    )


def _infer_status(expected_at: date, today: date, probability: float) -> str:
    if expected_at < today:
        return "late"
    if probability < 0.4:
        return "at_risk"
    return "expected"
