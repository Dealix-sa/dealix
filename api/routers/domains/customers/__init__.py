"""
Customers domain — success, CRM, portal, inbox, support.
مجال العملاء — النجاح، إدارة علاقات العملاء، البوابة، البريد الوارد، الدعم.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers import (
    billing,
    client_value_room,
    crm_v10,
    customer_company_portal,
    customer_data_plane,
    customer_inbox_v10,
    customer_loop,
    customer_success,
    customer_success_os,
    executive_pack_per_customer,
    support_os,
)
from api.routers import (
    company_brain_mvp as company_brain_mvp_router,
)
from api.routers import (
    customer_brain as customer_brain_router,
)
from api.routers import (
    service_sessions as service_sessions_router,
)
from api.routers import (
    support_journey as support_journey_router,
)
from api.routers.customer import dashboard as customer_dashboard_router

_ROUTERS = [
    # /api/v1/billing — subscribe, upgrade, cancel, invoices, features.
    # This module existed in full, with auth and tenant scoping on every
    # route, but was never imported anywhere, so none of its routes were
    # mounted: the product had no billing API at all. The three tests that
    # exercise it are xfailed for a missing PostgreSQL, which is true and
    # which also hid the 404s underneath.
    billing.router,
    company_brain_mvp_router.router,
    customer_success.router,
    customer_success_os.router,
    customer_loop.router,
    customer_data_plane.router,
    customer_brain_router.router,
    customer_company_portal.router,
    client_value_room.router,
    customer_dashboard_router.router,
    customer_inbox_v10.router,
    crm_v10.router,
    executive_pack_per_customer.router,
    service_sessions_router.router,
    support_journey_router.router,
    support_os.router,
]


def get_routers() -> list[APIRouter]:
    """Return all customers-domain routers."""
    return _ROUTERS
