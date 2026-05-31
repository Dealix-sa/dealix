"""Tenants — top-level isolation boundary for customers and partners."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Tenant(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str
    name: str
    plan: str = "starter"
    data_residency: str = "saudi_arabia"
    active: bool = True
