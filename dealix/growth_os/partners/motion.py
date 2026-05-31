"""Partner motion — the lifecycle stages for agencies / consultants."""

from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict


class PartnerStage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    label_ar: str
    label_en: str
    success_signal: str


PARTNER_MOTION_STAGES: Final[tuple[PartnerStage, ...]] = (
    PartnerStage(key="target", label_ar="هدف", label_en="Target", success_signal="logged_in_register"),
    PartnerStage(key="qualify", label_ar="تأهيل", label_en="Qualify", success_signal="fit_confirmed"),
    PartnerStage(key="onboard", label_ar="استقبال", label_en="Onboard", success_signal="program_accepted"),
    PartnerStage(key="enable", label_ar="تمكين", label_en="Enable", success_signal="enablement_completed"),
    PartnerStage(key="first_deal", label_ar="أول صفقة", label_en="First Deal", success_signal="first_deal_signed"),
    PartnerStage(key="repeat", label_ar="تكرار", label_en="Repeat", success_signal="second_deal_signed"),
    PartnerStage(key="strategic", label_ar="شراكة استراتيجية", label_en="Strategic", success_signal="quarterly_review_active"),
)


class PartnerMotion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stages: tuple[PartnerStage, ...] = PARTNER_MOTION_STAGES


def list_stages() -> list[PartnerStage]:
    return list(PARTNER_MOTION_STAGES)


__all__ = ["PARTNER_MOTION_STAGES", "PartnerMotion", "PartnerStage", "list_stages"]
