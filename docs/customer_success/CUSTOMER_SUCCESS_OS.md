# Customer Success OS

The Customer Success OS is the operating layer that holds the client relationship between delivery cycles. It is distinct from Delivery (which produces work) and from Retention (which secures renewal).

**Source of truth:** `$PRIVATE_OPS/customer_success_state.csv`
**Owner:** Customer Success Lead
**Trust gate:** A1 — all external communications follow the Reply Routing System (`docs/revenue/REPLY_ROUTING_SYSTEM.md`).

## Charter

Customer Success is responsible for:

1. Maintaining a current view of each client's objective, status, and Health Score.
2. Surfacing risks before they become churn signals.
3. Coordinating across Delivery, Revenue, and Finance on the client's behalf.
4. Capturing learning into the Capital Ledger (`docs/09_capital_os/CAPITAL_LEDGER.md`).

Customer Success does not own pricing, scope, or contract decisions.

## Client view

Each client carries a row in `customer_success_state.csv` with:

- Client identifier and primary contact role.
- Current engagement and stage.
- Health Score and trend.
- Last touch date and channel.
- Next scheduled touch and owner.
- Open risks with severity.
- Open opportunities with stage.

## Cadence

| Cadence | Activity | Output |
|---------|----------|--------|
| Daily | Inbox triage | Routed replies |
| Weekly | Health Score read | Updated state |
| Bi-weekly | Working session | Session notes |
| Monthly | Executive review | Founder digest |
| Quarterly | Strategic review | Renewal posture |

## Working sessions

Working sessions are short, structured meetings with the client's operational owner. The agenda is fixed:

1. Status of in-flight deliverables.
2. Health Score read and any change.
3. Risks and mitigations.
4. New requests (logged, not committed).
5. Next steps with owners and dates.

Notes are written in EN with an AR summary, stored in `$PRIVATE_OPS/clients/<client_id>/sessions/`.

## Risk register

Risks carry a severity (low / medium / high) and an owner. High-severity risks open within 24 hours of detection and escalate to the founder. The register is reviewed weekly.

## Failure modes

- **Silent client:** no inbound from a client for 14 days. Detection: nightly job. Recovery: CS Lead reaches out; if no response in 7 more days, founder escalates.
- **Cross-team handoff drop:** a client request reaches CS but is never assigned. Detection: weekly audit. Recovery: assign, apologise, log root cause.
- **Health Score divergence:** Health Score signals are positive but client signals are negative. Detection: working-session notes vs Health Score. Recovery: Health Score weights re-tuned (`docs/customer_success/CLIENT_HEALTH_SCORE_SYSTEM.md`).

## Recovery path

If Customer Success data is corrupted or lost, the founder triggers a manual reach-out to every active client within 5 business days to re-establish state.

## Metrics

- Active clients with current Health Score (target: 100%).
- Median days between client touches.
- High-severity risks open at month end.
- Capital Ledger entries per active client per month.

## Disclaimer

Customer Success is a relationship and risk function, not a guarantee of outcome. Estimated value is not Verified value.
