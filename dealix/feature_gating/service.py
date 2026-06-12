"""
Feature Gating Service — checks if a tenant can use a feature.
"""

from __future__ import annotations

from fastapi import HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from dealix.billing.service import BillingService


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
    Usage:
        @router.post("/projects")
        async def create_project(
            req: Request,
            _=Depends(FeatureGate("projects")),
        ):
            ...
    """

    def __init__(self, feature_key: str):
        self.feature_key = feature_key

    async def __call__(self, request: Request) -> None:
        tenant_id = getattr(request.state, "tenant_id", None)
        if tenant_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tenant context required",
            )

        from db.session import get_db_session
        async for session in get_db_session():
            gating = FeatureGatingService(session)
            await gating.require_feature(tenant_id, self.feature_key)
            break
