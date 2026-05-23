# Learning Router (Doctrine)

The Learning Router is the Learning OS's contract with the rest of the
company. It turns operational signals into decisions.

## Inputs

- DMs
- Replies
- Calls
- Proposals
- Payments
- Delivery feedback
- QA failures
- Trust escalations
- Product bugs

## Outputs

- Update message templates
- Update ICP
- Update pricing
- Update delivery playbook
- Update product roadmap
- Update trust policies

## Weekly Rule

Every week must produce at least one learning decision:

- `BUILD`
- `FIX`
- `KILL`
- `DEFER`

## Implementation

The executable implementation lives in `control_plane/learning_router.py`.
The rules are documented in `docs/control_plane/LEARNING_ROUTER.md`.
This file is the doctrine entry point — it states *why* the router exists
and what the company is required to do with its output.

## Anti-Pattern

Running the router and ignoring the output. If `BUILD` or `FIX` fires
two weeks in a row in the same area without a change being shipped, that
is itself a Founder Risk.
