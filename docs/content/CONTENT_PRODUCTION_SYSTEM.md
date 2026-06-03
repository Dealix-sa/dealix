# Content Production System

## Purpose
A repeatable pipeline from idea → draft → review → publish → track.

## Stages
1. **Idea** — captured in `content/content_ideas.md`.
2. **Draft** — written into the calendar with status `Draft`.
3. **Review** — claim scan + founder review.
4. **Approved** — status `Approved` in `content/content_calendar.csv`.
5. **Published** — moved to `Published`; row added to `content/published_log.csv`.
6. **Influence** — leads / proposals influenced by the asset logged in `content/content_pipeline_influence.csv`.

## Cadence targets
- Weekly: 1–2 founder posts (LinkedIn).
- Monthly: 1 case study (anonymized or named).
- Quarterly: 1 sector report.

## Approval gate
A post in status `Draft` cannot move to `Approved` until:
- `scripts/review_content_claims.py` runs clean.
- The proof level requirements are satisfied.
- The founder has read the final version.

## Channels
See `LINKEDIN_SYSTEM.md` for LinkedIn-specific guidance.
Newsletter, X, blog posts use the same pipeline with channel-appropriate length.

## Forbidden
- Auto-publishing posts.
- Scheduling content that hasn't gone through review.
- Republishing other authors' content without permission and attribution.

## Templates
- Founder post: `dealix-ops-private/content/templates/founder_post.md`.
- Case study: `dealix-ops-private/content/templates/case_study_outline.md`.
