"""Sprint Report Generator — bilingual deliverable for Day 7 sprint close.

Generates a complete Sprint Proof Report for the client.
All reports require founder review before client delivery.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class SprintDayRecord(BaseModel):
    """Record of a single sprint day execution."""

    model_config = ConfigDict(extra="forbid")

    day: int = Field(..., ge=1, le=7, description="Sprint day number 1-7.")
    status: str = Field(..., description="completed | skipped | partial")
    headline_ar: str = Field(..., min_length=1, description="Arabic headline for this day.")
    headline_en: str = Field(..., min_length=1, description="English headline for this day.")
    deliverables: list[str] = Field(
        default_factory=list,
        description="List of deliverable descriptions produced on this day.",
    )
    data_source: str = Field(..., min_length=1, description="What data was used on this day.")
    completed_at: Optional[datetime] = Field(
        default=None, description="UTC timestamp when this day was completed."
    )


class SprintProofReport(BaseModel):
    """Complete Sprint Proof Report for a Revenue Intelligence Sprint."""

    model_config = ConfigDict(extra="forbid")

    sprint_id: str = Field(..., min_length=1)
    account_id: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    service_tier: str = Field(default="sprint_499")
    week_label: str = Field(..., description='Label such as "Week of 2026-06-01".')
    day_records: list[SprintDayRecord] = Field(default_factory=list)

    # Executive Summary
    summary_ar: str = Field(default="")
    summary_en: str = Field(default="")

    # Key Findings (3-5 bullets per language)
    findings_ar: list[str] = Field(default_factory=list)
    findings_en: list[str] = Field(default_factory=list)

    # Proof Items (L0-L4)
    proof_items: list[dict] = Field(
        default_factory=list,
        description="Each item: {level, title_ar, title_en, evidence_type, verified}",
    )

    # Recommended Next Steps
    next_steps_ar: list[str] = Field(default_factory=list)
    next_steps_en: list[str] = Field(default_factory=list)

    # Retainer recommendation
    retainer_recommended: bool = Field(default=False)
    retainer_tier: Optional[str] = Field(
        default=None, description="starter_2999 | growth_3999 | scale_4999"
    )
    retainer_reason_ar: str = Field(default="")
    retainer_reason_en: str = Field(default="")

    # Governance — always True; founder must approve before delivery
    requires_founder_review: bool = Field(default=True)
    approved_at: Optional[datetime] = Field(default=None)

    def as_markdown(self) -> str:
        """Render the report as a bilingual Markdown document."""
        lines: list[str] = []

        lines.append(f"# Sprint Proof Report — {self.company_name}\n")
        lines.append(f"**Sprint ID:** `{self.sprint_id}`  ")
        lines.append(f"**Account:** `{self.account_id}`  ")
        lines.append(f"**Service Tier:** `{self.service_tier}`  ")
        lines.append(f"**Period:** {self.week_label}  ")
        approval_note = (
            f"Approved: {self.approved_at.isoformat()}"
            if self.approved_at
            else "**Pending founder review — do not share with client.**"
        )
        lines.append(f"**Status:** {approval_note}  ")
        lines.append("")

        # Executive Summary
        lines.append("---\n")
        lines.append("## الملخص التنفيذي / Executive Summary\n")
        if self.summary_ar:
            lines.append(f"**AR:** {self.summary_ar}\n")
        if self.summary_en:
            lines.append(f"**EN:** {self.summary_en}\n")

        # Key Findings
        if self.findings_ar or self.findings_en:
            lines.append("---\n")
            lines.append("## أبرز النتائج / Key Findings\n")
            if self.findings_ar:
                lines.append("**AR:**")
                for f_ar in self.findings_ar:
                    lines.append(f"- {f_ar}")
                lines.append("")
            if self.findings_en:
                lines.append("**EN:**")
                for f_en in self.findings_en:
                    lines.append(f"- {f_en}")
                lines.append("")

        # Day Records
        if self.day_records:
            lines.append("---\n")
            lines.append("## سجل الأيام / Day-by-Day Log\n")
            for rec in self.day_records:
                status_emoji = {"completed": "[OK]", "partial": "[~]", "skipped": "[-]"}.get(
                    rec.status, "[?]"
                )
                lines.append(f"### {status_emoji} Day {rec.day}: {rec.headline_en} / {rec.headline_ar}")
                lines.append(f"- **Status:** {rec.status}")
                lines.append(f"- **Data source:** {rec.data_source}")
                if rec.completed_at:
                    lines.append(f"- **Completed at:** {rec.completed_at.isoformat()}")
                if rec.deliverables:
                    lines.append("- **Deliverables:**")
                    for d in rec.deliverables:
                        lines.append(f"  - {d}")
                lines.append("")

        # Proof Items
        if self.proof_items:
            lines.append("---\n")
            lines.append("## عناصر الإثبات / Proof Items\n")
            for item in self.proof_items:
                level = item.get("level", "L0")
                title_en = item.get("title_en", "")
                title_ar = item.get("title_ar", "")
                verified = item.get("verified", False)
                ev_type = item.get("evidence_type", "")
                verified_str = "Yes" if verified else "No"
                lines.append(
                    f"- **[{level}]** {title_en} / {title_ar} "
                    f"| Type: {ev_type} | Verified: {verified_str}"
                )
            lines.append("")

        # Next Steps
        if self.next_steps_ar or self.next_steps_en:
            lines.append("---\n")
            lines.append("## الخطوات التالية / Recommended Next Steps\n")
            if self.next_steps_ar:
                lines.append("**AR:**")
                for ns in self.next_steps_ar:
                    lines.append(f"- {ns}")
                lines.append("")
            if self.next_steps_en:
                lines.append("**EN:**")
                for ns in self.next_steps_en:
                    lines.append(f"- {ns}")
                lines.append("")

        # Retainer Recommendation
        lines.append("---\n")
        lines.append("## توصية الـRetainer / Retainer Recommendation\n")
        if self.retainer_recommended and self.retainer_tier:
            lines.append(f"**Recommended Tier:** `{self.retainer_tier}`  ")
            if self.retainer_reason_ar:
                lines.append(f"**AR:** {self.retainer_reason_ar}  ")
            if self.retainer_reason_en:
                lines.append(f"**EN:** {self.retainer_reason_en}  ")
        else:
            lines.append("No retainer recommended at this time.  ")
        lines.append("")

        # Governance note
        lines.append("---\n")
        lines.append("## ملاحظة الحوكمة / Governance Note\n")
        lines.append(
            "> هذا التقرير يتطلب مراجعة المؤسس قبل المشاركة مع العميل.  \n"
            "> This report requires founder review before sharing with the client."
        )

        return "\n".join(lines)

    def to_dict(self) -> dict:
        """Serialize the report to a plain dictionary."""
        return self.model_dump(mode="json")


# ---------------------------------------------------------------------------
# Default day headlines
# ---------------------------------------------------------------------------

_DAY_DEFAULTS: dict[int, tuple[str, str, list[str]]] = {
    1: (
        "تدقيق جواز المصدر",
        "Source Passport Audit",
        ["Source passport validated", "DQ baseline established"],
    ),
    2: (
        "درجة جودة البيانات",
        "Data Quality Score",
        ["DQ score computed per source", "Red flags documented"],
    ),
    3: (
        "تصنيف الحسابات",
        "Account Scoring",
        ["Top 10 accounts ranked by ICP score", "Recommended actions generated"],
    ),
    4: (
        "حزمة المسوّدات",
        "Draft Pack",
        ["WhatsApp drafts created", "Email sequence drafted", "Proposal rendered"],
    ),
    5: (
        "مراجعة الحوكمة",
        "Governance Review",
        ["Founder approval gate checked", "Drafts cleared or flagged"],
    ),
    6: (
        "تجميع حزمة الإثبات",
        "Proof Pack Assembly",
        ["L0-L4 evidence collected", "Proof Pack completeness scored"],
    ),
    7: (
        "تسجيل الأصل الرأسمالي وأهلية الـRetainer",
        "Capital Asset Registration & Retainer Eligibility",
        ["Capital asset registered", "Retainer eligibility evaluated"],
    ),
}


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------


class SprintReportGenerator:
    """Generates Sprint Proof Reports. No external I/O. No LLM calls."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_from_orchestrator_output(
        self,
        sprint_id: str,
        account_id: str,
        company_name: str,
        orchestrator_results: dict,
    ) -> SprintProofReport:
        """Generate a full proof report from completed sprint output.

        :param sprint_id: Unique sprint identifier.
        :param account_id: Client account identifier.
        :param company_name: Human-readable company name.
        :param orchestrator_results: Dict produced by
            ``SprintOrchestrator.run_all()`` where keys are day numbers (int
            or str) and values are ``SprintDayResult.to_dict()`` outputs.
        """
        day_records: list[SprintDayRecord] = []
        proof_items: list[dict] = []
        retainer_eligible = False
        retainer_tier: str | None = None

        # Normalise the orchestrator results into a day-keyed dict
        day_map: dict[int, dict] = {}
        if isinstance(orchestrator_results, list):
            for item in orchestrator_results:
                if isinstance(item, dict):
                    d = int(item.get("day", 0))
                    if d:
                        day_map[d] = item
        elif isinstance(orchestrator_results, dict):
            for k, v in orchestrator_results.items():
                try:
                    d = int(k)
                    day_map[d] = v if isinstance(v, dict) else {}
                except (ValueError, TypeError):
                    pass

        for day_num in range(1, 8):
            day_data = day_map.get(day_num, {})
            day_output = day_data.get("output", {}) if day_data else {}
            raw_status = (day_data.get("status", "skipped") if day_data else "skipped")
            status = _normalise_status(raw_status)

            defaults = _DAY_DEFAULTS.get(day_num, ("", f"Day {day_num}", []))
            headline_ar = day_data.get("title_ar", defaults[0]) if day_data else defaults[0]
            headline_en = day_data.get("title_en", defaults[1]) if day_data else defaults[1]

            # Build deliverables from the output dict
            deliverables = _extract_deliverables(day_num, day_output)
            data_source = _extract_data_source(day_num, day_output)

            completed_at: datetime | None = None
            if status == "completed" and day_data.get("generated_at"):
                try:
                    completed_at = datetime.fromisoformat(day_data["generated_at"])
                except (ValueError, TypeError):
                    completed_at = None

            day_records.append(
                SprintDayRecord(
                    day=day_num,
                    status=status,
                    headline_ar=headline_ar or defaults[0],
                    headline_en=headline_en or defaults[1],
                    deliverables=deliverables or list(defaults[2]),
                    data_source=data_source,
                    completed_at=completed_at,
                )
            )

            # Collect proof items from each day
            items = _extract_proof_items(day_num, day_output)
            proof_items.extend(items)

            # Retainer signals from Day 7
            if day_num == 7 and day_output:
                retainer_eligible = bool(day_output.get("retainer_eligible", False))
                offer = day_output.get("recommended_offer", "")
                if retainer_eligible and offer:
                    retainer_tier = _map_offer_to_tier(offer)

        # Build summary from Day 2 DQ + Day 3 scoring
        summary_en, summary_ar = _build_summary(account_id, company_name, day_map)
        findings_en, findings_ar = _build_findings(day_map)
        next_steps_en, next_steps_ar = _build_next_steps(retainer_eligible)

        retainer_reason_ar = ""
        retainer_reason_en = ""
        if retainer_eligible and retainer_tier:
            retainer_reason_ar = (
                "حقق Sprint نتائج قابلة للقياس تُؤهّل الشركة للانتقال إلى إدارة عمليات شهرية."
            )
            retainer_reason_en = (
                "The sprint produced measurable results that qualify for a monthly managed ops retainer."
            )

        from datetime import date

        week_label = f"Week of {date.today().isoformat()}"

        return SprintProofReport(
            sprint_id=sprint_id,
            account_id=account_id,
            company_name=company_name,
            service_tier="sprint_499",
            week_label=week_label,
            day_records=day_records,
            summary_ar=summary_ar,
            summary_en=summary_en,
            findings_ar=findings_ar,
            findings_en=findings_en,
            proof_items=proof_items,
            next_steps_ar=next_steps_ar,
            next_steps_en=next_steps_en,
            retainer_recommended=retainer_eligible,
            retainer_tier=retainer_tier,
            retainer_reason_ar=retainer_reason_ar,
            retainer_reason_en=retainer_reason_en,
            requires_founder_review=True,
            approved_at=None,
        )

    def generate_template(self, account_id: str, company_name: str) -> SprintProofReport:
        """Generate an empty template for manual completion."""
        from datetime import date

        week_label = f"Week of {date.today().isoformat()}"

        day_records = [
            SprintDayRecord(
                day=d,
                status="skipped",
                headline_ar=_DAY_DEFAULTS[d][0],
                headline_en=_DAY_DEFAULTS[d][1],
                deliverables=list(_DAY_DEFAULTS[d][2]),
                data_source="pending",
                completed_at=None,
            )
            for d in range(1, 8)
        ]

        return SprintProofReport(
            sprint_id=f"sprint_{account_id}_template",
            account_id=account_id,
            company_name=company_name,
            service_tier="sprint_499",
            week_label=week_label,
            day_records=day_records,
            summary_ar="يرجى إكمال هذا القسم بعد انتهاء Sprint.",
            summary_en="Please complete this section after the sprint concludes.",
            findings_ar=["— يُكمَل بعد التنفيذ —"],
            findings_en=["— To be completed after execution —"],
            proof_items=[],
            next_steps_ar=["— يُكمَل بعد التنفيذ —"],
            next_steps_en=["— To be completed after execution —"],
            retainer_recommended=False,
            retainer_tier=None,
            retainer_reason_ar="",
            retainer_reason_en="",
            requires_founder_review=True,
            approved_at=None,
        )


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _normalise_status(raw: str) -> str:
    """Map orchestrator status values to report status vocabulary."""
    mapping = {
        "complete": "completed",
        "completed": "completed",
        "pending": "partial",
        "partial": "partial",
        "blocked": "partial",
        "skipped": "skipped",
    }
    return mapping.get(raw.lower(), "skipped")


