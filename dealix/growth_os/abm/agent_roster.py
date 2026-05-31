"""Metadata-only registry of ABM agent personas.

These are not executable agents — they are role descriptors that the
draft / proposal flow attributes work to. No external sends.
"""

from __future__ import annotations

from typing import Final

from pydantic import BaseModel, ConfigDict, Field


class AgentMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str = Field(..., min_length=1)
    role_ar: str
    role_en: str
    responsibility_ar: str
    responsibility_en: str
    produces: list[str]
    requires_approval: bool = True


ABM_AGENT_ROSTER: Final[dict[str, AgentMetadata]] = {
    "account_research": AgentMetadata(
        key="account_research",
        role_ar="باحث الحسابات",
        role_en="Account Research",
        responsibility_ar="جمع إشارات عامة عن الحساب من مصادر مفتوحة",
        responsibility_en="Collects public, source-passport signals about the account",
        produces=["account_brief", "public_signals_list"],
    ),
    "stakeholder_mapper": AgentMetadata(
        key="stakeholder_mapper",
        role_ar="مخطّط أصحاب القرار",
        role_en="Stakeholder Mapper",
        responsibility_ar="يرسم خريطة أصحاب القرار والمؤيدين والمعارضين",
        responsibility_en="Maps champions, decision-makers, and blockers",
        produces=["stakeholder_map", "influence_graph"],
    ),
    "pain_hypothesis": AgentMetadata(
        key="pain_hypothesis",
        role_ar="فرضية الألم",
        role_en="Pain Hypothesis",
        responsibility_ar="يصيغ فرضية ألم قابلة للاختبار",
        responsibility_en="Drafts a testable pain hypothesis grounded in evidence",
        produces=["pain_hypothesis_draft"],
    ),
    "personalized_pitch": AgentMetadata(
        key="personalized_pitch",
        role_ar="عرض مخصّص",
        role_en="Personalized Pitch",
        responsibility_ar="يحوّل الفرضية إلى عرض مخصّص بمسوّدة فقط",
        responsibility_en="Converts hypothesis to a draft personalized offer",
        produces=["offer_draft", "value_one_pager_draft"],
    ),
    "followup": AgentMetadata(
        key="followup",
        role_ar="المتابعة",
        role_en="Follow-up",
        responsibility_ar="يقترح إيقاع متابعة بشري بدون أتمتة بارد",
        responsibility_en="Suggests human follow-up cadence, no cold automation",
        produces=["followup_plan_draft"],
    ),
    "deal_room": AgentMetadata(
        key="deal_room",
        role_ar="غرفة الصفقة",
        role_en="Deal Room",
        responsibility_ar="يجمع الإثباتات والعقود في غرفة الصفقة",
        responsibility_en="Assembles proofs and contracts into a deal room",
        produces=["deal_room_index", "proof_pack_link"],
    ),
}


def list_agents() -> list[AgentMetadata]:
    return list(ABM_AGENT_ROSTER.values())


def get_agent(key: str) -> AgentMetadata:
    if key not in ABM_AGENT_ROSTER:
        raise KeyError(f"unknown ABM agent key: {key!r}")
    return ABM_AGENT_ROSTER[key]


__all__ = ["ABM_AGENT_ROSTER", "AgentMetadata", "get_agent", "list_agents"]
