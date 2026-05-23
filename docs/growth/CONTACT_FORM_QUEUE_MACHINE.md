# Contact Form Queue Machine

The Contact Form Queue Machine produces drafts intended for the public
contact forms of target accounts — but only where the account has invited
contact via that form, and only in low volume. This machine is the
conservative back-up channel, not a primary outbound path.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Generate a small number of high-quality contact-form drafts for accounts
where this is the sanctioned channel. The drafts are queued for founder
approval. An operator submits the form manually. No automated form
submission.

## 2. Input

Sources:

- `growth/account_scores.csv` (priority + rotation only)
- `growth/personas.csv`
- `growth/icp_segments.csv`
- `growth/offer_channel_fit.csv` (channel = CF; sanctioned offers only)
- `growth/contact_form_inventory.csv` — list of accounts that publicly
  publish a contact form intended for business inquiries

The account must appear in the contact-form inventory with an
`invited_contact = true` flag. If not, the channel is not used.

## 3. Output

`outreach/contact_form_queue.csv` columns:

- `draft_id`
- `account_id`
- `persona_id`
- `form_url`
- `language` — ar | en | both
- `name_field`, `email_field`, `subject_field`, `message_field`
- `trigger_ref`
- `source_ref`
- `brand_voice_pass`
- `guarantee_scan`
- `approval_state`
- `drafted_by`
- `drafted_at`

The form fields are pre-filled in the queue so that the human operator
can submit them in one action after approval.

## 4. Source of truth

`outreach/contact_form_queue.csv` in the private ops runtime.

## 5. Approval class

A2. Draft generation autonomous; submission requires explicit founder
approval and is performed manually by an operator.

## 6. Trust gate

- Inventory check: account must be in `contact_form_inventory.csv` with
  `invited_contact = true`.
- Suppression list check.
- Guarantee scan.
- Brand voice check.
- Volume cap: 3 contact-form drafts per offer per week.
- No automated submission attempt. The worker never POSTs the form.

## 7. Owner

`distribution_operator`. Allowed write target: `outreach/`.

## 8. Worker

`scripts/dealix_contact_form_queue.py` (planned). Idempotent on
`(account_id, form_url, day)`.

## 9. KPI

- Form Reply Rate (replies / approved submissions).
- Brand voice first-pass rate.
- Suppression bleed (target 0).
- Inventory hygiene (forms still working when reviewed).

## 10. Failure mode

- Worker attempts automated submission. Trust Guardian halts (A3-shaped).
- Account not in inventory but draft produced. Worker rejects.
- Form changes; submission fails. Operator-driven failure, not machine
  failure; inventory updated.
- Buyer complaint. Suppression list updated; account removed from
  inventory until reviewed.

## 11. Recovery path

- For automated-submission attempt: incident opened, worker disabled,
  code reviewed.
- For inventory drift: monthly inventory audit refreshes
  `contact_form_inventory.csv`.
- For complaint: account suppressed; root-cause draft review.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Weekly | Inventory check; new draft batch |
| Monthly | Inventory refresh |
| Quarterly | Channel ROI review |

## 13. Saudi-specific overlays

- Many Saudi B2B sites publish forms but route them to a generic inbox;
  the inventory captures the realistic responsiveness expectation.
- Bilingual operating reality: drafts default to the dominant operating
  language of the account.
- Avoid corporate boilerplate; lead with a specific, named reason
  (trigger or content engagement).

## 14. Non-negotiables

- No automated form submission.
- No drafts for accounts without `invited_contact = true`.
- No guaranteed claims.
- A3 not used.

This channel is a safety net for accounts where no other sanctioned
channel exists. It is not a substitute for warm paths or partner intros.

## 15. Worker contract

- Reads inputs idempotently.
- Writes only to `outreach/contact_form_queue.csv`.
- Cannot perform HTTP POST against any external endpoint.
- Cannot store credentials.
- Logs every draft to the trust ledger.
- Honours the kill switch.

## 16. Audit trail

Every draft generates one ledger entry with `draft_id`, `account_id`,
`form_url`, `language`, brand_voice_pass, and guarantee_scan. The
ledger captures both the draft and the manual submission event (when
the operator submits the form externally).

## 17. Operator notes

- Operators copy the queued fields into the live form themselves.
- Submission is logged in `outreach/contact_form_submissions.csv` with
  the operator name, timestamp, and the form's response (success /
  failure / acknowledgement message).
- If the buyer responds via a different channel after a form
  submission, the reply router links the two events.

## 18. Cross-references

- `docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md` for the gate
  diagram.
- `docs/intelligence/OFFER_CHANNEL_FIT_SYSTEM.md` for channel caps.
- `policies/dealix_control_policy.yaml` for the enforced rules.
