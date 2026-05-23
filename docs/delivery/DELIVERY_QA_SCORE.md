# Delivery QA Score

## Purpose
Score every deliverable 0–100 before it leaves the building.

## Dimensions
| Dimension | Weight | Description |
|---|---|---|
| Data accuracy | 25 | Numbers, names, identifiers verified |
| Scope fit | 20 | Matches the proposal scope |
| Clarity | 15 | A non-expert can read and act |
| Privacy | 15 | Boundary respected; no leaked data |
| Tone | 10 | Bilingual where required; respectful |
| Formatting | 10 | Headers, alignment, file names per standard |
| Reproducibility | 5 | Can be regenerated from inputs |

## Pass threshold
QA score ≥ 75 to ship. Below 75: do not deliver; iterate.

## Where to record
`dealix-ops-private/delivery/qa_score_log.csv`:
- `date, client, deliverable, score, notes`.

## Per-deliverable QA checklist
Each client folder includes `qa_checklist.md`. Fill it in before scoring.

## Anti-bias
Score the deliverable as if you are the buyer. If you would not pay for it at the agreed price, the score is < 75 regardless of your effort.

## QA review by another person (when team grows)
- Second reviewer required for deliverables ≥ 5,000 SAR.
- Disagreements resolved by founder.
