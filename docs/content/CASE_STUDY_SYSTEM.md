# Case Study System

## Purpose
Convert a successful engagement into a reusable proof artifact.

## Inputs (per case study)
- Source: `clients/<slug>/delivery_report.md` and `clients/<slug>/feedback.md`.
- Proof approval: `clients/<slug>/proof_approval.md`.
- Trust workflow row in `trust/claim_review_log.csv`.

## Structure
1. **Client** — name (if approved) or anonymized descriptor.
2. **Problem** — the specific challenge.
3. **Approach** — what Dealix did.
4. **Outcome** — quantified results with cited sources.
5. **Method** — bulleted steps that can be applied elsewhere.
6. **Quote** — optional, with explicit consent.
7. **CTA**.

## Variants
- Anonymized version: published on LinkedIn, website, sales decks.
- Named version: shown to specific prospects with similar profiles, requires written approval to publish further.

## Length
- 1 page (PDF) for sales.
- ~500 words for LinkedIn.
- ~1,200 words for blog.

## Proof discipline
- Every number cited from a delivery artifact path.
- No "industry average" comparisons without source.

## Tracking
- Calendar row in `content/content_calendar.csv` with `proof_level=Named case` or `Anonymized case`.
- Influence rows in `content/content_pipeline_influence.csv`.

## Decay
- Refresh every 18 months or when the client moves on.
- Retire if the underlying engagement type is discontinued.
