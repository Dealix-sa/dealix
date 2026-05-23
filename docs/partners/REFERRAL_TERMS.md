# Referral Terms

> Commercial terms for partner-referred business.

## Definitions

- **Referral:** a partner introduces a named prospect, with an
  introduction email or call, and the prospect agrees to a conversation
  with us.
- **Closed referral:** the prospect becomes a paid Sprint or retainer
  customer within 120 days of introduction.

## Standard Commission

- **Sprint:** 15% of net Sprint revenue, paid on receipt of customer
  payment.
- **Retainer:** 10% of monthly retainer fee for the first 6 months,
  paid monthly on receipt of customer payment.

We do not pay commission on:

- Renewals after the first 6 months.
- Expansion MRR beyond the original retainer scope.
- Refunded revenue (commission clawed back pro-rata).
- Bad-debt revenue (commission not paid until cash collected).

## Tracking

- Each referral logged in `dealix-ops-private/partners/referrals.csv`
  with: partner, prospect, intro date, status, deal status, commission.
- Commission accrued monthly; paid quarterly to active partners.

## Special Cases

- **Co-sell:** partner participates in delivery (e.g. brings sector
  expertise). Custom terms; T3 decision.
- **White-label:** not offered. We refuse polite requests for it.
- **Reverse referral:** we refer a customer to a partner (when we
  refuse the customer per `BAD_REVENUE_FILTER.md`). No commission flows
  in either direction unless a reciprocity agreement is on file.

## Conflict Rules

- A prospect introduced by two partners: the first to introduce in
  writing is the source.
- A prospect already in our pipeline at time of introduction: no
  commission applies; partner is informed.

## Termination

- Either party can end the referral relationship with 30 days written
  notice.
- Commissions earned through paid customer payments before termination
  continue to vest for the original 6-month window.

## Disputes

- Plain-language conversation first.
- Disputes documented in writing.
- External mediation if unresolved at 30 days.
