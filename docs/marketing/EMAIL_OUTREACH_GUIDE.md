# Email Outreach Guide

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> Email outreach at Dealix is drafted, gated, and queued for
> approval. It is never sent autonomously. This document defines
> the system that produces email drafts and the contract that
> governs them.

Email outreach is one of the most reputation-damaging channels in
B2B when run carelessly, and one of the highest-leverage channels
when run with discipline. Dealix runs email outreach as a queue: the
Distribution Operator agent drafts, the founder approves, a human
sends. There is no exception.

## Operating Principles

- No external email send is automatic. The Distribution Operator
  queues; the founder approves; a human sends.
- No draft is queued if the target is on the suppression list.
- No draft contains guaranteed-outcome language.
- No draft references an unapproved customer or proof element.
- Daily volume is bounded by what the founder can review the same
  day. There is no "blast" mode.
- WhatsApp is allowed only for prior business relationships; cold
  WhatsApp is banned regardless of how the contact was obtained.

## Email Outreach Anatomy

A Dealix outreach email has six required elements:

1. **Subject.** 4–8 words, sober, sentence-case.
2. **Opening.** Names a specific signal observed about the buyer
   (their content, their public hire, their sector position). Not
   "I saw your LinkedIn".
3. **Value.** Names what Dealix would produce (the artefact, not the
   outcome). Typically a Diagnostic Engagement Note request.
4. **Refusal hint.** One sentence acknowledging the universal
   refusals so the buyer is not led to expect what Dealix does not
   do.
5. **Closing.** A clear next step that does not require a meeting.
6. **Signature.** Founder's name, real title, link to a working
   artefact (sector report, governance teardown), brand line.

A draft missing any element is invalid.

## Subject Line Patterns (Approved)

- "Diagnostic outcome — three named bottlenecks"
- "Sector report excerpt — Saudi B2B services"
- "Sprint scope letter (draft) for your review"
- "Quarterly trust audit — agenda inside"
- "Short question about your revenue posture"

## Subject Line Patterns (Rejected)

- "Quick question?" (vague, manipulative open pattern)
- "RE: our chat" (false-thread pattern)
- "Your CEO will love this" (manipulative)
- "5 minutes to transform your revenue" (R-COPY-002, R-COPY-007)

## Sequence Discipline

Dealix uses short sequences with a hard cap.

- First touch: cold or warmed-by-content.
- Second touch: day 3, only if no reply. Carries new evidence.
- Third touch: day 7, only if no reply. Offers a clean exit
  ("I will not follow up again unless you reply").
- No fourth touch unless the buyer has explicitly requested one.

Sequences are not branched by behavioural triggers (open / click).
Open and click signals are unreliable and PDPL-sensitive; Dealix
does not optimise on them.

## Personalisation Rules

- Personalisation must be specific. "I noticed your company is
  growing" is not personalisation; "I read your recent piece on
  Saudi B2B payment cycles" is.
- Personalisation cannot reference data the buyer has not chosen to
  share. Public sources only.
- A draft without specific personalisation is queued at lower
  priority and is more likely to be returned by the founder.

## Targeting

The Growth Strategist produces account scores. The Distribution
Operator drafts only for accounts that:

- Pass the suppression check.
- Have a relationship signal (content engagement, sector match,
  prior relationship).
- Match the founder-approved sector allow-list.
- Are not in a sector on the refusal list.

A draft for an account that fails any of these checks is denied at
the policy adapter.

## Suppression

Suppression sources:

- Inbound opt-outs (email replies, dedicated unsubscribe).
- Buyer-requested suppression.
- Founder-flagged suppression (sectors, conflicts, sensitive
  accounts).
- Sector or jurisdiction policy.

Suppression is reconciled before any draft is queued. The policy
adapter denies any draft targeting a suppressed identity
(`no_suppressed_outreach`).

## Volume and Pacing

- Daily volume per sender: bounded; founder-set. Never above what
  the founder can review the same day.
- Weekly volume: tracked by the Performance Analyst.
- Drafts are not queued faster than they can be approved; backlog
  beyond the daily cap is paused.
- Sequences pause automatically on a reply, an opt-out, a meeting
  booking, or a refusal signal.

## Reply Handling

Replies route to the founder's inbox.

- Positive reply: founder responds personally; the conversation is
  logged in the Founder Console; the next-step artefact is named.
- Negative reply: the contact is added to the suppression list with
  reason code.
