"""GEO content blueprint — the required sections for a GEO-ready page."""

from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict, Field

GEO_REQUIRED_SECTIONS: Final[tuple[str, ...]] = (
    "definition",
    "problem",
    "steps",
    "comparison_table",
    "examples",
    "faq",
    "sources",
    "cta",
)


class GEOContentSection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str = Field(..., min_length=1)
    label_ar: str
    label_en: str
    min_chars: int = 80
    required: bool = True


_SECTION_BLUEPRINT: Final[dict[str, GEOContentSection]] = {
    "definition": GEOContentSection(
        key="definition",
        label_ar="التعريف",
        label_en="Definition",
        min_chars=120,
    ),
    "problem": GEOContentSection(
        key="problem",
        label_ar="المشكلة",
        label_en="Problem",
        min_chars=120,
    ),
    "steps": GEOContentSection(
        key="steps",
        label_ar="الخطوات",
        label_en="Steps",
        min_chars=200,
    ),
    "comparison_table": GEOContentSection(
        key="comparison_table",
        label_ar="جدول مقارنة",
        label_en="Comparison Table",
        min_chars=120,
    ),
    "examples": GEOContentSection(
        key="examples",
        label_ar="أمثلة",
        label_en="Examples",
        min_chars=120,
    ),
    "faq": GEOContentSection(
        key="faq",
        label_ar="أسئلة شائعة",
        label_en="FAQ",
        min_chars=150,
    ),
    "sources": GEOContentSection(
        key="sources",
        label_ar="المصادر",
        label_en="Sources",
        min_chars=40,
    ),
    "cta": GEOContentSection(
        key="cta",
        label_ar="دعوة لاتخاذ إجراء",
        label_en="Call to Action",
        min_chars=20,
    ),
}


def blueprint_for(section_key: str) -> GEOContentSection:
    if section_key not in _SECTION_BLUEPRINT:
        raise KeyError(f"unknown GEO section key: {section_key!r}")
    return _SECTION_BLUEPRINT[section_key]


def list_blueprint() -> list[GEOContentSection]:
    return list(_SECTION_BLUEPRINT.values())


__all__ = [
    "GEO_REQUIRED_SECTIONS",
    "GEOContentSection",
    "blueprint_for",
    "list_blueprint",
]
