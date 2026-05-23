# Revenue Sprint — Final Report Template

> The deliverable handed to client on Day 7.
> Every section must pass `claim_guard.py` before send.

## Cover

- **Client:** {client_name}
- **Sprint:** Revenue Sprint
- **Period:** {kickoff_date} → {handoff_date}
- **Report version:** v1 (working)
- **Prepared by:** Dealix
- **Trust posture:** every external claim has a citation; no auto-sent messages during this Sprint

---

## 1. What We Did

A one-page narrative of the Sprint's actual work, day-by-day:
- Day 1: scope locked + sector setup
- Day 2–3: prospect sourcing + scoring
- Day 4: message drafts
- Day 5: objection responses + evidence pack
- Day 6: QA
- Day 7: handoff

Include hours spent, sources used, decisions made.

---

## 2. Scored Prospect List (50 rows)

Brief intro paragraph explaining:
- How fit was scored (`ICP_SCORING_MODEL.md` reference)
- What enrichment was used (sources cited)
- What was excluded (suppression / disqualifiers)

Then attached as:
- `prospects.csv` (working file)
- `prospects.pdf` (read-only friendly)

Each row includes: company, sector, buyer name + role, fit score breakdown, trigger signal, recommended channel.

---

## 3. Outreach Message Variants

Three variants per language (AR + EN):

```
Variant 1 — {framing label}
[Arabic text]

[English text]

Personalization slots: {trigger_signal}, {sector_pain}
Approval tier: A1 — client to approve each send personally
```

Include guidance on:
- Which variant to use for which segment
- How to fill personalization slots
- What to avoid (banned language list)

---

## 4. Objection Responses

Top 3 objections × 2 framings each:

```
Objection: "{verbatim}"
Framing 1 (acknowledge + reframe):
  [Arabic]
  [English]
Framing 2 (data + ask):
  [Arabic]
  [English]
```

---

## 5. Evidence Pack

- **Sources used** — full list with URLs + access dates
- **Methodology** — how we scored, how we enriched
- **Sanitization notes** — what we cleaned, why
- **Exclusions** — what we left out, why
- **Approval log** — every founder approval timestamp during the Sprint

This section is the trust artifact. Treat it as the second-most-important section after the prospect list.

---

## 6. What This Report Does NOT Promise

- A specific number of replies / meetings
- ROI / revenue figures
- That the messages will work without iteration
- That sending will produce results without client effort

---

## 7. Recommended Next Steps

- Top 3 prospects to outreach this week (with the recommended variant)
- Recommended sending cadence (per `OUTREACH_CADENCE.md`)
- Suggested follow-up window (default 7 days)
- Optional next rung: Data Pack or Managed Ops (with rung descriptions, not a hard sell)

---

## 8. Handoff Notes

- What's complete: _____
- What's outstanding (if anything): _____
- Where to find each file: _____
- Who to contact for questions: founder@dealix.sa

---

## 9. Trust Statement

> All claims in this report are sourced. All sample data is either synthetic or publicly cited. No third-party data was used without consent. Every external-facing artifact was passed through Dealix's claim_guard before delivery. The client's data captured during this Sprint is stored in Dealix's private workspace and is not shared, sold, or reused.

## Approval Trail

- Founder review: {date}
- claim_guard.py pass: {date} + commit hash
- Final approval: {date}

## Storage

- Final PDF + working files in `clients/{client}/deliverables/` (private)
- Sanitized version (if client consents for case study) saved later as `content/proof_library/sector/{sector}/case-study-{client_pseudonym}-v1.md`

## What This Template Refuses

- Vanity numbers
- Stock photos / fake screenshots
- Claims beyond what evidence supports
- "Customized" sections that bypass claim_guard
