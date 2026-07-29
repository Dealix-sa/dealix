"""Tenant resolution has exactly one home, and the compliance surface proves it.

``api/middleware/tenant_isolation.py`` used to resolve the request's tenant
from — in order — a JWT claim, an ``X-Tenant-ID`` header, an API-key prefix,
or a subdomain. The last three are caller-controlled, and the header branch
returned ``source="header"`` for a **normal** user: anyone could name any
tenant and be believed. That is the same defect removed from the entitlement
gate in #971 — a caller-declared tenant is an assertion, not a credential.

Nothing ever called it. That is exactly what made it dangerous: it is the
abstraction someone wires up later because it looks like the right shape, and
doing so would silently reopen every hole that has been closed. The resolver
is deleted; the fail-closed per-object assertions stay.

`/api/v1/compliance/status` also reported ``helpers_available`` from
``_module_present("api.middleware.tenant_isolation")`` — a security control
asserted because a file was on disk. A compliance surface that does that is
worse than one that reports nothing: it turns an unverified claim into an
auditable statement. It now runs the real resolver against the real attack.
"""

from __future__ import annotations

import pytest

from api.middleware.tenant_isolation import (
    CrossTenantAccessDenied,
    assert_tenant_match,
    filter_tenant_scoped_list,
)

# ── The unsafe resolver must not come back ────────────────────────────────


@pytest.mark.parametrize(
    "name",
    ["resolve_tenant_context", "TenantContext", "_parse_tenant_from_api_key",
     "_parse_tenant_from_host"],
)
def test_header_based_resolution_is_gone(name):
    """Each of these treated a caller-supplied value as the tenant."""
    import api.middleware.tenant_isolation as module

    assert not hasattr(module, name), (
        f"{name} is back — tenant resolution belongs to "
        f"api/security/tenant_scope.py, which denies a declared tenant"
    )


def test_the_canonical_resolver_denies_a_declared_tenant():
    """The behaviour the deleted resolver got wrong, pinned where it lives."""
    from api.security.tenant_scope import TenantScopeDenied, resolve_request_tenant_id

    with pytest.raises(TenantScopeDenied) as denied:
        resolve_request_tenant_id(
            user_tenant_id="tenant_a",
            system_role="member",
            requested_tenant_id="tenant_b",
        )

    assert denied.value.reason == "cross_tenant_access_denied"


# ── The assertions that were worth keeping ────────────────────────────────


def test_mismatched_tenants_are_refused():
    with pytest.raises(CrossTenantAccessDenied):
        assert_tenant_match(
            request_tenant="tenant_a",
            object_tenant="tenant_b",
            object_type="lead",
            object_id="lead_1",
        )


def test_matching_tenants_pass():
    assert_tenant_match(
        request_tenant="tenant_a",
        object_tenant="tenant_a",
        object_type="lead",
        object_id="lead_1",
    )


@pytest.mark.parametrize(
    ("request_tenant", "object_tenant"),
    [("", "tenant_a"), ("tenant_a", ""), ("", "")],
)
def test_an_empty_tenant_is_refused_not_waved_through(request_tenant, object_tenant):
    """Unknown ownership must block. A blank tenant matching a blank tenant
    would otherwise be the widest hole in the file."""
    with pytest.raises(CrossTenantAccessDenied):
        assert_tenant_match(
            request_tenant=request_tenant,
            object_tenant=object_tenant,
            object_type="lead",
            object_id="lead_1",
        )


def test_super_admin_may_cross_tenants():
    assert_tenant_match(
        request_tenant="tenant_a",
        object_tenant="tenant_b",
        object_type="lead",
        object_id="lead_1",
        is_super_admin=True,
    )


class _Row:
    def __init__(self, tenant_id: str) -> None:
        self.tenant_id = tenant_id


def test_list_filter_keeps_only_the_requesting_tenant():
    rows = [_Row("tenant_a"), _Row("tenant_b"), _Row("tenant_a")]

    kept = filter_tenant_scoped_list(rows, request_tenant="tenant_a")

    assert len(kept) == 2
    assert all(row.tenant_id == "tenant_a" for row in kept)


def test_list_filter_excludes_items_of_unknown_ownership():
    """An item with no tenant attribute has unknown ownership — exclude it."""
    kept = filter_tenant_scoped_list(
        [_Row("tenant_a"), object(), {"no_tenant": 1}], request_tenant="tenant_a"
    )

    assert len(kept) == 1


def test_list_filter_supports_dict_rows():
    kept = filter_tenant_scoped_list(
        [{"tenant_id": "tenant_a"}, {"tenant_id": "tenant_b"}],
        request_tenant="tenant_a",
    )

    assert kept == [{"tenant_id": "tenant_a"}]


# ── The compliance surface must report enforcement, not file presence ─────


def test_compliance_probe_runs_the_real_resolver():
    from api.routers.compliance_status import _caller_declared_tenant_rejected

    assert _caller_declared_tenant_rejected() is True


def test_compliance_probe_would_fail_if_the_resolver_stopped_denying(monkeypatch):
    """Proves the probe measures behaviour rather than importability."""
    import api.security.tenant_scope as scope
    from api.routers import compliance_status

    monkeypatch.setattr(
        scope, "resolve_request_tenant_id", lambda **_kw: ("tenant_b", "override")
    )

    assert compliance_status._caller_declared_tenant_rejected() is False


def test_compliance_status_no_longer_claims_isolation_from_a_file(monkeypatch):
    from api.routers import compliance_status

    payload = compliance_status._security_status()
    tenant = payload["tenant_isolation"]

    assert "helpers_available" not in tenant, (
        "module presence is back as evidence of a security control"
    )
    assert tenant["caller_declared_tenant_rejected"] is True
    assert tenant["repository_assertions_available"] is True


# ── Folded in from tests/test_tenant_isolation_v1.py ──────────────────────
#
# That file loaded the module by path and asserted the resolver's five
# priority levels — including `test_resolve_header_when_no_jwt`, which
# encoded the vulnerability as expected behaviour: a bare X-Tenant-ID header
# resolving to that tenant with `source="header"`. Eight of its eighteen
# tests covered the deleted API. Rather than leave a file half-asserting a
# removed contract, its two unique still-valid tests live here and the file
# is gone.


def test_the_denial_carries_audit_data():
    """The exception is the audit record — it must name both sides."""
    with pytest.raises(CrossTenantAccessDenied) as raised:
        assert_tenant_match(
            request_tenant="acme",
            object_tenant="khaleej",
            object_type="proof_event",
            object_id="pe_999",
        )

    exc = raised.value
    assert exc.request_tenant == "acme"
    assert exc.object_tenant == "khaleej"
    assert exc.object_type == "proof_event"
    assert exc.object_id == "pe_999"
    assert "Cross-tenant" in str(exc)


def test_list_filter_returns_everything_for_a_super_admin():
    items = [
        {"id": "a1", "tenant_id": "acme"},
        {"id": "k1", "tenant_id": "khaleej"},
    ]

    assert (
        len(filter_tenant_scoped_list(items, request_tenant="any", is_super_admin=True))
        == 2
    )
