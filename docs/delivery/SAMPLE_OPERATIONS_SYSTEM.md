# Sample Operations System

## Purpose
A sample is a small, focused proof artifact given to a qualified prospect to demonstrate capability without committing to delivery.

## Sample types
1. **Sector mini-report** — 1 page, 1 actionable insight specific to the prospect's sector.
2. **Lead table preview** — 10 hand-curated leads relevant to the prospect.
3. **Operating diagnostic** — a 1-page assessment of a public-facing problem.

## Constraints
- 60–120 minutes of effort. Max 180 minutes.
- No real customer data of others used in the sample.
- Anonymized examples only.
- Outputs land in `dealix-ops-private/delivery/samples/<prospect_slug>/`.

## Tracking
Log each sample in `delivery/sample_quality_log.csv`:
- `date, prospect, sector, sample_path, quality_score, status, next_action`.
- `quality_score` is the founder's 0–100 score: 60+ to deliver, 75+ to publish (with approval).

## Sample-to-proposal funnel
- If a sample is delivered and the prospect engages → propose the 499 SAR sprint.
- If the prospect responds with technical questions → propose the 1,500 SAR data pack.
- If the prospect asks "how do we make this ongoing?" → propose the 2,999+ SAR retainer.

## Privacy
- No real PII in the sample text. Use role + sector ("a clinic in Riyadh") instead of names.
- Do not include leaked competitor data even if available.

## When NOT to send a sample
- Lead is below 50 on the qualification score.
- Sample would require revealing real customer data.
- Sample is being requested as a free pilot in disguise.
