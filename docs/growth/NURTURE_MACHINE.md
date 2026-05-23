# Nurture Machine

The Nurture Machine produces draft messages for accounts that are
not-yet-ready — accounts that politely declined now, accounts that have
not engaged in active rotation, and accounts that engaged with content
but have not entered the outbound flow. It runs on a slow, content-led
cadence and never sends.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Maintain considered presence with accounts that are not in active
rotation, so that when they become ready, Dealix is the named choice.

## 2. Input

Sources:

- `growth/account_scores.csv` (warm band: 40-59).
- `outreach/reply_routing.csv` (`classification = unsure | non_buyer`
  and `routing_decision = nurture`).
- `marketing/content_calendar.csv` (approved content).
- `marketing/engagement_log.csv`.
- `outreach/suppression.csv`.

The account must not be suppressed. It must have an attributed source.

## 3. Output

`marketing/nurture_queue.csv` columns:

- `draft_id`
- `account_id`
- `persona_id`
- `nurture_step` — content_share | check_in | proof_share | re_score
- `language`
- `body`
- `referenced_content_id`
- `brand_voice_pass`
- `guarantee_scan`
- `approval_state`
- `drafted_by`
- `drafted_at`

Step contract:

- `content_share`: low-frequency share of relevant Dealix content.
- `check_in`: 90-day check-in, brief and named.
- `proof_share`: when a fresh approved proof artefact is relevant.
- `re_score`: triggers re-scoring of the account (not a message).

## 4. Source of truth

`marketing/nurture_queue.csv` in the private ops runtime.

## 5. Approval class

A2. Drafts are autonomous; external send is approval-gated.

## 6. Trust gate

- Suppression check.
- Guarantee scan.
- Brand voice check (nurture tone is reserved and content-led).
- Frequency cap: maximum 4 nurture touches per account per year, plus
  optional content shares only when content is freshly approved.
- Content integrity: `referenced_content_id` must point to an approved,
  published item.

## 7. Owner

`content_strategist`. Allowed write target: `marketing/`.

## 8. Worker

`scripts/dealix_nurture_queue.py` (planned). Idempotent on
`(account_id, nurture_step, quarter)`.

## 9. KPI

- Nurture-to-Rotation Rate (accounts moving from warm to rotation).
- Engagement Lift on shared content.
- Brand voice first-pass rate.
- Opt-out rate (target: very low).

## 10. Failure mode

- Nurture turns into outbound chase. Brand Guardian rewrites; cadence
  reset.
- Account replies but reply not routed back. Reply router state
  re-synced.
- Frequency cap breached. Worker halts; cap enforced.

## 11. Recovery path

- For chase drift: paused; rewrite session; resume.
- For cap breach: incident opened; worker locked until cap honoured.
- For reply drift: re-sync reply router.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Monthly | Nurture batch (per quarter step) |
| Quarterly | Re-score accounts; promote/demote |

## 13. Saudi-specific overlays

- Nurture works particularly well in Saudi B2B due to long memory and
  relationship density; a one-line "still happy to help when relevant"
  every 90-180 days compounds.
- Bilingual handling honoured.
- Content shares default to recent founder content with named context.

## 14. Non-negotiables

- No outbound chase disguised as nurture.
- No external send.
- No guaranteed claims.
- A3 not used.

The nurture queue is the long memory of the war machine. Treat it
gently.

## 15. Worker contract

- Reads inputs idempotently.
- Writes only to `marketing/nurture_queue.csv`.
- Cannot send messages.
- Cannot exceed the 4-touch-per-year cap without an explicit founder
  override.
- Logs every draft to the trust ledger.
- Honours the kill switch.

## 16. Audit trail

Every nurture draft generates a ledger entry with `draft_id`,
`account_id`, `nurture_step`, brand_voice_pass, and guarantee_scan.

## 17. Cross-references

- `docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md` for the gate
  diagram.
- `docs/growth/CONTENT_TO_DEMAND_ENGINE.md` for the source of
  approved content used in nurture.
- `docs/proof/PROOF_APPROVAL_OS.md` for any proof referenced.

## 18. Operator notes

- Nurture sends are spaced; the operator does not batch.
- Nurture replies that show new interest are escalated immediately to
  the Reply Router classifications path.
- Annual review of the nurture pool removes accounts that have not
  re-engaged.

## 19. Saudi-specific extra

- Major Saudi events (Hajj, national days, Ramadan) shift the nurture
  cadence; the worker reads the holiday calendar and pauses
  appropriately.
- Bilingual content shares default to the buyer's primary operating
  language.
