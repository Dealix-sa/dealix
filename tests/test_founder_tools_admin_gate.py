"""Founder-internal routers must stay behind the platform-admin credential.

`automation`, `data`, `dominance`, `drafts`, `email_send` and `outreach`
read and write the whole prospecting graph — accounts, contacts, scores —
across tenants by design. That is only acceptable behind the platform-admin
key. Before this guard they were reachable by any holder of the shared API
key, which is not an admin credential and carries no tenant.

The guard is applied at the router so a new route added to any of these
files cannot miss it, and this test asserts exactly that: every route in
every one of these modules carries the dependency.

These routers are also the reason the tenant-scoped-query gate allowlists
their `ContactRecord` queries. If the admin gate is ever removed, that
allowlist becomes a lie — so this test is what keeps it honest.
"""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest

from api.security.api_key import require_admin_key

FOUNDER_INTERNAL_ROUTERS = (
    "automation",
    "data",
    "dominance",
    "drafts",
    "email_send",
    "outreach",
)


@pytest.mark.parametrize("module_name", FOUNDER_INTERNAL_ROUTERS)
def test_every_route_requires_the_platform_admin_key(module_name):
    module = importlib.import_module(f"api.routers.{module_name}")
    routes = module.router.routes
    assert routes, f"{module_name} exposes no routes — is it still a router?"

    unguarded = [
        route.path
        for route in routes
        if not any(
            dependency.call is require_admin_key
            for dependency in route.dependant.dependencies
        )
    ]
    assert not unguarded, (
        f"{module_name} has routes reachable without the platform-admin key: "
        f"{unguarded}"
    )


@pytest.mark.parametrize("module_name", FOUNDER_INTERNAL_ROUTERS)
def test_the_guard_is_declared_on_the_router_not_per_route(module_name):
    """Router-level declaration is what makes new routes safe by default."""
    source = Path(
        importlib.import_module(f"api.routers.{module_name}").__file__ or ""
    )
    text = source.read_text(encoding="utf-8")
    assert "dependencies=[Depends(require_admin_key)]" in text, (
        f"{module_name} should declare the guard on APIRouter(...) so a new "
        "route cannot be added without it"
    )


def test_allowlist_reasons_match_the_gate():
    """The query gate's exemption must name the guard this test enforces."""
    from scripts.ops.check_tenant_scoped_queries import ALLOWLIST

    for module_name in FOUNDER_INTERNAL_ROUTERS:
        key = (f"api/routers/{module_name}.py", "ContactRecord")
        assert key in ALLOWLIST, f"{module_name} lost its documented exemption"
        assert "require_admin_key" in ALLOWLIST[key]
