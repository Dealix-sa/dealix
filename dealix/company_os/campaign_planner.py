"""Governed, evidence-first commercial campaign planning for directory companies."""
from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from typing import Any

from dealix.company_os.company_directory import DirectoryCandidate


@dataclass(frozen=True)
class ContactPermission:
    relationship_status: str = "unknown"
    channel: str = "research_only"
    consent_status: str = "unknown"
    opt_out: bool = False
    evidence_id: str | None = None


@dataclass(frozen=True)
class CampaignItem:
    id: str
    company_id: str
    company_name: str
    offer_id: str
    value_angle_ar: str
    channel: str
    status: str
    why_now: str
    qualification_questions_ar: tuple[str, ...]
    draft_preview_ar: str
    approval_required: bool
    external_action_permitted: bool
    blockers: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CampaignPlan:
    id: str
    mode: str
    audience_count: int
    research_only_count: int
    draft_ready_count: int
    items: tuple[CampaignItem, ...]
    guardrails: tuple[str, ...]
    external_actions_performed: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _permission_route(permission: ContactPermission) -> tuple[str, str, list[str]]:
    blockers: list[str] = []
    relationship_ok = permission.relationship_status in {
        "warm",
        "inbound",
        "customer",
        "referral",
        "known",
    }
    if permission.opt_out:
        return "blocked", "blocked", ["opt_out"]
    if not relationship_ok:
        blockers.append("relationship_not_proven")
    channel = permission.channel.casefold()
    if channel in ("whatsapp", "whatsapp_business"):
        if permission.consent_status != "opted_in" or not permission.evidence_id:
            blockers.append("whatsapp_opt_in_not_proven")
        return (
            "whatsapp_template_draft" if not blockers else "research_only",
            "draft_ready" if not blockers else "research_only",
            blockers,
        )
    if channel == "email":
        if permission.consent_status not in {"opted_in", "existing_relationship"}:
            blockers.append("email_permission_not_proven")
        return (
            "email_draft" if not blockers else "research_only",
            "draft_ready" if not blockers else "research_only",
            blockers,
        )
    if channel == "linkedin":
        blockers.append("linkedin_manual_send_only")
        return "linkedin_manual_draft", "draft_only_manual_send", blockers
    blockers.append("approved_channel_missing")
    return "research_only", "research_only", blockers


def build_campaign_plan(
    candidates: list[DirectoryCandidate],
    *,
    permissions: dict[str, ContactPermission] | None = None,
    max_items: int = 25,
) -> CampaignPlan:
    permission_map = permissions or {}
    selected = sorted(
        candidates,
        key=lambda candidate: (
            -candidate.research_priority_score,
            candidate.company_name,
        ),
    )[: max(1, min(max_items, 100))]
    items: list[CampaignItem] = []
    for candidate in selected:
        permission = permission_map.get(candidate.id, ContactPermission())
        channel, status, blockers = _permission_route(permission)
        why_now = (
            f"ملاءمة بحثية {candidate.research_priority_score:.1f}/100؛ "
            f"النشاط: {candidate.activity or 'غير محدد'}."
        )
        draft = (
            f"مرحبًا فريق {candidate.company_name}، أعددنا فرضية أولية حول "
            f"{candidate.value_angle_ar} قبل اقتراح أي حل نحتاج فهم خط الأساس "
            "والأولوية وصاحب القرار. هذه مسودة داخلية وليست رسالة مرسلة."
        )
        item_id = hashlib.sha256(
            f"{candidate.id}|{candidate.recommended_offer_id}|{channel}".encode("utf-8")
        ).hexdigest()[:20]
        items.append(
            CampaignItem(
                id=f"campaign_item_{item_id}",
                company_id=candidate.id,
                company_name=candidate.company_name,
                offer_id=candidate.recommended_offer_id,
                value_angle_ar=candidate.value_angle_ar,
                channel=channel,
                status=status,
                why_now=why_now,
                qualification_questions_ar=(
                    "ما أكبر عبء تشغيلي يستهلك وقت الفريق اليوم؟",
                    "ما أثره المالي أو أثره على العميل وكيف تقيسونه؟",
                    "من يملك القرار وما التوقيت المتوقع؟",
                    "ما الأنظمة والقيود التي يجب أن يعمل Dealix ضمنها؟",
                ),
                draft_preview_ar=draft,
                approval_required=True,
                external_action_permitted=False,
                blockers=tuple(dict.fromkeys(blockers)),
            )
        )
    digest = hashlib.sha256("|".join(item.id for item in items).encode("utf-8")).hexdigest()
    return CampaignPlan(
        id=f"campaign_{digest[:20]}",
        mode="draft_only",
        audience_count=len(items),
        research_only_count=sum(item.status == "research_only" for item in items),
        draft_ready_count=sum(item.status == "draft_ready" for item in items),
        items=tuple(items),
        guardrails=(
            "no_live_send",
            "no_cold_whatsapp",
            "no_linkedin_automation",
            "no_scraping",
            "no_fake_proof",
            "approval_required_for_every_external_action",
        ),
        external_actions_performed=0,
    )
