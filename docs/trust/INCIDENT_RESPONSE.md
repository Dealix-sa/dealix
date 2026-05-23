# Incident Response

The minimum steps Dealix takes when something goes wrong.

## What counts as an incident
- Over-claim that went out to a real prospect.
- Client data exposed beyond the engagement team.
- Outbound to a suppressed contact.
- Payment or invoice error visible to the client.
- Public outage of a Dealix service.
- Any event that, if known publicly, would erode trust.

## Response (24 hours)
1. **Acknowledge** internally. Time-stamp the discovery.
2. **Contain** — stop the action causing the incident.
3. **Notify** the founder.
4. **Document** in `dealix-ops-private/trust/incident_log.csv`.

## Response (1–7 days)
5. **Investigate** — root cause, scope, affected parties.
6. **Communicate** with affected parties when the impact is material.
7. **Remediate** the underlying cause.
8. **Update** the relevant policy or playbook.

## Post-incident
- Add the lesson to `docs/learning/EXPERIMENT_LOG.md` if it changes a process.
- Add the risk to `docs/founder/RISK_REGISTER.md` if it reveals a new risk class.
- Add the decision, if any, to `docs/founder/DECISION_LOG.md`.

## Rule
An incident without documentation will be repeated. Document, then fix.