- Out-of-office: sequence pauses for the duration of the OOO.
- Unsubscribe via reply: contact is added to the suppression list
  immediately.

## Email Authentication and Deliverability

- SPF, DKIM, DMARC configured on the sending domain.
- Sending domain is the Dealix domain or a clearly attributed
  domain; no spoofing.
- Bounce handling: hard bounces add to suppression; soft bounces
  retry with bounded backoff.
- Complaint handling: any spam complaint adds to suppression with
  high-severity reason code.

## PDPL Posture

- Dealix collects only the email addresses required to start a
  conversation.
- Stored email addresses are tied to the engagement they relate to.
- Retention follows the buyer's data scope agreement.
- A footer link to the Dealix PDPL posture is present in every
  email.
- An unsubscribe link is present in every email.

## Approval Markers (Email-Specific)

Each draft carries:

| Marker                 | Owner                       | States                  |
|------------------------|-----------------------------|-------------------------|
| `claims_safety`        | Brand Guardian              | PENDING, APPROVED       |
| `brand_voice`          | Brand Guardian              | PENDING, APPROVED       |
| `proof_safety`         | Proof Safety Agent          | PENDING, APPROVED, N/A  |
| `suppression_check`    | Trust Guardian              | PENDING, CLEAR          |
| `relationship_signal`  | Growth Strategist           | PENDING, PRESENT        |

A draft cannot move from `queued_for_review` to `approved` until
all five markers are in their terminal state.

## Templates (Approved Patterns)

The Distribution Operator works from approved templates, not from
freeform generation. Templates live in the private ops runtime.

- `tpl_warmed_by_content` — opens with a reference to a specific
  piece of Dealix content the buyer engaged with.
- `tpl_sector_report` — opens with a sector report excerpt and
  offers the full report.
- `tpl_referral` — opens with the referring party's name (with
  approval) and offers the Diagnostic.
- `tpl_post_diagnostic` — follow-up to a buyer who has received
  the Diagnostic and not yet responded.
- `tpl_proposal_followup` — follow-up to a buyer with a proposal in
  flight.
- `tpl_renewal` — renewal-window follow-up to a current retainer
  buyer.

Each template is versioned and reviewed quarterly.

## Failure Modes

- A draft is sent without an approval marker. Failure: process
  breach. The trust ledger records the breach; the sender is
  re-onboarded.
- A draft targets a suppressed identity. Failure: suppression
  reconciliation. The policy adapter denies the send; the breach is
  logged.
- A draft contains guaranteed-outcome wording. Failure: claims
  safety. Returned to the Distribution Operator.
- A reply is missed for more than 48 hours. Failure: response SLA
  breach. The Performance Analyst flags the lag.
- Spam complaint received. Failure: sender posture. The Trust
  Guardian raises a high-severity flag; outreach pauses for review.

## Anti-Patterns

- "Just one more touch." Sequences are capped at three; no fourth
  touch without an explicit buyer request.
- "Soft sells in the PS." The PS is not a hiding place for claims
  the rest of the email cannot make.
- "Branched sequence on open." Behavioural triggers on open and
  click are unreliable and PDPL-sensitive.
- "Lookalike audience." Dealix does not buy audiences.
- "Cold-style WhatsApp." Banned.

## Metrics That Matter

The Performance Analyst tracks:

- Drafts produced vs. approved vs. sent.
- Approval latency.
- Reply rate (positive, negative, OOO).
- Qualified conversation rate.
- Refusal rate.
- Bounce rate, complaint rate.

Metrics not optimised for: open rate, click rate.

## Cross-References

- Marketing OS: `docs/marketing/DEALIX_MARKETING_OS.md`.
- Distribution OS: `docs/product/PRODUCT_DISTRIBUTION_OS.md`.
- Copywriting rules: `docs/marketing/COPYWRITING_RULES.md`.
- Brand voice: `docs/marketing/BRAND_VOICE_EXAMPLES.md`.
- Trust contract: `policies/dealix_control_policy.yaml`.

## Why Discipline Compounds

The economic value of email outreach is destroyed by undisciplined
volume. The reputational value of email outreach is created by
disciplined cadence. Dealix runs email outreach not as a growth
hack but as a long-arc operating loop. Every queued draft, every
approval, every refusal compounds into a domain reputation and a
buyer-side perception that survives any single campaign. That is
the only kind of email outreach worth running.
