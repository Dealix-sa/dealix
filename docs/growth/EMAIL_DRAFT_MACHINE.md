# Email Draft Machine

The Email Draft Machine produces single-account, single-persona structured
email drafts. It does not batch-mail, it does not list-send, and it does
not connect to an email API to send. Every draft is queued for founder
approval and sent manually by an operator if approved.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Generate trust-checked email drafts for named accounts — drafts that read
as a thoughtful business introduction. The machine is the antithesis of
mass cold email tools.

## 2. Input

Sources:

- `growth/account_scores.csv` (priority + rotation bands only)
- `growth/personas.csv`
- `growth/icp_segments.csv`
- `growth/trigger_events.csv`
- `growth/offer_channel_fit.csv` (channel = EM)
- `growth/lead_source_registry.csv`
- `outreach/suppression.csv`
- `marketing/objection_library.csv`

Required: a valid, attributable source for the email; persona authority
shape; an in-half-life trigger or a content engagement signal; an offer
that is sanctioned for EM.

## 3. Output

`outreach/email_queue.csv` columns:

- `draft_id`
- `account_id`
- `persona_id`
- `email_type` — intro | followup | proof_share | meeting_request
- `language` — ar | en | both
- `subject`
- `body`
- `trigger_ref`
- `source_ref`
- `brand_voice_pass`
- `suppression_check`
- `guarantee_scan`
- `approval_state`
- `drafted_by`
- `drafted_at`

Constraints:
- Single recipient per draft. No BCC lists. No To-many. No marketing list.
- Subject line under 60 characters; no clickbait; no fake personalisation.
- Body opens with a specific, named reason for contact.

## 4. Source of truth

`outreach/email_queue.csv` in the private ops runtime.

## 5. Approval class

A2. Drafting is autonomous; external send requires explicit founder
approval per policy rule `approved_a2_can_request_execution`.

## 6. Trust gate

- Suppression list check.
- Guarantee scan.
- Brand voice check.
- Channel-fit (EM sanctioned for the offer).
- Domain reputation guard: outbound batch volume per day is capped at
  20 per persona; operator-level cap honoured.
- Single-recipient validation: drafts with multiple recipients are
  rejected.
- Source check: source must be in `LEAD_SOURCE_SYSTEM.md` allowed list.

## 7. Owner

`distribution_operator`. Allowed write target: `outreach/`.

## 8. Worker

`scripts/dealix_email_draft.py` (planned). Idempotent on
`(account_id, email_type, day)`.

## 9. KPI

- Email Reply Rate (positive + neutral replies / approved sends).
- Unsubscribe / opt-out rate (target: 0 from this machine's drafts).
- Brand voice first-pass rate.
- Suppression bleed (target 0).

## 10. Failure mode

- Draft batched accidentally. Worker rejects multi-recipient drafts.
- Domain reputation drop. Performance Analyst raises alert.
- Spam complaint. Suppression list updated; sender pattern reviewed.
- Generic copy drift. Brand Guardian rewrites; root cause logged.

## 11. Recovery path

- For domain reputation: pause; rotate sending account if necessary;
  rebuild deliverability with low-volume, high-personalisation sends.
- For complaint: suppress identity; ledger entry; review the draft path
  that generated the complaint.
- For drift: paused; rewrite session; resume.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Daily | Draft batch |
| Weekly | Deliverability and reply review |
| Monthly | Template audit |
| Quarterly | Worker tuning |

## 13. Saudi-specific overlays

- Default language is the buyer's primary operating language.
- Subject lines should be specific, not curiosity-baited. Saudi buyers
  delete generic subjects fast.
- Bilingual greetings (e.g. Arabic salutation + English body, or vice
  versa) are valid when supported by the persona's bilingual default.
- PDPL: consent and source attribution are mandatory.

## 14. Non-negotiables

- No mass send.
- No purchased list.
- No guaranteed claims.
- A3 not used.
- No scraping for emails.

The email is the most punished channel in B2B. The defence is hand-built
quality, not volume.

## 15. Worker contract

- Reads inputs idempotently.
- Writes only to `outreach/email_queue.csv`.
- Cannot call any email-sending API.
- Cannot read mailboxes.
- Cannot batch recipients.
- Logs every draft to the trust ledger.
- Honours the kill switch.

## 16. Audit trail

Every draft generates one ledger entry with `draft_id`, `account_id`,
`persona_id`, `subject`, `language`, brand_voice_pass, suppression_check,
and guarantee_scan. Replies routed against a previous send are linked
by `previous_send_id` in `outreach/reply_routing.csv`.

## 17. Operator notes

- Operators send approved drafts manually from the named operator
  inbox.
- Subject lines are reviewed once more by the operator before send.
- Drafts sent in a sequence respect the cadence cap.
- Drafts that include unattributed claims are rejected at trust gate.

## 18. Cross-references

- `docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md` for the gate
  diagram.
- `docs/intelligence/OFFER_CHANNEL_FIT_SYSTEM.md` for channel caps.
- `docs/revenue/OBJECTION_LIBRARY_SYSTEM.md` for objection-aware
  drafting.
