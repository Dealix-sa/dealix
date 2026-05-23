# Nurture Machine

**Owner:** Operations + Founder
**Source of truth:** This doc + `docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md`

## Purpose

The Nurture Machine maintains long-cycle relationships with personas and accounts that are not actively in an outreach thread but remain ICP-fit. It distributes Proof Pack excerpts, sector signals, and personal updates on a measured cadence to keep Dealix present without becoming noise.

It is the patient layer of the Distribution War Machine.

## Inputs

- **Accounts in Nurture state** — accounts moved here by the Follow-Up Machine (5-touch cycle ended with no reply), the Reply Router (`not_now_polite`), or operator decision (Tier B account, no trigger yet).
- **Published Proof Packs** — anonymized and signed-off content from the Proof to Demand Machine.
- **Published sector content** — from the Content to Demand Engine.
- **Persona contact-preference record** — preferred channel, preferred cadence, preferred language.

## Outputs

- **Personalized nurture touch** — typically a short message referencing a relevant piece of Dealix content, sent through the persona's preferred channel.
- **Nurture-to-reactivation signal** when a nurtured persona engages with content or replies positively.

## Default cadence

| Nurture level | Touch frequency | Channel |
|---|---|---|
| Active | 1 touch per 30 days | Persona-preferred (typically LinkedIn DM) |
| Slow | 1 touch per 90 days | Email warm (if opted in) |
| Low | 1 touch per 180 days | Email warm with explicit opt-out reminder |
| Suppressed | None | N/A |

Cadence escalates only on observed engagement (reply, content interaction). Cadence de-escalates on non-engagement after 3 cycles.

## Source of truth

This doc + the nurture queue + persona contact-preference record.

## Approval class

**A2** — Founder + Operator per touch. Nurture touches are not exempt from approval, but their template-driven nature usually allows quick approval.

## Trust gate

- No nurture touch to a suppressed persona.
- No nurture touch to a persona whose role no longer matches the ICP (re-verify monthly).
- No nurture broadcast without per-batch Founder approval.
- All nurture touches carry an explicit "if I'm off-base, no reply is fine" line.
- All bilingual nurture touches are parallel (per `DEALIX_BRAND_VOICE.md`).

## Owner

- **Code owner:** Operations Engineering.
- **Operational owner:** Operator + Founder.

## Worker script (placeholder)

`workers/nurture_worker.py` (planned). Runs daily; identifies due nurture touches; assembles draft from content and persona context; enqueues.

## KPI

| Metric | Target |
|---|---|
| Nurture cadence completion | >= 90 percent |
| Nurture-to-reactivation rate | observed |
| Nurture suppression accuracy | 100 percent |
| Engagement decay (post-3-cycle no-engagement → de-escalation) | 100 percent |

## Failure mode

- Nurture cadence loses personalization; reads as a newsletter.
- A nurtured persona is also in active Outbound — orchestration collision (see `AUTONOMOUS_DISTRIBUTION_MACHINES.md` Rule 4).
- Nurture continues past 3 non-engagement cycles without de-escalation.
- A suppressed persona receives a nurture touch.

## Recovery path

1. Re-personalize the cadence; pause until drafts pass voice checklist.
2. Move account out of Outbound during Nurture cycle.
3. Enforce de-escalation at the queue layer.
4. Audit suppression list integrity.

## What this machine does NOT do

- It does not blast newsletters.
- It does not enroll personas without consent for opt-in broadcasts.
- It does not auto-send.
- It does not generate Proof content; it distributes already-approved content.

## Cross-links

- Distribution War Machine: `docs/growth/DISTRIBUTION_WAR_MACHINE.md`
- Reply Router: `docs/growth/REPLY_ROUTER_MACHINE.md`
- Proof to Demand: `docs/growth/PROOF_TO_DEMAND_MACHINE.md`
- Content to Demand Engine: `docs/growth/CONTENT_TO_DEMAND_ENGINE.md`

## Disclaimer

Dealix does not guarantee that any nurture touch will reactivate an account. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
