"""Permission primitives shared across the trust plane."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Permission(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str = ""
    resource: str  # e.g. "tool:gmail_send"
    action: str  # e.g. "invoke" | "read" | "write"


class PermissionSet(BaseModel):
    model_config = ConfigDict(extra="forbid")

    owner_id: str
    permissions: list[Permission] = Field(default_factory=list)

    def grants(self, resource: str, action: str) -> bool:
        return any(p.resource == resource and p.action == action for p in self.permissions)
