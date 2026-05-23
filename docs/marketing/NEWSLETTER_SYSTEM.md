# Newsletter System

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> The Dealix newsletter is a weekly evidence drumbeat. It is not a
> mailing list. It is the most consistent way the Marketing OS
> exposes operating reality to the world.

The Dealix newsletter — provisionally titled "Saudi Revenue Notes"
or "GCC AI and Revenue Ops Notes" — is published weekly and gated by
the same trust contract that governs every other Marketing OS
component. This document defines how the newsletter is produced,
gated, and distributed.

## Operating Principles

- One issue per week. Missed weeks are acknowledged, not
  back-filled.
- Every issue carries at least one piece of new evidence from the
  evidence loop, one governance teardown, and one decision option
  the reader can take.
- No issue promises revenue, sales, or meetings.
- No issue publishes an unapproved customer reference.
- No issue is sent without the founder's recorded approval and a
  trust ledger entry.

## Issue Anatomy

A standard issue has six sections, each short and refusable.

1. **Opening pattern.** A two-paragraph pattern observation from
   the operating week.
2. **Governance teardown.** A specific governance decision (a new
   refusal marker, a policy rule update, an eval gate change) and
   why it happened.
3. **Evidence point.** An anonymised data point from the evidence
   loop, with method and caveat.
4. **Sector note.** A short note on a sector Dealix is active in,
   without naming buyers.
5. **Refusal of the week.** A specific request Dealix declined,
   anonymised, and why.
6. **Decision option.** One thing the reader could try on their
   own next week, framed as a decision option rather than a tactic.

A footer carries the brand line, the universal refusals, the
unsubscribe link, and the PDPL posture link.

## Cadence

- Weekly, on a fixed day (default: Wednesday).
- Length: 600–1,200 words.
- Bilingual: separate Arabic and English editions, sent the same
  day, peer-quality.
- Holidays and Ramadan: cadence is honoured but tone is adjusted;
  no off-cycle "make-up" issues.

## Drafting Workflow

1. Content Strategist drafts the issue from the week's operating
   notes (sales calls, governance changes, evidence points,
   refusals).
2. Brand Guardian eval (claims-safety, brand-voice).
3. Trust Guardian eval (refusal-list visibility, governance teardown
   accuracy).
4. Proof Safety Agent eval (anonymisation check on the evidence
   point and sector note).
5. Founder review and approval.
6. Issue queued for send.
7. Issue sent manually through the contracted email provider with
   the SPF/DKIM/DMARC posture in place.
8. Trust ledger entry recorded with issue id and version.

## Subscriber List

- Subscribers opt in through the Dealix landing page or sector
  report download.
- Double-opt-in is on by default for PDPL posture.
- Subscriber list is stored in the private ops runtime, not in this
  repository.
- Subscriber list is not shared with partners, exported to third
  parties, or used for any purpose outside the newsletter without
  founder approval and a recorded escalation.

## Unsubscribe and Suppression

- Every issue carries an unsubscribe link.
- Unsubscribe writes to the suppression list immediately.
- A subscriber who unsubscribes from the newsletter is not
  automatically removed from other Dealix communications they have
  opted into; the suppression is per channel unless the subscriber
  requests global suppression.

## Approval Markers (Newsletter-Specific)

| Marker                | Owner                                  | States                |
|-----------------------|----------------------------------------|-----------------------|
| `claims_safety`       | Brand Guardian                         | PENDING, APPROVED     |
| `brand_voice`         | Brand Guardian                         | PENDING, APPROVED     |
| `proof_safety`        | Proof Safety Agent                     | PENDING, APPROVED, N/A|
| `bilingual_parity`    | Content Strategist + founder review    | PENDING, APPROVED     |
| `founder_approval`    | Founder                                | PENDING, APPROVED     |

A subset of markers may be `N/A` for a given issue (e.g. no proof
references means `proof_safety` is `N/A`). Each `N/A` is recorded
with a rationale.

## Voice Calibration

The newsletter voice is the same as the founder voice elsewhere:
sober, specific, refusal-aware, evidence-bearing. Avoid:

- "5 ways to" headings.
- "Top X this week" listicles.
- Vendor reviews disguised as recommendations.
- Self-congratulatory metrics ("we hit X subscribers!").

Prefer:

- Specific pattern observations.
- Named governance decisions.
- Honest gaps and caveats.

## Failure Modes

- Issue sent with a guaranteed-outcome phrase. Failure: claims
  safety. Issue retracted via a follow-up note in the next issue;
  trust ledger records the retraction.
- Issue sent with an identifiable buyer reference. Failure: proof
  safety. Issue retracted; trust ledger records the retraction.
- Missed week. Failure mode: acknowledged in the next issue
  ("we did not send last week — here is why and here is what is
  in this week's issue").
- Subscriber list shared without approval. Failure: PDPL breach.
  Trust ledger records; Security Guardian opens an incident.

## Anti-Patterns

- "Newsletter sponsored by a third party." Dealix does not sell
  newsletter sponsorship in a way that compromises voice.
- "Newsletter as a sales channel." The newsletter offers decision
  options; it does not pitch.
- "Reused content from social." Newsletter content is composed for
  the newsletter even when it shares the underlying pattern with a
  social post.
- "Hidden unsubscribe link." The unsubscribe link is visible in
  every issue.

## Metrics That Matter

The Performance Analyst tracks:

- Subscribers (net of suppressions).
- Reply rate (newsletter replies are a strong signal).
- Qualified conversations sourced from the newsletter.
- Refusal rate (subscribers declined for follow-up).
- Unsubscribe rate (watched, not chased).

Metrics not optimised for: open rate (unreliable), click rate
(unreliable), forwards (unreliable).

## Renewal of Format

The newsletter format is reviewed quarterly. A format change
requires:

- A written rationale.
- Brand Guardian approval.
- Founder approval.
- A subscriber-facing note explaining the change.

Format change without these steps is not allowed.

## Localisation

Arabic and English editions are sent the same day, peer-quality.
Arabic is not a translation; Arabic is a co-authored edition. The
Content Strategist allocates time to both languages in the weekly
drafting block.

## Storage

- Issues are stored in the private ops runtime under
  `marketing/newsletter/issues/`.
- Subscriber list is stored under `marketing/newsletter/subscribers/`
  (suppression list reconciled).
- Trust ledger entries are stored per the standard ledger schema.
- Nothing about subscribers is stored in this repository.

## Cross-References

- Marketing OS: `docs/marketing/DEALIX_MARKETING_OS.md`.
- Content calendar: `docs/marketing/CONTENT_CALENDAR_SYSTEM.md`.
- Brand voice: `docs/marketing/BRAND_VOICE_EXAMPLES.md`.
- Copywriting rules: `docs/marketing/COPYWRITING_RULES.md`.
- Trust contract: `policies/dealix_control_policy.yaml`.

## Why a Newsletter

A weekly newsletter has three properties that almost no other
channel has:

- Subscribers opt in. The audience is consented.
- Cadence builds memory. A reader who receives 12 issues across a
  quarter remembers Dealix in a way no single post can produce.
- The format invites depth. A 1,000-word issue can carry the kind
  of governance and evidence pattern that does not survive a social
  post.

The newsletter is the most patient compounding the Marketing OS
runs. Done weekly for a year, it is one of the most important
trust signals Dealix produces.
