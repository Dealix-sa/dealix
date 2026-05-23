# Scoring Rules — Revenue Sprint

Apply on top of the candidate table from research.

## Score = ICP score + relevance adjustments
1. Base score from `docs/acquisition/ICP_SCORING_MODEL.md`.
2. **+10** if the lead matches the client's stated "good lead" definition exactly.
3. **+5** if the lead is in a city the client prioritised.
4. **−10** if the lead is in the client's exclusion list (also flag for removal).
5. **−20** if the lead is in the Dealix suppression list.
6. **Exclude** if Claim Guard flags a sector or entity that Dealix cannot serve.

## Banding for the final lead table
- **A** — score 85+. Top of the report.
- **B** — score 70–84. Recommended outreach.
- **C** — score 60–69. Optional, lower priority.
- **Drop** — score below 60. Not delivered.

## Output
- Per-lead score and reason in the table.
- A short summary in the report explaining the cut.

## Rule
A score is a number plus a one-sentence reason. Without the reason, the score is rejected at QA.
