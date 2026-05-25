"""Roles and role assignments."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Role(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role_id: str
    name: str
    description: str = ""
    permissions: list[str] = Field(default_factory=list)


class RoleAssignment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str
    role_id: str
    workspace_id: str | None = None
    assigned_by: str = "Sami"
