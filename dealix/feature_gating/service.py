"""
Feature Gating Service — checks if a tenant can use a feature.
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.auth_deps import get_current_user
from db.models import UserRecord
from db.session import get_db
from dealix.billing.service import BillingService
from dealix.feature_gating.tenant_context import (
    TENANT_OVERRIDE_HEADER,
    EntitlementTenantDenied,
    resolve_entitlement_tenant_id,
)


class FeatureGatingService:
    """
    Checks feature access for tenants.
    Can be used as a FastAPI dependency.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.billing = BillingService(session)

    async def require_feature(self, tenant_id: str, feature_key: str) -> bool:
        """Raise 403 if feature is not enabled."""
        enabled = await self.billing.is_feature_enabled(tenant_id, feature_key)
        if not enabled:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "feature_not_available",
                    "feature": feature_key,
                    "message": f"Feature '{feature_key}' is not available on your current plan. Please upgrade.",
                    "message_ar": f"الميزة '{feature_key}' غير متوفرة في خطتك الحالية. يرجى الترقية.",
                },
            )
        return True

    async def check_feature(self, tenant_id: str, feature_key: str) -> bool:
        """Return True/False without raising."""
        return await self.billing.is_feature_enabled(tenant_id, feature_key)

    async def get_all_features(self, tenant_id: str) -> dict[str, bool]:
        """Return all features for tenant."""
        return await self.billing.list_features_for_tenant(tenant_id)


class FeatureGate:
    """
    FastAPI dependency factory for feature gating.

    The gated tenant is resolved from the **authenticated user**, never
    from ``request.state`` or a client-supplied header — see
    ``dealix.feature_gating.tenant_context``. A super admin may target a
    tenant explicitly with the ``X-Tenant-ID`` header; for everyone else a
    mismatching header is a cross-tenant attempt and is rejected.

    Usage:
        @router.post("/projects", dependencies=[Depends(FeatureGate("projects"))])
        async def create_project(...):
            ...
    """

    def __init__(self, feature_key: str):
        self.feature_key = feature_key

    async def __call__(
        self,
        request: Request,
        user: UserRecord = Depends(get_current_user),
        session: AsyncSession = Depends(get_db),
    ) -> None:
        try:
            tenant_id, source = resolve_entitlement_tenant_id(
                user_tenant_id=getattr(user, "tenant_id", None),
                system_role=getattr(user, "system_role", None),
                requested_tenant_id=request.headers.get(TENANT_OVERRIDE_HEADER),
            )
        except EntitlementTenantDenied as denied:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": denied.reason, "message": denied.detail},
            ) from denied

        # Authoritative, identity-derived context for downstream handlers
        # and the audit trail. Overwrites any advisory value.
        request.state.tenant_id = tenant_id
        request.state.tenant_id_source = source

        await FeatureGatingService(session).require_feature(
            tenant_id, self.feature_key
        )
