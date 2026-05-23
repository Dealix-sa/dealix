# Market Domination Intelligence

Wordmark: DEALIX
Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System (RevOS).

This document is the meta-layer for every piece of market intelligence Dealix
produces. It binds the sector ranking system, ICP segmentation, buyer
personas, trigger events, competitive view, and account scoring into a single
operating loop. No piece of intelligence stands alone — each one is an
input into a single decision: where do we place the next unit of operator
attention, and what offer do we put in front of it.

## 1. Why this layer exists

Saudi B2B is a relationship-dense, trust-first market. Generic CRM thinking
treats every account as a row in a list; that approach loses against
operators who understand sector context, decision authority, and trigger
timing. Dealix replaces "rows in a list" with a layered model:

- Sectors are ranked, not assumed.
- ICPs are segmented inside each sector, not flattened.
- Personas are mapped to decision authority and pain, not titles.
- Triggers convert static accounts into time-bounded opportunities.
- Account scoring synthesises all of the above into a single priority value.

The output is a ranked, dated, defensible action list — never a vague
"prospect list." It is the input to the Distribution War Machine and the
Revenue Factory.

## 2. The intelligence loop

```
Sector Ranking  ->  ICP Segmentation  ->  Persona Map
        |               |                   |
        v               v                   v
                   Account Universe
                          |
                          v
              Trigger Event Detection (date-bound)
                          |
                          v
                 Account Scoring Model
                          |
                          v
        Ranked Operator Action List (CSV)
                          |
                          v
            Distribution War Machine (drafts only)
                          |
                          v
              Founder approval at trust gate
                          |
                          v
                  Revenue Factory
```

Every arrow is a one-way information flow into an approval queue. No step
sends anything externally on its own. The loop is human-gated at the
distribution and revenue boundary.

## 3. Component documents

- `SECTOR_RANKING_SYSTEM.md` — scoring rubric for Saudi sectors and the
  weight table used to rank them.
- `ICP_SEGMENTATION_SYSTEM.md` — structured definition of the ideal customer
  inside each ranked sector, plus tiers and disqualifiers.
- `BUYER_PERSONA_SYSTEM.md` — persona library for CEO, CRO, COO, CTO, and
  Head of Marketing.
- `TRIGGER_EVENT_SYSTEM.md` — catalogue of trigger events that move an
  account from "interesting" to "ready."
- `ACCOUNT_SCORING_MODEL.md` — feature list, weights, calibration cadence,
  and CSV output schema.
- `COMPETITIVE_INTELLIGENCE_SYSTEM.md` — how Dealix tracks alternatives
  (scraping tools, spam tools, generic CRM, agencies) ethically.
- `OFFER_CHANNEL_FIT_SYSTEM.md` — which offers belong in which channels.
- `SAUDI_B2B_MARKET_MAP.md` — the sector map and current state of each
  sector at the time of writing.
- `LEAD_SOURCE_SYSTEM.md` — sanctioned lead sources only. No scraping.
- `MARKET_RESEARCH_PROTOCOL.md` — research cadence and ethical guardrails.

## 4. Operating cadence

| Cadence | Activity | Owner | Output |
|---|---|---|---|
| Daily | Trigger event scan; account list refresh | Growth Strategist | `growth/account_scores.csv` |
| Weekly | Sector ranking refresh; ICP review | Growth Strategist | `growth/sector_targets.csv` |
| Monthly | Persona library review; objection log sync | Growth Strategist + Founder | `growth/persona_review.md` |
| Quarterly | Account scoring calibration; weight retune | Growth Strategist + Performance Analyst | `growth/scoring_calibration.md` |

All outputs are written to the private ops runtime in the listed paths and
then surfaced to the Founder Console for approval. Nothing in this layer
sends anything externally.

## 5. Pillars binding

- Built on Trust: every source is named, every score has a calibration log.
- Driven by Growth: ranking is a forcing function, not a vanity dashboard.
- Closing Deals: the loop ends at an approval queue with a draft, not a
  research note.
- Focused on Results: scoring is recalibrated against pipeline outcomes.
- Global Mindset, Local Impact: sector models account for Saudi-specific
  authority, procurement, and trust patterns.

## 6. Non-negotiables

- No guaranteed revenue, sales, or meetings claims appear anywhere in the
  scoring outputs or the briefs they generate.
- No external send is initiated by any agent. The loop always terminates in
  an approval queue.
- Every score, every weight, and every trigger source is auditable to a
  named row in the trust ledger.
- A3 (autonomous external action) is banned across the intelligence layer
  and every downstream machine. Only A1 (observe / draft) and A2 (assist
  with explicit approval) are permitted.

## 7. Inputs and outputs (summary)

Inputs:
- Sector reports (published, dated, attributable).
- Founder content and warm referrals.
- Partner-introduced accounts.
- Public funding and hiring signals (with source attribution).
- Internal pipeline outcomes from `sales/proposal_queue.csv` and
  `customer_success/referral_queue.csv`.

Outputs (all in private ops runtime):
- `growth/sector_targets.csv`
- `growth/account_scores.csv`
- `growth/trigger_events.csv`
- `growth/persona_review.md`
- `growth/scoring_calibration.md`

## 8. Failure modes and recovery

| Failure | Symptom | Recovery |
|---|---|---|
| Stale sector ranking | Targets drift from real demand | Re-run sector ranking; flag in weekly brief |
| Persona drift | Reply rates drop below band | Reopen persona library, re-interview 3 buyers |
| Trigger fatigue | Same trigger fires too often | Add trigger half-life; require corroboration |
| Score-outcome divergence | Top-scored accounts under-convert | Run calibration; retune weights |
| Source contamination | Source no longer attributable | Quarantine source; rebuild from sanctioned list |

## 9. Authority and review

This document is owned by the Growth Strategist agent (`growth_strategist`
in `registries/agent_registry.yaml`, approval class max A2). All structural
changes require founder approval. Weight or threshold changes are logged in
the trust ledger and rolled forward in the quarterly calibration entry.

The intelligence layer never speaks to a prospect directly. It tells the
operator where to spend the next hour. That is the whole job.
