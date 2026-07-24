"""
Self-Serve Onboarding API — signup, wizard, and approval-first team invite.
"""

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from api.security.auth_deps import get_current_user, require_tenant_admin
from core.email import send_invite_email
from db.session import get_db as get_db_session
from dealix.onboarding.service import OnboardingService

router = APIRouter(prefix="/api/v1/onboarding", tags=["Onboarding"])


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
    invite_id: str
    invite_url: str
    delivery_status: str
    message: str
    message_ar: str


@router.post("/signup", response_model=SignupOut, status_code=status.HTTP_201_CREATED)
async def signup(
    req: SignupRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """Create the tenant, canonical admin identity, and SaaS subscription."""
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
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    await session.commit()
    return {
        "tenant_id": result["tenant"].id,
        "user_id": result["user"].id,
        "subscription_id": result["subscription"].id,
        "plan_slug": req.plan_slug,
        "requires_email_verification": result["requires_email_verification"],
        "message": "Account and workspace created successfully.",
        "message_ar": "تم إنشاء الحساب ومساحة العمل بنجاح.",
    }


@router.post("/wizard")
async def complete_wizard(
    req: WizardRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(get_current_user),
) -> dict[str, Any]:
    """Complete the tenant onboarding profile."""
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


@router.post("/invite", response_model=InviteOut, status_code=status.HTTP_201_CREATED)
async def invite_team_member(
    req: InviteRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user=Depends(require_tenant_admin),
) -> dict[str, Any]:
    """
    Create a single-use team invitation and attempt policy-gated delivery.

    External email remains fail-closed unless ``EMAIL_ALLOW_LIVE_SEND`` is
    explicitly enabled by an operator. A manual link is always returned to the
    authenticated tenant administrator as the recovery path.
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
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    # Persist the invitation before any optional external delivery attempt.
    await session.commit()

    web_base_url = os.getenv("DEALIX_WEB_URL", "https://dealix.me").rstrip("/")
    invite_url = f"{web_base_url}{result['invite_url']}"
    delivery = await send_invite_email(
        to_email=str(req.email),
        invited_by_name=current_user.name or current_user.email or "Dealix admin",
        accept_url=invite_url,
    )

    if delivery.delivered:
        delivery_status = "delivered"
        message = "Invitation created and delivered."
        message_ar = "تم إنشاء الدعوة وإرسالها."
    elif delivery.blocked_by_policy:
        delivery_status = "manual_share_required"
        message = "Invitation created for manual sharing. Nothing was sent."
        message_ar = "تم إنشاء الدعوة للمشاركة اليدوية. لم يتم إرسال أي رسالة."
    else:
        delivery_status = "delivery_failed_manual_share_required"
        message = "Invitation created, but delivery failed. Share the link manually."
        message_ar = "تم إنشاء الدعوة، لكن تعذر الإرسال. شارك الرابط يدويًا."

    return {
        "invite_id": result["invite"].id,
        "invite_url": invite_url,
        "delivery_status": delivery_status,
        "message": message,
        "message_ar": message_ar,
    }
