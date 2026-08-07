# Revenue Command Room Artifact Spec

## Goal

Create a reviewable design artifact for the Dealix Revenue Command Room.

## Primary user

Founder, sales operator, or Dealix operator.

## Required sections

1. Today's revenue focus
2. Target accounts
3. Follow-up queue
4. Proposal queue
5. Approval cards
6. Trust and outbound status
7. Next 10 actions
8. Risks and blockers

## Required states

```text
draft
prepared_not_sent
needs_approval
approved
blocked
verified
```

## Required safety indicators

- live sends disabled or enabled status
- opt-out status for email drafts
- WhatsApp opt-in/template status
- LinkedIn manual-only status
- source verification status

## Output recommendation

Start as markdown in `reports/design/revenue-command-room-v0.md`, then promote to an `apps/web` demo route only after review.
