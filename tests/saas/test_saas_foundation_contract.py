from api.tenant_context import TenantContext, assert_server_validated_context
from app.saas.access_policy import has_permission
from app.saas.tenant_guard import assert_same_organization


def test_tenant_context_blocks_client_supplied_only():
    context = TenantContext("org_1", "ws_1", "user_1", "owner", source="client_supplied_only")
    try:
        assert_server_validated_context(context)
    except PermissionError:
        return
    raise AssertionError("client supplied tenant context must be blocked")


def test_cross_tenant_access_denied():
    context = TenantContext("org_1", "ws_1", "user_1", "owner")
    try:
        assert_same_organization(context, "org_2")
    except PermissionError:
        return
    raise AssertionError("cross-tenant access must be denied")


def test_owner_has_admin_permission():
    assert has_permission("owner", "billing:write")