def _extract_deliverables(day: int, output: dict) -> list[str]:
    """Extract human-readable deliverable strings from a day's output."""
    deliverables: list[str] = []
    if not output:
        return list(_DAY_DEFAULTS.get(day, ("", "", []))[2])

    if day == 1:
        n = output.get("sources_audited", 0)
        if n:
            deliverables.append(f"Audited {n} source(s)")
        if output.get("all_passports_valid"):
            deliverables.append("All source passports valid")

    elif day == 2:
        score = output.get("overall_dq")
        if score is not None:
            deliverables.append(f"DQ score: {score}/100")
        rows = output.get("total_rows", 0)
        if rows:
            deliverables.append(f"Processed {rows} data rows")

    elif day == 3:
        total = output.get("total_accounts", 0)
        top = output.get("top_10", [])
        if total:
            deliverables.append(f"Scored {total} accounts")
        if top:
            deliverables.append(f"Top {len(top)} accounts ranked")

    elif day == 4:
        drafts = output.get("whatsapp_drafts", [])
        if drafts:
            deliverables.append(f"{len(drafts)} WhatsApp draft(s) created")
        if output.get("email_sequence"):
            deliverables.append("Email sequence drafted")
        if output.get("proposal_preview_md"):
            deliverables.append("Proposal rendered")

    elif day == 5:
        if output.get("approved"):
            deliverables.append("Founder approval confirmed")
        else:
            deliverables.append("Pending founder approval")

    elif day == 6:
        score = output.get("completeness_score")
        band = output.get("strength_band", "")
        if score is not None:
            deliverables.append(f"Proof Pack assembled — score: {score}/100 ({band})")
        pack = output.get("proof_pack", {})
        if pack:
            n_sections = len(pack.get("sections", {}))
            if n_sections:
                deliverables.append(f"{n_sections} sections populated")

    elif day == 7:
        if output.get("capital_asset_id"):
            deliverables.append(f"Capital asset registered: {output['capital_asset_id']}")
        if output.get("retainer_eligible"):
            deliverables.append(f"Retainer eligible — offer: {output.get('recommended_offer', '')}")
        else:
            gaps = output.get("retainer_gaps", [])
            if gaps:
                deliverables.append(f"Retainer gaps: {', '.join(gaps)}")

    return deliverables or list(_DAY_DEFAULTS.get(day, ("", "", []))[2])


