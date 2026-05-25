"""Five content types Dealix produces, bilingual labels."""

from __future__ import annotations

from typing import Final, Literal

from pydantic import BaseModel, ConfigDict, Field

ContentType = Literal[
    "trust",
    "revenue",
    "partner",
    "executive",
    "market_radar",
]

CONTENT_TYPES: Final[tuple[ContentType, ...]] = (
    "trust",
    "revenue",
    "partner",
    "executive",
    "market_radar",
)


class ContentTypeDescription(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: ContentType
    label_ar: str
    label_en: str
    purpose_ar: str
    purpose_en: str
    primary_audience: list[str] = Field(default_factory=list)


CONTENT_TYPE_DESCRIPTIONS: Final[dict[ContentType, ContentTypeDescription]] = {
    "trust": ContentTypeDescription(
        key="trust",
        label_ar="محتوى الثقة",
        label_en="Trust Content",
        purpose_ar="يبرهن على الحوكمة والسلامة",
        purpose_en="Proves governance and safety posture",
        primary_audience=["enterprise", "ai_users_governance"],
    ),
    "revenue": ContentTypeDescription(
        key="revenue",
        label_ar="محتوى الإيراد",
        label_en="Revenue Content",
        purpose_ar="يوضّح أثر مالي قابل للقياس",
        purpose_en="Surfaces measurable financial impact",
        primary_audience=["b2b_smb", "founders"],
    ),
    "partner": ContentTypeDescription(
        key="partner",
        label_ar="محتوى الشركاء",
        label_en="Partner Content",
        purpose_ar="يبني قنوات الشركاء والوكالات",
        purpose_en="Builds partner and agency channels",
        primary_audience=["agencies", "consultants"],
    ),
    "executive": ContentTypeDescription(
        key="executive",
        label_ar="محتوى تنفيذي",
        label_en="Executive Content",
        purpose_ar="يخاطب أصحاب القرار باختصار",
        purpose_en="Speaks to executives with brevity",
        primary_audience=["enterprise", "founders"],
    ),
    "market_radar": ContentTypeDescription(
        key="market_radar",
        label_ar="رادار السوق",
        label_en="Market Radar",
        purpose_ar="يقرأ إشارات السوق ويربطها بقرار",
        purpose_en="Reads market signals and ties them to a decision",
        primary_audience=["founders", "enterprise"],
    ),
}


def describe_content_type(key: ContentType) -> ContentTypeDescription:
    return CONTENT_TYPE_DESCRIPTIONS[key]


__all__ = [
    "CONTENT_TYPES",
    "CONTENT_TYPE_DESCRIPTIONS",
    "ContentType",
    "ContentTypeDescription",
    "describe_content_type",
]
