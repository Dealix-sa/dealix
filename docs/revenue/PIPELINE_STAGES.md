# مراحل خط الإيرادات — Pipeline Stages

> Formal stages with definitions and exit criteria. No vibes.

## Purpose
Make stage transitions auditable. Two people looking at the same opportunity should pick the same stage.

## Owner
Founder/CEO.

## Inputs
- Opportunity records (CRM).
- Revenue control system (`REVENUE_CONTROL_SYSTEM.md`).
- ICP fit (`docs/strategy/ICP_STRATEGY.md`).

## Outputs
- Per-opportunity stage history.
- Daily snapshot in `REVENUE_COMMAND_CENTER.md`.

## Rules
1. A stage transition is recorded only when its exit criteria are met. Backdating is forbidden.
2. Every opportunity has a single current stage. Multi-stage tagging is not allowed.
3. Stages are linear: Lead → DM identified → Reply → Call scheduled → Sample → Proposal sent → Proposal accepted → Invoiced → Paid → Delivery → (Retainer attached / Lost).
4. Move to "Lost" requires a written reason from one of the codes below.
5. Move to "Paid" requires confirmed receipt per `CASH_RULES.md` — not "verbal yes," not "signed but unpaid."

## Metrics
- Conversion rate per transition.
- Median time in each stage.
- Stage aging > 21 days count.
- Lost-reason distribution.

## Cadence
Reviewed Daily on the Revenue Command Center; Weekly stuck-stage sweep.

## Evidence
CRM exports; per-stage transition log in `dealix-ops-private/revenue/opps/`.

## Verifier
`make pipeline-verify` — checks all active opps have current stage, age, and required artifact.

## Runtime Command
`make pipeline-snapshot`

---

## Stage definitions

### Lead
- Definition: a new contact recorded with source and ICP-fit score.
- Exit: DM identified and contact attempt made within 5 days.

### DM identified
- Definition: the decision-maker's name and role are known. The DM can sign within the proposed SAR band.
- Exit: written reply received from DM or DM's delegate.

### Reply
- Definition: a meaningful written reply from the DM acknowledging interest in a conversation.
- Exit: call scheduled with agenda.

### Call scheduled
- Definition: calendar event with agenda sent in advance, confirmed by the DM.
- Exit: call completed with notes saved; either a Signal Sample is sold or the opportunity is moved to "Lost."

### Sample
- Definition: a paid Signal Sample is signed and deposit received per `CASH_RULES.md`.
- Exit: Sample delivered and proposal for Revenue Sprint (or higher rung) sent.

### Proposal sent
- Definition: proposal file produced from `templates/PROPOSAL_*.md.j2`, sent to DM.
- Exit: written acceptance (or written rejection → Lost).

### Proposal accepted
- Definition: DM has confirmed in writing acceptance of scope and price.
- Exit: invoice issued per `docs/finance/INVOICE_WORKFLOW.md`.

### Invoiced
- Definition: invoice issued in the customer's name and currency (SAR default).
- Exit: full payment received per `CASH_RULES.md`.

### Paid
- Definition: payment received in Dealix's account; invoice marked paid in accounting.
- Exit: delivery kickoff scheduled within 7 days.

### Delivery
- Definition: sprint in progress per `docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`.
- Exit: acceptance signed; case-safe artifact published; retainer attach pursued.

### Retainer attached (terminal positive)
- Definition: Revenue Desk retainer signed and first month invoiced.

### Lost (terminal negative)
- Definition: opportunity will not progress. Reason code required.

## Lost reason codes

| Code | Meaning |
|---|---|
| L-NOFIT | ICP-fit too low; should not have entered pipeline |
| L-BUDGET | Budget mismatch unresolved |
| L-TIMING | Decision deferred > 90 days |
| L-COMPETITOR | Chose alternative vendor |
| L-INACTION | DM ghosted after two follow-ups |
| L-GUARANTEE | Required a guarantee we won't make |
| L-SCRAPE | Required a banned tactic |
| L-OTHER | Free text required |

## Stage age thresholds (per `REVENUE_CONTROL_SYSTEM.md`)

| Stage | Max age | Action |
|---|---|---|
| Lead | 3 days | Reach out or archive |
| DM identified | 5 days | Reach out via warm intro |
| Reply | 7 days | One follow-up, then defer |
| Call scheduled | 7 days | Re-confirm |
| Sample | 14 days | Send proposal or close |
| Proposal sent | 14 days | One follow-up; if no reply, mark Lost: L-INACTION |
| Invoiced | 21 days | Per `PAYMENT_RULES.md` late policy |

## Artifact required per stage
| Stage | Artifact |
|---|---|
| Lead | Source + ICP-fit score |
| DM identified | DM name + role |
| Reply | Saved reply text (anonymized) |
| Call scheduled | Calendar entry + agenda |
| Sample | Signed sample agreement + deposit receipt |
| Proposal sent | Proposal file (templated) |
| Proposal accepted | Written acceptance message |
| Invoiced | Invoice file + payment terms |
| Paid | Payment receipt |
| Delivery | Sprint kickoff doc |

## القواعد العربية
1. كل انتقال مرحلة يتطلب استيفاء معاييره. لا تأريخ بأثر رجعي.
2. الفرصة في مرحلة واحدة فقط في كل وقت.
3. "مدفوع" يعني نقدًا مستلَمًا، لا موافقة شفوية.

## Cross-links
- `REVENUE_CONTROL_SYSTEM.md`
- `OFFER_LADDER.md`
- `CASH_RULES.md`
- `docs/finance/INVOICE_WORKFLOW.md`
- `docs/finance/PAYMENT_RULES.md`
