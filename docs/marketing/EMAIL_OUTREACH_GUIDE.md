# Email Outreach Guide

Dealix email outreach is considered, named, and approved. Bulk send sequences are not a Dealix channel. Every email is one human writing to another human, gated by the founder.

**Source of truth:** `$PRIVATE_OPS/email_outreach_log.csv`
**Owner:** Founder + Revenue Lead
**Trust gate:** A2 — every email to a non-customer is approved by the founder before send.

## What's allowed

- A direct email to a named individual with a specific reason.
- An email replying to an inbound or a warm introduction.
- A scheduled follow-up to a previously consenting contact.

## What's not allowed

- Scraped contact lists.
- Bulk send sequences without explicit recipient consent.
- Templates with variable insertion sent as one-to-many.
- Purchased or rented lists.
- Re-targeting an unsubscribed contact.

These are blocked by `policies/dealix_control_policy.yaml`.

## Anatomy of a Dealix outreach email

| Section | Length |
|---------|--------|
| Subject (concrete, no clickbait) | 6-10 words |
| Opening (named, with a specific reason) | 1 sentence |
| Context (why we're reaching out, evidence-forward) | 2-3 sentences |
| Offer (one named action) | 1 sentence |
| Disclosure | 1 line |
| Signature (founder or named Revenue Lead) | 2 lines |

Bilingual when the recipient is a Saudi business reader: AR top, EN below, or per recipient preference if known.

## Subject discipline

- No "RE:" when there is no prior thread.
- No "[Urgent]" or "[Important]" unless materially true.
- No emojis.
- One concrete noun in the subject.

Examples on-brand: "Sector pattern for Riyadh industrial suppliers" — "30-minute diagnostic — your team's invoice cycle time" — "Following up on your sector report download".

## Send process

1. Revenue Lead drafts the email in the email-draft template.
2. Brand Guardian lints (`docs/ai/BRAND_GUARDIAN_AGENT.md`).
3. Founder reviews and approves at A2.
4. Email is sent from a named human account.
5. Send event logged in `email_outreach_log.csv`.

The system never sends on the founder's behalf. The founder either sends, or instructs a named human to send under their watch.

## Unsubscribe

Every email carries an unsubscribe path appropriate to the channel. Honoured immediately. Contact moves to `$PRIVATE_OPS/suppression_list.csv` and is removed from any planned follow-up.

## Failure modes

- **Bulk-send attempt:** a draft expands to many recipients. Detection: policy engine. Recovery: blocked at send time; root cause filed.
- **Unsubscribe bypass:** a suppressed contact is included. Detection: pre-send check. Recovery: contact removed; audit row.
- **Template guarantee:** an outreach draft contains a guarantee phrase. Detection: lint. Recovery: rewrite, re-approve.

## Recovery path

If outreach data becomes unreliable, the founder freezes outbound until the suppression list and the log are reconciled.

## Metrics

- Emails sent per week.
- Reply rate (estimated).
- Qualified conversation rate (estimated).
- Suppression honour rate (target: 100%).

## Disclaimer

Outreach is a respectful, consent-aware activity. Dealix does not guarantee replies, conversations, or revenue. Estimated value is not Verified value.
