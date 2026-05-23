# Audit Policy

How Dealix periodically reviews its own behavior.

## Monthly audits
- **Outreach audit** — random sample of 20 sent messages reviewed against `MESSAGE_QUALITY_STANDARD.md` and `CLAIM_GUARD.md`.
- **Proposal audit** — every proposal sent in the month reviewed against `PROPOSAL_RULES.md`.
- **Approval log audit** — every A2 and A3 action checked for matching log entries.
- **Suppression audit** — 100% of outbound sample cross-checked against the suppression list.

## Quarterly audits
- **Data retention audit** — review of client folders for items past retention.
- **Public repo audit** — scan for sensitive content that should be private.
- **Claim audit** — random sample of public content reviewed for over-claim.

## Annual audit
- Full review of every policy in `docs/trust/`.
- External review where possible.

## Outputs
- Findings logged in `dealix-ops-private/trust/audit_log.csv`.
- Material findings escalate to `INCIDENT_RESPONSE.md`.
- Process changes logged in `DECISION_LOG.md`.

## Rule
A policy that is never audited is a policy that does not exist.
