# Client Success Reporting — تقارير نجاح العميل

How Dealix reports progress to clients across every offer. The report is evidence-forward and honestly labeled. It never presents Estimated value as Verified.

كيف نُبلّغ العميل بالتقدّم عبر كل العروض. التقرير قائم على الأدلة وموسوم بصدق، ولا يقدّم القيمة التقديرية كأنها مُتحقَّقة.

## Cadence — التواتر

| Offer | Client-facing report cadence |
|---|---|
| Diagnostic | One report at delivery |
| Pilot | Weekly check-in note + close-out report |
| Department OS | Phase-end reports + handover report |
| Retainer | Monthly report + quarterly business review |

## Standard report sections — أقسام التقرير القياسية

Every client report, AR and EN, follows the same structure:

1. **What ran this period** — workflows operated, drafts generated, reviews completed.
2. **Evidenced opportunities and results** — labeled Estimated, Observed, or Verified.
3. **Review yield** — drafts generated vs. approved, and cycle time.
4. **Safety and compliance** — violations caught, rejections, and how they were handled.
5. **What we recommend next** — concrete, scoped, optional.
6. **Limitations** — what this period's numbers do and do not show.

## Value labeling — وسم القيمة

- **Estimated** — modeled from inputs, not yet seen in the workflow.
- **Observed** — measured in the operated workflow this period.
- **Verified** — confirmed by the client against their own records.

Definitions: [08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md](../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md). Ledger: [08_value_os/VALUE_LEDGER.md](../08_value_os/VALUE_LEDGER.md).

## Core client success metrics — مقاييس نجاح العميل الأساسية

| Metric | Definition | Source |
|---|---|---|
| Drafts generated | Drafts produced this period | Run ledger |
| Review yield | Approved ÷ generated | Run ledger |
| Cycle time | Intake to approved draft | Run ledger |
| Observed value | Measured value this period (labeled) | Value ledger |
| Safety violations | Unsafe drafts caught pre-send | Governance log |
| Compliance rejections | Drafts rejected on policy | Governance log |
| Cadence adherence | Cycles delivered on time | Engagement registry |

All metrics are manually entered or exported from system ledgers. No figure is fabricated; if a number is unavailable, the report states "not measured this period."

## Approval before send — اعتماد قبل الإرسال

Every client report is `draft_only` until the founder approves it in the governance ledger. Reports follow the same human-approval and no-external-send boundaries as all delivery artifacts.

## Forbidden in reports — ممنوع في التقارير

No "guaranteed ROI", "100%", "replace your team", "automate everything", "no human needed", or fabricated urgency. No Verified label without client confirmation.

## Related — مراجع

- Weekly internal report: [../analytics-os/03_WEEKLY_REPORT_TEMPLATE.md](../analytics-os/03_WEEKLY_REPORT_TEMPLATE.md)
- Board report: [../analytics-os/04_MONTHLY_BOARD_REPORT.md](../analytics-os/04_MONTHLY_BOARD_REPORT.md)
- Handover: [06_HANDOVER_TEMPLATE.md](06_HANDOVER_TEMPLATE.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