def _extract_data_source(day: int, output: dict) -> str:
    """Infer the data source description for a day's record."""
    if not output:
        return "not available"
    sources: dict[int, str] = {
        1: "Source Passport declarations",
        2: "Client-uploaded data rows",
        3: "Scored account list",
        4: "Orchestrator context + pain summary",
        5: "Governance engine — founder decision",
        6: "Sprint day outputs (Days 1-5)",
        7: "Adoption OS + Capital OS + Retainer eligibility engine",
    }
    return sources.get(day, "sprint context")


def _extract_proof_items(day: int, output: dict) -> list[dict]:
    """Build proof item entries from a day's output."""
    items: list[dict] = []
    if not output:
        return items

    if day == 1 and output.get("all_passports_valid"):
        items.append(
            {
                "level": "L1",
                "title_ar": "جواز المصدر صالح",
                "title_en": "Source Passport Valid",
                "evidence_type": "audit_log",
                "verified": True,
            }
        )
    elif day == 1:
        items.append(
            {
                "level": "L0",
                "title_ar": "جواز المصدر — قيد المراجعة",
                "title_en": "Source Passport — Under Review",
                "evidence_type": "audit_log",
                "verified": False,
            }
        )

    if day == 2:
        score = output.get("overall_dq")
        if score is not None:
            items.append(
                {
                    "level": "L1",
                    "title_ar": f"درجة جودة البيانات: {score}/100",
                    "title_en": f"Data Quality Score: {score}/100",
                    "evidence_type": "operational_metric",
                    "verified": True,
                }
            )

    if day == 3 and output.get("top_10"):
        items.append(
            {
                "level": "L1",
                "title_ar": "قائمة الحسابات المصنَّفة (أعلى 10)",
                "title_en": "Ranked Account List (Top 10)",
                "evidence_type": "operational_metric",
                "verified": True,
            }
        )

    if day == 6:
        score = output.get("completeness_score")
        if score is not None:
            items.append(
                {
                    "level": "L2",
                    "title_ar": f"حزمة الإثبات — اكتمال {score}/100",
                    "title_en": f"Proof Pack — Completeness {score}/100",
                    "evidence_type": "financial_report",
                    "verified": True,
                }
            )

    if day == 7 and output.get("capital_asset_id"):
        items.append(
            {
                "level": "L2",
                "title_ar": "أصل رأسمالي مسجَّل",
                "title_en": "Capital Asset Registered",
                "evidence_type": "audit_log",
                "verified": True,
            }
        )

    return items


