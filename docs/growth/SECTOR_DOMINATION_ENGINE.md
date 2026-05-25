# Sector Domination Engine

How Dealix builds compounding presence inside one sector at a time so that 12 months in, that sector trusts us as the default revenue operating system.

## 1. Doctrine

- **One lead sector per quarter.** No more. Focus compounds.
- **One supporting sector per quarter.** Builds optionality without splitting attention.
- **Two ignored sectors per quarter.** Documented refusals are healthy.
- **Sector lead is named.** A specific founder/operator is the sector champion that quarter.

## 2. Inputs (per sector)

| Input                 | Source                                                 |
|-----------------------|--------------------------------------------------------|
| Sector size (KSA)     | Public databases, sector associations                  |
| Top 50 accounts       | Manual mapping in `data/growth/sector_targets.csv`     |
| Buyer titles map      | `BUYER_PERSONA_SYSTEM.md`                              |
| Sector content theme  | Quarterly content calendar entry                       |
| Sector pricing band   | Hypothesis, refined every 5 deals                      |
| Sector partner short-list | 3–5 partners we'd co-deliver with                  |

## 3. Phases

### Phase 0 — Selection (Week 0)

- Pick the lead sector based on: deal size potential, founder enthusiasm, evidence of pain, and existing introductions.
- Document the choice in `data/growth/sector_targets.csv` with a `selected_at` timestamp.

### Phase 1 — Listening (Weeks 1–2)

- 10 founder-led conversations (no pitch, just listen).
- Build the sector pain hypothesis.
- Identify the 2–3 metrics every sector buyer talks about.

### Phase 2 — Sample (Weeks 3–4)

- Build 1 sector sample artefact: a sector-specific Proof Pack with anonymised data.
- Bilingual (AR + EN).
- Publish to landing page + send to the 10 conversations.

### Phase 3 — Outreach (Weeks 5–8)

- Founder-approved outreach to the top 50 accounts (with the sector sample as the lead asset).
- Daily approval queue review.
- Target: 5 booked diagnostics.

### Phase 4 — Delivery (Weeks 9–12)

- Run 5 paid Revenue Sprints.
- Document every deliverable. Capture before/after metrics.
- Build the second sector sample from the real (anonymised) data.

### Phase 5 — Compound (Quarter 2 onwards)

- Convert 3 of the 5 Sprints into Revenue Desk retainers.
- Publish a sector report. Drive demand from the report.
- Repeat with new top-50 (refreshed).

## 4. Output: per sector

```
sector_id, sector_name, status,
sector_lead, quarter_target_revenue_sar,
top_50_count, hypotheses_documented,
samples_published, conversations_held,
sprints_booked, sprints_delivered, retainers_won,
content_pieces_published, partners_engaged,
last_review_at
```

See `data/growth/sector_targets.csv` for the live tracker.

## 5. Decision gates

- Move to Phase 2 only if Phase 1 produced ≥ 7 documented conversations.
- Move to Phase 3 only if a bilingual sector sample exists and is approved.
- Continue to Phase 5 only if ≥ 3 sprints have been delivered with documented results.

## 6. Quitting a sector

It is doctrine that we **drop a sector** if:

- 12 weeks have passed and we have < 1 paid Sprint delivered.
- We cannot find a sector champion willing to spend 3 hours/week with us.
- The sector's economics do not support our offer ladder.

A documented sector quit is healthier than 12 months of half-presence.
