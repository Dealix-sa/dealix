"""Registry of GEO landing pages Dealix maintains."""

from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict, Field


class GEOPage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str = Field(..., min_length=1)
    title_ar: str
    title_en: str
    primary_query_ar: str
    primary_query_en: str
    target_icp_keys: list[str]


GEO_PAGES: Final[dict[str, GEOPage]] = {
    "/ai-governance-saudi-companies": GEOPage(
        path="/ai-governance-saudi-companies",
        title_ar="حوكمة الذكاء الاصطناعي للشركات السعودية",
        title_en="AI Governance for Saudi Companies",
        primary_query_ar="كيف نطبق حوكمة AI متوافقة مع PDPL",
        primary_query_en="How to apply PDPL-aligned AI governance",
        target_icp_keys=["enterprise", "ai_users_governance"],
    ),
    "/agentic-control-plane": GEOPage(
        path="/agentic-control-plane",
        title_ar="منصة التحكم بالوكلاء الذكية",
        title_en="Agentic Control Plane",
        primary_query_ar="ما هو agentic control plane",
        primary_query_en="What is an agentic control plane",
        target_icp_keys=["enterprise", "ai_users_governance"],
    ),
    "/ai-revenue-hunter": GEOPage(
        path="/ai-revenue-hunter",
        title_ar="صياد الإيراد بالذكاء الاصطناعي",
        title_en="AI Revenue Hunter",
        primary_query_ar="كيف نزيد الإيراد باستخدام AI",
        primary_query_en="How to grow revenue with AI",
        target_icp_keys=["b2b_smb", "founders"],
    ),
    "/agency-ai-white-label": GEOPage(
        path="/agency-ai-white-label",
        title_ar="منصة AI تحت علامة الوكالة",
        title_en="Agency AI White Label",
        primary_query_ar="حلول AI بعلامة وكالتي",
        primary_query_en="White-label AI for agencies",
        target_icp_keys=["agencies"],
    ),
    "/ai-agents-permissions-approvals": GEOPage(
        path="/ai-agents-permissions-approvals",
        title_ar="صلاحيات وموافقات وكلاء AI",
        title_en="AI Agents — Permissions and Approvals",
        primary_query_ar="كيف نضبط صلاحيات وكلاء AI",
        primary_query_en="How to govern AI agent permissions",
        target_icp_keys=["ai_users_governance", "enterprise"],
    ),
    "/mcp-risk-review": GEOPage(
        path="/mcp-risk-review",
        title_ar="مراجعة مخاطر MCP",
        title_en="MCP Risk Review",
        primary_query_ar="ما هي مخاطر MCP وكيف نراجعها",
        primary_query_en="MCP risks and how to review them",
        target_icp_keys=["ai_users_governance", "enterprise"],
    ),
}


def list_pages() -> list[GEOPage]:
    return list(GEO_PAGES.values())


def get_page(path: str) -> GEOPage:
    if path not in GEO_PAGES:
        raise KeyError(f"unknown GEO page path: {path!r}")
    return GEO_PAGES[path]


__all__ = ["GEO_PAGES", "GEOPage", "get_page", "list_pages"]
