"""
Self-Serve Onboarding API — signup, wizard, invite.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db as get_db_session
from api.security.auth_deps import get_current_user
from dealix.onboarding.service import OnboardingService

router = APIRouter(prefix="/api/v1/onboarding", tags=["Onboarding"])


# ── Schemas ──────────────────────────────────────────────────────

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=2)
    company_name: str = Field(..., min_length=2)
    plan_slug: str = Field(default="free")
    billing_cycle: str = Field(default="monthly", pattern="^(monthly|yearly)$")


class SignupOut(BaseModel):
    tenant_id: str
    user_id: str
    subscription_id: str
    plan_slug: str
    requires_email_verification: bool
    message: str
    message_ar: str


class WizardRequest(BaseModel):
    sector: str | None = None
    company_size: str | None = None
    phone: str | None = None
    website: str | None = None


class InviteRequest(BaseModel):
    email: EmailStr
    role_name: str = Field(default="viewer")


class InviteOut(BaseModel):
    user_id: str
    invite_url: str
    message: str
    message_ar: str


# ── Endpoints ────────────────────────────────────────────────────

@router.post("/signup", response_model=SignupOut, status_code=status.HTTP_201_CREATED)
async def signup(
    req: SignupRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """
    Self-serve signup: creates tenant, user, role, and subscription.
    """
    svc = OnboardingService(session)
    try:
        result = await svc.signup(
            email=str(req.email),
            password=req.password,
            name=req.name,
            company_name=req.company_name,
            plan_slug=req.plan_slug,
            billing_cycle=req.billing_cycle,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    await session.commit()
    return {
        "tenant_id": result["tenant"].id,
        "user_id": result["user"].id,
        "subscription_id": result["subscription"].id,
        "plan_slug": req.plan_slug,
        "requires_email_verification": result["requires_email_verification"],
        "message": "Account created successfully. Please verify your email.",
        "message_ar": "تم إنشاء الحساب بنجاح. يرجى التحقق من بريدك الإلكتروني.",
    }


@router.post("/wizard")
async def complete_wizard(
    req: WizardRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    """
    Complete onboarding wizard for the tenant.
    """
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tenant")

    svc = OnboardingService(session)
    await svc.complete_onboarding_wizard(
        tenant_id=tenant_id,
        sector=req.sector,
        company_size=req.company_size,
        phone=req.phone,
        website=req.website,
    )
    await session.commit()

    return {
        "status": "completed",
        "message": "Onboarding completed successfully.",
        "message_ar": "تم إكمال الإعداد بنجاح.",
    }


@router.post("/invite", response_model=InviteOut)
async def invite_team_member(
    req: InviteRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    """
    Invite a team member to the tenant.
    """
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tenant")

    svc = OnboardingService(session)
    try:
        result = await svc.invite_team_member(
            tenant_id=tenant_id,
            invited_by=current_user.id,
            email=str(req.email),
            role_name=req.role_name,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    await session.commit()
    return {
        "user_id": result["user"].id,
        "invite_url": result["invite_url"],
        "message": f"Invitation sent to {req.email}",
        "message_ar": f"تم إرسال الدعوة إلى {req.email}",
    }
