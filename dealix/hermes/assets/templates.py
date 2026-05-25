"""Templates — drop-in reusable artefacts."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Template(BaseModel):
    model_config = ConfigDict(extra="forbid")

    template_id: str
    title: str
    category: str
    body: str
    locale: str = "en"
    tags: list[str] = Field(default_factory=list)
