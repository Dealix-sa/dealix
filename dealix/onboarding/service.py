"""
Self-Serve Onboarding Service.
خدمة التسجيل الذاتي.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils import utcnow
from db.models import RoleRecord, TenantRecord, UserRecord
from db.models_subscription import PlanRecord, SubscriptionRecord
from dealix.billing.service import BillingService

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class OnboardingService:
    """
    Orchestrates the self-serve signup → tenant → plan → payment → wizard flow.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.billing = BillingService(session)

    async def signup(
        self,
        email: str,
        password: str,
        name: str,
        company_name: str,
        plan_slug: str = "free",
        billing_cycle: str = "monthly",
    ) -> dict[str, Any]:
        """
        Full signup flow:
        1. Check email uniqueness
        2. Create tenant
        3. Create owner user
        4. Create role
        5. Create subscription
        6. Return tenant + user + subscription
        """
        # Check existing user
        stmt = select(UserRecord).where(UserRecord.email == email)
        result = await self.session.execute(stmt)
        if result.scalar_one_or_none():
            raise ValueError("Email already registered")

        plan = await self.billing.get_plan_by_slug(plan_slug)
        if plan is None:
            raise ValueError(f"Plan {plan_slug} not found")

        now = utcnow()
        tenant_id = f"tnt_{uuid.uuid4().hex[:12]}"
        user_id = f"usr_{uuid.uuid4().hex[:12]}"
        role_id = f"rol_{uuid.uuid4().hex[:12]}"

        # Create tenant
        slug_base = company_name.lower().replace(" ", "-")[:30] or tenant_id
        tenant = TenantRecord(
            id=tenant_id,
            name=company_name,
            slug=f"{slug_base}-{uuid.uuid4().hex[:6]}",
            plan=plan_slug,
            status="active",
            timezone="Asia/Riyadh",
            locale="ar",
            currency="SAR",
            max_users=plan.max_users,
            max_leads_per_month=plan.max_leads_per_month,
            features=plan.features,
            created_at=now,
            updated_at=now,
        )
        self.session.add(tenant)

        # Create owner role
        owner_role = RoleRecord(
            id=role_id,
            tenant_id=tenant_id,
            name="owner",
            permissions=[
                "*:*",  # Full access
            ],
            description="Tenant owner — full access",
            is_system=True,
            created_at=now,
        )
        self.session.add(owner_role)

        # Create user
        user = UserRecord(
            id=user_id,
            tenant_id=tenant_id,
            role_id=role_id,
            email=email,
            name=name,
            hashed_password=_pwd_ctx.hash(password),
            is_active=True,
            is_verified=False,  # Email verification pending
            created_at=now,
            updated_at=now,
        )
        self.session.add(user)

        # Create subscription
        sub = await self.billing.create_subscription(
            tenant_id=tenant_id,
            plan_id=plan.id,
            billing_cycle=billing_cycle,
            seat_count=1,
        )

        await self.session.flush()

        return {
            "tenant": tenant,
            "user": user,
            "subscription": sub,
            "requires_email_verification": True,
        }

    async def complete_onboarding_wizard(
        self,
        tenant_id: str,
        sector: str | None = None,
        company_size: str | None = None,
        phone: str | None = None,
        website: str | None = None,
    ) -> TenantRecord:
        tenant = await self.session.get(TenantRecord, tenant_id)
        if tenant is None:
            raise ValueError("Tenant not found")

        if sector:
            # Update metadata with onboarding info
            meta = dict(tenant.meta_json or {})
            meta["onboarding"] = {
                "sector": sector,
                "company_size": company_size,
                "phone": phone,
                "website": website,
                "completed_at": utcnow().isoformat(),
            }
            tenant.meta_json = meta

        tenant.updated_at = utcnow()
        await self.session.flush()
        return tenant

    async def resend_verification_email(self, user_id: str) -> None:
        # Placeholder — actual email sending would integrate with Resend
        pass

    async def verify_email(self, token: str) -> UserRecord:
        # Placeholder — actual verification would decode JWT token
        raise NotImplementedError("Email verification token decoding not yet implemented")

    async def invite_team_member(
        self,
        tenant_id: str,
        invited_by: str,
        email: str,
        role_name: str = "viewer",
    ) -> dict[str, Any]:
        """
        Invite a team member to the tenant.
        """
        # Check tenant seat limit
        tenant = await self.session.get(TenantRecord, tenant_id)
        if tenant is None:
            raise ValueError("Tenant not found")

        sub = await self.billing.get_active_subscription_for_tenant(tenant_id)
        if sub is None:
            raise ValueError("No active subscription")

        plan = await self.billing.get_plan(sub.plan_id)
        if plan is None:
            raise ValueError("Plan not found")

        # Count current users
        stmt = select(UserRecord).where(
            UserRecord.tenant_id == tenant_id,
            UserRecord.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        current_users = len(result.scalars().all())

        if current_users >= plan.max_users:
            raise ValueError(
                f"Seat limit reached ({plan.max_users}). Upgrade plan to add more users."
            )

        # Check if email already invited/registered
        stmt = select(UserRecord).where(
            UserRecord.tenant_id == tenant_id,
            UserRecord.email == email,
        )
        result = await self.session.execute(stmt)
        if result.scalar_one_or_none():
            raise ValueError("User already in tenant")

        # Create role if not exists
        stmt = select(RoleRecord).where(
            RoleRecord.tenant_id == tenant_id,
            RoleRecord.name == role_name,
        )
        result = await self.session.execute(stmt)
        role = result.scalar_one_or_none()

        if role is None:
            role = RoleRecord(
                id=f"rol_{uuid.uuid4().hex[:12]}",
                tenant_id=tenant_id,
                name=role_name,
                permissions=self._default_permissions_for_role(role_name),
                is_system=False,
                created_at=utcnow(),
            )
            self.session.add(role)
            await self.session.flush()

        # Create invite token
        invite_token = f"inv_{uuid.uuid4().hex[:24]}"

        # For now, create the user as pending
        user = UserRecord(
            id=f"usr_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            role_id=role.id,
            email=email,
            name="",
            hashed_password="",  # Will be set on first login
            is_active=False,
            is_verified=False,
            created_at=utcnow(),
            updated_at=utcnow(),
        )
        self.session.add(user)
        await self.session.flush()

        return {
            "user": user,
            "invite_token": invite_token,
            "invite_url": f"/accept-invite?token={invite_token}",
        }

    def _default_permissions_for_role(self, role_name: str) -> list[str]:
        defaults = {
            "owner": ["*:*"],
            "admin": [
                "leads:*", "deals:*", "contacts:*",
                "projects:*", "tasks:*",
                "users:read", "users:write", "settings:*",
                "reports:*", "billing:read",
            ],
            "sales_rep": [
                "leads:*", "deals:*", "contacts:*",
                "tasks:read", "tasks:write",
                "reports:read",
            ],
            "viewer": [
                "leads:read", "deals:read", "contacts:read",
                "tasks:read", "reports:read",
            ],
            "agent_operator": [
                "leads:read", "deals:read",
                "agents:run", "drafts:read", "drafts:write",
            ],
        }
        return defaults.get(role_name, ["leads:read"])
