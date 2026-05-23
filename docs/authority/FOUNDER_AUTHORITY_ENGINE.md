# Founder Authority Engine

> The system that lets the founder publish proof-safe, sector-relevant
> content on a regular cadence — without becoming a content factory.

## Operating principle

Authority is earned by **specific observations** about Saudi B2B
sectors that very few other people can make. It is *not* earned by
generic "AI for SMEs" takes.

## Inputs

| Source                                 | What it provides                   |
| -------------------------------------- | ---------------------------------- |
| `authority/sector_insights.csv`        | the actual observations            |
| `market_attack/objection_library.csv`  | what buyers actually push back on  |
| `campaigns/campaign_results.csv`       | what messages produce signal       |
| `partners/partner_pipeline.csv`        | ecosystem moves to call out        |

## Outputs

| Output                                                | Tracker                          |
| ----------------------------------------------------- | -------------------------------- |
| LinkedIn posts (drafted, not sent)                    | `authority/founder_posts.csv`    |
| Sector insight notes                                  | `authority/sector_insights.csv`  |
| Long-form sector report ideas                         | `authority/report_ideas.csv`     |
| Content angle backlog                                 | `authority/content_angles.csv`   |

## Cadence (planned, not forced)

- 2–3 founder posts / week, all in the beachhead sector.
- 1 sector insight / week derived from the week's data.
- 1 sector report / quarter, governance-reviewed before publishing.

## Doctrine

- Founder posts are drafted in the queue with `approval_status=pending`.
  Nothing is auto-published.
- Every post links to either an underlying insight row or a proof
  artifact. Posts that lack both are rejected by the verifier.
- No "growth-hack" posts. No "X tips" listicles unless each tip is
  backed by a Dealix-observed signal.
