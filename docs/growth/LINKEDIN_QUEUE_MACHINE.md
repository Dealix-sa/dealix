# LinkedIn Queue Machine

The LinkedIn Queue Machine produces channel-specific draft messages for
LinkedIn — connection notes, follow-ups, and direct messages. It honours
the platform's terms, the buyer's authority shape, and Dealix's bilingual
operating reality.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Draft LinkedIn messages that read as a thoughtful, named, business
introduction — never as templated outbound spray — and queue them for
founder approval. No auto-send, no auto-connect, no scraping.

## 2. Input

Sources:

- `growth/account_scores.csv` (eligible bands only)
- `growth/personas.csv`
- `growth/icp_segments.csv`
- `growth/trigger_events.csv`
- `growth/offer_channel_fit.csv` (channel = LI)
- `outreach/suppression.csv`
- `marketing/founder_content_log.csv` (engagement-aware drafts)

Required minimum: persona authority shape, ICP, an attributed source, a
recent (within half-life) trigger or a content engagement signal.

## 3. Output

`outreach/linkedin_queue.csv` columns:

- `draft_id`
- `account_id`
- `persona_id`
- `message_type` — connection_note | dm_intro | dm_followup | comment
- `language` — ar | en | both
- `body`
- `referenced_content_id` (optional)
- `trigger_ref`
- `source_ref`
- `brand_voice_pass`
- `suppression_check`
- `guarantee_scan`
- `approval_state`
- `drafted_by`
- `drafted_at`

Message-type contracts:

- `connection_note`: 280 characters maximum, named context, no pitch.
- `dm_intro`: short, named context, one specific reason for contact.
- `dm_followup`: refers to a prior named interaction.
- `comment`: public comment on the buyer's post; intended to be relevant,
  not promotional.

## 4. Source of truth

`outreach/linkedin_queue.csv` in the private ops runtime.

## 5. Approval class

A2. Draft generation is autonomous; external action requires approval.

## 6. Trust gate

- Suppression check.
- Guarantee scan.
- Brand voice check (LinkedIn-specific tone).
- Channel-fit (offer must be sanctioned for LI per
  `OFFER_CHANNEL_FIT_SYSTEM.md`).
- Volume cap (default 10 per persona per week; override requires
  founder).
- Content-reference integrity: if `referenced_content_id` is present,
  it must point to a published, approved item.

## 7. Owner

`distribution_operator`. Allowed write target: `outreach/`.

## 8. Worker

`scripts/dealix_linkedin_queue.py` (planned). Idempotent on
`(account_id, message_type, day)`.

## 9. KPI

- LinkedIn Reply Rate (replies / approved sends), by persona.
- Connection Accept Rate (when applicable).
- Brand Voice First-Pass Rate.
- Suppression Bleed (target 0).

## 10. Failure mode

- Drafts read as templated. Brand Guardian flags.
- Auto-connect attempted. Trust Guardian halts (would be A3-shaped).
- Cap exceeded. Trust Guardian halts; cap re-enforced.
- Referenced content not approved. Draft blocked.

## 11. Recovery path

- For template drift: paused; rewrite session; resume.
- For A3-shaped behaviour: incident opened; root cause; worker locked.
- For cap breach: paused; founder approves the override or accepts the
  cap.
- For content integrity failure: content re-checked in
  `marketing/content_calendar.csv`.

## 12. Saudi-specific overlays

- Many Saudi buyers receive a large volume of LinkedIn outreach; the
  default tone is reserved. We do not lead with the company name; we
  lead with a specific, named context.
- Arabic-first drafts are not lower priority — they are essential for
  some personas; the worker uses the persona's bilingual default.
- Authority concentration: drafts to founder-CEOs use a different tone
  than drafts to corporate CROs.

## 13. Non-negotiables

- No auto-connect. No auto-send. No scraping.
- No mass templates.
- No guaranteed claims.
- A3 not used.

LinkedIn is a high-trust, easily-burned channel in Saudi B2B. The queue
is conservative on purpose.

## 15. Worker contract

- Reads inputs idempotently.
- Writes only to `outreach/linkedin_queue.csv`.
- Cannot call any LinkedIn API.
- Cannot store credentials.
- Logs every draft to the trust ledger with the source attribution.
- Honours the kill switch on the agent registry entry.

## 16. Audit trail

Every draft generates one ledger entry with `draft_id`, `account_id`,
`persona_id`, `message_type`, `language`, the brand_voice_pass status,
the suppression_check status, and the guarantee_scan status. The
ledger is append-only.

## 17. Operator notes

- Operators send approved drafts manually from the founder's own
  LinkedIn account or a named operator account; the system does not
  share or store the operator's session.
- Connection requests without notes are not used.
- Drafts that read like cold templates are rewritten until they read
  like a specific business introduction.
- Cadence pauses automatically during the buyer's stated holidays
  where known.

## 18. Cross-references

- `docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md` for the gate
  diagram.
- `docs/intelligence/OFFER_CHANNEL_FIT_SYSTEM.md` for channel caps.
- `docs/revenue/OBJECTION_LIBRARY_SYSTEM.md` for objection-aware
  drafting.
- `policies/dealix_control_policy.yaml` for the enforced rules.
