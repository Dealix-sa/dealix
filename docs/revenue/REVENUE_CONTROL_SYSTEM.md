# نظام التحكم بالإيرادات — Revenue Control System

> The control loop: lead → DM → reply → call → sample → proposal → payment.

## Purpose
Define the seven control points between a new lead and recognized cash. Each control point has a rule, an SLA, and a verifier.

## Owner
Founder/CEO.

## Inputs
- Inbound signals (founder content, intros, inbound).
- Pipeline stages (`PIPELINE_STAGES.md`).
- ICP fit scores (`docs/strategy/ICP_STRATEGY.md`).
- Offer ladder (`OFFER_LADDER.md`).
- Cash rules (`CASH_RULES.md`).

## Outputs
- Per-opportunity record in CRM with stage transitions.
- Daily snapshot in `REVENUE_COMMAND_CENTER.md`.
- Stuck-stage report (weekly).

## Rules
1. Every opportunity passes through all seven control points in order. Skipping is logged as an exception with reason.
2. Each control point has a maximum age. Exceeding it triggers either an action or a kill.
3. No control point is "marked done" without the artifact required (see table).
4. No external automated sends at any point. All sends are personal and disclosed.
5. The loop ends only at "Paid" per `CASH_RULES.md` — not at "verbal yes."

## Metrics
- Stage-to-stage conversion rates (each control point).
- Stage aging distribution.
- End-to-end median time (Lead → Paid).
- Exception rate (skipped control points).

## Cadence
Reviewed Daily on `REVENUE_COMMAND_CENTER.md`. Weekly stuck-stage sweep.

## Evidence
CRM, per-opportunity files in `dealix-ops-private/revenue/opps/`.

## Verifier
`make revenue-control-verify` — checks every open opportunity has a current stage, age, and required artifact.

## Runtime Command
`make stage-sweep`

---

## The Seven Control Points

| # | Stage | Required artifact | Max age | Action on age trigger |
|---|---|---|---|---|
| 1 | Lead | Source recorded; ICP-fit score | 3 days | Reach out or archive |
| 2 | DM identified | DM name, role, AR/EN preference | 5 days | Reach out via warm intro or content |
| 3 | Reply | First reply text saved (anonymized) | 7 days | One follow-up, then defer |
| 4 | Call scheduled | Calendar entry; agenda | 7 days | Re-confirm or move to defer |
| 5 | Sample (paid Signal Sample) | Signed sample agreement; deposit received | 14 days | Send proposal or close out |
| 6 | Proposal sent | Proposal file (templated) | 14 days | Follow up; if no reply → defer |
| 7 | Paid | Invoice paid in full per `CASH_RULES.md` | n/a | Move to delivery |

## Rule per stage

### 1. Lead
- Recorded with source and ICP-fit score within 24 hours.
- ICP-fit < 5: not added to active pipeline; recorded in passive log.

### 2. DM identified
- The "DM" is the decision-maker who can sign the SAR amount under discussion.
- If the contact is not the DM, the stage does not advance until the DM is identified.

### 3. Reply
- The first written reply is captured (anonymized). No reply within 7 days of contact → one follow-up only, then defer.

### 4. Call scheduled
- Call has a written agenda sent in advance.
- Agenda includes: scope of Signal Sample, expected outputs, disclosure language.

### 5. Sample (Signal Sample)
- Smallest paid rung from `OFFER_LADDER.md`.
- Deposit required before work starts (per `CASH_RULES.md`).
- Output: a written sample report (case-safe template usable as anonymized evidence).

### 6. Proposal sent
- Uses `templates/PROPOSAL_*.md.j2`.
- Includes scope, exclusions, deliverables, price, payment terms, disclosure footer.
- Sent in AR + EN if customer is bilingual; otherwise in the customer's primary language.

### 7. Paid
- Per `CASH_RULES.md` — only when invoice is fully paid does the opportunity move to "Paid."
- Partial payments are tracked but do not count as closed.

## Banned actions inside the loop
- Sending unsolicited templated emails to lists.
- Using LinkedIn automation tools to "warm up" cold contacts.
- Telling a prospect "guaranteed" or "we ensure" or "ROI of N%".
- Promising case study features without written customer consent.

## Exceptions (allowed with written reason)
- Skipping a stage when a warm intro replaces it (e.g., DM identified at Lead stage).
- Extending an age threshold for sectors with structurally longer cycles — must be approved by founder.

## القواعد العربية
1. كل فرصة تمر بالنقاط السبع بالترتيب.
2. لكل نقطة دليل مطلوب وسقف عمر. تجاوز السقف يفعّل إجراءً أو إلغاءً.
3. لا إرسال آلي خارجي في أي مرحلة.

## Cross-links
- `PIPELINE_STAGES.md`
- `OFFER_LADDER.md`
- `CASH_RULES.md`
- `REVENUE_COMMAND_CENTER.md`
- `docs/strategy/ICP_STRATEGY.md`
