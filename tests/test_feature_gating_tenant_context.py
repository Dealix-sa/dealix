"""Tenant-isolation contract for entitlement (feature-gating) checks.

Guards four defects found on main:

D1  nothing in the running app populated ``request.state.tenant_id``, so the
    gate rejected every authenticated caller;
D2  ``FeatureGate`` imported ``db.session.get_db_session``, which does not
    exist — the gate raised ImportError instead of a decision;
D3  the middleware resolved the tenant from the browser-controlled
    ``x-tenant-id`` header before the token, letting a caller pick whose
    plan gets evaluated;
D4  the middleware verified tokens with the wrong secret and read a
    ``tenant_id`` claim that Dealix tokens never carry (the claim is ``tid``),
    so the identity path could never resolve a tenant at all.
"""

from __future__ import annotations

import inspect

import pytest
from starlette.requests import Request

from api.security.jwt import create_access_token
from dealix.feature_gating.middleware import FeatureGatingMiddleware
from dealix.feature_gating.service import FeatureGate
from dealix.feature_gating.tenant_context import (
    EntitlementTenantDenied,
    resolve_entitlement_tenant_id,
)

TENANT_A = "tenant_a"
TENANT_B = "tenant_b"


def _request(headers: dict[str, str] | None = None) -> Request:
    raw = [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()]
    return Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/api/v1/erp/finance/accounts",
            "headers": raw,
            "query_string": b"",
            "scheme": "http",
            "server": ("test", 80),
            "client": ("1.2.3.4", 0),
        }
    )


# ── resolve_entitlement_tenant_id ────────────────────────────────────


def test_normal_user_is_scoped_to_own_tenant():
    tenant_id, source = resolve_entitlement_tenant_id(
        user_tenant_id=TENANT_A, system_role="user"
    )
    assert tenant_id == TENANT_A
    assert source == "authenticated_user"


def test_matching_tenant_header_is_accepted():
    tenant_id, source = resolve_entitlement_tenant_id(
        user_tenant_id=TENANT_A, system_role="user", requested_tenant_id=TENANT_A
    )
    assert tenant_id == TENANT_A
    assert source == "authenticated_user"


def test_cross_tenant_header_is_denied_not_silently_ignored():
    """D3 — a spoofed header must surface as a denial, never as tenant B."""
    with pytest.raises(EntitlementTenantDenied) as exc:
        resolve_entitlement_tenant_id(
            user_tenant_id=TENANT_A, system_role="user", requested_tenant_id=TENANT_B
        )
    assert exc.value.reason == "cross_tenant_entitlement_denied"


def test_user_without_tenant_is_denied():
    for empty in (None, "", "   "):
        with pytest.raises(EntitlementTenantDenied) as exc:
            resolve_entitlement_tenant_id(user_tenant_id=empty, system_role="user")
        assert exc.value.reason == "tenant_context_required"


def test_super_admin_must_name_the_target_tenant():
    """No tenant must never mean 'every feature'."""
    with pytest.raises(EntitlementTenantDenied) as exc:
        resolve_entitlement_tenant_id(user_tenant_id=None, system_role="super_admin")
    assert exc.value.reason == "super_admin_tenant_required"


def test_super_admin_override_is_explicit_and_labelled():
    tenant_id, source = resolve_entitlement_tenant_id(
        user_tenant_id=TENANT_A,
        system_role="super_admin",
        requested_tenant_id=TENANT_B,
    )
    assert tenant_id == TENANT_B
    assert source == "super_admin_override"


# ── FeatureGate wiring ───────────────────────────────────────────────


def test_gate_depends_on_authenticated_user_and_db_session():
    """D1/D2 — the gate resolves identity and a session through FastAPI."""
    from api.security.auth_deps import get_current_user
    from db.session import get_db

    params = inspect.signature(FeatureGate("finance").__call__).parameters
    dependencies = {
        getattr(param.default, "dependency", None) for param in params.values()
    }
    assert get_current_user in dependencies
    assert get_db in dependencies


def test_gate_does_not_import_a_nonexistent_session_helper():
    """D2 — regression guard on the exact broken import."""
    import db.session as session_module

    source = inspect.getsource(FeatureGate)
    assert "get_db_session" not in source
    assert not hasattr(session_module, "get_db_session")


def test_gate_no_longer_reads_tenant_from_request_state():
    """D1 — request.state is advisory; identity is the authority."""
    source = inspect.getsource(FeatureGate.__call__)
    assert "getattr(request.state" not in source


# ── Middleware ───────────────────────────────────────────────────────


def test_middleware_ignores_spoofed_tenant_header():
    """D3 — the header must not produce tenant context."""
    middleware = FeatureGatingMiddleware(app=None)
    spoofed = _request({"x-tenant-id": TENANT_B})
    assert middleware._extract_tenant_id(spoofed) is None


def test_middleware_reads_the_tenant_claim_of_a_real_token():
    """D4 — a genuine Dealix access token must resolve its tenant."""
    middleware = FeatureGatingMiddleware(app=None)
    token = create_access_token(user_id="u1", tenant_id=TENANT_A, role="viewer")
    authed = _request({"authorization": f"Bearer {token}"})
    assert middleware._extract_tenant_id(authed) == TENANT_A


def test_middleware_rejects_tampered_or_missing_tokens():
    middleware = FeatureGatingMiddleware(app=None)
    token = create_access_token(user_id="u1", tenant_id=TENANT_A, role="viewer")

    assert middleware._extract_tenant_id(_request({})) is None
    assert middleware._extract_tenant_id(_request({"authorization": "Bearer "})) is None
    assert (
        middleware._extract_tenant_id(_request({"authorization": f"Basic {token}"}))
        is None
    )
    assert (
        middleware._extract_tenant_id(
            _request({"authorization": f"Bearer {token}tampered"})
        )
        is None
    )


def test_middleware_header_cannot_override_a_verified_token():
    """Combined attack: valid token for A, header claiming B."""
    middleware = FeatureGatingMiddleware(app=None)
    token = create_access_token(user_id="u1", tenant_id=TENANT_A, role="viewer")
    attack = _request(
        {"authorization": f"Bearer {token}", "x-tenant-id": TENANT_B}
    )
    assert middleware._extract_tenant_id(attack) == TENANT_A


# ── Compliance truthfulness ──────────────────────────────────────────


def test_compliance_reports_enforcement_not_module_presence():
    from api.routers.compliance_status import _entitlement_tenant_context_enforced

    assert _entitlement_tenant_context_enforced() is True
