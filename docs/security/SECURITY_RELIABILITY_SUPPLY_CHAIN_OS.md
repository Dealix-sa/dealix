# Security, Reliability, and Supply Chain OS

## Purpose
Operate Dealix safely across three pillars: security (confidentiality + integrity), reliability (availability + recoverability), and supply chain (dependency + identity + provenance).

## Pillar 1 — Security
- **Authentication**: every external surface requires authenticated access; no public write endpoints.
- **Authorization**: least-privilege; role boundaries enforced server-side.
- **Secrets**: stored in environment manager (Doppler / Railway env / .env files outside git); never logged.
- **Encryption**: TLS in transit, at-rest encryption for databases, hashed secrets at rest.
- **Audit logging**: every privileged action logged with actor + timestamp + outcome.
- **Threat surface review**: each new public endpoint reviewed against OWASP top 10 before merge.

## Pillar 2 — Reliability
- **Backups**: nightly DB backup, weekly full snapshot, monthly restore drill.
- **Health checks**: `/healthz` for liveness, `/readyz` for dependency readiness.
- **Runbooks**: every external surface has an entry in `docs/ops/INCIDENT_RUNBOOK.md`.
- **SLO**: 99.5% monthly availability for the founder-facing systems during business hours.
- **Capacity**: pre-launch load test against `locustfile.py`; results recorded in evidence ledger.

## Pillar 3 — Supply chain
- **Pinned dependencies** in `requirements.txt` and `requirements-dev.txt`.
- **No git URLs** for production dependencies.
- **Dependabot enabled**; advisories triaged within 5 business days.
- **License scan**: only permissive licenses (MIT, Apache-2.0, BSD, ISC) in production.
- **Build provenance**: container images built via documented Dockerfile; no `:latest` in production tags.

## Operating cadence
- Daily: secret scan during pre-commit.
- Weekly: dependency review run, advisory triage.
- Monthly: restore drill, access review, threat-model walk.

## Failure modes (and responses)
| Failure | Response |
|---|---|
| Secret detected post-commit | Rotate immediately; force push only with founder approval; record in `dealix-ops-private/trust/approval_log.csv`. |
| Critical CVE in pinned dep | Pin to patched version; open PR within 48h; document in evidence ledger. |
| Restore drill failure | Halt deployment of new features until drill passes. |
| Public boundary violation | Revert; investigate; update `docs/data/DATA_PRIVACY_BOUNDARY.md`. |

## Evidence
All security events, restore drills, and supply-chain reviews are logged in `dealix-ops-private/evidence/execution_evidence_ledger.csv`.
