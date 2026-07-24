"""
Self-Serve Onboarding Service.
خدمة التسجيل الذاتي.
"""

from __future__ import annotations

import uuid
from typing import Any

from passlib.context import CryptContext
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.jwt import create_invite_token, hash_token, token_expires_at
from api.security.rbac import DEFAULT_TENANT_ROLES, Role
from core.utils import utcnow
from db.models import RoleRecord, TenantRecord, UserInviteRecord, UserRecord
from dealix.billing.service import BillingService

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
_VALID_ROLE_NAMES = {role.value for role in Role}


class OnboardingService:
    """
    Orchestrates the self-serve signup → tenant → plan → subscription → wizard flow.

    The service deliberately reuses the canonical authentication contracts:
    every tenant receives the standard RBAC roles and every invitation is stored
    as a single-use hashed token in ``user_invites``. It never creates a blank-
    password placeholder user.
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
        """Create a tenant, canonical roles, first admin, and subscription."""
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

        slug_base = "".join(
            char if char.isalnum() else "-" for char in company_name.lower()
        ).strip("-")[:30]
        slug_base = slug_base or tenant_id
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
            meta_json={"onboarding_status": "account_created"},
            created_at=now,
            updated_at=now,
        )
        self.session.add(tenant)

        roles: dict[str, RoleRecord] = {}
        for role_definition in DEFAULT_TENANT_ROLES:
            role_name = str(role_definition["name"])
            role = RoleRecord(
                id=f"rol_{uuid.uuid4().hex[:12]}",
                tenant_id=tenant_id,
                name=role_name,
                permissions=list(role_definition["permissions"]),
                description=role_definition["description"],
                is_system=bool(role_definition["is_system"]),
                created_at=now,
            )
            self.session.add(role)
            roles[role_name] = role

        await self.session.flush()
        admin_role = roles[Role.TENANT_ADMIN.value]

        user = UserRecord(
            id=user_id,
            tenant_id=tenant_id,
            role_id=admin_role.id,
            email=email,
            name=name,
            hashed_password=_pwd_ctx.hash(password),
            is_active=True,
            # The canonical /auth/register flow currently verifies the first
            # tenant administrator at account creation. Keep both signup paths
            # aligned until a dedicated email-verification record is introduced.
            is_verified=True,
            created_at=now,
            updated_at=now,
        )
        self.session.add(user)

        subscription = await self.billing.create_subscription(
            tenant_id=tenant_id,
            plan_id=plan.id,
            billing_cycle=billing_cycle,
            seat_count=1,
        )

        await self.session.flush()
        return {
            "tenant": tenant,
            "user": user,
            "subscription": subscription,
            "requires_email_verification": False,
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

        meta = dict(tenant.meta_json or {})
        meta["onboarding"] = {
            "sector": sector,
            "company_size": company_size,
            "phone": phone,
            "website": website,
            "completed_at": utcnow().isoformat(),
        }
        meta["onboarding_status"] = "completed"
        tenant.meta_json = meta
        tenant.updated_at = utcnow()
        await self.session.flush()
        return tenant

    async def invite_team_member(
        self,
        tenant_id: str,
        invited_by: str,
        email: str,
        role_name: str = Role.VIEWER.value,
    ) -> dict[str, Any]:
        """Create a canonical, single-use invitation without sending it."""
        role_name = role_name.strip().lower()
        if role_name not in _VALID_ROLE_NAMES:
            raise ValueError(f"Unsupported role: {role_name}")

        tenant = await self.session.get(TenantRecord, tenant_id)
        if tenant is None:
            raise ValueError("Tenant not found")

        subscription = await self.billing.get_active_subscription_for_tenant(tenant_id)
        if subscription is None:
            raise ValueError("No active subscription")

        plan = await self.billing.get_plan(subscription.plan_id)
        if plan is None:
            raise ValueError("Plan not found")

        existing_user = await self.session.execute(
            select(UserRecord).where(
                UserRecord.tenant_id == tenant_id,
                UserRecord.email == email,
                UserRecord.deleted_at.is_(None),
            )
        )
        if existing_user.scalar_one_or_none():
            raise ValueError("User already in tenant")

        active_users = await self.session.scalar(
            select(func.count())
            .select_from(UserRecord)
            .where(
                UserRecord.tenant_id == tenant_id,
                UserRecord.deleted_at.is_(None),
                UserRecord.is_active.is_(True),
            )
        )
        pending_invites = await self.session.scalar(
            select(func.count())
            .select_from(UserInviteRecord)
            .where(
                UserInviteRecord.tenant_id == tenant_id,
                UserInviteRecord.email != email,
                UserInviteRecord.accepted_at.is_(None),
                UserInviteRecord.expires_at > utcnow(),
            )
        )
        if int(active_users or 0) + int(pending_invites or 0) >= plan.max_users:
            raise ValueError(
                f"Seat limit reached ({plan.max_users}). Upgrade plan to add more users."
            )

        role_result = await self.session.execute(
            select(RoleRecord).where(
                RoleRecord.tenant_id == tenant_id,
                RoleRecord.name == role_name,
            )
        )
        role = role_result.scalar_one_or_none()
        if role is None:
            raise ValueError(f"Canonical role not found: {role_name}")

        # A renewed invitation replaces the previous pending token so the
        # database unique constraint remains deterministic.
        await self.session.execute(
            delete(UserInviteRecord).where(
                UserInviteRecord.tenant_id == tenant_id,
                UserInviteRecord.email == email,
                UserInviteRecord.accepted_at.is_(None),
            )
        )

        invite_token = create_invite_token(
            tenant_id=tenant_id,
            email=email,
            role_id=role.id,
            invited_by=invited_by,
        )
        expires_at = token_expires_at(invite_token)
        invite = UserInviteRecord(
            id=f"inv_{uuid.uuid4().hex[:24]}",
            tenant_id=tenant_id,
            email=email,
            role_id=role.id,
            invited_by=invited_by,
            token_hash=hash_token(invite_token),
            expires_at=(
                expires_at.replace(tzinfo=None) if expires_at is not None else utcnow()
            ),
        )
        self.session.add(invite)
        await self.session.flush()

        return {
            "invite": invite,
            "invite_token": invite_token,
            "invite_url": f"/accept-invite?token={invite_token}",
            "delivery_status": "manual_share_required",
        }
