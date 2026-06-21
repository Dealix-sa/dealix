"""Transformation OS Proposal Generator — bilingual (AR+EN), governed, stateless.

Builds an enterprise transformation proposal from the canonical service catalog
(`auto_client_acquisition.service_catalog`). It NEVER hardcodes prices (Article 11
+ no_invented_crm_kpi) — every figure is read from the registry and stamped as an
estimate (Article 8). Output defaults to `approval_status="approval_required"` and
is never auto-sent (NO_LIVE_SEND). Guaranteed-outcome language in the request is
rejected (doctrine: no_guaranteed_sales_claims).

Input:  TransformationProposalRequest (company, sector, selected_system_ids, …)
Output: TransformationProposal (line items from catalog + bilingual markdown)
Gate:   approval_required — founder reviews before anything reaches a customer.
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.service_catalog import get_offering

log = logging.getLogger(__name__)

# Tokens that would turn a proposal into a forbidden guarantee (doctrine).
_FORBIDDEN_AR = ("نضمن", "ضمان مؤكد", "مضمون")
_FORBIDDEN_EN = ("guarantee", "guaranteed")

_DISCLAIMER_AR = "القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value."
_APPROVAL_NOTE_AR = "هذا العرض للمراجعة فقط — لن يُرسَل لأي عميل دون موافقة المؤسس."
_APPROVAL_NOTE_EN = "This proposal is for review only — will not be sent without founder approval."


class TransformationProposalError(ValueError):
    """Raised on doctrine violation or empty/invalid selection. Routers map → 400."""


class TransformationProposalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company_name: str = Field(..., min_length=1)
    sector: str = "b2b_services"
    selected_system_ids: list[str] = Field(default_factory=list)
    stakeholders: list[str] = Field(default_factory=list)  # e.g. CEO, CFO, CTO, COO
    pain_points: list[str] = Field(default_factory=list)
    notes: str = ""


class ProposalLineItem(BaseModel):
    system_id: str
    name_ar: str
    name_en: str
    price_unit: str
    setup_sar_min: float
    setup_sar_max: float | None = None
    monthly_sar_min: float | None = None
    monthly_sar_max: float | None = None
    deliverables: list[str] = Field(default_factory=list)
    is_estimate: bool = True


class TransformationProposal(BaseModel):
    proposal_id: str
    company_name: str
    sector: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    stakeholders: list[str] = Field(default_factory=list)
    line_items: list[ProposalLineItem]
    unknown_system_ids: list[str] = Field(default_factory=list)
    total_setup_sar_min: float = 0.0
    total_setup_sar_max: float = 0.0
    total_monthly_sar_min: float = 0.0
    total_monthly_sar_max: float = 0.0
    markdown_ar_en: str = ""
    is_estimate: bool = True
    approval_status: str = "approval_required"
    governance_decision: str = "pending"  # pending | approved | rejected

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


class TransformationProposalGenerator:
    """Assembles a bilingual transformation proposal from catalog offerings."""

    def generate(self, req: TransformationProposalRequest) -> TransformationProposal:
        self._guard_no_guarantee(req)

        if not req.selected_system_ids:
            raise TransformationProposalError(
                "selected_system_ids is empty — اختر نظامًا واحدًا على الأقل من الكتالوج."
            )

        line_items: list[ProposalLineItem] = []
        unknown: list[str] = []
        for sid in req.selected_system_ids:
            offering = get_offering(sid)
            # Only enterprise transformation systems are valid here.
            if offering is None or offering.customer_journey_stage != "transformation":
                unknown.append(sid)
                continue
            line_items.append(
                ProposalLineItem(
                    system_id=offering.id,
                    name_ar=offering.name_ar,
                    name_en=offering.name_en,
                    price_unit=offering.price_unit,
                    setup_sar_min=offering.price_sar,
                    setup_sar_max=offering.price_sar_max,
                    monthly_sar_min=offering.price_monthly_sar_min,
                    monthly_sar_max=offering.price_monthly_sar_max,
                    deliverables=list(offering.deliverables),
                )
            )

        if not line_items:
            raise TransformationProposalError(
                "No valid transformation systems selected — "
                f"unknown ids: {', '.join(unknown) or '(none)'}"
            )

        totals = self._totals(line_items)
        proposal_id = self._proposal_id(req)
        proposal = TransformationProposal(
            proposal_id=proposal_id,
            company_name=req.company_name,
            sector=req.sector,
            stakeholders=list(req.stakeholders),
            line_items=line_items,
            unknown_system_ids=unknown,
            **totals,
        )
        proposal.markdown_ar_en = self._render_markdown(req, proposal)
        log.info(
            "transformation_proposal_generated proposal_id=%s company=%s systems=%d",
            proposal_id,
            req.company_name,
            len(line_items),
        )
        return proposal

    # ── helpers ──────────────────────────────────────────────────────────

    def _guard_no_guarantee(self, req: TransformationProposalRequest) -> None:
        blob = " ".join([req.notes, *req.pain_points]).lower()
        if any(tok in blob for tok in _FORBIDDEN_EN) or any(
            tok in (req.notes + " ".join(req.pain_points)) for tok in _FORBIDDEN_AR
        ):
            raise TransformationProposalError(
                "Guaranteed-outcome language is forbidden (no_guaranteed_sales_claims) — "
                "ممنوع وعود مبيعات مضمونة."
            )

    @staticmethod
    def _proposal_id(req: TransformationProposalRequest) -> str:
        seed = f"{req.company_name}{req.sector}{datetime.now(UTC).isoformat()}"
        return "txp_" + hashlib.sha256(seed.encode()).hexdigest()[:16]

    @staticmethod
    def _totals(items: list[ProposalLineItem]) -> dict[str, float]:
        setup_min = sum(i.setup_sar_min for i in items)
        # For the ceiling, fall back to the floor when a system has no max (custom).
        setup_max = sum(
            (i.setup_sar_max if i.setup_sar_max is not None else i.setup_sar_min) for i in items
        )
        monthly_min = sum((i.monthly_sar_min or 0.0) for i in items)
        monthly_max = sum(
            (i.monthly_sar_max if i.monthly_sar_max is not None else (i.monthly_sar_min or 0.0))
            for i in items
        )
        return {
            "total_setup_sar_min": float(setup_min),
            "total_setup_sar_max": float(setup_max),
            "total_monthly_sar_min": float(monthly_min),
            "total_monthly_sar_max": float(monthly_max),
        }

    @staticmethod
    def _fmt_range(low: float | None, high: float | None) -> str:
        if not low and not high:
            return "Custom / مخصص"
        lo = f"{int(low):,}" if low else "0"
        if high is None or high == low:
            return f"{lo} SAR"
        return f"{lo}–{int(high):,} SAR"

    def _render_markdown(
        self, req: TransformationProposalRequest, p: TransformationProposal
    ) -> str:
        now = p.generated_at.strftime("%Y-%m-%d")
        lines: list[str] = [
            f"# عرض التحول — {req.company_name}",
            f"**Dealix Transformation Proposal — {req.company_name}**",
            "",
            f"المعرف: `{p.proposal_id}` | التاريخ: {now} | الحالة: **يتطلب موافقة المؤسس**",
            f"ID: `{p.proposal_id}` | Date: {now} | Status: **approval_required**",
            "",
            f"القطاع / Sector: {req.sector}",
        ]
        if req.stakeholders:
            lines.append(f"أصحاب القرار / Stakeholders: {', '.join(req.stakeholders)}")
        lines += [
            "",
            "## ملخص تنفيذي / Executive Summary",
            "",
            "نصمّم نظام تشغيل أعمال AI-native يحوّل العمليات اليومية إلى workflows "
            "قابلة للقياس، مرتبطة بالمبيعات والتقارير والحوكمة وتجربة العميل.",
            "",
            "We design an AI-native business operating system that turns daily operations "
            "into measurable workflows wired to sales, reporting, governance, and CX.",
            "",
            "## الأنظمة المقترحة / Recommended Systems",
            "",
            "| System | Setup (estimate) | Monthly (estimate) |",
            "|---|---|---|",
        ]
        for it in p.line_items:
            setup = self._fmt_range(it.setup_sar_min, it.setup_sar_max)
            monthly = self._fmt_range(it.monthly_sar_min, it.monthly_sar_max)
            lines.append(f"| {it.name_en} — {it.name_ar} | {setup} | {monthly} |")
        lines += [
            "",
            f"**إجمالي الإعداد التقديري / Estimated total setup:** "
            f"{self._fmt_range(p.total_setup_sar_min, p.total_setup_sar_max)}",
            f"**إجمالي الشهري التقديري / Estimated total monthly:** "
            f"{self._fmt_range(p.total_monthly_sar_min, p.total_monthly_sar_max)}",
            "",
        ]
        for it in p.line_items:
            lines += [f"### {it.name_en} — {it.name_ar}", ""]
            lines += [f"- {d}" for d in it.deliverables]
            lines.append("")
        if p.unknown_system_ids:
            lines += [
                "> تم تجاهل معرفات غير معروفة / Ignored unknown ids: "
                + ", ".join(p.unknown_system_ids),
                "",
            ]
        lines += [
            "## خطة التسليم / Delivery Plan",
            "",
            "| Phase | Output |",
            "|---|---|",
            "| Diagnostic | Workflow map, leakage map, KPIs, data sources |",
            "| Prototype | Dashboard wireframe, workflow states, report sample |",
            "| Build | System, automations, templates, reports, SOPs |",
            "| Pilot | Live usage, feedback, first weekly report |",
            "| Scale | More workflows, integrations, governance, SLA |",
            "",
            "## الحوكمة / Governance",
            "",
            "- كل إرسال خارجي مسودة تتطلب موافقة — لا إرسال تلقائي.",
            "- All external sends are approval-gated drafts — no autonomous execution.",
            "- لا واتساب بارد، لا أتمتة LinkedIn، لا scraping، لا إرسال جماعي.",
            "",
            "## الخطوة التالية / Next Step",
            "",
            "جلسة تشخيص تحوّل مدفوعة (٤٥ دقيقة) قبل أي التزام كبير.",
            "A paid 45-minute transformation diagnostic before any large commitment.",
            "",
            "---",
            "",
            f"> {_APPROVAL_NOTE_AR}",
            f"> {_APPROVAL_NOTE_EN}",
            "",
            f"> **{_DISCLAIMER_AR}**",
        ]
        return "\n".join(lines)
