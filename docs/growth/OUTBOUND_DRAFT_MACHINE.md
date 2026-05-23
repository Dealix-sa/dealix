# Outbound Draft Machine

The Outbound Draft Machine is the universal draft factory at the head of
the Distribution War Machine. It takes ranked accounts, attached personas,
and trigger context, and produces single-account, single-persona drafts
for any sanctioned channel.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Produce trust-checked, brand-checked, bilingual-aware draft messages for
the founder approval queue. The machine never sends. It writes one draft
per account at a time.

## 2. Input

Sources:

- `growth/account_scores.csv`
- `growth/icp_segments.csv`
- `growth/personas.csv`
- `growth/icp_persona_matrix.csv`
- `growth/trigger_events.csv`
- `growth/lead_source_registry.csv`
- `growth/offer_channel_fit.csv`
- `outreach/suppression.csv`
- `marketing/objection_library.csv`

Required columns from `growth/account_scores.csv`:

- `account_id`, `score`, `band`, `icp_id`, `primary_persona_id`,
  `sector_id`, `disqualifier_flag`.

Only accounts where `band in {priority, rotation}` and
`disqualifier_flag = false` are eligible.

## 3. Output

Primary file: `outreach/outreach_queue.csv` with columns:

- `draft_id`
- `account_id`
- `persona_id`
- `channel_id` — LI | EM | CF | WARM
- `language` — ar | en | both
- `subject` (channel-dependent; may be blank)
- `body`
- `trigger_ref` — references `growth/trigger_events.csv`
- `source_ref` — references `growth/lead_source_registry.csv`
- `brand_voice_pass` — true | false
- `suppression_check` — pass | fail
- `guarantee_scan` — pass | fail
- `approval_state` — drafted | queued | approved | rejected
- `drafted_by` — agent id
- `drafted_at`

## 4. Source of truth

`outreach/outreach_queue.csv` in the private ops runtime is the only
canonical store for queued outbound drafts. Worker scripts and the
Founder Console reference this file.

## 5. Approval class

A2. Drafts may be queued autonomously by the agent, but they require
explicit founder approval before any external action. Per
`policies/dealix_control_policy.yaml` rule
`approved_a2_can_request_execution`, A2 drafts cannot be acted on
externally until approved.

## 6. Trust gate

- `no_suppressed_outreach` — target identity must not be on the
  suppression list.
- `no_guaranteed_revenue_claims` — copy must not include guaranteed
  outcomes.
- Brand voice check (Brand Guardian).
- Offer-channel fit (per `OFFER_CHANNEL_FIT_SYSTEM.md`).
- Source check (must reference an allowed source).
- Bilingual default check (matches buyer's primary language).

A draft that fails any check is sent back to the rewrite loop and never
appears in the founder approval queue.

## 7. Owner

`distribution_operator` in `registries/agent_registry.yaml`. Approval
class max A2. Allowed write targets: `outreach/`.

## 8. Worker

`scripts/dealix_outbound_draft.py` (planned worker script). The worker:

1. Reads inputs.
2. Computes eligible accounts.
3. For each eligible account, produces one draft per sanctioned channel
   the operator selects.
4. Runs the trust gate checks.
5. Writes to `outreach/outreach_queue.csv`.

The worker is idempotent on `(account_id, channel_id, day)`. Re-runs do
not duplicate drafts.

## 9. KPI

Primary: Draft Approval Rate (first-pass approvals / total drafts).
Target band: 60-80 percent (depending on offer maturity).

Secondary:
- Brand Voice First-Pass Rate.
- Time-to-Queue (intelligence input -> queued draft).
- Suppression Bleed (target 0).
- Reply quality on accepted drafts (measured downstream).

## 10. Failure mode

- Drafts include guaranteed claims: Brand Guardian blocks; drafts are
  rewritten; root cause logged.
- Drafts target suppressed identities: Trust Guardian halts the worker;
  suppression check re-run.
- Channel fit ignored: drafts blocked at trust gate; offer-channel
  matrix consulted.
- Drift toward template copy: weekly brand audit raises drift flag;
  drafting paused until language refreshed.
- Volume exceeds intensity caps: Trust Guardian halts; cap honoured.

## 11. Recovery path

- For trust-gate failure: rewrite, re-run trust gate, re-queue. No
  bypass.
- For drift: paused; founder approves a rewrite session; resume.
- For source contamination: affected drafts purged; ledger entry; source
  reclassified per `LEAD_SOURCE_SYSTEM.md`.
- For policy violation: incident opened in `trust/incidents.csv` by
  `incident_response_agent`.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Daily | Draft batch (priority + rotation bands) |
| Weekly | Quality + reply review |
| Monthly | Brand voice and template audit |
| Quarterly | Worker tuning vs. outcomes |

## 13. Saudi-specific overlays

- Default to the buyer's operating language.
- Honour the buyer's authority concentration shape — drafts for
  founder-CEOs use founder-to-founder voice.
- Avoid generic "Hi {first_name}" patterns; either the personalisation
  is real or the draft is rewritten.

## 14. Non-negotiables

- No external send from this machine.
- No guaranteed claims.
- No bypass of suppression.
- No drafts without a source reference.
- A3 not used.

The draft is a hypothesis. The founder approves the hypothesis. The
operator delivers it. The reply teaches the next draft. That is the
loop.
