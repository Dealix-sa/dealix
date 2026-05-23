# Ultimate Finance OS

The Finance OS is the closed-loop system that connects every engagement to cash, cost, margin, and forecast. It is the financial spine of the Revenue Factory.

**Source of truth:** `$PRIVATE_OPS/finance_ledger.csv` plus monthly archives in `$PRIVATE_OPS/finance_archives/`
**Owner:** Founder
**Trust gate:** A2 — financial commitments, pricing exceptions, refunds, and external financial disclosures require founder approval.

## Modules

| Module | Source doc |
|--------|-----------|
| Payment Capture | `docs/finance/PAYMENT_CAPTURE_OS.md` |
| AI Unit Economics | `docs/finance/AI_UNIT_ECONOMICS_SYSTEM.md` |
| Revenue recognition | this doc |
| Cost ledger | this doc |
| Forecast | this doc |
| Treasury | this doc |

## Revenue recognition

Dealix recognises revenue on the delivery method:

- **Pilot / sample:** at delivery acceptance.
- **Sprint:** linear over the sprint window once started.
- **Retainer:** monthly over the term.
- **Enterprise OS:** subscription period plus separate professional-services line.

Recognition entries are written to `finance_ledger.csv` with `recognition_basis`, `period_start`, `period_end`, `amount_sar`, and `linked_invoice_id`.

## Cost ledger

Costs are bucketed into:

| Bucket | Examples |
|--------|----------|
| Direct AI inference | LLM gateway spend per client (see `docs/06_llm_gateway/COST_GUARD.md`) |
| Direct delivery | Contractor hours, sector data licences |
| Platform infrastructure | Hosting, observability, security |
| Marketing | Content production, paid distribution |
| G&A | Legal, accounting, founder time allocation |

Direct costs are attributable to a client. Platform, marketing, and G&A are allocated.

## Forecast

A 13-week cash forecast runs each Monday. It uses:

- Committed cash (signed contracts, scheduled invoices).
- Pipeline-weighted cash (stage-weighted probability from `docs/revenue/REVENUE_FACTORY_OS.md`).
- Committed costs (recurring infrastructure, contracted labour).

The forecast is internal. External financial statements are produced only under explicit founder direction with auditor involvement.

## Treasury

- Operating bank account holds two months of fixed costs at minimum.
- Reserve account holds an additional three months. Reserve transfers require A2.
- No foreign-exchange speculation. Cross-border invoices convert at receipt.

## Failure modes

- **Recognition error:** revenue recognised before delivery. Detection: monthly reconciliation against delivery state. Recovery: reversal entry with reason.
- **Forecast drift:** actual cash diverges from forecast by more than 20% for two consecutive weeks. Detection: weekly review. Recovery: forecast recalibrated, assumptions documented.
- **Cost outlier:** unit AI cost spikes above guardrail. Detection: COST_GUARD alarm. Recovery: pause non-essential agents, investigate root cause.

## Recovery path

If the ledger becomes inconsistent, the founder freezes new financial commitments and runs a full re-close from invoice and bank export sources. No external financial communication is issued until the close is certified.

## Metrics

- Monthly recurring revenue (estimated and verified).
- Gross margin per engagement (verified).
- Cash runway in months (verified).
- Customer acquisition cost (estimated; see AI Unit Economics).
- Net dollar retention (verified, rolling 12 months).

## Disclaimer

Financial figures in this OS are operational. They are not audited financial statements. Dealix does not guarantee future revenue or margin. Estimated value is not Verified value.
