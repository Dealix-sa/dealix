# Content-to-Demand Engine

The Content-to-Demand Engine plans, drafts, and tracks content that
generates demand. It is the slowest-moving part of the war machine, but
the highest-leverage long term. It sends nothing externally.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Plan and draft Dealix-owned content (founder posts, articles,
newsletters, sector briefs, proof-derived pieces) that earns attention
from the target ICPs and converts engagement into inbound interest.

## 2. Input

Sources:

- `growth/sector_targets.csv`, `growth/icp_segments.csv`,
  `growth/personas.csv`.
- `marketing/content_calendar.csv` (existing schedule).
- `marketing/content_ideas.csv` (idea inbox).
- `proof/proof_library.csv` (approved proof for content derivation).
- `marketing/engagement_log.csv` (signal from previous content).
- `marketing/objection_library.csv` (content addressing real
  objections).

## 3. Output

Two queues:

- `marketing/content_calendar.csv` — scheduled content with planned
  publication dates.
- `marketing/content_demand_queue.csv` — content-to-account mapping;
  for each piece of approved content, which accounts and personas it
  is intended to land with.

`marketing/content_calendar.csv` columns:

- `content_id`
- `title`
- `format` — post | article | newsletter | brief | thread
- `persona_targets` — pipe-delimited
- `sector_targets` — pipe-delimited
- `language`
- `proof_refs`
- `objection_refs`
- `state` — drafted | approved | published | archived
- `approval_state`
- `drafted_by`
- `planned_publish_at`

`marketing/content_demand_queue.csv` columns:

- `entry_id`
- `content_id`
- `account_id`
- `persona_id`
- `expected_signal` — read | engage | book_call | share
- `language`
- `notes`

## 4. Source of truth

`marketing/content_calendar.csv` for content; `engagement_log.csv` for
observed engagement.

## 5. Approval class

A2. Drafts require founder approval before publication. Publication is
performed by a named operator manually.

## 6. Trust gate

- Brand voice check.
- Guarantee scan (no guaranteed revenue claims in any content).
- Proof integrity (every referenced proof is approved and current).
- Bilingual check (the content's stated language matches its actual
  language).
- Source attribution: any claim that references a market source
  carries the citation.

## 7. Owner

`content_strategist`. Allowed write target: `marketing/`.

## 8. Worker

`scripts/dealix_content_to_demand.py` (planned). The worker:

1. Reads the content calendar.
2. Drafts the planned pieces.
3. Maps each approved piece to the accounts and personas most likely to
   value it.
4. Writes to `marketing/content_calendar.csv` and
   `marketing/content_demand_queue.csv`.

## 9. KPI

- Engagement Rate per piece (by persona).
- Inbound Interest per piece (book-a-call, content reply, share).
- Time-to-Approval.
- Brand voice first-pass rate.
- Bilingual coverage (target: balanced over a quarter).

## 10. Failure mode

- Content drift to generic SaaS thinkpiece. Brand Guardian rewrites.
- Content references unapproved proof. Worker rejects.
- Content includes a guaranteed-outcome line. Trust Guardian halts;
  rewrite.
- Calendar slippage (publish-date pile-up). Founder triages.

## 11. Recovery path

- For drift: paused; rewrite session; resume.
- For proof failure: proof safety agent expedites or content uses a
  redacted form.
- For guarantee scan failure: rewrite; ledger entry; root cause review.
- For slippage: priorities reset; cadence reset.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Weekly | 2-3 pieces drafted; 1-2 published |
| Monthly | Engagement review; backlog grooming |
| Quarterly | Calendar reset against sector priorities |

## 13. Saudi-specific overlays

- Bilingual cadence: each quarter, at least half of the calendar pieces
  default to Arabic primary or bilingual.
- Sector-specific content: pieces written for ranked-active sectors
  outperform generic.
- Founder voice: the founder's own posts are the strongest content; the
  worker prepares drafts in that voice but the founder retains final
  edit and publication.

## 14. Non-negotiables

- No external publication without founder approval.
- No guaranteed claims.
- No fabricated quotes or fabricated metrics.
- No proof reference that is not approved.
- A3 not used.

The point of content is patient compounding of trust. The engine plans
that compounding so it does not depend on bursts.
