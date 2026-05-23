# Follow-Up Machine

**Owner:** Operations + Founder
**Source of truth:** This doc + `docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md` + `docs/growth/FOLLOW_UP_CADENCE.md`

## Purpose

The Follow-Up Machine schedules and drafts follow-up touches for any active outreach thread that has not yet produced a definitive reply. It enforces cadence discipline — no operator overruns the per-persona touch cap, and no operator forgets a follow-up that the cadence calls for.

It is the operational memory of the Distribution War Machine.

## Inputs

- **Open outreach threads** from the LinkedIn Queue Machine, Email Draft Machine, and Contact Form Queue Machine.
- **Reply Router state** — has a reply been received and classified?
- **Active cadence definition** — see `docs/growth/FOLLOW_UP_CADENCE.md`.
- **Per-persona touch cap state** — last touch date.

## Outputs

- **Scheduled follow-up reminder** per open thread.
- **Drafted follow-up message** queued for Founder approval (A2).
- **Thread closure signal** when the cadence ends with no reply (moves account to Nurture Machine).

## Cadence (default)

| Touch # | Days after prior touch | Tone | Channel |
|---|---|---|---|
| 1 (initial) | T+0 | First-touch draft | Per offer-channel matrix |
| 2 | T+5 | Soft reminder; add one new specific signal | Same channel |
| 3 | T+10 | Different angle, different format (e.g., resource share) | Same channel |
| 4 | T+18 | Last touch; explicit "if I'm off-base, no reply is fine" | Same channel |
| Move to Nurture | T+25 | If no reply by T+25, thread closes; account enters Nurture | N/A |

This cadence is overridable per sector but never extended beyond 5 follow-ups in one cycle. Five-and-out.

## Source of truth

This doc + `docs/growth/FOLLOW_UP_CADENCE.md` + the follow-up queue.

## Approval class

**A2** — Founder + Operator per follow-up draft.

## Trust gate

- No follow-up if the persona has explicitly replied "not now" or "remove me" — those move to permanent suppression or Nurture-low.
- No follow-up if the persona has changed roles (Buyer Access re-verification).
- No follow-up that uses guilt, urgency manufacture, or social-pressure tactics.
- All follow-ups pass the voice checklist.

## Owner

- **Code owner:** Operations Engineering.
- **Operational owner:** Operator + Founder.

## Worker script (placeholder)

`workers/follow_up_worker.py` (planned). Runs daily; identifies threads due for follow-up; calls the drafter; enqueues.

## KPI

| Metric | Target |
|---|---|
| Follow-up completion rate (cadence executed on time) | >= 90 percent |
| Reply lift from follow-up #2 vs #1 | observed |
| Move-to-Nurture rate | observed |
| Suppression accuracy (no follow-up after "remove me") | 100 percent |

## Failure mode

- Follow-up sent after explicit removal request.
- Follow-up uses urgency-manufacturing language.
- Cadence skips touches; thread dies.
- Cadence overruns 5 touches.

## Recovery path

1. Immediate suppression for any account where post-removal touch was sent; written apology.
2. Re-train operator on cadence language.
3. Re-anchor cadence in the queue UI.
4. Hard-cap the 5-touch rule at the queue level.

## What this machine does NOT do

- It does not auto-send follow-ups.
- It does not write follow-ups that manufacture urgency.
- It does not bypass suppression lists.
- It does not continue past 5 touches.

## Cross-links

- Cadence definitions: `docs/growth/FOLLOW_UP_CADENCE.md`
- Nurture Machine: `docs/growth/NURTURE_MACHINE.md`
- Reply Router: `docs/growth/REPLY_ROUTER_MACHINE.md`
- Approval policy: `docs/05_governance_os/APPROVAL_POLICY.md`

## Disclaimer

Dealix does not guarantee that any follow-up will produce a reply. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
