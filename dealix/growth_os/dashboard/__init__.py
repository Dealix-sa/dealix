"""Growth dashboard — snapshot metrics + red-flag detection."""

from __future__ import annotations

from dealix.growth_os.dashboard.metrics import (
    GrowthDashboardSnapshot,
    build_snapshot,
)
from dealix.growth_os.dashboard.red_flags import (
    RED_FLAG_CATALOG,
    RedFlag,
    detect_red_flags,
)

__all__ = [
    "RED_FLAG_CATALOG",
    "GrowthDashboardSnapshot",
    "RedFlag",
    "build_snapshot",
    "detect_red_flags",
]
