"""Recurring Revenue Radar — portfolio-level expansion scanner.

Scans the book of business (post-sprint accounts) and surfaces, each day, which
accounts should convert from one-off engagements into *recurring* Managed-Ops
retainers — ranked by expected incremental monthly recurring revenue (MRR).

This is the compounding-revenue lever: turning one-off Revenue Proof Sprints
into 2,999 / 3,999 / 4,999 SAR/month retainers. Individual eligibility checks
already exist (``RetainerEligibilityEngine``); this module aggregates them into
a single ranked, founder-facing daily radar with approval-first drafts.

Doctrine (non-negotiables enforced in code and in tests):
  * **No revenue before paid.** ``realized_mrr_sar`` only sums accounts whose
    latest invoice is *paid*. Expansion figures are labelled **PIPELINE**
    (opportunity) and are never mixed into realised revenue.
  * **Proof before upsell.** An account is only an expansion opportunity when it
    is retainer-eligible (proof_level >= L1, satisfaction >= 7, measurable
    result achieved) — reusing ``RetainerEligibilityEngine``.
  * **Approval-first.** Every recommended action is a *draft* requiring founder
    approval (``requires_approval=True``, ``mode="draft_only"``). Nothing is
    sent or charged automatically.

The engine is deterministic with no external I/O. Persistence (the radar log)
is a single JSON file, gitignored, single-process safe.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from dealix.revenue_ops_autopilot.retainer_eligibility import (
    ProofLevel,
    RetainerEligibilityEngine,
    RetainerTier,
)

# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

_PROOF_LEVEL_RANK: dict[str, int] = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4}

# Monthly recurring price for each retainer tier (SAR). The tier identifiers
# embed the price; this map is asserted against them in the test-suite so the
# two can never silently drift apart.
RETAINER_TIER_MRR_SAR: dict[RetainerTier, int] = {
    "starter_2999": 2999,
    "growth_3999": 3999,
    "scale_4999": 4999,
}

_TIER_LABEL: dict[RetainerTier, tuple[str, str]] = {
    "starter_2999": ("Managed Ops — Starter", "باقة العمليات المُدارة — Starter"),
    "growth_3999": ("Managed Ops — Growth", "باقة العمليات المُدارة — Growth"),
    "scale_4999": ("Managed Ops — Scale", "باقة العمليات المُدارة — Scale"),
}

_DEFAULT_LEDGER_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "recurring_revenue" / "radar_log.json"
)

SCHEMA_VERSION = "1.0"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class AccountSnapshot(BaseModel):
    """One account's latest post-sprint state, as fed to the radar.

    ``current_mrr_sar`` is what the account already pays *recurring* today
    (0 for one-off-only clients). It is only treated as realised revenue when
    ``latest_invoice_paid`` is True — the no-revenue-before-paid rule.
    """

    model_config = ConfigDict(extra="forbid")

    account_id: str = Field(..., min_length=1)
    company_name: str = Field(default="", max_length=200)
    sprint_id: str = Field(default="", description="Latest sprint id; synthesised if blank.")
    proof_level: ProofLevel = Field(default="L0")
    satisfaction_score: float = Field(default=0.0, ge=0.0, le=10.0)
    measurable_result_achieved: bool = Field(default=False)
    current_mrr_sar: float = Field(
        default=0.0, ge=0.0, description="Recurring SAR/month the account pays today."
    )
    latest_invoice_paid: bool = Field(
        default=False,
        description="Whether the most recent invoice is paid (gates realised MRR).",
    )
    months_active: int = Field(default=0, ge=0)
    last_touch_iso: str | None = Field(default=None)
    notes: str = Field(default="", max_length=2000)


class ExpansionOpportunity(BaseModel):
    """A single ranked expansion opportunity (or a non-opportunity with blockers)."""

    model_config = ConfigDict(extra="forbid")

    account_id: str
    company_name: str = ""
    is_expansion_opportunity: bool = False
    recommended_tier: RetainerTier | None = None
    recommended_tier_label_en: str = ""
    recommended_tier_label_ar: str = ""
    recommended_tier_mrr_sar: float = 0.0
    current_mrr_sar: float = Field(
        default=0.0, description="Realised (paid-only) recurring SAR/month today."
    )
    expected_incremental_mrr_sar: float = Field(
        default=0.0, description="PIPELINE — incremental MRR if upgraded. Not realised."
    )
    expected_incremental_arr_sar: float = 0.0
    priority_score: float = 0.0
    proof_level: ProofLevel = "L0"
    satisfaction_score: float = 0.0
    blockers: list[str] = Field(default_factory=list)
    next_action_ar: str = ""
    next_action_en: str = ""
    upsell_pitch_ar: str = ""
    upsell_pitch_en: str = ""
    requires_approval: bool = True
    mode: Literal["draft_only"] = "draft_only"


class PortfolioSummary(BaseModel):
    """Portfolio-wide recurring-revenue snapshot for one radar run."""

    model_config = ConfigDict(extra="forbid")

    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    schema_version: str = SCHEMA_VERSION
    accounts_total: int = 0
    opportunities_count: int = 0
    realized_mrr_sar: float = Field(
        default=0.0, description="Sum of paid recurring MRR — realised revenue only."
    )
    realized_arr_sar: float = 0.0
    pipeline_incremental_mrr_sar: float = Field(
        default=0.0, description="PIPELINE — sum of incremental MRR across opportunities."
    )
    pipeline_incremental_arr_sar: float = 0.0
    by_tier: dict[str, int] = Field(default_factory=dict)
    opportunities: list[ExpansionOpportunity] = Field(default_factory=list)
    doctrine_ar: str = ""
    doctrine_en: str = ""
    guardrails: dict[str, bool] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

_DOCTRINE_AR = (
    "أرقام التوسّع (PIPELINE) فرصة مُقدّرة وليست إيراداً محقّقاً — الإيراد المحقّق "
    "يُحتسب فقط بعد سداد الفاتورة. كل إجراء مُقترح مسودة تتطلب موافقة المؤسس قبل أي "
    "تواصل أو فوترة. لا ترقية قبل Proof (L1+)."
)
_DOCTRINE_EN = (
    "Expansion figures (PIPELINE) are estimated opportunity, not realised revenue — "
    "realised revenue is counted only after the invoice is paid. Every recommended "
    "action is a draft requiring founder approval before any outreach or billing. "
    "No upsell before Proof (L1+)."
)


class RecurringRevenueRadar:
    """Aggregates per-account retainer eligibility into a ranked portfolio radar.

    Deterministic; performs no external I/O. Reuses ``RetainerEligibilityEngine``
    so the eligibility gates (proof level, satisfaction, measurable result) and
    the recommended tier stay the single source of truth.
    """

    def __init__(self, eligibility_engine: RetainerEligibilityEngine | None = None) -> None:
        self._engine = eligibility_engine or RetainerEligibilityEngine()

    # -- per-account ----------------------------------------------------

    def evaluate_account(self, snap: AccountSnapshot) -> ExpansionOpportunity:
        sprint_id = snap.sprint_id or f"sprint::{snap.account_id}"
        check = self._engine.check(
            {
                "sprint_id": sprint_id,
                "account_id": snap.account_id,
                "proof_level": snap.proof_level,
                "satisfaction_score": snap.satisfaction_score,
                "measurable_result_achieved": snap.measurable_result_achieved,
            }
        )

        # No-revenue-before-paid: only paid recurring counts as the baseline.
        realized_current_mrr = snap.current_mrr_sar if snap.latest_invoice_paid else 0.0

        blockers: list[str] = list(check.ineligibility_reasons)
        if snap.current_mrr_sar > 0 and not snap.latest_invoice_paid:
            blockers.append("unverified_current_mrr_excluded_until_paid")

        tier = check.recommended_tier if check.is_eligible else None
        tier_mrr = float(RETAINER_TIER_MRR_SAR[tier]) if tier else 0.0
        incremental = max(0.0, tier_mrr - realized_current_mrr) if tier else 0.0
        is_opportunity = bool(tier) and incremental > 0.0

        if check.is_eligible and not is_opportunity:
            blockers.append("already_at_or_above_recommended_tier")

        label_en, label_ar = _TIER_LABEL.get(tier, ("", "")) if tier else ("", "")
        next_ar, next_en = _draft_next_action(
            company=snap.company_name or snap.account_id,
            tier=tier,
            tier_mrr=tier_mrr,
            incremental=incremental,
            is_opportunity=is_opportunity,
            blockers=blockers,
        )

        # Deterministic priority: incremental MRR dominates, then satisfaction,
        # then proof strength. (Final ordering uses the full tuple in evaluate.)
        proof_rank = _PROOF_LEVEL_RANK.get(snap.proof_level, 0)
        priority_score = round(incremental + snap.satisfaction_score + proof_rank, 2)

        return ExpansionOpportunity(
            account_id=snap.account_id,
            company_name=snap.company_name,
            is_expansion_opportunity=is_opportunity,
            recommended_tier=tier,
            recommended_tier_label_en=label_en,
            recommended_tier_label_ar=label_ar,
            recommended_tier_mrr_sar=tier_mrr,
            current_mrr_sar=realized_current_mrr,
            expected_incremental_mrr_sar=incremental,
            expected_incremental_arr_sar=round(incremental * 12, 2),
            priority_score=priority_score,
            proof_level=snap.proof_level,
            satisfaction_score=snap.satisfaction_score,
            blockers=blockers,
            next_action_ar=next_ar,
            next_action_en=next_en,
            upsell_pitch_ar=check.upsell_pitch_ar,
            upsell_pitch_en=check.upsell_pitch_en,
        )

    # -- portfolio ------------------------------------------------------

    def evaluate(self, accounts: list[AccountSnapshot]) -> PortfolioSummary:
        opportunities = [self.evaluate_account(a) for a in accounts]

        # Deterministic ranking: opportunities first, then by incremental MRR,
        # satisfaction, proof strength, and finally account_id for stability.
        opportunities.sort(
            key=lambda o: (
                not o.is_expansion_opportunity,
                -o.expected_incremental_mrr_sar,
                -o.satisfaction_score,
                -_PROOF_LEVEL_RANK.get(o.proof_level, 0),
                o.account_id,
            )
        )

        realized_mrr = round(
            sum(a.current_mrr_sar for a in accounts if a.latest_invoice_paid), 2
        )
        pipeline_mrr = round(
            sum(o.expected_incremental_mrr_sar for o in opportunities if o.is_expansion_opportunity),
            2,
        )
        by_tier: dict[str, int] = {}
        for o in opportunities:
            if o.is_expansion_opportunity and o.recommended_tier:
                by_tier[o.recommended_tier] = by_tier.get(o.recommended_tier, 0) + 1

        return PortfolioSummary(
            accounts_total=len(accounts),
            opportunities_count=sum(1 for o in opportunities if o.is_expansion_opportunity),
            realized_mrr_sar=realized_mrr,
            realized_arr_sar=round(realized_mrr * 12, 2),
            pipeline_incremental_mrr_sar=pipeline_mrr,
            pipeline_incremental_arr_sar=round(pipeline_mrr * 12, 2),
            by_tier=by_tier,
            opportunities=opportunities,
            doctrine_ar=_DOCTRINE_AR,
            doctrine_en=_DOCTRINE_EN,
            guardrails={
                "no_revenue_before_paid": True,
                "proof_before_upsell": True,
                "approval_first": True,
                "no_auto_send": True,
            },
        )


def _draft_next_action(
    *,
    company: str,
    tier: RetainerTier | None,
    tier_mrr: float,
    incremental: float,
    is_opportunity: bool,
    blockers: list[str],
) -> tuple[str, str]:
    """Approval-first, guarantee-free draft action lines (AR, EN)."""
    if is_opportunity and tier:
        ar = (
            f"راجع حساب «{company}»: مؤهّل لـ {_TIER_LABEL[tier][1]} بـ "
            f"{int(tier_mrr):,} ر.س/شهر (+{int(incremental):,} ر.س MRR). جهّز عرض ترقية "
            "كمسودة من Proof Pack الحالي واطلب موافقة قبل الإرسال."
        )
        en = (
            f"Review «{company}»: eligible for {_TIER_LABEL[tier][0]} at "
            f"{int(tier_mrr):,} SAR/mo (+{int(incremental):,} SAR MRR). Prepare an upgrade "
            "proposal as a draft from the existing Proof Pack and request approval before sending."
        )
        return ar, en
    if "already_at_or_above_recommended_tier" in blockers:
        ar = f"حساب «{company}» على المستوى الموصى به — ركّز على الاحتفاظ وتجديد العقد بدليل القيمة."
        en = f"«{company}» is at/above the recommended tier — focus on retention and renewal with the value ledger."
        return ar, en
    ar = (
        f"حساب «{company}» غير مؤهّل للترقية بعد ({', '.join(blockers) or 'بيانات ناقصة'}). "
        "اجمع Proof إضافي أو حدّث درجة الرضا قبل أي عرض."
    )
    en = (
        f"«{company}» not yet eligible to upgrade ({', '.join(blockers) or 'incomplete data'}). "
        "Gather more Proof or refresh satisfaction before any offer."
    )
    return ar, en


# ---------------------------------------------------------------------------
# Markdown render (founder pack)
# ---------------------------------------------------------------------------


def render_radar_markdown(summary: PortfolioSummary, *, top_n: int = 10) -> str:
    """Bilingual founder pack for the daily brief / terminal."""
    day = summary.generated_at[:10]
    lines: list[str] = [
        f"# Recurring Revenue Radar · رادار الإيراد المتكرّر · {day}",
        "",
        "## Portfolio · المحفظة",
        "",
        f"- **Accounts scanned / الحسابات:** {summary.accounts_total}",
        f"- **Expansion opportunities / فرص التوسّع:** {summary.opportunities_count}",
        f"- **Realised MRR (paid) / إيراد متكرّر محقّق:** {summary.realized_mrr_sar:,.0f} SAR "
        f"(ARR {summary.realized_arr_sar:,.0f})",
        f"- **PIPELINE incremental MRR / إيراد إضافي محتمل:** "
        f"{summary.pipeline_incremental_mrr_sar:,.0f} SAR "
        f"(ARR {summary.pipeline_incremental_arr_sar:,.0f}) — _opportunity, not realised_",
        "",
        "## Top opportunities · أعلى الفرص",
        "",
        "| # | Account | Recommended tier | Current → Tier MRR | +MRR (pipeline) | Proof | Sat |",
        "|---|---------|------------------|--------------------|-----------------|-------|-----|",
    ]
    ranked = [o for o in summary.opportunities if o.is_expansion_opportunity][:top_n]
    if not ranked:
        lines.append("| — | _No expansion opportunities today_ | — | — | — | — | — |")
    for i, o in enumerate(ranked, start=1):
        lines.append(
            f"| {i} | {o.company_name or o.account_id} | {o.recommended_tier_label_en} "
            f"| {o.current_mrr_sar:,.0f} → {o.recommended_tier_mrr_sar:,.0f} "
            f"| +{o.expected_incremental_mrr_sar:,.0f} | {o.proof_level} | {o.satisfaction_score:g} |"
        )
    lines.extend(["", "### Drafts (approval-first) · مسودات (موافقة أولاً)", ""])
    for o in ranked:
        lines.append(f"- **{o.company_name or o.account_id}** — {o.next_action_ar}")
    lines.extend(
        [
            "",
            "## Governance · الحوكمة",
            "",
            f"- {summary.doctrine_ar}",
            f"- {summary.doctrine_en}",
            "",
            "_Mode: draft_only — review in /ar/ops/approvals before any send or invoice._",
            "",
        ]
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Ledger (append-only run log)
# ---------------------------------------------------------------------------


class RecurringRevenueRadarLedger:
    """Append-only JSON log of radar runs for trend tracking.

    Single-process safe (file-level read/write, no advisory locks). For
    multi-worker deployments migrate to a database backend.
    """

    def __init__(self, ledger_path: Path | None = None) -> None:
        self._path: Path = ledger_path or _DEFAULT_LEDGER_PATH

    def _load(self) -> list[dict]:
        if not self._path.exists():
            return []
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def _save(self, records: list[dict]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def append_run(self, summary: PortfolioSummary) -> dict:
        """Record a compact snapshot of one radar run. Returns the record."""
        top = [
            {
                "account_id": o.account_id,
                "company_name": o.company_name,
                "recommended_tier": o.recommended_tier,
                "expected_incremental_mrr_sar": o.expected_incremental_mrr_sar,
            }
            for o in summary.opportunities
            if o.is_expansion_opportunity
        ][:5]
        record = {
            "date": summary.generated_at[:10],
            "generated_at": summary.generated_at,
            "accounts_total": summary.accounts_total,
            "opportunities_count": summary.opportunities_count,
            "realized_mrr_sar": summary.realized_mrr_sar,
            "pipeline_incremental_mrr_sar": summary.pipeline_incremental_mrr_sar,
            "top": top,
        }
        records = self._load()
        records.append(record)
        self._save(records)
        return record

    def history(self, limit: int = 30) -> list[dict]:
        return self._load()[-limit:]

    def latest(self) -> dict | None:
        records = self._load()
        return records[-1] if records else None


# ---------------------------------------------------------------------------
# Convenience helpers
# ---------------------------------------------------------------------------


def run_radar(accounts: list[dict] | list[AccountSnapshot]) -> PortfolioSummary:
    """Evaluate a portfolio from raw dicts or AccountSnapshot models."""
    snaps = [a if isinstance(a, AccountSnapshot) else AccountSnapshot(**a) for a in accounts]
    return RecurringRevenueRadar().evaluate(snaps)


def load_accounts_from_file(path: Path) -> list[AccountSnapshot]:
    """Load a portfolio seed file: a JSON list of account snapshot dicts."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    items = raw.get("accounts", raw) if isinstance(raw, dict) else raw
    return [AccountSnapshot(**a) for a in items]


__all__ = [
    "RETAINER_TIER_MRR_SAR",
    "SCHEMA_VERSION",
    "AccountSnapshot",
    "ExpansionOpportunity",
    "PortfolioSummary",
    "RecurringRevenueRadar",
    "RecurringRevenueRadarLedger",
    "load_accounts_from_file",
    "render_radar_markdown",
    "run_radar",
]
