# سياسة الاسترداد — Refund Policy

> When refunds apply. Who approves. How they are logged.

## Purpose
A written refund policy is part of the Trust moat. Customers see consistency; the founder makes the call inside a written frame.

## Owner
Founder/CEO.

## Inputs
- Engagement contract / proposal.
- Delivery state (`docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`).
- Cash rules (`docs/revenue/CASH_RULES.md`).
- Trust posture (`docs/14_trust_os/TRUST_OS.md`).

## Outputs
- Refund decisions in `dealix-ops-private/finance/refunds/YYYY-MM-DD_<slug>.md`.
- Credit note(s) via `INVOICE_WORKFLOW.md`.
- North star adjustment per `docs/strategy/NORTH_STAR.md` (refunded sprint subtracts).

## Rules
1. Every refund decision is written. No verbal-only refunds.
2. Refund approval is the founder's, with reviewer if A3 (publicly visible).
3. Refund timing follows the schedule below; no surprise refunds.
4. Refunds reverse recognized revenue in the month paid (per `CASH_RULES.md`).
5. The customer relationship after a refund is documented: continue / off-board / referral.
6. Refunds are a Trust event and update the Trust dashboard.

## Metrics
- Refund rate: target ≤ 2% of cash-in (rolling 90 days).
- Refund decision turnaround: target ≤ 5 business days.
- Repeat refund customers: target 0.

## Cadence
Per case. Aggregate reviewed Monthly.

## Evidence
`dealix-ops-private/finance/refunds/`.

## Verifier
`make refund-verify` — checks every refund has a decision file, credit note, and recognition reversal.

## Runtime Command
`make refund slug=<slug>`

---

## When refunds apply

### Signal Sample
- Eligible for full refund if Dealix has not started work within 7 days of cash clearing AND the customer requests in writing.
- Not refundable once the sample report has been delivered.

### Revenue Sprint / Managed Pilot
- Deposit (first 50%): refundable in full if Dealix has not started work AND no scoping artifact has been delivered.
- After kickoff: prorated refund based on percentage of scope completed, minus founder shadow hours at SAR 600/hour.
- Final tranche: payable on acceptance. If acceptance is refused after delivery, the dispute escalates per the contract; refund is decided case-by-case.

### Revenue Desk (Retainer)
- Cancellable with 30-day notice after the 3-month minimum.
- Refunds for the current paid month: only if no service has been rendered in that month.

### Dealix OS
- Annual fee: prorated refund within first 30 days only.
- After 30 days: no refund; cancellation effective at end of license year.

## Refund schedule

| Step | Owner | Target time |
|---|---|---|
| Customer requests refund (written) | Customer | day 0 |
| Acknowledge receipt | Founder | day 1 |
| Review eligibility | Founder | day 1–3 |
| Decision (Approve / Deny / Partial) | Founder | day 5 |
| Credit note issued | Founder | day 6 |
| Refund paid | Founder | day 7–14 |
| Recognized revenue reversal logged | Founder | day 7–14 |
| Trust dashboard updated | Founder | day 14 |

## Decision file template

```
# Refund Decision — <slug>
Date: YYYY-MM-DD
Customer (anon for repo): Customer-XX
Engagement: <rung + sprint id>
Amount paid (SAR): X
Amount delivered (% scope): NN
Amount refunded (SAR): X

## Reason (per customer)
<paraphrased; not verbatim if PII risk>

## Eligibility against policy
<reference: Signal Sample / Sprint / Retainer / OS clause>

## Decision
[ ] Full refund
[ ] Partial refund — amount SAR X
[ ] Denied — reason

## Approval
Founder: signed YYYY-MM-DD
Reviewer (if A3): signed YYYY-MM-DD

## Aftermath
- Credit note id: CN-YYYY-NNNN
- Revenue recognition reversal: YYYY-MM-DD entry
- North star adjustment: -1 PSDE (if applicable)
- Relationship status: continue / off-board / referral

## Learning extracted (one sentence)
<text>
```

## What is NOT refundable
- Work that has been delivered and accepted.
- Sprints delivered with case-safe artifacts already published with customer consent (consent withdrawal is handled separately, not via refund).
- Disputes over the value of outcomes when scope was met.

## Customer-facing refund language (proposal footer)
> Refund policy: Refunds are governed by Dealix's `REFUND_POLICY.md`. In short: deposits are refundable before work starts; prorated refunds apply for partial delivery; retainers cancellable with 30-day notice after the 3-month minimum. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

## القواعد العربية
1. كل قرار استرداد مكتوب. لا قرارات شفهية.
2. الاسترداد يُلغي الاعتراف بالإيراد في شهر الاسترداد.
3. الاسترداد حدث ثقة يُحدِّث لوحة الثقة.

## Cross-links
- `BILLING_POLICY.md`
- `PAYMENT_RULES.md`
- `INVOICE_WORKFLOW.md`
- `docs/revenue/CASH_RULES.md`
- `docs/14_trust_os/TRUST_OS.md`
- `docs/strategy/NORTH_STAR.md`
