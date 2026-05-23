"""Tests for referral program endpoints (W13.13)."""
from __future__ import annotations

import pytest

ADMIN_HEADER = "X-Admin-API-Key"


async def _create_test_code(async_client, api_key: str = "test_admin_ref_seed") -> str:
    """Helper: create a referral code via the API and return the code string."""
    import os
    _orig = os.environ.get("ADMIN_API_KEYS")
    os.environ["ADMIN_API_KEYS"] = api_key
    try:
        res = await async_client.post(
            "/api/v1/referrals/create",
            json={"referrer_handle": "acme_saas", "referrer_email": "test@acme.sa"},
            headers={ADMIN_HEADER: api_key},
        )
        if res.status_code != 200:
            pytest.skip(f"Could not create test referral code: {res.status_code}")
        return res.json()["code"]
    finally:
        if _orig is None:
            os.environ.pop("ADMIN_API_KEYS", None)
        else:
            os.environ["ADMIN_API_KEYS"] = _orig


@pytest.mark.asyncio
async def test_program_terms_public_no_auth(async_client):
    """Program terms must be publicly visible — referrer reads before sharing."""
    res = await async_client.get("/api/v1/referrals/_program-terms")
    assert res.status_code == 200
    body = res.json()
    assert body["referrer_reward"]["amount_sar"] == 5000
    assert body["referred_reward"]["discount_pct"] == 50
    assert "rules" in body and len(body["rules"]) > 3
    assert "anti_abuse" in body  # anti-abuse rules must be documented


@pytest.mark.asyncio
async def test_create_requires_admin(async_client):
    res = await async_client.post(
        "/api/v1/referrals/create",
        json={"referrer_handle": "acme_saas", "referrer_email": "x@acme.sa"},
    )
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_create_returns_code(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_ref_create")
    res = await async_client.post(
        "/api/v1/referrals/create",
        json={"referrer_handle": "acme_saas", "referrer_email": "founder@acme.sa"},
        headers={ADMIN_HEADER: "test_admin_ref_create"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["code"].startswith("REF-")
    assert len(body["code"]) == 12  # "REF-" + 8 chars
    assert "share_template" in body  # Arabic template provided
    # Email NEVER returned, only hash
    assert "founder@acme.sa" not in str(body)


@pytest.mark.asyncio
async def test_create_validates_handle(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_ref_handle")
    res = await async_client.post(
        "/api/v1/referrals/create",
        json={"referrer_handle": "BAD-HANDLE", "referrer_email": "x@x.sa"},
        headers={ADMIN_HEADER: "test_admin_ref_handle"},
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_create_validates_email(async_client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_ref_email")
    res = await async_client.post(
        "/api/v1/referrals/create",
        json={"referrer_handle": "acme_saas", "referrer_email": "not-an-email"},
        headers={ADMIN_HEADER: "test_admin_ref_email"},
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_verify_code_validates_format(async_client):
    res = await async_client.get("/api/v1/referrals/INVALID")
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_verify_code_returns_discount_terms(async_client):
    code = await _create_test_code(async_client, "test_admin_verify")
    res = await async_client.get(f"/api/v1/referrals/{code}")
    assert res.status_code == 200
    body = res.json()
    assert body["discount_pct"] == 50
    assert "valid_for_plans" in body


@pytest.mark.asyncio
async def test_redeem_validates_inputs(async_client):
    """Redeem needs code + referred_email + referred_company."""
    res = await async_client.post(
        "/api/v1/referrals/redeem",
        json={"code": "REF-12345ABC"},  # missing email/company
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_redeem_success_returns_discount(async_client):
    code = await _create_test_code(async_client, "test_admin_redeem")
    res = await async_client.post(
        "/api/v1/referrals/redeem",
        json={
            "code": code,
            "referred_email": "newcustomer@example.sa",
            "referred_company": "New B2B Co",
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["discount_pct"] == 50
    # Email NEVER echoed
    assert "newcustomer@example.sa" not in str(body)


@pytest.mark.asyncio
async def test_convert_requires_admin(async_client):
    res = await async_client.post("/api/v1/referrals/REF-12345ABC/convert")
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_convert_returns_credit_amount(async_client, monkeypatch):
    code = await _create_test_code(async_client, "test_admin_ref_convert")
    # Redeem first (convert requires a redeemed referral)
    await async_client.post(
        "/api/v1/referrals/redeem",
        json={"code": code, "referred_email": "c@b.sa", "referred_company": "Co B"},
    )
    monkeypatch.setenv("ADMIN_API_KEYS", "test_admin_ref_convert")
    res = await async_client.post(
        f"/api/v1/referrals/{code}/convert",
        headers={ADMIN_HEADER: "test_admin_ref_convert"},
    )
    assert res.status_code == 200
    assert res.json()["referrer_credit_sar"] == 5000
