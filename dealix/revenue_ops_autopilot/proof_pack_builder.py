"""Proof Pack Builder — assembles L0-L4 evidence from sprint output.

Evidence levels:
L0 = Claim (stated, not verified)
L1 = Screenshot / document
L2 = System-generated report (this tool)
L3 = Third-party verified (accountant, auditor)
L4 = Published case study (founder-approved + customer-consented)
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

_PROOF_LEVEL_RANK: dict[str, int] = {
    "L0": 0,
    "L1": 1,
    "L2": 2,
    "L3": 3,
    "L4": 4,
}

_VALID_EVIDENCE_TYPES = frozenset(
    {
        "financial_report",
        "operational_metric",
        "customer_quote",
        "audit_log",
        "screenshot",
        "system_report",
    }
)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ProofItem(BaseModel):
    """A single evidence item within a Proof Pack."""

    model_config = ConfigDict(extra="forbid")

    item_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Auto-generated unique identifier for this proof item.",
    )
    level: str = Field(
        ...,
        description="Evidence tier: L0 (unverified claim) through L4 (published case study).",
    )
    title_ar: str = Field(..., min_length=1, description="Arabic title for this proof item.")
    title_en: str = Field(..., min_length=1, description="English title for this proof item.")
    evidence_type: str = Field(
        ...,
        description="financial_report | operational_metric | customer_quote | audit_log | screenshot | system_report",
    )
    description_ar: str = Field(default="", description="Arabic description of the evidence.")
    description_en: str = Field(default="", description="English description of the evidence.")
    value_ar: str = Field(
        default="",
        description="Specific proven value in Arabic (time/cost framing, not revenue guarantee).",
    )
    value_en: str = Field(
        default="",
        description="Specific proven value in English (time/cost framing, not revenue guarantee).",
    )
    data_source: str = Field(
        default="sprint_output",
        description="Origin of the evidence data.",
    )
    verified: bool = Field(
        default=False,
        description="True when evidence has been cross-checked.",
    )
    verified_by: Optional[str] = Field(
        default=None,
        description="Identifier of the party who verified this item.",
    )
    verified_at: Optional[datetime] = Field(
        default=None,
        description="UTC timestamp of verification.",
    )
    customer_consented: bool = Field(
        default=False,
        description="Client has explicitly consented to inclusion in reports.",
    )
    publishable: bool = Field(
        default=False,
        description="True only when level >= L2, verified=True, and customer_consented=True.",
    )

    def model_post_init(self, __context: object) -> None:
        """Enforce publishable flag invariant."""
        # publishable can only be True if level >= L2, verified, and consented
        if self.publishable:
            rank = _PROOF_LEVEL_RANK.get(self.level, 0)
            if rank < _PROOF_LEVEL_RANK["L2"] or not self.verified or not self.customer_consented:
                # Silently downgrade — never auto-promote
                object.__setattr__(self, "publishable", False)


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


class ProofPackBuilder:
    """Extracts and structures proof items from 7-day sprint output.

    No external I/O. No LLM calls.
    """

    def from_sprint_output(self, sprint_results: dict, account_id: str) -> list[ProofItem]:
        """Extract proof items from 7-day sprint output.

        Day 1 (source audit)     → L1 proof items
        Day 2 (DQ score)         → L1 proof items
        Day 3 (account scoring)  → L1 proof items
        Day 4 (draft pack)       → L0 items
        Day 5 (governance)       → L0 items (approval state)
        Day 6 (proof assembly)   → L2 items
        Day 7 (capital/retainer) → L2 items

        :param sprint_results: Dict or list from SprintOrchestrator.run_all().
        :param account_id: Client account identifier (used for source labelling).
        """
        day_map = _normalise_sprint_results(sprint_results)
        items: list[ProofItem] = []

        items.extend(self._extract_day1_items(day_map.get(1, {}), account_id))
        items.extend(self._extract_day2_items(day_map.get(2, {}), account_id))
        items.extend(self._extract_day3_items(day_map.get(3, {}), account_id))
        items.extend(self._extract_day4_items(day_map.get(4, {}), account_id))
        items.extend(self._extract_day5_items(day_map.get(5, {}), account_id))
        items.extend(self._extract_day6_items(day_map.get(6, {}), account_id))
        items.extend(self._extract_day7_items(day_map.get(7, {}), account_id))

        return items

    def get_publishable(self, items: list[ProofItem]) -> list[ProofItem]:
        """Return only items safe for case studies (L2+ and customer-consented)."""
        return [
            i
            for i in items
            if i.publishable
            and _PROOF_LEVEL_RANK.get(i.level, 0) >= _PROOF_LEVEL_RANK["L2"]
        ]

    def as_markdown_section(self, items: list[ProofItem], locale: str = "ar") -> str:
        """Format proof items as a Markdown section for inclusion in reports."""
        if not items:
            return "## عناصر الإثبات / Proof Items\n\n_لا توجد عناصر. / No items._\n"

        lines: list[str] = ["## عناصر الإثبات / Proof Items\n"]

        for item in items:
            if locale == "ar":
                title = item.title_ar
                desc = item.description_ar
                value = item.value_ar
            else:
                title = item.title_en
                desc = item.description_en
                value = item.value_en

            verified_str = "نعم / Yes" if item.verified else "لا / No"
            publishable_str = "نعم / Yes" if item.publishable else "لا / No"

            lines.append(f"### [{item.level}] {title}")
            lines.append(f"- **النوع / Type:** {item.evidence_type}")
            lines.append(f"- **مصدر البيانات / Data Source:** {item.data_source}")
            lines.append(f"- **موثَّق / Verified:** {verified_str}")
            lines.append(f"- **قابل للنشر / Publishable:** {publishable_str}")
            if desc:
                lines.append(f"- **الوصف / Description:** {desc}")
            if value:
                lines.append(f"- **القيمة المُثبَتة / Proven Value:** {value}")
            if item.verified_by:
                lines.append(f"- **وثَّقه / Verified by:** {item.verified_by}")
            lines.append("")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Per-day extractors (private)
    # ------------------------------------------------------------------

    def _extract_day1_items(self, day_data: dict, account_id: str) -> list[ProofItem]:
        output = day_data.get("output", {})
        if not output:
            return []
        items: list[ProofItem] = []
        n = output.get("sources_audited", 0)
        all_valid = output.get("all_passports_valid", False)
        level = "L1" if all_valid else "L0"
        items.append(
            ProofItem(
                level=level,
                title_ar=f"تدقيق جواز المصدر — {n} مصدر",
                title_en=f"Source Passport Audit — {n} source(s)",
                evidence_type="audit_log",
                description_ar="تحقق من صلاحية جوازات مصادر البيانات.",
                description_en="Validated data source passports for this engagement.",
                value_ar=f"تم تدقيق {n} مصدر بيانات",
                value_en=f"{n} data source(s) audited",
                data_source=f"sprint_day1_{account_id}",
                verified=all_valid,
            )
        )
        return items

    def _extract_day2_items(self, day_data: dict, account_id: str) -> list[ProofItem]:
        output = day_data.get("output", {})
        if not output:
            return []
        items: list[ProofItem] = []
        score = output.get("overall_dq")
        rows = output.get("total_rows", 0)
        if score is not None:
            items.append(
                ProofItem(
                    level="L1",
                    title_ar=f"درجة جودة البيانات: {score}/100",
                    title_en=f"Data Quality Score: {score}/100",
                    evidence_type="operational_metric",
                    description_ar="درجة جودة البيانات المحسوبة عبر نظام Dealix.",
                    description_en="Data quality score computed by the Dealix DQ engine.",
                    value_ar=f"درجة DQ: {score}/100 عبر {rows} سجل",
                    value_en=f"DQ score: {score}/100 across {rows} records",
                    data_source=f"sprint_day2_{account_id}",
                    verified=True,
                )
            )
        return items

    def _extract_day3_items(self, day_data: dict, account_id: str) -> list[ProofItem]:
        output = day_data.get("output", {})
        if not output:
            return []
        items: list[ProofItem] = []
        total = output.get("total_accounts", 0)
        top = output.get("top_10", [])
        if top:
            items.append(
                ProofItem(
                    level="L1",
                    title_ar=f"قائمة أعلى {len(top)} حسابات بمعيار ICP",
                    title_en=f"Top {len(top)} Accounts by ICP Score",
                    evidence_type="operational_metric",
                    description_ar="تصنيف الحسابات بمعيار ICP لتحديد أولويات التواصل.",
                    description_en="Accounts ranked by ICP score to prioritise outreach.",
                    value_ar=f"تم تصنيف {total} حساب — أعلى {len(top)} معرَّفة",
                    value_en=f"{total} accounts scored — top {len(top)} identified",
                    data_source=f"sprint_day3_{account_id}",
                    verified=True,
                )
            )
        return items

    def _extract_day4_items(self, day_data: dict, account_id: str) -> list[ProofItem]:
        output = day_data.get("output", {})
        if not output:
            return []
        items: list[ProofItem] = []
        drafts = output.get("whatsapp_drafts", [])
        n = len(drafts)
        passed = output.get("all_drafts_passed_governance", False)
        if n:
            items.append(
                ProofItem(
                    level="L0",
                    title_ar=f"{n} مسودة رسائل (Draft Only)",
                    title_en=f"{n} Message Draft(s) (Draft Only)",
                    evidence_type="audit_log",
                    description_ar="مسودات اتصال تنتظر موافقة المؤسس قبل الإرسال.",
                    description_en="Communication drafts awaiting founder approval before sending.",
                    value_ar=f"أنشئت {n} مسودة — الحوكمة: {'ناجحة' if passed else 'تحتاج مراجعة'}",
                    value_en=f"{n} draft(s) created — governance: {'passed' if passed else 'review required'}",
                    data_source=f"sprint_day4_{account_id}",
                    verified=False,
                )
            )
        return items

    def _extract_day5_items(self, day_data: dict, account_id: str) -> list[ProofItem]:
        output = day_data.get("output", {})
        if not output:
            return []
        items: list[ProofItem] = []
        approved = output.get("approved", False)
        items.append(
            ProofItem(
                level="L0",
                title_ar="قرار الحوكمة — موافقة المؤسس",
                title_en="Governance Decision — Founder Approval",
                evidence_type="audit_log",
                description_ar="تحقق من موافقة المؤسس على مخرجات Sprint.",
                description_en="Founder approval status for sprint outputs.",
                value_ar="موافقة المؤسس: " + ("تم التأكيد" if approved else "في الانتظار"),
                value_en="Founder approval: " + ("confirmed" if approved else "pending"),
                data_source=f"sprint_day5_{account_id}",
                verified=approved,
            )
        )
        return items

    def _extract_day6_items(self, day_data: dict, account_id: str) -> list[ProofItem]:
        output = day_data.get("output", {})
        if not output:
            return []
        items: list[ProofItem] = []
        score = output.get("completeness_score")
        band = output.get("strength_band", "")
        if score is not None:
            items.append(
                ProofItem(
                    level="L2",
                    title_ar=f"Proof Pack — اكتمال {score}/100 ({band})",
                    title_en=f"Proof Pack — Completeness {score}/100 ({band})",
                    evidence_type="system_report",
                    description_ar="تقرير Proof Pack المولَّد من منظومة Dealix.",
                    description_en="Proof Pack report generated by the Dealix system.",
                    value_ar=f"حزمة إثبات مكتملة بنسبة {score}/100",
                    value_en=f"Proof pack assembled at {score}/100 completeness",
                    data_source=f"sprint_day6_{account_id}",
                    verified=True,
                )
            )
        return items

    def _extract_day7_items(self, day_data: dict, account_id: str) -> list[ProofItem]:
        output = day_data.get("output", {})
        if not output:
            return []
        items: list[ProofItem] = []
        asset_id = output.get("capital_asset_id", "")
        if asset_id:
            items.append(
                ProofItem(
                    level="L2",
                    title_ar="أصل رأسمالي مسجَّل",
                    title_en="Capital Asset Registered",
                    evidence_type="system_report",
                    description_ar="تسجيل أصل قابل لإعادة الاستخدام في سجل الرأسمال.",
                    description_en="Reusable asset recorded in the capital registry.",
                    value_ar=f"أصل رأسمالي: {asset_id}",
                    value_en=f"Capital asset: {asset_id}",
                    data_source=f"sprint_day7_{account_id}",
                    verified=True,
                )
            )

        retainer_eligible = output.get("retainer_eligible", False)
        offer = output.get("recommended_offer", "")
        items.append(
            ProofItem(
                level="L2",
                title_ar="تقييم أهلية الـRetainer",
                title_en="Retainer Eligibility Assessment",
                evidence_type="system_report",
                description_ar="تقييم موضوعي لأهلية العميل للانتقال إلى الإدارة الشهرية.",
                description_en="Objective assessment of client eligibility for monthly managed ops.",
                value_ar=(
                    f"مؤهَّل — المقترح: {offer}"
                    if retainer_eligible
                    else "غير مؤهَّل — ثغرات مسجَّلة"
                ),
                value_en=(
                    f"Eligible — recommended: {offer}"
                    if retainer_eligible
                    else "Not eligible — gaps documented"
                ),
                data_source=f"sprint_day7_{account_id}",
                verified=True,
            )
        )
        return items


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalise_sprint_results(sprint_results: object) -> dict[int, dict]:
    """Convert orchestrator output (list or dict) into a day-keyed dict."""
    day_map: dict[int, dict] = {}
    if isinstance(sprint_results, list):
        for item in sprint_results:
            if isinstance(item, dict):
                d = int(item.get("day", 0))
                if d:
                    day_map[d] = item
    elif isinstance(sprint_results, dict):
        for k, v in sprint_results.items():
            try:
                d = int(k)
                day_map[d] = v if isinstance(v, dict) else {}
            except (ValueError, TypeError):
                pass
    return day_map


__all__ = [
    "ProofItem",
    "ProofPackBuilder",
]
