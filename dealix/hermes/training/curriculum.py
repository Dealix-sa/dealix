"""Curricula are ordered modules."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CurriculumModule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    module_id: str
    title: str
    duration_minutes: int = 60
    material_ids: list[str] = Field(default_factory=list)


class Curriculum(BaseModel):
    model_config = ConfigDict(extra="forbid")

    curriculum_id: str
    title: str
    audience: str
    modules: list[CurriculumModule] = Field(default_factory=list)
