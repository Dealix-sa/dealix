# Objection Library System

The Objection Library System is the structured store of objections
Dealix has actually heard from buyers, the approved responses, and the
operating data that tells the team which response works for which
persona. Objections are not adversaries; they are signals.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Capture every recurring objection, the persona it tends to come from,
the approved response, and the link to proof or content that supports
the response. Make objection handling a structured asset, not a
recurring scramble.

## 2. Library structure

`marketing/objection_library.csv` columns:

- `objection_id`
- `objection_text` — canonical phrasing
- `persona_ids` — pipe-delimited
- `sector_ids` — pipe-delimited (where the objection skews to a sector)
- `root_cause` — what is actually behind the objection
- `approved_response_ar` — Arabic response
- `approved_response_en` — English response
- `referenced_proof_ids`
- `referenced_content_ids`
- `competitor_refs` — links to `growth/competitor_intel.csv` where the
  objection traces to a competitor experience
- `last_validated_at`
- `validated_by`

## 3. Categories

- Trust objections (e.g. "show me a Saudi reference").
- Authority objections ("not me — that is the CRO").
- Process objections ("procurement will take months").
- Tooling objections ("we already use HubSpot/Salesforce").
- Outcome objections ("will this actually work for us").
- AI/governance objections ("how is data handled, where are evals").
- Brand objections ("this conflicts with our agency").
- Risk objections ("what if it fails").

Each objection is categorised and tied to a root cause that operators
can address — not a surface counter-argument.

## 4. Approved response shape

Every approved response follows the same shape:

1. Acknowledge specifically.
2. Reframe the root cause honestly.
3. Offer a concrete next step (sample, named reference, proof
   artefact, calibrated commitment).
4. Avoid guaranteed-outcome language.
5. Honour bilingual operating reality (Arabic + English versions).

## 5. Source of truth

`marketing/objection_library.csv` is the canonical store. Reply drafts,
proposal drafts, and content all reference it by `objection_id`.

## 6. Approval class

A2. Library entries are drafted autonomously by the Distribution
Operator from real reply data; the founder approves additions and
edits.

## 7. Trust gate

- Guarantee scan on every approved_response_ar and approved_response_en
  entry.
- Brand voice check.
- Proof integrity (referenced_proof_ids must be approved).
- Content integrity (referenced_content_ids must be published).
- Competitor reference accuracy (no fabricated claims).
- Bilingual integrity.

## 8. Owner

`distribution_operator` for capture; founder for approval. Auditor:
trust guardian.

## 9. Worker

The library is updated by a small worker (`scripts/dealix_objection_library_sync.py`,
planned) that ingests routed replies and proposes new objection entries
from real text — never fabricates.

## 10. KPI

- Objection Coverage (% of routed objections that hit a library
  entry).
- Response Effectiveness (operator-tagged: did the response advance
  the conversation).
- Library Hygiene (entries with citations and recent validation).

## 11. Failure mode

- Library fabricates an objection. Worker is restricted to ingest from
  real replies; any fabrication is treated as a critical bug.
- Approved response drifts into guarantee. Brand Guardian blocks; entry
  rewritten.
- Bilingual mismatch. Held until aligned.
- Stale entry (over 180 days since validation). Marked for re-check.

## 12. Recovery path

- For fabrication: worker disabled; root cause; ingestion gate
  re-tested.
- For drift: rewrite; ledger entry.
- For mismatch: copy aligned; reviewer rechecks.
- For staleness: validation cycle scheduled.

## 13. Cadence

| Cadence | Activity |
|---|---|
| Weekly | Ingest new objections from routed replies |
| Monthly | Library audit; root-cause review |
| Quarterly | Effectiveness review against pipeline outcomes |

## 14. Saudi specifics

- Many Saudi objections are politely indirect; the library captures
  both the surface phrasing and the underlying root cause.
- Bilingual responses are mandatory.
- Trust-anchored references (Saudi customer names, where consented)
  carry disproportionate weight; the library prioritises them when
  available.

## 15. Non-negotiables

- No fabricated objections.
- No guaranteed-outcome responses.
- No competitor smear.
- A3 not used.

The library is the institutional memory of the sales motion. It
compounds when every reply teaches the next response.

## 16. Worker contract

- The library worker reads `outreach/reply_routing.csv` for new
  objections and proposes additions.
- It writes only to `marketing/objection_library.csv` and a draft
  state for new entries.
- It does not generate replies; downstream draft machines consume the
  library.
- It honours the kill switch.

## 17. Audit trail

Each addition or edit to the library generates a ledger entry with
the `objection_id`, the proposing source, the founder approval state,
and the updated reviewer.

## 18. Cross-references

- `docs/growth/OUTBOUND_DRAFT_MACHINE.md` and
  `docs/growth/EMAIL_DRAFT_MACHINE.md` for outbound drafts that use
  the library.
- `docs/revenue/REPLY_ROUTING_SYSTEM.md` for objection-class routing.
