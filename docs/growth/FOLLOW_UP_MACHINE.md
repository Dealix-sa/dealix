# Follow-up Machine

The Follow-up Machine produces cadence drafts after a first contact —
including bumps, value-adds, and graceful exits. It enforces a maximum
number of touches per account per channel, and never sends. Drafts are
queued for founder approval.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Produce well-timed follow-up drafts that maintain context and respect the
buyer's posture. The cadence is short, considered, and bounded.

## 2. Input

Sources:

- `outreach/outreach_queue.csv` (with `approval_state = approved` and a
  recorded send timestamp).
- `outreach/email_queue.csv`, `outreach/linkedin_queue.csv`,
  `outreach/contact_form_queue.csv` (sent items).
- `outreach/reply_routing.csv` (reply state).
- `growth/personas.csv`, `growth/icp_segments.csv`,
  `growth/account_scores.csv`.
- `outreach/suppression.csv`.

A follow-up is eligible only when:

- An earlier touch was approved and recorded as sent.
- The reply router has not recorded a reply or opt-out.
- The account is not suppressed.
- The follow-up cadence step has not yet been reached for this account
  and channel.

## 3. Output

`outreach/followup_queue.csv` columns:

- `draft_id`
- `account_id`
- `persona_id`
- `channel_id` — LI | EM | CF | WARM
- `cadence_step` — 1 | 2 | 3 | exit
- `language`
- `subject` (channel-dependent)
- `body`
- `trigger_ref`
- `previous_send_id`
- `brand_voice_pass`
- `suppression_check`
- `guarantee_scan`
- `approval_state`
- `drafted_by`
- `drafted_at`

Cadence contract (default; per-offer overrides allowed):

- Step 1: 5 business days after first touch — short bump, references
  the prior message specifically.
- Step 2: 10 business days after step 1 — value-add (proof, content,
  named reference), not a chase.
- Step 3: 15 business days after step 2 — final follow-up with a
  graceful exit option.
- Exit: an explicit "happy to step back; reach out when relevant"
  message; account moves to nurture.

## 4. Source of truth

`outreach/followup_queue.csv` in the private ops runtime.

## 5. Approval class

A2. Drafting is autonomous; external send is approval-gated.

## 6. Trust gate

- Suppression list re-checked at every follow-up step.
- Guarantee scan.
- Brand voice check (follow-up tone is reserved).
- Cadence step integrity: the worker rejects drafts that would skip a
  step or send out-of-order.
- Reply check: the reply router state is consulted; replies (including
  opt-outs) suppress further follow-ups.
- Maximum-touches cap: 3 follow-ups + exit. No exceptions.

## 7. Owner

`distribution_operator`. Allowed write target: `outreach/`.

## 8. Worker

`scripts/dealix_followup_queue.py` (planned). Idempotent on
`(account_id, channel_id, cadence_step)`.

## 9. KPI

- Follow-up Reply Rate by step.
- Opt-out rate by step (target: very low, watched).
- Brand voice first-pass rate.
- Cadence integrity violations (target: 0).
- Total cadence touches per account (target: <= 4 including exit).

## 10. Failure mode

- Cadence runs past exit. Worker halts; cap enforced.
- Reply state stale; follow-up drafted after a reply. Worker halted;
  reply router re-synced.
- Brand voice drift on follow-ups. Brand Guardian rewrites pipeline.
- Suppressed identity re-engaged. Trust Guardian halts; incident
  opened.

## 11. Recovery path

- For cadence breach: worker disabled until cap honoured; ledger entry.
- For reply drift: re-sync reply router; affected drafts purged.
- For drift: paused; rewrite session.
- For suppression bleed: incident opened in `trust/incidents.csv`.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Daily | Step calculation; draft batch |
| Weekly | Step-by-step quality review |
| Monthly | Cadence calibration vs. reply outcomes |

## 13. Saudi-specific overlays

- Saudi B2B replies often arrive after the typical 5/10/15-day cadence
  — the exit message is deliberately graceful so that a late reply is
  still possible.
- Bilingual handling: follow-ups match the language used at the prior
  step unless the buyer switched.
- Tone is conservative; bumps are short and named.

## 14. Non-negotiables

- No more than 3 follow-ups + exit.
- No external send.
- No re-engaging opt-outs.
- No guaranteed claims.
- A3 not used.

The exit message is the most important part of the cadence. It is the
proof that we respect the buyer's time.

## 15. Worker contract

- Reads inputs idempotently.
- Writes only to `outreach/followup_queue.csv`.
- Cannot call any sending API.
- Cannot generate a follow-up past step 3 + exit.
- Logs every draft to the trust ledger.
- Honours the kill switch.

## 16. Audit trail

Every draft generates a ledger entry with `draft_id`, `account_id`,
`channel_id`, `cadence_step`, brand_voice_pass, suppression_check, and
guarantee_scan. The previous-send link allows a full thread audit.

## 17. Cross-references

- `docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md` for the gate
  diagram.
- `docs/growth/REPLY_ROUTER_MACHINE.md` for the reply-state interlock.
- `docs/revenue/OBJECTION_LIBRARY_SYSTEM.md` for objection-aware
  follow-ups.
