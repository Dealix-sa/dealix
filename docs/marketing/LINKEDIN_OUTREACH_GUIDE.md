# LinkedIn Outreach Guide

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> LinkedIn outreach at Dealix is drafted by the Distribution
> Operator, approved by the founder, and executed manually. It is
> never automated.

LinkedIn is a high-trust, low-volume channel for Dealix. The
platform rewards specificity and punishes spray-and-pray automation.
This guide describes how Dealix produces LinkedIn outreach that
fits the platform's grain and the buyer's tolerance.

## Operating Principles

- No external LinkedIn action is automatic. The Distribution
  Operator drafts; the founder approves; a human (founder or
  delegated operator) sends or posts.
- No LinkedIn automation tool is used for connection requests,
  messages, or post engagement. The platform's terms of service
  prohibit it; the trust contract reinforces the prohibition.
- No connection request is sent without a clear relationship
  signal (content engagement, sector match, prior relationship).
- No message contains guaranteed-outcome language or unapproved
  proof.
- Daily volume is bounded; never more than the founder can review
  the same day.

## Channels Within LinkedIn

LinkedIn outreach has three sub-channels at Dealix:

- **Founder-led posts.** Five per week, Sunday through Thursday.
  See `FOUNDER_LED_CONTENT_SYSTEM.md`.
- **Direct messages.** Drafted by the Distribution Operator, queued
  for approval, sent manually by the founder or named operator.
- **Engagement on others' posts.** Comments on relevant posts.
  Founder-driven; drafts may be prepared but the founder posts.

InMail, paid Sales Navigator messaging, and any automation tool are
not in use.

## Connection Request Discipline

Connection requests are not drafted in bulk. They are queued one at
a time with:

- A relationship signal (specific reference to the target's recent
  activity).
- A short note (one sentence, no pitch).
- A trust ledger entry on send.

A connection request without a relationship signal is denied at the
policy adapter (rule pattern analogous to `no_suppressed_outreach`).

## Direct Message Anatomy

A Dealix LinkedIn DM has five required elements:

1. **Opening signal.** A specific reference to a post, an article,
   or a mutual context. Not "I noticed you work in B2B".
2. **One-sentence value.** What Dealix would produce if the buyer
   was interested — almost always the Diagnostic.
3. **Refusal hint.** A short acknowledgement of the universal
   refusals.
4. **Clean exit.** A statement that Dealix will not follow up more
   than once on LinkedIn.
5. **Next step.** A pointer to a working artefact (sector report,
   governance teardown) and an offer to schedule a Diagnostic if
   relevant.

A draft missing any element is invalid.

## Approved Patterns

**First-touch DM (warmed by post engagement):**

> Hi [name],
>
> I read your recent post on [specific topic] — your point on
> [specific point] matches what we see in the field at Dealix.
>
> We publish a sector report on [topic]; happy to send the
> excerpt if useful. We do not run sequences on LinkedIn; if this
> is not the right time, no follow-up.
>
> [founder signature]

**Referral-warmed DM:**

> Hi [name],
>
> [referrer], who introduced us in passing last week, suggested I
> reach out. Dealix runs a free, evidence-only Diagnostic for
> Saudi B2B founders. We do not promise pipeline; we produce a
> brief and a scorecard within seven business days.
>
> If you would like the Diagnostic, reply with a time. We do not
> follow up more than once.
>
> [founder signature]

## Rejected Patterns

- "Quick question — got 5 minutes?" (vague, manipulative open)
- "I see you're in revenue ops, here's how we 10x pipelines"
  (R-COPY-001, R-COPY-002, R-COPY-007)
- "Connecting because we both know [name]" (when "knowing" is a
  weak signal)
- "Loved your post! Check out my [link]" (false-rapport pattern)
- Any DM that opens with a screenshot of unredacted data.

## Post Engagement (Comments)

Comments on others' posts are part of the founder voice and follow
the same rules.

- Comments are substantive. One-line "great post!" comments are
  not in the Dealix voice.
- Comments add evidence or a refusal-aware reframe. They do not
  pitch.
- Comments do not link out to a Dealix landing page unless the
  thread invites it.
