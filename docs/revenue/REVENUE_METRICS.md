# Revenue Metrics

The numbers that define whether the company is winning.

## Core metrics
| Metric | Definition | Cadence | Source |
|---|---|---|---|
| Cash collected | SAR received and reconciled | Weekly | `cash_collected.csv` |
| MRR | Sum of active recurring contracts | Weekly | `mrr_tracker.csv` |
| Pipeline value | Sum of open proposals × stage weight | Weekly | Pipeline CSV |
| New deals | Count of newly Paid deals | Weekly | Pipeline CSV |
| Average deal size | Cash / count for new deals | Monthly | Derived |
| Win rate | Paid / Proposal Sent | Monthly | Pipeline CSV |
| Retainer conversion | Retainer / Delivered | Monthly | Pipeline CSV |
| Refund rate | Refunds / Cash collected | Monthly | Finance |
| AR aging | Outstanding invoices by age | Weekly | Finance |
| Gross margin estimate | Revenue minus direct cost | Monthly | Finance |

## Definitions
- **MRR** counts only signed, active, paying retainers. Trials and pilots do not count.
- **Cash collected** is bank-confirmed, not invoice-issued.
- **Pipeline value** uses fixed weights from `PIPELINE_STAGES.md` (e.g., Proposal Sent = 0.4, Call Booked = 0.2).

## Rule
A metric without a definition is a story. Every metric here has one definition, one source, and one owner.
