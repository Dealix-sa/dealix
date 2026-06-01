#!/usr/bin/env python3
"""
founder_growth_daily_report.py — Dealix Founder Growth Daily Report

Generates a structured daily growth report for the founder including:
  - top_opportunities: top 25 companies from queue
  - top_drafts: best 10 drafts by persuasion score
  - pending_approvals: list
  - channel_health: per channel vs limits
  - anti_ban_warnings: if any channel is nearing limits
  - revenue_forecast_sar: estimate
  - today_actions: three clear commands
  - no_live_send: True (hard gate)
  - no_live_charge: True (hard gate)

Doctrine:
  - No live sends under any circumstances
  - No live charges under any circumstances
  - All values are estimates — not verified revenue
  - Governance decision required on output object

Output: prints to stdout + writes to data/daily_brief/YYYY-MM-DD.md
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
OS_DIR = REPO_ROOT / "os"
GROWTH_DIR = OS_DIR / "growth"
OUTPUT_DIR = REPO_ROOT / "data" / "daily_brief"

# ---------------------------------------------------------------------------
# Hard gates — NEVER change these
# ---------------------------------------------------------------------------
NO_LIVE_SEND: bool = True
NO_LIVE_CHARGE: bool = True


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class Opportunity:
    rank: int
    company: str
    sector: str
    score: float
    best_offer: str
    best_channel: str
    action: str
    country: str = "SA"


@dataclass
class DraftItem:
    draft_id: str
    company: str
    channel: str
    offer: str
    persuasion_score: float
    risk_level: str
    status: str = "pending_approval"
    requires_approval: bool = True


@dataclass
class ChannelHealth:
    channel: str
    daily_limit: int
    used_today: int
    pct_used: float
    status: str  # GREEN | YELLOW | RED


@dataclass
class GrowthReport:
    date: str
    generated_at: str
    no_live_send: bool
    no_live_charge: bool
    top_opportunities: list[Opportunity]
    top_drafts: list[DraftItem]
    pending_approvals: list[str]
    channel_health: list[ChannelHealth]
    anti_ban_warnings: list[str]
    revenue_forecast_sar: dict[str, Any]
    today_actions: list[dict[str, str]]
    governance_decision: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Channel limits (mirrors ANTI_BAN_GUARDIAN.yml)
# ---------------------------------------------------------------------------

CHANNEL_LIMITS: dict[str, int] = {
    "Email": 50,
    "WhatsApp_opt_in": 20,
    "LinkedIn_manual": 20,
    "Phone_calls": 10,
    "Meta_inbound": 200,
    "TikTok_lead_forms": 100,
    "Google_lead_ads": 500,
}


def _channel_status(pct: float) -> str:
    if pct < 60:
        return "GREEN"
    if pct < 80:
        return "YELLOW"
    return "RED"


# ---------------------------------------------------------------------------
# Load OS configs
# ---------------------------------------------------------------------------


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        with path.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        return data or {}
    except yaml.YAMLError:
        return {}


def _load_offers() -> dict:
    data = _load_yaml(OS_DIR / "03_OFFERS.yml")
    return data.get("offers", {})


def _load_scoring_thresholds() -> dict:
    data = _load_yaml(OS_DIR / "05_SCORING.yml")
    return data.get("decision_thresholds", {})


def _load_channel_router() -> dict:
    data = _load_yaml(GROWTH_DIR / "CHANNEL_ROUTER.yml")
    return data.get("channels", {})


def _load_gcc_sectors() -> dict:
    data = _load_yaml(GROWTH_DIR / "GCC_SECTOR_OFFERS.yml")
    return data.get("sectors", {})


# ---------------------------------------------------------------------------
# Sample data generation (dry-run / no real customer data)
# ---------------------------------------------------------------------------

SAMPLE_COMPANIES = [
    ("Al Rashid Facilities", "Facilities Management", 88, "maintenance_intelligence_os", "Email", "SA"),
    ("Gulf Contracting Co", "Construction", 85, "project_controls_ai_os", "Email", "SA"),
    ("Riyadh Legal Partners", "Legal Firms", 82, "sovereign_knowledge_rag", "Email", "SA"),
    ("Saudi FM Solutions", "Facilities Management", 80, "maintenance_intelligence_os", "Email", "SA"),
    ("Al Noor Healthcare", "Healthcare", 78, "ai_workflow_audit", "Email", "SA"),
    ("Jeddah PMO Group", "Consulting", 76, "project_controls_ai_os", "Email", "SA"),
    ("AlFanar Industrial", "Manufacturing", 74, "maintenance_intelligence_os", "Email", "SA"),
    ("Kingdom Real Estate", "Real Estate", 73, "project_controls_ai_os", "Email", "SA"),
    ("Emirates FM Corp", "Facilities Management", 72, "maintenance_intelligence_os", "Email", "AE"),
    ("Kuwait Consulting Group", "Consulting", 71, "revenue_ai_os", "Email", "KW"),
    ("Al Khobar Tech", "Technology", 70, "sovereign_knowledge_rag", "Email", "SA"),
    ("Makkah Construction", "Construction", 69, "project_controls_ai_os", "Email", "SA"),
    ("Medina Healthcare", "Healthcare", 68, "ai_workflow_audit", "Email", "SA"),
    ("Saudi Investment House", "Finance", 67, "sovereign_knowledge_rag", "Email", "SA"),
    ("Dammam Industrial Co", "Manufacturing", 66, "maintenance_intelligence_os", "Email", "SA"),
    ("Gulf Property Dev", "Real Estate", 65, "project_controls_ai_os", "Email", "SA"),
    ("Riyadh Law Firm", "Legal Firms", 64, "sovereign_knowledge_rag", "Email", "SA"),
    ("Saudi Tech Solutions", "Technology", 63, "sovereign_knowledge_rag", "Email", "SA"),
    ("Al Muftah Contracting", "Construction", 62, "project_controls_ai_os", "Email", "QA"),
    ("Doha Consulting", "Consulting", 61, "revenue_ai_os", "Email", "QA"),
    ("Abu Dhabi FM", "Facilities Management", 60, "maintenance_intelligence_os", "Email", "AE"),
    ("Bahrain Finance Co", "Finance", 59, "sovereign_knowledge_rag", "Email", "BH"),
    ("Oman Manufacturing", "Manufacturing", 58, "maintenance_intelligence_os", "Email", "OM"),
    ("Kuwait Real Estate", "Real Estate", 57, "project_controls_ai_os", "Email", "KW"),
    ("Saudi Retail Group", "Retail", 56, "revenue_ai_os", "Email", "SA"),
]

SAMPLE_DRAFTS = [
    ("DFT-001", "Al Rashid Facilities", "Email", "maintenance_intelligence_os", 87.5, "low"),
    ("DFT-002", "Gulf Contracting Co", "Email", "project_controls_ai_os", 84.0, "low"),
    ("DFT-003", "Riyadh Legal Partners", "Email", "sovereign_knowledge_rag", 81.5, "medium"),
    ("DFT-004", "Saudi FM Solutions", "Email", "maintenance_intelligence_os", 79.0, "low"),
    ("DFT-005", "Al Noor Healthcare", "Email", "ai_workflow_audit", 77.5, "medium"),
    ("DFT-006", "Jeddah PMO Group", "Email", "project_controls_ai_os", 75.0, "low"),
    ("DFT-007", "AlFanar Industrial", "Email", "maintenance_intelligence_os", 73.5, "low"),
    ("DFT-008", "Kingdom Real Estate", "Email", "project_controls_ai_os", 72.0, "low"),
    ("DFT-009", "Emirates FM Corp", "Email", "maintenance_intelligence_os", 71.5, "medium"),
    ("DFT-010", "Kuwait Consulting Group", "Email", "revenue_ai_os", 70.0, "low"),
]


# ---------------------------------------------------------------------------
# Report builder
# ---------------------------------------------------------------------------


def build_channel_health(usage_counts: dict[str, int] | None = None) -> list[ChannelHealth]:
    if usage_counts is None:
        usage_counts = {}
    health = []
    for channel, limit in CHANNEL_LIMITS.items():
        used = usage_counts.get(channel, 0)
        pct = (used / limit * 100) if limit > 0 else 0.0
        health.append(
            ChannelHealth(
                channel=channel,
                daily_limit=limit,
                used_today=used,
                pct_used=round(pct, 1),
                status=_channel_status(pct),
            )
        )
    return health


def build_anti_ban_warnings(channel_health: list[ChannelHealth]) -> list[str]:
    warnings = []
    for ch in channel_health:
        if ch.status == "RED":
            warnings.append(
                f"CRITICAL: {ch.channel} at {ch.pct_used}% of daily limit "
                f"({ch.used_today}/{ch.daily_limit}) — pause outbound immediately"
            )
        elif ch.status == "YELLOW":
            warnings.append(
                f"WARNING: {ch.channel} at {ch.pct_used}% of daily limit "
                f"({ch.used_today}/{ch.daily_limit}) — approaching limit"
            )
    return warnings


def build_revenue_forecast(opportunities: list[Opportunity]) -> dict[str, Any]:
    total_pipeline = len(opportunities) * 25000  # Rough SAR estimate per opportunity
    conversion_5pct = total_pipeline * 0.05
    return {
        "pipeline_top_25_sar": total_pipeline,
        "expected_at_5pct_conversion_sar": conversion_5pct,
        "retainer_target_monthly_sar": 8000,
        "current_mrr_sar": 0,  # No live customers yet — honest zero
        "disclaimer": (
            "Estimated value is not Verified value / "
            "القيمة التقديرية ليست قيمة مُتحقَّقة"
        ),
    }


def build_today_actions(
    top_opportunities: list[Opportunity],
    top_drafts: list[DraftItem],
    anti_ban_warnings: list[str],
) -> list[dict[str, str]]:
    actions = []

    if anti_ban_warnings:
        actions.append(
            {
                "title": "Review anti-ban warnings",
                "what": f"{len(anti_ban_warnings)} channel(s) approaching limits",
                "command": "python scripts/validate_os_configs.py",
                "outcome": "Confirm channel health before any outbound activity",
            }
        )

    if top_drafts:
        best = top_drafts[0]
        actions.append(
            {
                "title": f"Review top draft for {best.company}",
                "what": (
                    f"Draft {best.draft_id} ready — {best.channel} / "
                    f"{best.offer} (score: {best.persuasion_score})"
                ),
                "command": (
                    f"python -m dealix.os_runtime approval-check "
                    f"--draft-id {best.draft_id}"
                ),
                "outcome": "Approve or reject to keep queue moving",
            }
        )

    if top_opportunities:
        top = top_opportunities[0]
        actions.append(
            {
                "title": f"Generate dossier for top opportunity: {top.company}",
                "what": (
                    f"Score {top.score}/100 — {top.sector} — "
                    f"recommend {top.best_offer}"
                ),
                "command": (
                    f"python scripts/growth_dry_run.py "
                    f"--companies 1 --focus {top.company!r}"
                ),
                "outcome": "Ready-to-review draft within 2 minutes",
            }
        )

    # Pad to 3 actions if needed
    while len(actions) < 3:
        idx = len(actions) + 1
        actions.append(
            {
                "title": f"Review pipeline company #{idx + len(top_drafts)}",
                "what": "Review scoring and prepare draft",
                "command": "python scripts/growth_dry_run.py --companies 10",
                "outcome": "10 new drafts queued for review",
            }
        )

    return actions[:3]


def generate_report(usage_counts: dict[str, int] | None = None) -> GrowthReport:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    generated_at = datetime.now(timezone.utc).isoformat()

    opportunities = [
        Opportunity(
            rank=i + 1,
            company=c[0],
            sector=c[1],
            score=c[2],
            best_offer=c[3],
            best_channel=c[4],
            country=c[5],
            action="Review & approve draft" if i < 5 else "Generate draft",
        )
        for i, c in enumerate(SAMPLE_COMPANIES[:25])
    ]

    drafts = [
        DraftItem(
            draft_id=d[0],
            company=d[1],
            channel=d[2],
            offer=d[3],
            persuasion_score=d[4],
            risk_level=d[5],
        )
        for d in SAMPLE_DRAFTS
    ]

    channel_health = build_channel_health(usage_counts)
    anti_ban_warnings = build_anti_ban_warnings(channel_health)
    revenue_forecast = build_revenue_forecast(opportunities)
    today_actions = build_today_actions(opportunities, drafts, anti_ban_warnings)

    report = GrowthReport(
        date=today,
        generated_at=generated_at,
        no_live_send=NO_LIVE_SEND,
        no_live_charge=NO_LIVE_CHARGE,
        top_opportunities=opportunities,
        top_drafts=drafts,
        pending_approvals=[d.draft_id for d in drafts if d.status == "pending_approval"],
        channel_health=channel_health,
        anti_ban_warnings=anti_ban_warnings,
        revenue_forecast_sar=revenue_forecast,
        today_actions=today_actions,
        governance_decision={
            "report_type": "growth_daily_report",
            "no_live_actions": True,
            "no_live_sends": NO_LIVE_SEND,
            "no_live_charges": NO_LIVE_CHARGE,
            "all_values_estimated": True,
            "generated_at": generated_at,
        },
    )
    return report


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def render_markdown(report: GrowthReport) -> str:
    lines = [
        f"# Dealix Daily Growth Report — {report.date}",
        "",
        f"> Generated at: {report.generated_at}",
        f"> NO_LIVE_SEND: {report.no_live_send} | NO_LIVE_CHARGE: {report.no_live_charge}",
        "",
        "---",
        "",
        "## Top 25 Opportunities",
        "",
        "| Rank | Company | Sector | Score | Best Offer | Channel | Country |",
        "|------|---------|--------|-------|------------|---------|---------|",
    ]
    for opp in report.top_opportunities:
        lines.append(
            f"| {opp.rank} | {opp.company} | {opp.sector} | {opp.score} "
            f"| {opp.best_offer} | {opp.best_channel} | {opp.country} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Top 10 Drafts Ready for Review",
        "",
        "| Draft ID | Company | Channel | Offer | Score | Risk | Action |",
        "|----------|---------|---------|-------|-------|------|--------|",
    ]
    for draft in report.top_drafts:
        lines.append(
            f"| {draft.draft_id} | {draft.company} | {draft.channel} | "
            f"{draft.offer} | {draft.persuasion_score} | {draft.risk_level} "
            f"| Approve / Reject |"
        )

    lines += [
        "",
        "---",
        "",
        "## Pending Approvals",
        "",
        f"Total pending: {len(report.pending_approvals)}",
        "",
    ]
    for a in report.pending_approvals[:10]:
        lines.append(f"- {a}")

    lines += [
        "",
        "---",
        "",
        "## Channel Health",
        "",
        "| Channel | Daily Limit | Used Today | % Used | Status |",
        "|---------|------------|-----------|--------|--------|",
    ]
    for ch in report.channel_health:
        lines.append(
            f"| {ch.channel} | {ch.daily_limit} | {ch.used_today} "
            f"| {ch.pct_used}% | {ch.status} |"
        )

    lines += ["", "---", "", "## Anti-Ban Status", ""]
    if report.anti_ban_warnings:
        for w in report.anti_ban_warnings:
            lines.append(f"- {w}")
    else:
        lines.append("All channels within safe limits. No warnings.")

    lines += ["", "---", "", "## Revenue Forecast (SAR)", ""]
    fc = report.revenue_forecast_sar
    lines += [
        f"- Pipeline (top 25): **{fc['pipeline_top_25_sar']:,} SAR** (estimated)",
        f"- Expected at 5% conversion: **{fc['expected_at_5pct_conversion_sar']:,.0f} SAR**",
        f"- Current MRR: **{fc['current_mrr_sar']:,} SAR** (verified paid only)",
        "",
        f"> {fc['disclaimer']}",
    ]

    lines += ["", "---", "", "## Today's 3 Priority Actions", ""]
    for i, action in enumerate(report.today_actions, 1):
        lines += [
            f"### {i}. {action['title']}",
            f"- What: {action['what']}",
            f"- Command: `{action['command']}`",
            f"- Expected outcome: {action['outcome']}",
            "",
        ]

    lines += [
        "---",
        "",
        "## Doctrine Reminders",
        "",
        "- No draft is sent without explicit founder approval.",
        "- No cold WhatsApp automation — opted-in contacts only.",
        "- No LinkedIn automation — founder sends manually only.",
        "- No guaranteed revenue claims to prospects.",
        "- All estimates labeled as estimated, not verified.",
        "",
        "---",
        "",
        "*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*",
    ]

    return "\n".join(lines)


def render_json(report: GrowthReport) -> str:
    def _serialize(obj: Any) -> Any:
        if hasattr(obj, "__dataclass_fields__"):
            return asdict(obj)
        return str(obj)

    return json.dumps(asdict(report), ensure_ascii=False, indent=2, default=_serialize)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Dealix Founder Growth Daily Report")
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Write output to file (default: data/daily_brief/YYYY-MM-DD.md)",
    )
    args = parser.parse_args()

    report = generate_report()

    if args.format == "json":
        content = render_json(report)
        suffix = ".json"
    else:
        content = render_markdown(report)
        suffix = ".md"

    print(content)

    output_path = args.output
    if output_path is None:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / f"{report.date}{suffix}"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"\n[saved to {output_path}]", file=sys.stderr)


if __name__ == "__main__":
    main()
