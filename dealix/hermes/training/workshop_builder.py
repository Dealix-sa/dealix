"""Workshop builder."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Workshop(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workshop_id: str
    title: str
    audience: str
    duration_minutes: int = Field(default=120, ge=30)
    learning_outcomes: list[str] = Field(default_factory=list)
    materials: list[str] = Field(default_factory=list)


def build_workshop(
    *,
    workshop_id: str,
    title: str,
    audience: str,
    learning_outcomes: list[str],
    duration_minutes: int = 120,
) -> Workshop:
    return Workshop(
        workshop_id=workshop_id,
        title=title,
        audience=audience,
        learning_outcomes=learning_outcomes,
        duration_minutes=duration_minutes,
    )
