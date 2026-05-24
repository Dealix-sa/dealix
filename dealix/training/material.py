"""خادم التدريب — Material + MaterialLibrary."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from dealix.hermes.core.schemas import utcnow


class MaterialType(StrEnum):
    SLIDE_DECK = "slide_deck"
    WORKBOOK = "workbook"
    VIDEO = "video"
    TEMPLATE = "template"
    CASE_STUDY = "case_study"


def _new_material_id() -> str:
    return f"mat_{uuid4().hex[:12]}"


class Material(BaseModel):
    """A training material record."""

    model_config = ConfigDict(extra="forbid")

    material_id: str = Field(default_factory=_new_material_id)
    title: str = Field(..., min_length=1, max_length=200)
    material_type: MaterialType
    audience: str = Field(..., min_length=1, max_length=120)
    summary: str = Field(..., min_length=1, max_length=600)
    tags: list[str] = Field(default_factory=list, max_length=12)
    created_at: datetime = Field(default_factory=utcnow)


_SEED_MATERIALS: tuple[Material, ...] = (
    Material(
        title="Dealix Trust 101",
        material_type=MaterialType.SLIDE_DECK,
        audience="Operators",
        summary="Sovereignty levels, guardrails, evidence packs in 30 minutes.",
        tags=["trust", "operators", "onboarding"],
    ),
    Material(
        title="Revenue Hunter Field Guide",
        material_type=MaterialType.WORKBOOK,
        audience="Sales",
        summary="Workbook: pick targets, draft proposals, run Friday review.",
        tags=["revenue", "sales"],
    ),
    Material(
        title="Partner Pitch Template",
        material_type=MaterialType.TEMPLATE,
        audience="Partner managers",
        summary="Reusable structure for partner-pitch drafts (matches §41 gate).",
        tags=["partner", "template"],
    ),
)


class MaterialLibrary:
    """In-memory training materials library."""

    def __init__(self, seed: bool = True) -> None:
        self._materials: dict[str, Material] = {}
        if seed:
            for material in _SEED_MATERIALS:
                # Copy to avoid sharing pydantic instances between callers.
                self.register(
                    Material(
                        title=material.title,
                        material_type=material.material_type,
                        audience=material.audience,
                        summary=material.summary,
                        tags=list(material.tags),
                    )
                )

    def register(self, material: Material) -> Material:
        if material.material_id in self._materials:
            raise ValueError(f"material already registered: {material.material_id}")
        self._materials[material.material_id] = material
        return material

    def get(self, material_id: str) -> Material:
        try:
            return self._materials[material_id]
        except KeyError as exc:
            raise KeyError(f"unknown material: {material_id}") from exc

    def all(self) -> list[Material]:
        return list(self._materials.values())

    def list_for_audience(self, audience: str) -> list[Material]:
        needle = audience.lower().strip()
        if not needle:
            return self.all()
        return [m for m in self._materials.values() if needle in m.audience.lower()]


__all__ = ["Material", "MaterialLibrary", "MaterialType"]
