# Strategic Targeting OS

The Strategic Targeting OS is how Dealix decides **who to approach, why, and with which offer**. It is doctrine + data + scoring + decision rules. The OS is built on five components:

1. **ICP** — Ideal Customer Profile (`ICP_SEGMENTATION_SYSTEM.md`).
2. **Sectors** — focus verticals (`SECTOR_DOMINATION_ENGINE.md`).
3. **Account scoring** — A/B/C/Reject (`ACCOUNT_SCORING_MODEL.md`).
4. **Buyer personas** — titles, pain, evidence (`BUYER_PERSONA_SYSTEM.md`).
5. **Offer/channel fit** — which rung of the offer ladder for whom, via which channel (`OFFER_CHANNEL_FIT_MATRIX.md`).

## 1. Doctrine

- **Saudi-first.** KSA companies are the default target. Outside-KSA is the exception.
- **B2B-only.** No consumer business.
- **High-ticket.** Average engagement value ≥ 5,000 SAR/month or one-off ≥ 15,000 SAR.
- **Trust-gateable.** The buyer must accept human-approved outbound. We do not chase customers who insist on uncontrolled automation.
- **Verifiable pain.** We refuse to engage with pain we cannot diagnose from data within 7 days.

## 2. Target sectors (canonical)

| Sector                                       | Why                                                | Initial buyer titles                              |
|----------------------------------------------|----------------------------------------------------|---------------------------------------------------|
| ERP / CRM implementers                       | Big projects, slow lead flow, need productisation  | Managing partner, head of sales, CRO              |
| Cybersecurity firms                          | High deal size, long cycles, need pipeline lift    | Sales director, founder, BD lead                  |
| B2B agencies (digital, performance)          | Pain: own marketing is the cobbler's children      | Founder, head of growth, ops lead                 |
| Logistics / industrial services              | Saudi expansion, RFP-driven, need warm intros      | Commercial director, GM, founder                  |
| Consulting / digital transformation          | Need productised offers, struggle with sample work | Partner, MD, head of sales                        |
| SaaS / software vendors                      | Need outbound that respects compliance             | Head of sales, founder, RevOps lead               |
| Enterprise services (KSA mid-market)         | Need revenue intelligence + bilingual delivery     | CEO, CCO, head of sales                           |
| Saudi high-ticket B2B providers              | The Dealix sweet spot                              | Founder, MD, CRO                                  |

## 3. Scoring fields (canonical)

These are the **only fields** that determine A/B/C/Reject priority. The verifier and `data/growth/account_scores.csv` enforce them.

| Field                          | Range       | Notes                                          |
|--------------------------------|-------------|------------------------------------------------|
| Saudi relevance                | 0–10        | Higher = KSA HQ, KSA revenue, KSA hiring       |
| B2B fit                        | 0–10        | B2B selling motion present                     |
| High-ticket potential          | 0–10        | ARR or deal size matches our offer ladder      |
| Buyer clarity                  | 0–10        | A specific named buyer + title + reachable     |
| Pain urgency                   | 0–10        | Active pain, not theoretical                   |
| Outreach fit                   | 0–10        | They accept email/LinkedIn outreach            |
| Proof fit                      | 0–10        | We can produce a proof artefact for them       |
| Partner potential              | 0–10        | They could co-deliver / refer / co-brand       |
| Delivery complexity            | 0–10        | LOWER is better — we down-weight high-complexity |
| Trust risk                     | 0–10        | LOWER is better — we down-weight high-risk     |
| **Final priority**             | A / B / C / Reject | Rule below                                  |

### Priority rule

- **A** — sum (Saudi + B2B + ticket + buyer + pain) ≥ 38 AND trust_risk ≤ 4 AND delivery_complexity ≤ 6.
- **B** — sum ≥ 30 AND trust_risk ≤ 6.
- **C** — sum ≥ 22.
- **Reject** — anything below, OR trust_risk ≥ 8, OR delivery_complexity ≥ 9.

Only **A** accounts feed the active outreach queue. **B** feeds the warm nurture stream. **C** sits in the watch list. **Reject** is documented and removed.

## 4. Output schema (per account)

For every scored account we record:

```
account_id, name, sector, country, hq_city,
saudi_relevance, b2b_fit, high_ticket_potential, buyer_clarity,
pain_urgency, outreach_fit, proof_fit, partner_potential,
delivery_complexity, trust_risk,
final_priority,
next_action, proof_needed, recommended_offer, recommended_channel,
owner, last_review_at
```

See `data/growth/account_scores.csv` for the live record.

## 5. Operating cadence

- **Daily:** review new accounts entering the queue (≤ 15 per day).
- **Weekly:** founder reviews the **A** queue and recommended next actions.
- **Monthly:** sector-level retrospective — which segment converted, which to drop.

## 6. Decision gates

- No outbound to an account without a recorded final_priority.
- No proposal to an account without a recommended_offer.
- No referral request without partner_potential ≥ 6.