def _build_summary(
    account_id: str, company_name: str, day_map: dict[int, dict]
) -> tuple[str, str]:
    """Build executive summary from available day outputs."""
    d2 = day_map.get(2, {}).get("output", {})
    d3 = day_map.get(3, {}).get("output", {})

    dq_score = d2.get("overall_dq", "N/A") if d2 else "N/A"
    total_accounts = d3.get("total_accounts", 0) if d3 else 0
    top_count = len(d3.get("top_10", [])) if d3 else 0

    summary_en = (
        f"Revenue Intelligence Sprint completed for {company_name} (account: {account_id}). "
        f"Data Quality Score: {dq_score}/100. "
        f"Scored {total_accounts} accounts; top {top_count} prioritised for outreach."
    )
    summary_ar = (
        f"اكتمل Sprint ذكاء الإيراد لـ{company_name} (الحساب: {account_id}). "
        f"درجة جودة البيانات: {dq_score}/100. "
        f"تم تصنيف {total_accounts} حساب؛ أعلى {top_count} تم اختيارها للتواصل."
    )
    return summary_en, summary_ar


def _build_findings(day_map: dict[int, dict]) -> tuple[list[str], list[str]]:
    """Extract key findings from sprint day outputs."""
    findings_en: list[str] = []
    findings_ar: list[str] = []

    d1 = day_map.get(1, {}).get("output", {})
    if d1:
        n = d1.get("sources_audited", 0)
        valid = d1.get("all_passports_valid", False)
        findings_en.append(
            f"{n} data source(s) audited — passport validity: {'pass' if valid else 'requires attention'}."
        )
        findings_ar.append(
            f"تم تدقيق {n} مصدر بيانات — صلاحية الجواز: {'ناجح' if valid else 'يحتاج مراجعة'}."
        )

    d2 = day_map.get(2, {}).get("output", {})
    if d2:
        score = d2.get("overall_dq", "N/A")
        rows = d2.get("total_rows", 0)
        findings_en.append(f"Data quality scored {score}/100 across {rows} records.")
        findings_ar.append(f"جودة البيانات: {score}/100 عبر {rows} سجل.")

    d3 = day_map.get(3, {}).get("output", {})
    if d3 and d3.get("top_10"):
        top = d3["top_10"]
        top_name = top[0].get("company_name", "—") if top else "—"
        findings_en.append(f"Top-ranked account by ICP score: {top_name}.")
        findings_ar.append(f"أعلى حساب بمعيار ICP: {top_name}.")

    d6 = day_map.get(6, {}).get("output", {})
    if d6:
        ps = d6.get("completeness_score")
        band = d6.get("strength_band", "")
        if ps is not None:
            findings_en.append(f"Proof Pack assembled — completeness {ps}/100 ({band}).")
            findings_ar.append(f"تم تجميع Proof Pack — اكتمال {ps}/100 ({band}).")

    d7 = day_map.get(7, {}).get("output", {})
    if d7:
        if d7.get("retainer_eligible"):
            offer = d7.get("recommended_offer", "")
            findings_en.append(f"Client eligible for retainer — recommended offer: {offer}.")
            findings_ar.append(f"العميل مؤهَّل للـRetainer — المقترح: {offer}.")
        else:
            gaps = d7.get("retainer_gaps", [])
            if gaps:
                findings_en.append(f"Retainer not yet eligible. Gaps: {', '.join(gaps)}.")
                findings_ar.append(f"الـRetainer غير متاح بعد. الثغرات: {', '.join(gaps)}.")

    # Always include at least one finding
    if not findings_en:
        findings_en = ["Sprint executed. Findings require manual review."]
        findings_ar = ["اكتمل Sprint. النتائج تحتاج مراجعة يدوية."]

    return findings_en, findings_ar


