"""Playbooks — ordered, repeatable workflows."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PlaybookStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_id: str
    title: str
    detail: str
    owner: str = "agent"


class Playbook(BaseModel):
    model_config = ConfigDict(extra="forbid")

    playbook_id: str
    title: str
    domain: str
    steps: list[PlaybookStep] = Field(default_factory=list)
