# ABM Strategic Account Machine

The ABM Strategic Account Machine handles the small set of accounts that
deserve bespoke, multi-touch, multi-persona orchestration. It plans the
account-level play, but it still terminates at approval queues for each
individual draft.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Plan and execute account-based plays on the top 20-30 named accounts at
any given time. Each play includes multiple personas, a sequence of
touches, proof artefact selection, and partner alignment.

## 2. Input

Sources:

- `growth/account_scores.csv` (priority band, with additional manual
  promotion).
- `growth/personas.csv`, `growth/icp_persona_matrix.csv`.
- `growth/trigger_events.csv`.
- `proof/proof_library.csv` — approved proof artefacts.
- `customer_success/partner_registry.csv`.
- `outreach/suppression.csv`.

An account is eligible only on explicit founder selection. ABM does not
auto-recruit accounts from the rotation band.

## 3. Output

`growth/abm_queue.csv` columns:

- `play_id`
- `account_id`
- `play_name`
- `personas` — pipe-delimited
- `touch_plan` — JSON describing channel and step sequence
- `proof_refs`
- `partner_refs`
- `language`
- `state` — drafted | active | held | won | lost | parked
- `approval_state`
- `owner`
- `started_at`
- `last_review_at`

Per-touch drafts are written to the relevant downstream queues
(`outreach/outreach_queue.csv`, `outreach/email_queue.csv`,
`outreach/linkedin_queue.csv`, `customer_success/referral_queue.csv`).
The ABM machine is the orchestrator; the individual queues are the
producers.

## 4. Source of truth

`growth/abm_queue.csv` in the private ops runtime.

## 5. Approval class

A2. Plays are drafted autonomously and reviewed by the founder; every
external touch in the touch plan is approval-gated at its own queue.

## 6. Trust gate

- Suppression checks per touch.
- Guarantee scan on every draft.
- Brand voice check.
- Proof integrity: every referenced proof must be approved.
- Partner agreement integrity: referenced partners must be active.
- Touch frequency cap: no more than 1 touch per persona per week
  without founder approval.

## 7. Owner

`growth_strategist`. Allowed write target: `growth/`. Coordinates with
`distribution_operator`, `partner_revenue_agent`, and
`proof_safety_agent`.

## 8. Worker

`scripts/dealix_abm_queue.py` (planned). The worker:

1. Reads selected accounts.
2. Builds the touch plan from persona authority, trigger context, and
   proof availability.
3. Writes draft entries to the downstream queues.
4. Tracks state in `growth/abm_queue.csv`.

## 9. KPI

- ABM Win Rate (target: significantly above non-ABM accounts).
- Time-to-First-Meeting on ABM accounts.
- Multi-Persona Coverage (target: 2+ personas engaged per play).
- Play-Lifetime Cost vs. Deal Size.

## 10. Failure mode

- Plan over-touches the same persona. Cap enforced; plan rewritten.
- Plan references unapproved proof. Worker rejects.
- Plan ignores trust risk flag. Trust Guardian halts; plan reviewed.
- Partner integration mid-play breaks. Play paused; partner re-engaged.

## 11. Recovery path

- For over-touch: cap enforced; plan trimmed.
- For proof failure: proof factory expedites the next approval; plan
  paused until ready.
- For partner pause: parallel paths considered (warm path, content
  path); never bypass partner relationship.
- For lost: post-mortem in `growth/abm_loss_log.md`.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Weekly | Play state review with founder |
| Monthly | Account promotion / demotion |
| Quarterly | Portfolio review |

## 13. Saudi-specific overlays

- Bilingual orchestration is the default; some plays run in Arabic for
  founder-CEOs and English for COOs in the same account.
- Authority concentration: plays for founder-CEOs prioritise warm path
  and founder content over volume.
- Partner alignment: many top accounts are reachable via a partner;
  the play includes partner-led options where present.

## 14. Non-negotiables

- No autonomous send.
- No play without founder selection.
- No guaranteed claims.
- A3 not used.

ABM is the highest-care channel in the system. The right metric is not
volume but specificity.

## 15. Worker contract

- Reads inputs idempotently.
- Writes only to `growth/abm_queue.csv` and downstream draft queues.
- Cannot send messages.
- Cannot exceed touch caps without approval.
- Logs every play to the trust ledger.
- Honours the kill switch.

## 16. Audit trail

Every play and each downstream touch share a `play_id`. The ledger
captures the persona coverage, the proof references, the partner
references, and the eventual won/lost/hold outcome.

## 17. Cross-references

- `docs/intelligence/ACCOUNT_SCORING_MODEL.md` for promotion criteria.
- `docs/growth/PROOF_TO_DEMAND_MACHINE.md` for proof-driven plays.
- `docs/revenue/PIPELINE_STAGE_DEFINITIONS.md` for the pipeline
  states ABM plays move through.
