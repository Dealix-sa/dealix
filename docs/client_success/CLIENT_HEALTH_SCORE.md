# Client Health Score

> A 100-point rubric, updated monthly per active retainer.

## Components (each 0–20)

### 1. Engagement (0–20)
- Did the client read the weekly report? (binary signal: replies, comments)
- Did they attend the monthly review?
- Did they action our suggestions?

### 2. Outcome (0–20)
- Did our outreach produce replies?
- Did replies convert to calls?
- Did calls convert to opportunities (in their CRM)?

### 3. Sentiment (0–20)
- Did they express positive feedback in writing?
- Did they introduce us to peers?
- Have they referenced us publicly (with consent)?

### 4. Expansion Signal (0–20)
- Did they ask for more accounts / segments?
- Did they ask for additional services?
- Have they raised pricing without our prompting?

### 5. Continuity (0–20)
- Did they renew on time?
- Did they pay on time?
- Are they on auto-renew?

## Tiering

| Score | Tier | Action |
|-------|------|--------|
| 80–100 | A — Compounding | Upsell candidate; case study candidate |
| 60–79 | B — Healthy | Maintain |
| 40–59 | C — At-risk | Intervention plan within 7 days |
| 0–39 | D — Critical | Founder personal intervention this week |

## Update Cadence

- Each retainer scored monthly.
- Scoring happens within 7 days of the monthly review.
- Tracker: `dealix-ops-private/client_success/health_scores.csv`.

## Anti-Patterns

- Scoring based on vibes ("I think they like us").
- Scoring high because they paid on time and nothing else.
- Skipping the score because "no time".

## Use in CEO Review

- Number of A / B / C / D retainers reported in `BOARD_PACK_TEMPLATE.md`.
- Trend: are we improving or degrading?
