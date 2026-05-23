# Community and Ecosystem Engine

The Community and Ecosystem Engine plans and tracks Dealix presence in
the communities and ecosystems where Saudi B2B buyers spend time —
sector groups, founder communities, professional associations, and
operator networks. It does not send.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Build considered, sustained presence in communities where buyers
gather, so that Dealix is named when relevant. Plan the activities;
draft the contributions; queue for approval.

## 2. Input

Sources:

- `marketing/community_registry.csv` — registry of communities (name,
  type, sector, language, our membership posture).
- `marketing/community_activity_log.csv` — observed activity within
  sanctioned communities.
- `growth/sector_targets.csv`, `growth/personas.csv`.
- `proof/proof_library.csv` (for contributions that reference proof).
- `outreach/suppression.csv`.

A community is sanctioned only if:

- It has a clear charter and code of conduct.
- Dealix has joined under named participation (not anonymous).
- Membership is consistent with the community's rules.
- Activity does not violate the community's promotional rules.

## 3. Output

`marketing/community_queue.csv` columns:

- `entry_id`
- `community_id`
- `activity_type` — answer | post | event_attend | introduction
- `persona_focus` — pipe-delimited personas this activity is intended
  to serve
- `language`
- `draft_body` (where applicable)
- `referenced_content_id` (optional)
- `referenced_proof_id` (optional)
- `brand_voice_pass`
- `guarantee_scan`
- `approval_state`
- `drafted_by`
- `drafted_at`

## 4. Source of truth

`marketing/community_queue.csv` in the private ops runtime.

## 5. Approval class

A2. Drafts are produced autonomously; community contributions are
approved by the founder before posting and posted manually by a named
operator.

## 6. Trust gate

- Community-rule compliance: drafts must follow the community's posted
  rules (no self-promotion in restricted threads, etc.).
- Suppression check (where the activity targets a named individual).
- Guarantee scan.
- Brand voice check.
- Proof integrity (every referenced proof is approved).
- Anti-spam check: cadence cap per community is enforced.

## 7. Owner

`content_strategist`. Allowed write target: `marketing/`. Coordinates
with `partner_revenue_agent` for partner-led communities.

## 8. Worker

`scripts/dealix_community_engine.py` (planned). Idempotent on
`(community_id, activity_type, day)`.

## 9. KPI

- Community Engagement Quality (operator-rated relevance, peer
  acknowledgement).
- Inbound Interest (book-a-call, named DM that references the
  community contribution).
- Brand voice first-pass rate.
- Community rule violations (target: 0).

## 10. Failure mode

- Contribution reads as promotion. Brand Guardian rewrites; cadence
  reset.
- Community rule violation. Trust Guardian halts; ledger entry;
  community-membership review.
- Cadence overrun (too many contributions per community per week).
  Cap enforced.
- Proof reference confidentiality breach. Critical incident opened.

## 11. Recovery path

- For promotion drift: rewrite session; resume.
- For community rule violation: apology issued (manually, by named
  operator), participation paused; review with the community moderator.
- For cap breach: paused; cap honoured; ledger entry.
- For confidentiality breach: incident opened in `trust/incidents.csv`.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Weekly | New contribution drafts (1-2 per active community) |
| Monthly | Community engagement review |
| Quarterly | Community membership posture review |

## 13. Saudi-specific overlays

- Saudi founder and operator communities respond strongly to specific
  named contribution and weakly to generic promotion.
- Bilingual contributions; Arabic-primary often outperforms in local
  founder communities.
- Sector-specific moderators are influential; the engine prioritises
  building moderator relationships, not posting volume.

## 14. Non-negotiables

- No anonymous participation.
- No promotional drift in restricted threads.
- No guaranteed claims.
- A3 not used.

The community engine compounds slowly. Burned communities do not
recover. Restraint is the dominant feature.

## 15. Worker contract

- Reads inputs idempotently.
- Writes only to `marketing/community_queue.csv`.
- Cannot post or comment.
- Cannot bypass community-rule checks.
- Logs every draft to the trust ledger.
- Honours the kill switch.

## 16. Audit trail

Every draft generates a ledger entry with `entry_id`, `community_id`,
`activity_type`, `language`, brand_voice_pass, and guarantee_scan.
Community-rule violations open a separate incident.

## 17. Cross-references

- `docs/growth/CONTENT_TO_DEMAND_ENGINE.md` for the content
  pipeline that supplies many community contributions.
- `docs/growth/EVENTS_AND_PARTNERSHIP_ENGINE.md` for partner-led
  communities.
