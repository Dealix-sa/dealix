# External Actions Policy

> أي فعل خارجي = موافقة بشرية أولًا. النظام يقترح، الإنسان ينفّذ.

Defines which actions reach the outside world and how they are gated. The
targeting OS is **read + compose only**; it performs no outbound action.

---

## Internal actions (allowed, automatic)

- Read config + master data.
- Score, map weaknesses, route offers.
- Compose drafts to `out/`.
- Create customer folders on a recorded paid outcome.
- Write retrospectives.

These are deterministic, offline, and reversible (they only write to the repo).

## External actions (human-gated, never automatic)

| Action | Gate |
|--------|------|
| Sending a message (any channel) | founder manual send |
| Charging a customer | out of scope for these scripts entirely |
| Publishing a case study / claim | customer approval (proof L3+) |
| Contacting a sensitive-sector company | governance sign-off |
| Posting to social / LinkedIn | manual, approved drafts only |

---

## Enforcement points

- Draft Lab stamps `AUTO_SEND: false` and `validate_draft()` blocks `auto_send`.
- Delivery handoff only fires on `stage == "paid"`; it creates files, charges
  nothing, sends nothing.
- No script in this OS opens a network socket.

See [OUTREACH_APPROVAL_POLICY.md](OUTREACH_APPROVAL_POLICY.md) and
[NO_SPAM_POLICY.md](NO_SPAM_POLICY.md).
