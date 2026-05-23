# Contact Form Queue Machine

## purpose
Draft messages to send via prospects' public contact forms — a
respectful, low-friction inbound surface for high-tier accounts that
have a public form.

## inputs
- `growth/account_scores.csv` (tier A only).
- The account's public contact-form URL (manually curated).
- `growth/personas.csv`.

## outputs
`distribution/contact_form_queue.csv`:
```
draft_id,account_id,form_url,name_field,email_field,
subject,message,founder_note,fallback_share,created_at,status
```

## source
- Founder-curated form URLs.
- Public-only.

## approval_class
per-form.

## trust_gate
The founder reviews the draft and submits it manually (or via a
trusted delegate). Dealix does not automate form submission.

## owner
distribution_operator (drafter) → founder (submitter).

## worker
`distribution_contact_form_worker`.

## KPI
- Forms drafted per week.
- Approval rate.
- Reply rate (logged back into the queue).

## failure_mode
- Form URL changed.
- Form has anti-bot protection (expected and respected).

## recovery_path
- Mark URL as stale; ask for refresh.

## kill_switch
`make growth-kill-contact-form`.

## audit
`audit/distribution_contact_form_runs.jsonl`.

## hard refusals
- ❌ No automated form submission.
- ❌ No CAPTCHA bypass.
- ❌ No mass submission across many accounts in a single batch.
