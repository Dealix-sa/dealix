"""Workspaces — the unit of data and policy isolation."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class WorkspaceType(StrEnum):
    sovereign = "sovereign"
    dealix_internal = "dealix_internal"
    customer = "customer"
    partner = "partner"
    trust = "trust"
    venture = "venture"
    marketplace = "marketplace"
    api = "api"


class Workspace(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workspace_id: str
    workspace_type: WorkspaceType
    name: str
    owner_id: str
    tenant_id: str | None = None
    sovereignty_isolated: bool = False
    tags: list[str] = Field(default_factory=list)
    active: bool = True
