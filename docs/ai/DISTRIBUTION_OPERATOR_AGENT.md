# Distribution Operator Agent

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> The Distribution Operator drafts outreach and queues it for
> approval across email, LinkedIn, and contact forms. It does not
> send. The founder approves; humans execute.

## Agent Contract

| Field                       | Value                                                                  |
|-----------------------------|------------------------------------------------------------------------|
| `id`                        | `distribution_operator`                                                |
| `name`                      | Distribution Operator                                                  |
| `purpose`                   | Draft outreach and queue approvals across email/LinkedIn/forms.        |
| `approval_class_max`        | A2                                                                     |
| `tools`                     | `outreach_drafter`, `suppression_check`, `brand_voice_check`, `relationship_signal_check`, `platform_tos_check` |
| `outputs`                   | `outreach/outreach_queue.csv`, `outreach/linkedin_queue.csv`, `outreach/contact_form_queue.csv`, `outreach/followup_queue.csv` |
| `external_action_allowed`   | false                                                                  |
| `kill_switch`               | true                                                                   |
| `eval_required`             | true                                                                   |
| `audit_required`            | true                                                                   |
| `owner`                     | founder                                                                |
| `allowed_write_targets`     | `outreach/`                                                            |
| `KPI`                       | Approval rate, reply rate on approved sends, refusal rate, queue latency |
| `failure_mode`              | Drafts containing guaranteed-outcome language; drafts targeting suppressed identities; over-personalisation that crosses PDPL boundaries |

## Purpose

The Distribution Operator is the agent responsible for producing
the queue of outreach drafts across the channels Dealix uses. It
operates strictly at A2: draft and queue. It does not send. It
does not branch sequences on behavioural triggers. It does not run
the channel; it produces the artefacts the founder reviews.

## Responsibilities

- Draft email, LinkedIn, and contact-form outreach using approved
  templates and the Growth Strategist's recommendations.
- Reconcile each draft against the suppression list before queueing.
- Run brand voice, claims safety, and platform ToS checks on each
  draft.
- Maintain follow-up queues bounded by Dealix sequence caps
  (max three touches per account per channel).
- Pause queued sequences when a reply, opt-out, meeting booking, or
  refusal signal is detected.

## Tools

- `outreach_drafter` — template-driven draft generation.
- `suppression_check` — cross-references the suppression list.
- `brand_voice_check` — invokes the Brand Guardian's evals.
- `relationship_signal_check` — verifies the target has a defensible
  relationship signal.
- `platform_tos_check` — verifies the action complies with the
  target platform's terms of service (LinkedIn especially).

The agent cannot invoke any tool that sends, posts, or transmits to
a third party.

## Outputs

- `outreach/outreach_queue.csv` — email drafts pending review.
- `outreach/linkedin_queue.csv` — LinkedIn DM and connection
  request drafts pending review.
- `outreach/contact_form_queue.csv` — contact-form drafts pending
  review.
- `outreach/followup_queue.csv` — scheduled follow-ups pending
  review at their target date.

Each row carries the draft body, the markers (claims, brand voice,
proof safety, suppression, relationship signal, platform ToS), and
the approval state.

## External Action

Always `false`. The agent does not execute sends. Sends are
performed manually by the founder or by a named operator with
explicit delegation in the Founder Console.

## Kill Switch

Anyone with operator role can pause. Reasons to pause:

- The suppression list integration is suspect.
- A guaranteed-outcome phrase has slipped into a draft.
- The relationship signal logic is producing weak signals.
- The platform ToS posture has changed.

## Eval Requirements

The Distribution Operator's eval suite covers:

- Claims-safety scan on every draft.
- Brand-voice scan on every draft.
- Suppression cross-check.
- Relationship signal validation.
- Platform ToS check.
- Sequence cap enforcement (no draft exceeds the three-touch cap).
- PDPL posture (no field beyond the approved data scope is
  referenced).

A failed eval prevents the draft from moving to
`queued_for_review`.

## Audit Requirements

Every draft, every approval decision, and every send (after
manual execution) writes an audit entry. Entries include:

- `draft_id`
- `channel`
- `target_id`
- `markers`
- `approval_state`
- `human_action`
- `time_to_approval`
- `time_to_send`

## Owner

Founder.

## Allowed Write Targets

`outreach/` only.

## KPI

- Approval rate: drafts approved over drafts produced. Target ≥
  0.70; persistent low rate indicates calibration drift.
- Reply rate on approved sends: reply count over approved sends.
  Watched, not chased.
- Refusal rate: drafts declined for claims, suppression, scope, or
  signal reasons. A target band; too low indicates the agent is
  drafting too narrowly, too high indicates over-production.
- Queue latency: time from draft to founder review. A founder-set
  service level.

## Failure Modes

- A draft contains guaranteed-outcome language. Mitigation: the
  claims-safety eval blocks the draft; the agent is recalibrated
  if the pattern recurs.
- A draft targets a suppressed identity. Mitigation: the policy
  adapter denies the draft at queue time; the suppression list
  integration is audited.
- A draft over-personalises by referencing data outside the
  approved data scope. Mitigation: the PDPL posture check is a
  blocking eval; data scope is mirrored into the agent's prompt.
- A draft exceeds the sequence cap. Mitigation: the cap is enforced
  at queue time; sequences that hit the cap are closed with a clean
  exit note.

## Cross-Agent Dependencies

- Reads recommendations from the Growth Strategist.
- Calls the Brand Guardian and the Trust Guardian for eval
  responses.
- Writes queues consumed by the founder and the Performance
  Analyst.
- Refusals here feed the Trust Guardian's review.

## Operating Cadence

- Daily: produces drafts up to the bounded daily cap; queues for
  review.
- Weekly: produces a sequence health summary appended to
  `outreach/outreach_queue.csv`.
- Monthly: template review with the Content Strategist.
- Quarterly: registry review.

## Banned Behaviours

- Sending, posting, or transmitting externally.
- Branching sequences on open/click triggers.
- Using third-party automation tools on LinkedIn or any platform.
- Drafting cold WhatsApp messages.
- Writing outside `outreach/`.
- Bypassing the suppression check.

## Failure Response

If a draft is sent without approval (process breach by a human):

1. The audit ledger logs the breach with the human actor's id.
2. The Trust Guardian opens a high-severity flag.
3. The Distribution Operator's queue is paused for review.
4. The send process is re-onboarded.

If the suppression integration fails:

1. All draft queues are paused.
2. The Trust Guardian opens a critical-severity flag.
3. The Security Guardian and the founder are notified.
4. The integration is repaired and a full re-reconciliation is
   performed.

## Why an Agent, Not a Sequencer

Sequencers automate sends. The Distribution Operator queues drafts
behind a hard human-approval gate. The distinction is not
cosmetic. It is the difference between a system that scales volume
and a system that scales discipline. Dealix scales discipline.

## Cross-References

- Distribution OS: `docs/product/PRODUCT_DISTRIBUTION_OS.md`.
- Email outreach guide: `docs/marketing/EMAIL_OUTREACH_GUIDE.md`.
- LinkedIn outreach guide: `docs/marketing/LINKEDIN_OUTREACH_GUIDE.md`.
- Agent registry: `registries/agent_registry.yaml`.
- Trust contract: `policies/dealix_control_policy.yaml`.
