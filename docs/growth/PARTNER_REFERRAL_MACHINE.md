# Partner Referral Machine

> Tracks partner contracts, queues warm intro drafts, monitors mutual revenue.

## 1. Purpose

Build and operate a small, deliberate partner network — agencies, consultancies, implementers — that send Dealix qualified opportunities and accept reciprocity.

## 2. Input

- `data/growth/partners.csv` (partner master).
- Partner contracts (private ops, not in repo).
- Reciprocity ledger (private ops).
- Account scoring output — to know which accounts a partner might warmly introduce.

## 3. Output

- Queued warm intro drafts in `data/marketing/outreach_drafts.csv` with `channel = warm_intro` and `partner_id` set.
- Monthly partner scorecard in `data/growth/partner_scorecards.csv` (created on demand).

## 4. Approval class

**A2.** Founder + partner both approve any warm intro before it goes out.

## 5. Owner

Distribution Operator + founder + named partner contact.

## 6. Worker name

`partner_referral_worker`.

## 7. KPI

- Active partners: target 5–10 (not more — focus matters).
- Warm intros queued per partner per month: ≥ 1.
- Mutual revenue per partner per quarter: tracked, founder-reviewed.
- Reciprocity balance: drafts queued *from* Dealix to the partner per quarter ≥ drafts queued *from* partner to Dealix.

## 8. Failure modes

| Failure                                                   | Recovery                                       |
|-----------------------------------------------------------|------------------------------------------------|
| Partner has not produced an intro in 90 days              | Founder reviews; possibly archive partner      |
| Reciprocity imbalance > 3:1 against us                    | Pause new requests; founder discussion         |
| Intro target is in another partner's exclusive sector     | Refuse; document the conflict                  |

## 9. Doctrine

- We do **not** pay per-referral commissions in v1. Reciprocity is the currency.
- Partner contracts are co-signed and stored privately.
- A partner cannot dictate our brand voice or override the brand verifier.

## 10. Audit

Every warm intro carries a `partner_id`. Every partner outcome (booked / declined / closed) is logged. Quarterly review by the founder.