- The founder owns comment posting. The Content Strategist may
  prepare draft comments for the founder to review, but never
  posts on the founder's behalf.

## Volume and Pacing

- Connection requests: bounded daily cap; founder-set.
- Direct messages: bounded daily cap; founder-set.
- Posts: 4–5 per week, Sunday through Thursday.
- Comments: 5–15 per week across the founder's network.
- Sales Navigator: read-only use; no messaging from Sales Navigator.

The daily cap is a soft ceiling; the hard ceiling is "what the
founder can review and personally send the same day."

## Suppression and Refusal

Suppression on LinkedIn comes from:

- Targets who have declined a previous Dealix outreach.
- Targets in sectors on the refusal list.
- Founder-flagged accounts.
- Mutual-connection suppression — if a target is connected to a
  known sensitive party, the founder is consulted before outreach.

A draft targeting a suppressed identity is denied at the policy
adapter.

## PDPL and LinkedIn Data

- Dealix does not scrape LinkedIn. Data used for targeting is
  drawn from manual research or from the buyer-shared context.
- Dealix does not import LinkedIn connections into the CRM
  automatically. Imports require founder approval.
- Dealix does not store LinkedIn profile data outside what is
  necessary for the engagement.

## Approval Markers (LinkedIn DM-Specific)

| Marker                 | Owner                       | States                  |
|------------------------|-----------------------------|-------------------------|
| `claims_safety`        | Brand Guardian              | PENDING, APPROVED       |
| `brand_voice`          | Brand Guardian              | PENDING, APPROVED       |
| `proof_safety`         | Proof Safety Agent          | PENDING, APPROVED, N/A  |
| `suppression_check`    | Trust Guardian              | PENDING, CLEAR          |
| `relationship_signal`  | Growth Strategist           | PENDING, PRESENT        |
| `platform_tos`         | Trust Guardian              | PENDING, CLEAR          |

The `platform_tos` marker confirms the action complies with
LinkedIn terms of service. Automation tooling is automatically
flagged here.

## Failure Modes

- A DM sent without approval markers. Failure: process breach.
  Trust ledger records; sender re-onboarded.
- An automation tool engaged. Failure: platform ToS breach. The
  tool is removed; trust ledger records; outreach pauses for
  review.
- Connection request without relationship signal. Failure: policy
  adapter denies the request; founder is notified.
- Aggressive follow-up loop. Failure: the second touch was sent
  before the first response window expired. Sender re-onboarded.

## Anti-Patterns

- "Mass-add connections." Banned.
- "Engagement pods." Banned.
- "Drip sequence on LinkedIn." Banned.
- "Buy followers." Banned.
- "Repost others without attribution." Banned.

## Metrics That Matter

The Performance Analyst tracks:

- Connection requests sent / accepted.
- DMs sent / replied.
- Qualified conversations from LinkedIn.
- Refusal rate.
- Post engagement quality (not raw count — quality scored by
  comment substance).

Metrics not optimised for: connection count, post reach, profile
views.

## Cross-References

- Marketing OS: `docs/marketing/DEALIX_MARKETING_OS.md`.
- Distribution OS: `docs/product/PRODUCT_DISTRIBUTION_OS.md`.
- Founder-led content: `docs/marketing/FOUNDER_LED_CONTENT_SYSTEM.md`.
- Copywriting rules: `docs/marketing/COPYWRITING_RULES.md`.
- Brand voice: `docs/marketing/BRAND_VOICE_EXAMPLES.md`.

## Localisation

DMs in Arabic and English follow the same rules. The founder
chooses the language based on the target's primary language of
content and conversation. Mixed-language DMs are avoided; a clean
single-language DM reads better than a "translated" one.

## Why Manual

LinkedIn rewards the cadence and texture that only a human
sender can produce. Automation produces volume; humans produce
trust. Dealix runs LinkedIn for trust. The discipline is harder to
scale than automation, but it does not destroy the founder's
reputation or the buyer's tolerance. Both are the only assets that
matter at scale.

The Dealix LinkedIn presence is meant to look like a serious
operator's network, not a marketing automation account. The rules
above are how Dealix keeps it that way.
