"""The founder-internal admin gate must fail closed in production.

Three routers — commercial, weekly reports, customer health — used to guard
themselves with a locally-defined dependency::

    _ADMIN_KEY = os.getenv("DEALIX_ADMIN_API_KEY", "")

    def _require_admin(x_api_key: str = Header(default="", alias="X-Admin-API-Key")):
        if not _ADMIN_KEY:
            return                       # ← every caller admitted
        ...

Two defects, both live:

1. **Fail open.** The early return applied in every environment, so a
   production deployment with no ``DEALIX_ADMIN_API_KEY`` admitted anonymous
   callers to payment-link creation, proposal generation and customer health
   data. And ``DEALIX_ADMIN_API_KEY`` is the *client* variable — the Railway
   contract sets the server-side ``ADMIN_API_KEYS`` instead, so the empty
   branch was the expected state, not a corner case.
2. **Wrong header on ``commercial``.** Its parameter carried no ``alias``, so
   FastAPI derived the header name from the parameter and read ``x-api-key``
   — comparing the *service* credential against the *admin* key. Now that the
   two key sets are required to be disjoint, that comparison can never
   succeed, leaving the endpoints unreachable once a key is configured.

These tests pin the replacement (``api.security.api_key
.require_founder_admin_key``): permissive in dev when nothing is configured,
closed in production, and reading the admin header on all three routers.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

# One representative endpoint per router. Each carries Depends(_require_admin);
# the body is whatever the handler needs to reach a non-auth response.
GUARDED_ENDPOINTS = [
    ("commercial", "GET", "/api/v1/commercial/payment/tiers", None),
    ("weekly_reports", "POST", "/api/v1/reports/weekly/generate", {}),
    (
        "customer_health",
        "POST",
        "/api/v1/customer-health/score",
        {"account_id": "acc_1", "company_name": "Test Co"},
    ),
]

SERVICE_KEY = "service-key-for-the-middleware"
ADMIN_KEY = "admin-key-under-test"


@pytest.fixture
def client() -> TestClient:
    from api.main import app

    return TestClient(app)


def _call(client: TestClient, method: str, path: str, body, headers: dict[str, str]):
    if method == "GET":
        return client.get(path, headers=headers)
    return client.post(path, json=body, headers=headers)


def _production(monkeypatch) -> None:
    """Production, with the platform API key configured.

    ``APIKeyMiddleware`` rejects an unconfigured production deployment before
    routing, so the service key has to be present for these tests to reach the
    admin gate at all — otherwise every case would pass for the wrong reason.
    """
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("API_KEYS", SERVICE_KEY)


def _service_headers() -> dict[str, str]:
    return {"X-API-Key": SERVICE_KEY}


# ── Fail closed ───────────────────────────────────────────────────────────


@pytest.mark.parametrize(("name", "method", "path", "body"), GUARDED_ENDPOINTS)
def test_production_without_any_admin_key_is_refused(
    client, monkeypatch, name, method, path, body
):
    """The defect itself: no admin key configured used to mean "let everyone in"."""
    _production(monkeypatch)
    monkeypatch.setenv("ADMIN_API_KEYS", "")
    monkeypatch.delenv("DEALIX_ADMIN_API_KEY", raising=False)

    resp = _call(client, method, path, body, _service_headers())

    assert resp.status_code == 401, f"{name} admitted an anonymous production caller"
    assert "not configured" in resp.json()["detail"]


@pytest.mark.parametrize(("name", "method", "path", "body"), GUARDED_ENDPOINTS)
def test_configured_admin_key_rejects_missing_header(
    client, monkeypatch, name, method, path, body
):
    _production(monkeypatch)
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)

    resp = _call(client, method, path, body, _service_headers())

    assert resp.status_code == 401, f"{name} served a caller with no admin header"


@pytest.mark.parametrize(("name", "method", "path", "body"), GUARDED_ENDPOINTS)
def test_configured_admin_key_rejects_wrong_key(
    client, monkeypatch, name, method, path, body
):
    _production(monkeypatch)
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)

    resp = _call(
        client,
        method,
        path,
        body,
        {**_service_headers(), "X-Admin-API-Key": "not-the-admin-key"},
    )

    assert resp.status_code == 403, f"{name} accepted a wrong admin key"


# ── Still usable once configured ──────────────────────────────────────────


@pytest.mark.parametrize(("name", "method", "path", "body"), GUARDED_ENDPOINTS)
def test_correct_admin_key_is_accepted(client, monkeypatch, name, method, path, body):
    _production(monkeypatch)
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)

    resp = _call(
        client,
        method,
        path,
        body,
        {**_service_headers(), "X-Admin-API-Key": ADMIN_KEY},
    )

    assert resp.status_code == 200, f"{name} rejected the configured admin key: {resp.text}"


@pytest.mark.parametrize(("name", "method", "path", "body"), GUARDED_ENDPOINTS)
def test_single_key_env_var_is_also_honoured(client, monkeypatch, name, method, path, body):
    """A host that sets only the single-key form is gated, not wide open."""
    _production(monkeypatch)
    monkeypatch.setenv("ADMIN_API_KEYS", "")
    monkeypatch.setenv("DEALIX_ADMIN_API_KEY", ADMIN_KEY)

    accepted = _call(
        client, method, path, body, {**_service_headers(), "X-Admin-API-Key": ADMIN_KEY}
    )
    refused = _call(
        client, method, path, body, {**_service_headers(), "X-Admin-API-Key": "wrong"}
    )

    assert accepted.status_code == 200, f"{name}: {accepted.text}"
    assert refused.status_code == 403, f"{name} accepted a wrong key"


# ── Header identity ───────────────────────────────────────────────────────


def test_commercial_reads_the_admin_header_not_the_service_header(client, monkeypatch):
    """Regression for the missing ``alias`` on ``commercial._require_admin``.

    The admin credential presented in ``X-API-Key`` must not satisfy the admin
    gate, and the service credential must not be mistaken for it.
    """
    _production(monkeypatch)
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)

    admin_key_in_service_header = client.get(
        "/api/v1/commercial/payment/tiers",
        headers={"X-API-Key": SERVICE_KEY, "X-Admin-API-Key": "", "X-Api-Key": ADMIN_KEY},
    )
    assert admin_key_in_service_header.status_code in (401, 403)

    correct = client.get(
        "/api/v1/commercial/payment/tiers",
        headers={"X-API-Key": SERVICE_KEY, "X-Admin-API-Key": ADMIN_KEY},
    )
    assert correct.status_code == 200, correct.text


# ── Dev ergonomics preserved ──────────────────────────────────────────────


@pytest.mark.parametrize(("name", "method", "path", "body"), GUARDED_ENDPOINTS)
def test_unconfigured_dev_environment_stays_open(
    client, monkeypatch, name, method, path, body
):
    """Local runs deliberately leave the key unset — they must keep working.

    This mirrors ``APIKeyMiddleware``: an unconfigured deployment is refused
    in production and admitted everywhere else.
    """
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("API_KEYS", "")
    monkeypatch.setenv("ADMIN_API_KEYS", "")
    monkeypatch.delenv("DEALIX_ADMIN_API_KEY", raising=False)

    resp = _call(client, method, path, body, {})

    assert resp.status_code == 200, f"{name} broke unauthenticated local use: {resp.text}"


# ── Configuration is read per request ─────────────────────────────────────


def test_admin_keys_are_read_per_request_not_captured_at_import(client, monkeypatch):
    """The old guard snapshotted the env at import, so rotation needed a restart."""
    _production(monkeypatch)

    monkeypatch.setenv("ADMIN_API_KEYS", "first-key")
    first = client.get(
        "/api/v1/commercial/payment/tiers",
        headers={**_service_headers(), "X-Admin-API-Key": "first-key"},
    )
    assert first.status_code == 200, first.text

    monkeypatch.setenv("ADMIN_API_KEYS", "rotated-key")
    stale = client.get(
        "/api/v1/commercial/payment/tiers",
        headers={**_service_headers(), "X-Admin-API-Key": "first-key"},
    )
    rotated = client.get(
        "/api/v1/commercial/payment/tiers",
        headers={**_service_headers(), "X-Admin-API-Key": "rotated-key"},
    )

    assert stale.status_code == 403, "the retired key still worked"
    assert rotated.status_code == 200, rotated.text


def test_non_ascii_admin_header_is_rejected_not_a_server_error(client, monkeypatch):
    """``hmac.compare_digest`` raises TypeError on non-ASCII ``str`` inputs.

    Starlette decodes header bytes as latin-1, so a byte above 0x7F reaches the
    dependency as a non-ASCII ``str``. Comparing that directly would surface as
    a 500, letting a caller distinguish this gate from a plain rejection. The
    header is passed as raw bytes because the HTTP client will not encode a
    non-ASCII ``str`` for us.
    """
    _production(monkeypatch)
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)

    resp = client.get(
        "/api/v1/commercial/payment/tiers",
        headers={**_service_headers(), "X-Admin-API-Key": "مفتاح-غير-صحيح".encode()},
    )

    assert resp.status_code == 403, resp.text


@pytest.mark.parametrize("verifier", ["verify_api_key", "verify_admin_key"])
def test_shared_verifiers_reject_non_ascii_without_raising(monkeypatch, verifier):
    """The same TypeError exposure on the two long-standing verifiers.

    Both compared ``str`` to ``str`` through ``hmac.compare_digest``, which
    accepts only ASCII ``str``. These back ``require_admin_key`` on
    ``/api/v1/admin/*`` and ``APIKeyMiddleware`` on every other route, so a
    caller sending one high byte could turn a 401 into a 500.
    """
    from api.security import api_key as mod

    monkeypatch.setenv("API_KEYS", ADMIN_KEY)
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)

    check = getattr(mod, verifier)
    assert check("مفتاح") is False
    assert check(ADMIN_KEY) is True
