# Retention & Referral OS

How Dealix earns the next month of revenue and the next ten warm
leads from existing customers — without "automating" the relationship.

## 1. Retention loop

- Daily health roll-up per active engagement.
- Weekly retention review on the founder console.
- Monthly business review (MBR) prepared automatically as a draft.
- Renewal motion opens 60 days before contract end with a draft
  retention offer the founder reviews.

## 2. Referral ask

- A referral-ask draft is generated only when:
  - the customer health is "green" for the last 21 days, and
  - a concrete proof artifact has been shipped, and
  - the customer has acknowledged at least one outcome.
- The ask is drafted; the founder sends it.

## 3. Ledgers

- `revenue/retention_register.csv`:
  ```
  account_id,health,last_check_at,renewal_due_at,offer_id,status
  ```
- `revenue/referral_register.csv`:
  ```
  ask_id,account_id,referee_name,channel,draft_id,status
  ```

## 4. KPIs

- Net retention (when measurable).
- Logo retention.
- Referral acceptance rate per ask.
- Time from "green" → referral ask.

## 5. Banned patterns

- ❌ Asking for referrals after any unresolved complaint.
- ❌ Asking the same customer for more than one referral per 60 days.
- ❌ Sharing referee details without their consent.
