# Reply Router Machine

**Owner:** Operations + Founder
**Source of truth:** This doc + `docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md`

## Purpose

The Reply Router Machine classifies every reply across every channel (LinkedIn, email, Contact Form) and routes it to the right next action. It is the central nervous system of the Distribution War Machine — when a reply lands, everything else pauses for that persona until the router classifies it.

## Inputs

- **Incoming replies** — LinkedIn DM responses, email responses, Contact Form follow-up replies.
- **Active thread state** — what was the last Dealix touch?
- **Persona record** — current role, current contact preferences.

## Outputs

Each reply is classified into one of seven buckets:

| Bucket | Definition | Default route |
|---|---|---|
| `hot_buying_intent` | Reply asks for call, asks for proposal, names a sprint | Founder direct; meeting scheduler opens |
| `warm_curious` | Reply asks clarifying questions, requests info | Founder direct; Follow-Up #2 paused, custom reply queued |
| `referral_offer` | Reply offers to introduce to a colleague | Founder direct; intro accepted, new account created |
| `not_now_polite` | "Not now, ping me in Q3" | Nurture Machine with date |
| `remove_me` | Opt-out request | Permanent suppression list |
| `not_a_fit` | Reply explains why they are not a fit | Nurture-low or suppression; ICP feedback |
| `automated_oof` | Out-of-office or auto-reply | Reschedule the touch by N days |

Routing decisions are logged with classification confidence and operator override (if any).

## Source of truth

This doc + the reply log + the approval queue (for replies that require Founder action).

## Approval class

**A1** — Operator classification. Auto-routes for non-judgment buckets (auto-OOF, remove_me).
**A2** — Founder review for `hot_buying_intent`, `warm_curious`, and `referral_offer` routings before any send.

## Trust gate

- Replies are NEVER auto-replied to with a generated message.
- `remove_me` triggers immediate suppression and is irreversible without explicit re-opt-in from the persona.
- `hot_buying_intent` replies pause Outbound, Follow-Up, and Nurture machines for the entire account, not just the persona.
- Routing decisions over 7 days old are re-classified.

## Owner

- **Code owner:** Operations Engineering.
- **Operational owner:** Operator + Founder.

## Worker script (placeholder)

`workers/reply_router_worker.py` (planned). Runs on inbox webhook trigger. Classifies, routes, pauses adjacent machines, alerts Founder.

## KPI

| Metric | Target |
|---|---|
| Reply classification latency | <= 15 minutes |
| Hot-reply Founder-notification latency | <= 5 minutes |
| Classification accuracy (operator agrees) | >= 90 percent |
| Suppression accuracy (no touch after remove_me) | 100 percent |
| Adjacent-machine pause accuracy | 100 percent |

## Failure mode

- A `remove_me` reply is misclassified; persona receives another touch.
- A `hot_buying_intent` reply sits unrouted overnight; the conversation cools.
- Adjacent machines fire while the router is still classifying.
- Classifier mis-tags a referral as "not a fit."

## Recovery path

1. Suppression: immediately suppress; written apology to persona.
2. Hot reply: route immediately; Founder reaches out with explicit context note.
3. Re-train classifier from misclassifications weekly.
4. Re-enforce machine-pause hand-off at the queue layer.

## What this machine does NOT do

- It does not auto-reply with generated content.
- It does not aggregate reply data for any purpose other than Dealix internal routing and KPI reporting.
- It does not bypass suppression.

## Cross-links

- Distribution War Machine: `docs/growth/DISTRIBUTION_WAR_MACHINE.md`
- Follow-Up Machine: `docs/growth/FOLLOW_UP_MACHINE.md`
- Nurture Machine: `docs/growth/NURTURE_MACHINE.md`
- Approval policy: `docs/05_governance_os/APPROVAL_POLICY.md`

## Disclaimer

Dealix does not guarantee that any reply will convert to a meeting or sprint. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
