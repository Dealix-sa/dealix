"""Smoke tests for the Autonomous Company Control Plane."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_company_state_to_dict_round_trip() -> None:
    from control_plane import CompanyState

    state = CompanyState()
    data = state.to_dict()
    # Serialisable to JSON without custom encoders.
    json.dumps(data)
    # Top-level blocks documented in COMPANY_STATE_SCHEMA.md.
    for key in ("revenue", "sales", "delivery", "trust", "product", "learning", "as_of"):
        assert key in data


def test_red_signals_fire_on_a3_attempt() -> None:
    from control_plane import CompanyState

    state = CompanyState()
    state.trust.a3_blocked_actions = 1
    assert "A3 action attempted" in state.red_signals()


def test_red_signals_fire_on_blocked_paid_delivery() -> None:
    from control_plane import CompanyState

    state = CompanyState()
    state.delivery.blocked_deliveries = 1
    state.product.ci_status = "broken"
    reds = state.red_signals()
    assert "paid delivery blocked" in reds
    assert "CI broken on main" in reds


def test_yellow_signals_fire_on_replies_without_calls() -> None:
    from control_plane import CompanyState

    state = CompanyState()
    state.sales.replies = 3
    state.sales.calls_booked = 0
    assert "replies without follow-up calls" in state.yellow_signals()


@pytest.mark.parametrize(
    ("action", "expected"),
    [
        ("update CRM stage for ACME", "execute"),
        ("draft outreach message for ERP segment", "draft"),
        ("send proposal to client", "approve"),
        ("review compliance claim", "escalate"),
        ("guaranteed revenue claim", "block"),
        ("totally unknown action", "escalate"),  # safe default
    ],
)
def test_action_router_paths(action: str, expected: str) -> None:
    from control_plane import ActionRouter

    routed = ActionRouter().route(action)
    assert routed.path.value == expected


def test_verify_company_os_passes() -> None:
    """Running scripts/verify_company_os.py against the repo must pass."""

    result = subprocess.run(
        [sys.executable, "scripts/verify_company_os.py", "--json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
    data = json.loads(result.stdout)
    assert data["all_pass"] is True
    assert data["import_smoke"]["pass"] is True