def _build_next_steps(retainer_eligible: bool) -> tuple[list[str], list[str]]:
    """Build standard next-step recommendations."""
    en = [
        "Share the Proof Pack with the client after founder approval.",
        "Schedule a debrief call within 48 hours of delivery.",
        "Collect NPS score from the client (target: 8+).",
    ]
    ar = [
        "شارك Proof Pack مع العميل بعد موافقة المؤسس.",
        "جدوِّل مكالمة إحاطة خلال 48 ساعة من التسليم.",
        "اجمع تقييم NPS من العميل (الهدف: 8+).",
    ]
    if retainer_eligible:
        en.append("Present the retainer offer — client meets eligibility criteria.")
        ar.append("قدِّم عرض الـRetainer — العميل يستوفي معايير الأهلية.")
    else:
        en.append("Re-evaluate retainer eligibility after the 30-day follow-up.")
        ar.append("أعد تقييم أهلية الـRetainer بعد متابعة 30 يوماً.")
    return en, ar


def _map_offer_to_tier(offer: str) -> str:
    """Map a recommended_offer string to the retainer tier vocabulary."""
    offer_lower = offer.lower()
    if "scale" in offer_lower or "4999" in offer_lower:
        return "scale_4999"
    if "growth" in offer_lower or "3999" in offer_lower:
        return "growth_3999"
    return "starter_2999"


__all__ = [
    "SprintDayRecord",
    "SprintProofReport",
    "SprintReportGenerator",
]
