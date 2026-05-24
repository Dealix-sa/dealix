"""Regression gate: AUTOPILOT_ROUTERS must be registered on the FastAPI app.

History: the 9 split routers in `api/routers/revenue_ops_autopilot.py` were
authored but `app.include_router(...)` was never called, so
`/api/v1/ops-autopilot/*` (founder cockpit, daily-pack, war-room, …) all
404'd in production while the `/ar/ops/founder` frontend rendered empty.

This test fails fast if any subsequent refactor drops the registration.
"""

from __future__ import annotations

from api.main import create_app
from api.routers.revenue_ops_autopilot import AUTOPILOT_ROUTERS


REQUIRED_PATHS = [
    "/api/v1/ops-autopilot/founder/cockpit",
    "/api/v1/ops-autopilot/founder/daily-pack",
    "/api/v1/ops-autopilot/founder/strongest-plan",
    "/api/v1/ops-autopilot/founder/strongest-ops",
    "/api/v1/ops-autopilot/founder/full-autopilot",
    "/api/v1/ops-autopilot/founder/full-autonomous-ops",
    "/api/v1/ops-autopilot/founder/complete-autonomous-day",
    "/api/v1/ops-autopilot/founder/commercial-value-map",
    "/api/v1/ops-autopilot/founder/value-plan",
    "/api/v1/ops-autopilot/founder/evidence/csv-append",
    "/api/v1/ops-autopilot/war-room",
    "/api/v1/ops-autopilot/war-room/today-pack",
    "/api/v1/ops-autopilot/leads",
]


def test_autopilot_routers_export_is_non_empty() -> None:
    assert len(AUTOPILOT_ROUTERS) >= 9, (
        "AUTOPILOT_ROUTERS shrank; was 9 (public/sales/evidence/support/"
        "kb/diag/inv/ops/marketing)"
    )


def test_autopilot_required_paths_in_openapi() -> None:
    app = create_app()
    registered = {r.path for r in app.routes if hasattr(r, "path")}
    missing = [p for p in REQUIRED_PATHS if p not in registered]
    assert not missing, (
        f"AUTOPILOT_ROUTERS not wired into api/main.py; missing paths: {missing}"
    )


def test_autopilot_ops_route_count_meets_floor() -> None:
    app = create_app()
    ops_paths = {r.path for r in app.routes if hasattr(r, "path") and "/ops-autopilot/" in r.path}
    assert len(ops_paths) >= 40, (
        f"Expected ≥40 /api/v1/ops-autopilot/* routes (founder + war-room + "
        f"marketing + leads), found {len(ops_paths)}"
    )
