# OpenShip adoption decision

**Status:** Pilot only  
**Date:** 2026-07-20  
**Applies to:** Dealix production, staging, disaster recovery, email and autonomous deployment tooling

## Executive decision

OpenShip is useful to Dealix as an **isolated deployment-portability and recovery pilot**. It is not approved as the production control plane, customer-data host, DNS authority or mail platform.

The immediate Dealix priorities remain:

1. restore truthful production health and remove the current Vercel false-green state;
2. keep Railway as the canonical FastAPI/backend runtime until an evidence-backed cutover is approved;
3. reconcile the public offer, pricing and claims;
4. resolve Saudi data-flow and cross-border-transfer posture before importing real customer/contact data;
5. prove the founder-first commercial loop and first paid close.

OpenShip must not displace any of those P0 items.

## Why OpenShip is strategically useful

OpenShip provides a self-hosted control plane for application deployment and operations. The pilot should test only the capabilities that reduce Dealix platform risk or create a reusable asset:

- deploy the existing Docker image from an exact Git commit;
- health-gated release verification;
- rollback to a previous commit;
- backup and restore evidence;
- isolated domain and TLS handling;
- an MCP/REST operations interface for a future approval-gated Engineering Agent;
- provider portability and a measured infrastructure-cost baseline;
- a possible Saudi-hosted deployment option after privacy and legal review.

## Why production migration is blocked

OpenShip is still early-stage and actively developed. Its documentation and roadmap identify capabilities that remain incomplete or evolving. Dealix also has unresolved production, privacy and commercial-trust blockers. Moving the production control plane now would add a second migration and a new operational dependency before the existing launch path is trusted.

Production migration remains blocked until all of the following are proven with artifacts:

- current Dealix P0 production issues are closed;
- a disposable-host pilot passes every gate in `dealix/config/openship_adoption_policy.json`;
- rollback and restore are demonstrated, not merely configured;
- security updates and vulnerability response are operationalized;
- observability, retention and audit-log requirements are documented;
- Saudi data residency and cross-border processing have an approved posture;
- a founder-approved cutover packet includes cost, recovery time, blast radius and rollback;
- a separate production-change approval is granted.

## Mail-server decision

OpenShip's mail capability is **not approved** for Dealix transactional or outreach email.

Self-hosting mail introduces deliverability, IP reputation, reverse-DNS, abuse handling, block-list monitoring, backup, anti-spam and security-patching obligations. Those obligations do not improve the current first-revenue bottleneck. Dealix should continue using an approved email provider and Gmail draft/approval workflows until a separate mail-platform decision is justified.

The pilot must not:

- provision a public mail server;
- alter MX, SPF, DKIM or DMARC records;
- send test messages to external recipients;
- import customer mailboxes;
- expose SMTP credentials.

## MCP decision

MCP is the highest-leverage OpenShip capability for Dealix, but it starts read-only.

Allowed pilot actions:

- list projects, deployments and servers;
- inspect deployment status and logs;
- retrieve health and rollback candidates;
- generate an approval packet.

Blocked without a separate approval and audit trail:

- deploy;
- rollback;
- change domains or DNS;
- change secrets;
- create or delete databases;
- create mail domains or accounts;
- mutate production.

## Architecture boundary

```text
Vercel / public frontend decision       separate P0 work
Railway / canonical backend             remains authoritative
OpenShip disposable pilot               no production traffic
Synthetic data only                     no tenant or contact data
Engineering Agent                       inspect and draft only
Founder approval                        required before mutations
Proof artifacts                         required for every gate
```

## Source of truth

Machine-enforced policy:

- `dealix/config/openship_adoption_policy.json`
- `scripts/ops/verify_openship_adoption_gate.py`
- `tests/test_openship_adoption_gate.py`

Operational procedure:

- `docs/ops/OPENSHIP_PILOT_RUNBOOK.md`

## Exit criteria

At the end of the pilot, choose exactly one outcome:

1. **Reject** — operational risk or cost exceeds benefit.
2. **Retain as DR lab** — useful for recovery rehearsal only.
3. **Retain as staging/preview control plane** — useful outside production.
4. **Prepare production cutover proposal** — only after all gates pass; still requires a separate founder approval.

No pilot result itself authorizes production migration.
