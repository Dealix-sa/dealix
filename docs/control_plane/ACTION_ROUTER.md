# Action Router

Every action proposed by an agent, workflow, or human inside Dealix is
routed to one of five paths. The canonical implementation lives in
`control_plane/action_router.py`.

## 1. Execute Automatically
Low-risk internal action.
Examples:
- update CRM stage
- deduplicate leads
- calculate score

## 2. Draft for Review
AI prepares, founder reviews.
Examples:
- outreach message
- proposal draft
- content post

## 3. Request Explicit Approval
Cannot proceed without founder approval.
Examples:
- proposal sending
- client delivery
- pricing exception
- public case study

## 4. Escalate
High-risk or ambiguous action.
Examples:
- sensitive data issue
- legal language
- compliance claim

## 5. Block
Never allowed.
Examples:
- guaranteed revenue claim
- contract change without review
- sensitive data export
- refund approval

## Routing Order

Patterns are evaluated in this order, first match wins:

1. BLOCK
2. ESCALATE
3. APPROVE
4. DRAFT
5. EXECUTE

Unknown actions default to **ESCALATE** rather than EXECUTE. The safe
default is to ask the CEO rather than silently auto-run an untyped
action.

## Guardrail Mapping

| Path     | Logged to                  | CEO touch        |
|----------|----------------------------|------------------|
| EXECUTE  | system audit log           | none             |
| DRAFT    | drafts queue               | review optional  |
| APPROVE  | `trust/approval_log.csv`   | required         |
| ESCALATE | CEO Decision Queue         | required (with evidence) |
| BLOCK    | `trust/a3_blocked.log`     | post-hoc review  |
