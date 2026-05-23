# Buyer Persona System

We do not write Hollywood personas with names and hobbies. We write **operating personas**: title, decisions they own, metrics they're measured on, pain, evidence we look for, and what we offer them.

## 1. Persona schema

```
persona_id, title, sector_relevance,
decisions_owned, kpis, pains,
evidence_we_look_for,
preferred_channel, preferred_language,
recommended_offer, refused_offers,
example_open_lines
```

## 2. Canonical personas

### P-CEO-MidMarket — CEO / Managing Director (Saudi mid-market B2B)

- **Decisions owned:** sector strategy, hiring of head of sales, partner deals.
- **KPIs:** total revenue, EBITDA, gross margin, KSA market share.
- **Pains:** sales is unpredictable; can't see real-time pipeline; depends on 2–3 rainmaker reps.
- **Evidence:** the CEO talks about "predictable revenue", or has hired a CRO in the last 12 months.
- **Channel:** warm intro > LinkedIn > email.
- **Language:** bilingual; opening in AR.
- **Recommended offer:** Revenue Sprint → Revenue Desk → Founder Console.
- **Refused:** never push Free Sample to a CEO — they want decisions, not freebies.

### P-CRO — Chief Revenue Officer / Head of Sales

- **Decisions owned:** sales team structure, quota, sales tooling, pipeline coverage.
- **KPIs:** win rate, cycle time, deal size, pipeline coverage ratio.
- **Pains:** team spends time on low-quality leads; weak forecasting; manual reporting.
- **Evidence:** CRO posts about pipeline coverage, forecasting, or hires AEs/BDRs publicly.
- **Channel:** LinkedIn > email.
- **Language:** EN (often), AR optional.
- **Recommended offer:** Revenue Sprint → Revenue Desk.
- **Refused:** Founder Console (not their buying authority).

### P-Founder-Agency — Founder of B2B agency / consultancy

- **Decisions owned:** everything.
- **KPIs:** monthly billings, project margin, retainer count.
- **Pains:** the cobbler's children — their own marketing is the worst-served account.
- **Evidence:** agency posts case studies for clients but their own pipeline is opaque.
- **Channel:** LinkedIn (founder-to-founder).
- **Language:** bilingual, often EN-first.
- **Recommended offer:** Revenue Sprint → Partner / White-label.
- **Refused:** Free Sample of low-effort kind — they will not engage.

### P-Implementer — ERP / CRM implementation partner

- **Decisions owned:** which sectors to chase, which products to resell.
- **KPIs:** licence revenue, implementation revenue, partner tier with the vendor.
- **Pains:** pipeline is RFP-driven and slow; need warm intros and proof artefacts.
- **Evidence:** vendor partner badges, sector case studies on their site.
- **Channel:** warm intro > LinkedIn > email.
- **Language:** bilingual.
- **Recommended offer:** Revenue Sprint → Partner / White-label.
- **Refused:** Free Sample without a discovery call first.

### P-Cyber-SalesDirector — Sales director at a cybersecurity firm

- **Decisions owned:** pipeline strategy, BDR team, channel partner mix.
- **KPIs:** booked meetings, qualified pipeline, sector wins.
- **Pains:** long cycle, depend on conferences and channel referrals.
- **Evidence:** talks about pipeline coverage, ABM, channel partner programmes.
- **Channel:** LinkedIn > warm intro.
- **Language:** EN-first.
- **Recommended offer:** Revenue Sprint focused on ABM.
- **Refused:** generic free sample — they have many vendors and need a sector-specific artefact.

### P-Logistics-CCO — Commercial director at a logistics/industrial firm

- **Decisions owned:** which verticals to target, RFP responses.
- **KPIs:** new logo revenue, expansion revenue, RFP win rate.
- **Pains:** RFP-only pipeline, missing top-of-funnel.
- **Evidence:** posts about KSA mega-projects, vertical expansion.
- **Channel:** warm intro > email.
- **Language:** bilingual.
- **Recommended offer:** Revenue Sprint with sector-specific Proof Pack.
- **Refused:** Founder Console (procurement-led organisation).

### P-SaaS-RevOps — RevOps lead at a SaaS / software vendor

- **Decisions owned:** sales tooling, sequencing, pipeline analytics.
- **KPIs:** sequence response rate, MQL-to-SQL, pipeline velocity.
- **Pains:** their outbound tools violate KSA compliance posture; need trust-gated motion.
- **Evidence:** posts about Outreach/Salesloft, KSA market entry.
- **Channel:** LinkedIn.
- **Language:** EN-first.
- **Recommended offer:** Revenue Sprint → Revenue Desk.
- **Refused:** Free Sample (they want to see proof artefacts).

## 3. Persona × offer matrix

See `OFFER_CHANNEL_FIT_MATRIX.md` for the recommended offer × channel × persona grid.

## 4. Refusal patterns

Every persona has at least one **refused offer**. Pushing a refused offer to a persona is a doctrine violation — the verifier checks recent proposals against persona refusal lists.

## 5. Evidence requirements

We do not invent pain. For every persona we approach, we cite at least one piece of public evidence (a post, a press release, a job ad) in the outreach draft. The verifier blocks outreach drafts that have an empty `personalisation_evidence` field.
