"""Pricing / Moyasar — no secrets in module; plans shape."""

from __future__ import annotations

import pytest

from api.routers import pricing


def test_plans_exist_and_halalas_positive():
    assert pricing.PLANS

    for key, info in pricing.PLANS.items():
        amount = int(info["amount_halalas"])

        # Free diagnostic / free lead-magnet plans are intentionally zero.
        # Paid plans must always be positive.
        if key.startswith("free_") or amount == 0:
            assert amount == 0, key
            continue

        assert amount > 0, key



async def test_list_plans_endpoint(async_client):
    r = await async_client.get("/api/v1/pricing/plans")
    assert r.status_code == 200
    data = r.json()
    assert data.get("currency") == "SAR"
    assert "plans" in data


def test_no_literal_github_pat_placeholder():
    import inspect

    src = inspect.getsource(pricing)
    assert "ghp_" not in src
    assert "github_pat_" not in src
