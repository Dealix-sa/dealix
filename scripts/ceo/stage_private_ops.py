"""Scaffold the gitignored dealix-ops-private/ directory.

Idempotent: never overwrites existing private files.
See docs/founder/PRIVATE_OPS_LAYOUT.md.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "dealix-ops-private"


@dataclass(frozen=True)
class CSVFile:
    path: str
    headers: tuple[str, ...]


@dataclass(frozen=True)
class MarkdownFile:
    path: str
    title: str
    body: str = ""


DIRECTORIES: tuple[str, ...] = (
    "founder",
    "revenue/invoices",
    "revenue/receipts",
    "revenue/payments",
    "sales/call_notes",
    "sales/proposal_notes",
    "delivery/samples",
    "delivery/research",
    "delivery/reports",
    "delivery/qa",
    "delivery/handoffs",
    "delivery/case_studies_private",
    "clients",
    "client_success/feedback",
    "trust/audits",
    "finance",
    "product",
    "engineering",
    "content/case_study_pre_consents",
    "content/case_study_consents",
    "people/scorecards",
    "people/onboarding_logs",
    "partners/scorecards",
)


CSV_FILES: tuple[CSVFile, ...] = (
    CSVFile(
        "revenue/revenue_action_log.csv",
        ("date", "action", "outcome", "evidence_link", "follow_up_date"),
    ),
    CSVFile(
        "revenue/cash_collected.csv",
        ("date", "invoice_no", "customer", "amount_sar", "method", "status", "notes"),
    ),
    CSVFile(
        "revenue/pipeline_value.csv",
        ("snapshot_date", "stage", "deal_count", "amount_sar", "weighted_amount_sar"),
    ),
    CSVFile(
        "revenue/mrr_tracker.csv",
        (
            "month",
            "customer_id",
            "retainer_status",
            "monthly_fee_sar",
            "contract_start",
            "contract_end",
            "paid",
            "notes",
        ),
    ),
    CSVFile(
        "sales/pipeline.csv",
        (
            "lead_id",
            "account",
            "decision_maker",
            "sector",
            "stage",
            "stage_entered",
            "amount_sar",
            "next_action",
            "next_action_date",
            "owner",
            "notes",
        ),
    ),
    CSVFile(
        "sales/dms_sent.csv",
        (
            "date_sent",
            "recipient_name",
            "recipient_company",
            "channel",
            "signal_cited",
            "reply",
            "reply_quality",
            "next_action",
        ),
    ),
    CSVFile(
        "sales/proposal_followups.csv",
        (
            "proposal_id",
            "sent_date",
            "day_2_done",
            "day_5_done",
            "day_7_done",
            "outcome",
            "outcome_date",
            "loss_reason",
        ),
    ),
    CSVFile(
        "sales/refusals.csv",
        (
            "date",
            "account",
            "reason",
            "estimated_revenue_declined_sar",
            "referral_made",
            "referred_to",
        ),
    ),
    CSVFile(
        "delivery/sprint_register.csv",
        (
            "sprint_id",
            "customer_id",
            "scope_signed_on",
            "delivered_on",
            "paid_amount_sar",
            "qa_pass",
            "retainer_asked",
            "retainer_outcome",
            "notes",
        ),
    ),
    CSVFile(
        "client_success/retainers.csv",
        (
            "customer_id",
            "monthly_fee_sar",
            "contract_start",
            "contract_end",
            "tier",
            "paid_current_month",
            "notes",
        ),
    ),
    CSVFile(
        "client_success/health_scores.csv",
        (
            "month",
            "customer_id",
            "engagement",
            "outcome",
            "sentiment",
            "expansion",
            "continuity",
            "total",
            "tier",
        ),
    ),
    CSVFile(
        "client_success/tiers.csv",
        ("customer_id", "tier", "as_of", "notes"),
    ),
    CSVFile(
        "client_success/retainer_asks.csv",
        (
            "date",
            "customer_id",
            "ask_price_sar",
            "outcome",
            "reason_if_no",
            "next_action",
        ),
    ),
    CSVFile(
        "finance/expenses.csv",
        (
            "date",
            "category",
            "vendor",
            "amount_sar",
            "recurring",
            "approved_by",
            "evidence_link",
        ),
    ),
    CSVFile(
        "product/workflow_success_log.csv",
        (
            "workflow_id",
            "success_date",
            "customer_id",
            "evidence_link",
            "level_after",
        ),
    ),
    CSVFile(
        "engineering/dora.csv",
        (
            "deploy_at",
            "change_ref",
            "lead_time_hours",
            "success",
            "restore_time_minutes",
        ),
    ),
    CSVFile(
        "content/post_log.csv",
        (
            "date",
            "platform",
            "pillar",
            "url",
            "engagement_saved",
            "engagement_shared",
            "inbound_from_icp",
            "notes",
        ),
    ),
    CSVFile(
        "people/roles.csv",
        (
            "role_id",
            "person",
            "type",
            "started_on",
            "review_due",
            "scorecard_path",
            "status",
        ),
    ),
    CSVFile(
        "partners/partner_register.csv",
        (
            "partner_id",
            "name",
            "category",
            "agreement_signed",
            "agreement_path",
            "status",
            "last_review",
        ),
    ),
    CSVFile(
        "partners/referrals.csv",
        (
            "date",
            "partner_id",
            "prospect",
            "status",
            "deal_outcome",
            "commission_sar",
        ),
    ),
)


MARKDOWN_FILES: tuple[MarkdownFile, ...] = (
    MarkdownFile(
        "founder/ceo_command.md",
        "CEO Command — Private",
        "> Pulled from docs/founder/CEO_COMMAND_CENTER.md. Update daily.\n",
    ),
    MarkdownFile(
        "founder/daily_brief.md",
        "Daily Brief — Private",
        "> Copy docs/founder/DAILY_COMMAND_BRIEF.md and fill in.\n",
    ),
    MarkdownFile(
        "founder/decision_queue.md",
        "Decision Queue",
        "> See docs/founder/GO_NO_GO_DECISION_SYSTEM.md.\n",
    ),
    MarkdownFile(
        "founder/approvals_waiting.md",
        "Approvals Waiting",
        "> See docs/trust/APPROVAL_MATRIX.md.\n",
    ),
    MarkdownFile(
        "founder/risk_log.md",
        "Risk Log",
        "> See docs/trust/TRUST_COMMAND_CENTER.md.\n",
    ),
    MarkdownFile(
        "founder/focus_queue.md",
        "Focus Queue",
        "> Tomorrow's single revenue action lives here.\n",
    ),
    MarkdownFile(
        "founder/founder_time_log.md",
        "Founder Time Log",
        "> See docs/founder/FOUNDER_TIME_ACCOUNTING.md.\n",
    ),
    MarkdownFile(
        "founder/weekly_ceo_review.md",
        "Weekly CEO Review — Private",
        "> Copy docs/founder/WEEKLY_CEO_REVIEW.md weekly.\n",
    ),
    MarkdownFile(
        "founder/board_pack.md",
        "Board Pack — Monthly",
        "> Copy docs/founder/BOARD_PACK_TEMPLATE.md monthly.\n",
    ),
    MarkdownFile(
        "founder/master_dashboard.md",
        "Master CEO Dashboard",
        "> Refreshed by `make dashboard`. Read each morning.\n",
    ),
    MarkdownFile(
        "revenue/pricing_experiments.md",
        "Pricing Experiments",
        "> See docs/revenue/OFFER_EVOLUTION_SYSTEM.md.\n",
    ),
    MarkdownFile(
        "revenue/payment_followup_templates.md",
        "Payment Follow-up Templates",
        "> See docs/finance/PAYMENT_RULES.md.\n",
    ),
    MarkdownFile(
        "sales/objections_log.md",
        "Objections Log — Private",
        "> See docs/sales/OBJECTIONS_LOG.md.\n",
    ),
    MarkdownFile(
        "trust/approvals_log.md",
        "Approvals Log",
        "> See docs/trust/APPROVAL_MATRIX.md and docs/ai_management/AI_HUMAN_OVERSIGHT.md.\n",
    ),
    MarkdownFile(
        "trust/incident_log.md",
        "Incident Log",
        "> See docs/trust/INCIDENT_RESPONSE.md.\n",
    ),
    MarkdownFile(
        "trust/autonomy_audit.md",
        "Autonomy Audit",
        "> See docs/trust/AUTONOMY_POLICY.md.\n",
    ),
    MarkdownFile(
        "finance/cash_plan.md",
        "Cash Plan",
        "> See docs/finance/CAPITAL_ALLOCATION.md.\n",
    ),
    MarkdownFile(
        "finance/monthly_finance_review.md",
        "Monthly Finance Review",
        "> See docs/finance/FINANCIAL_DASHBOARD.md.\n",
    ),
    MarkdownFile(
        "finance/runway_estimate.md",
        "Runway Estimate",
        "> Updated monthly. See docs/finance/FINANCIAL_DASHBOARD.md.\n",
    ),
    MarkdownFile(
        "finance/capital_allocation_review.md",
        "Capital Allocation Review",
        "> Monthly. See docs/finance/CAPITAL_ALLOCATION.md.\n",
    ),
    MarkdownFile(
        "finance/refund_log.md",
        "Refund Log",
        "> See docs/finance/REFUND_POLICY.md.\n",
    ),
    MarkdownFile(
        "finance/transfers_log.md",
        "Transfers Log",
        "> See docs/finance/CASH_CONTROL.md.\n",
    ),
    MarkdownFile(
        "finance/founder_compensation.md",
        "Founder Compensation",
        "> See docs/finance/CASH_CONTROL.md.\n",
    ),
    MarkdownFile(
        "product/workflow_promotions.md",
        "Workflow Promotions",
        "> See docs/product/PRODUCTIZATION_ENGINE.md.\n",
    ),
    MarkdownFile(
        "product/feature_intake.md",
        "Feature Intake Queue",
        "> See docs/product/FEATURE_INTAKE.md.\n",
    ),
    MarkdownFile(
        "product/build_defer_kill_log.md",
        "Build / Defer / Kill Log",
        "> See docs/product/BUILD_DEFER_KILL.md.\n",
    ),
)


def main() -> int:
    created: list[str] = []
    existing: list[str] = []

    PRIVATE.mkdir(exist_ok=True)

    for d in DIRECTORIES:
        target = PRIVATE / d
        if target.exists():
            existing.append(f"dir {d}")
        else:
            target.mkdir(parents=True, exist_ok=True)
            created.append(f"dir {d}")

    for csv in CSV_FILES:
        target = PRIVATE / csv.path
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            existing.append(f"csv {csv.path}")
            continue
        target.write_text(",".join(csv.headers) + "\n", encoding="utf-8")
        created.append(f"csv {csv.path}")

    for md in MARKDOWN_FILES:
        target = PRIVATE / md.path
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            existing.append(f"md  {md.path}")
            continue
        content = f"# {md.title}\n\n{md.body}"
        target.write_text(content, encoding="utf-8")
        created.append(f"md  {md.path}")

    print("[stage] dealix-ops-private layout")
    print(f"        created : {len(created)}")
    print(f"        existing: {len(existing)}")
    if created:
        print()
        print("Created:")
        for item in created:
            print(f"  + {item}")
    if not created and not existing:
        print("[stage] nothing to do (this is unusual)")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
