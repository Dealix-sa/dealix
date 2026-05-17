"""Founder operator signals — shared by business-now and founder dashboard."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def build_operator_signals() -> dict[str, Any]:
    from api.routers.founder_dashboard import (
        _friction_last_7d,
        _leads_waiting,
        _pending_approvals,
    )

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "leads_waiting_24h_plus": _leads_waiting(),
        "friction_last_7d": _friction_last_7d(),
        "pending_approvals": _pending_approvals(),
    }
