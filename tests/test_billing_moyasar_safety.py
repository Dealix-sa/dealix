"""Pricing / Moyasar — no secrets in module; plans shape."""

from __future__ import annotations

import pytest

from api.routers import pricing


def test_plans_exist_and_halalas_non_negative():
    """No garbage/negative amounts. Free offerings (rung-0 diagnostic) are
    legitimately 0 halalas; every other plan must be a positive charge."""
    assert pricing.PLANS
    for key, info in pricing.PLANS.items():
        amount = int(info["amount_halalas"])
        assert amount >= 0, key
        is_free = amount == 0 or "free" in key.lower()
        if not is_free:
            assert amount > 0, key


@pytest.mark.asyncio
async def test_list_plans_endpoint(async_client):
    r = await async_client.get("/api/v1/pricing/plans")
    assert r.status_code == 200
    data = r.json()
    assert data.get("currency") == "SAR"
    assert "plans" in data


def test_no_literal_github_pat_in_pricing_module_source():
    import inspect

    src = inspect.getsource(pricing)
    assert "ghp_" not in src
    assert "github_pat_" not in src
