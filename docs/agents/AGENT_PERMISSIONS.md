# Agent Permissions

## Principle

Agents follow least-privilege. Read access is scoped to what the agent
needs for its job; write access is restricted to the agent's own ledger
or queue, never to client-facing artifacts.

## Permission Table

| Agent | Read | Write | External Send |
|---|---|---|---|
| Founder Brief Agent | metrics, ledgers, pipeline | `docs/founder/DAILY_COMMAND_BRIEF.md` draft section | No |
| Lead Finder Agent | public sources, ICP rubric | leads queue | No |
| Scoring Agent | leads queue, ICP rubric | score field on leads | No |
| Message Agent | leads queue, offer ladder | draft queue | No (A1/A2 gates) |
| Proposal Agent | call notes, proposal template | draft proposal in queue | No (A2 gate) |
| Trust Guard Agent | any drafted artifact in queue | risk flags on artifacts | No |
| Learning Agent | logs, metrics, ledgers | recommendation queue | No |
| Delivery QA Agent | deliverable + checklist | QA report on deliverable | No |

## Hard Denies

No agent may:
- Write to `docs/founder/DECISION_LOG.md` directly.
- Write to client-facing artifacts after Trust Guard approval.
- Read from secrets, credentials, or private keys.
- Make outbound network calls outside the allow-list.
- Read raw client data without the engagement having data consent recorded.

## Network Allow-List

Network destinations an agent may reach are explicitly listed per agent
in `dealix/agents/<agent>/network_allowlist.yml` (file managed by the
engineering sub-agent). Anything not on the list is blocked.

## Auditing

Every read and write made by an agent is logged per `AGENT_LOGGING.md`.
