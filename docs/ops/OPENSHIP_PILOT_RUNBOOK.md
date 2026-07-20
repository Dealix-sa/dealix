# OpenShip isolated pilot runbook

This runbook tests OpenShip as a deployment-portability and recovery tool for Dealix. It does not authorize production use.

## Hard boundaries

- Use a disposable VPS or isolated local host.
- Use synthetic data and the public repository only.
- Do not connect production Postgres, Redis, MongoDB, Gmail, WhatsApp, payments or customer systems.
- Do not copy production environment-variable values.
- Do not point `dealix.me`, `api.dealix.me`, email DNS or any customer domain at the pilot.
- Do not enable OpenShip mail.
- Do not permit an MCP client to mutate infrastructure during the first pass.
- Destroy or quarantine the host after evidence collection.

## Recommended host

Minimum evaluation host:

- Ubuntu 24.04 LTS;
- 4 vCPU;
- 8 GB RAM;
- at least 50 GB encrypted storage;
- dedicated public IP;
- firewall default deny;
- SSH keys only;
- a throwaway subdomain, for example `openship-lab.example.invalid` until a real isolated test domain is approved.

The host must not share credentials, volumes or networks with Dealix production.

## Phase 0 — repository gate

From the Dealix repository:

```bash
python scripts/ops/verify_openship_adoption_gate.py
pytest -q -o addopts='' tests/test_openship_adoption_gate.py
```

Expected result: every required guard is `PASS` and the decision is `pilot_only`.

## Phase 1 — host preparation

Record without secrets:

- provider and region;
- instance type;
- monthly list price;
- operating-system image;
- public IP fingerprint or redacted identifier;
- creation timestamp;
- responsible owner;
- destruction date.

Apply:

- security updates;
- firewall rules;
- SSH hardening;
- disk encryption where the provider supports it;
- automatic security-patch policy;
- system clock synchronization;
- log rotation.

Do not paste shell history, environment dumps or secret values into issues or reports.

## Phase 2 — install OpenShip

Use the official current-release installation path and pin the evaluated release where the installer supports it. Record:

- OpenShip version;
- installer checksum or release reference;
- installation start/end timestamps;
- listening ports;
- service status;
- failed units or warnings.

Do not expose the dashboard or API to the public internet without authentication and a network allowlist.

## Phase 3 — deploy Dealix from an exact commit

Deploy only the existing production Docker contract:

- source repository: `Dealix-sa/dealix`;
- exact commit SHA, never a floating branch for the proof run;
- Dockerfile build;
- runtime command from Dockerfile `/app/start.sh`;
- health path `/healthz`;
- synthetic, generated secrets unique to the lab;
- isolated empty databases or mocked dependencies.

Do not use `docker-compose.yml` as the pilot production definition. That file is explicitly a local-development stack and contains development defaults and host port mappings.

Required evidence:

- commit SHA shown by the deployment;
- build result;
- container image identifier;
- non-root runtime user;
- health response status and timestamp;
- no secret values in logs.

## Phase 4 — health and failure behavior

Verify:

1. `/healthz` reaches HTTP 200.
2. The deployed SHA is visible through the approved health surface.
3. A deliberately unhealthy candidate does not receive traffic.
4. Restart policy behaves as documented.
5. Logs identify the failure without revealing secrets.

Do not weaken Dealix's production-secret validation to make the lab boot. Generate strong lab-only values instead.

## Phase 5 — rollback proof

1. Deploy candidate A from SHA A.
2. Deploy candidate B from SHA B.
3. Confirm B is healthy.
4. Roll back to A.
5. Confirm A is healthy again.
6. Record recovery time and every human approval.

Success requires a demonstrated rollback, not a dashboard screenshot showing that a rollback button exists.

## Phase 6 — backup and restore proof

Use synthetic records only.

1. Create an isolated pilot database.
2. Insert a known synthetic fixture.
3. Produce an encrypted backup.
4. Delete or replace the fixture in the pilot database.
5. Restore the backup into a fresh isolated database.
6. Verify the fixture checksum.
7. Record backup time, restore time, storage location class and retention.

Do not claim disaster-recovery readiness without a successful restore.

## Phase 7 — TLS and domain isolation

Use only an approved lab subdomain.

Verify:

- certificate issuance and renewal mechanism;
- HTTPS-only redirect;
- no overlap with production DNS;
- no wildcard certificate or DNS credential broader than necessary;
- clean removal at the end of the pilot.

## Phase 8 — MCP read-only evaluation

Connect an isolated MCP client with the least privilege available.

Allowed tests:

- list projects;
- list deployments;
- inspect a deployment;
- read logs;
- read health;
- identify rollback candidates;
- generate a proposed action packet.

Pass conditions:

- every tool call is attributable;
- secret values are not returned;
- mutating calls are unavailable or denied;
- the output contains enough evidence for a human decision.

A second, separately approved test may evaluate one mutation on the disposable host. No MCP mutation is permitted against production.

## Phase 9 — security review

Verify and record:

- authentication mode;
- role/permission model;
- session expiration;
- API-token scope and rotation;
- webhook signature validation;
- audit-log coverage;
- dependency and image update procedure;
- backup encryption;
- vulnerability-reporting path;
- network exposure;
- rate limiting;
- deletion procedure.

Any critical or high-severity unresolved finding ends the pilot with `REJECT` or `HOLD`.

## Phase 10 — cost and operational comparison

Compare the pilot with the current Railway/Vercel architecture. Include:

- fixed monthly infrastructure cost;
- storage and backup cost;
- operator time;
- patching burden;
- monitoring burden;
- recovery time;
- deployment time;
- rollback time;
- data-region options;
- single-point-of-failure risk;
- vendor lock-in and exit cost.

Do not compare only headline VPS price. Include engineering and incident-response cost.

## Proof pack

Create a dated internal proof pack containing:

- scope and boundaries;
- host metadata without credentials;
- OpenShip version;
- exact Dealix SHAs;
- health evidence;
- rollback evidence;
- restore evidence;
- MCP permission evidence;
- security findings;
- monthly cost estimate;
- operator time;
- failures and lessons;
- recommendation: Reject, DR lab, staging/preview, or prepare cutover proposal.

## Destruction / closure

At completion:

- revoke lab tokens;
- remove lab DNS;
- destroy or quarantine the VPS;
- delete synthetic databases and volumes;
- retain only sanitized proof artifacts;
- record the destruction timestamp.

## Production cutover rule

A successful pilot does not authorize production changes. A production cutover requires a separate PR, risk register, rollback plan, data-residency approval, secret migration plan, maintenance window and explicit founder approval.
