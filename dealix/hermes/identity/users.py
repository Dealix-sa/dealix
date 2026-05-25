"""Hermes user model — humans, agents, tools, API clients, marketplace publishers."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class UserType(StrEnum):
    sami = "sami"
    internal_operator = "internal_operator"
    customer_admin = "customer_admin"
    customer_user = "customer_user"
    partner_admin = "partner_admin"
    agent_identity = "agent_identity"
    tool_identity = "tool_identity"
    api_client = "api_client"
    marketplace_publisher = "marketplace_publisher"


class User(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str
    user_type: UserType
    display_name: str
    email: str | None = None
    tenant_id: str | None = None
    workspace_ids: list[str] = Field(default_factory=list)
    active: bool = True
