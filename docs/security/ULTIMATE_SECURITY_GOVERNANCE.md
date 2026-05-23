# Ultimate Security Governance

Security at Dealix is a continuous discipline, not a yearly audit. It connects identity, data, runtime, and trust into a single posture that is reviewed monthly and tested quarterly.

**Source of truth:** this doc + `docs/security/` + `policies/dealix_control_policy.yaml`
**Owner:** Founder + Engineering Lead
**Trust gate:** A2 — security policy changes require founder approval.

## Posture domains

| Domain | Doc |
|--------|-----|
| Identity and access | this doc + `docs/security/INTERNAL_API_AUTH_GATE.md` |
| Data | `docs/data/ULTIMATE_DATA_PLATFORM.md`, `docs/04_data_os/` |
| Network | `docs/security/CORS_POLICY.md`, rate limits |
| Application | `docs/security/PRODUCTION_SECURITY_GATE.md` |
| AI agents | `docs/ai/AGENT_REGISTRY_SYSTEM.md`, `docs/ai/EVAL_RED_TEAM_SYSTEM.md` |
| Operational | Key rotation, secrets, audit log |
| Compliance | PDPL, CITC, ZATCA awareness |

## Identity and access

- Founder identity is hardware-key gated.
- Engineering Lead identity requires MFA.
- Service accounts are scoped, auditable, and rotated.
- No shared credentials.
- Access reviews quarterly (`docs/data/ULTIMATE_DATA_PLATFORM.md`).

## Secrets

- Secrets live in a managed secrets store.
- Inline secrets in code or in CSVs are a P0 incident.
- Key rotation: `docs/security/KEY_ROTATION.md`.

## Network posture

- CORS restricted (`docs/security/CORS_POLICY.md`).
- Rate limits enforced (`docs/security/RATE_LIMITS.md`).
- Outbound from workers limited to allowlisted endpoints.

## Application posture

- Production deploys gated (`docs/security/PRODUCTION_SECURITY_GATE.md`).
- Required CI checks (`docs/security/BRANCH_PROTECTION_REQUIRED_CHECKS.md`).
- Dependency scanning on every PR.

## Agent posture

- Agents registered (`registries/agent_registry.yaml`).
- Eval and red-team gated (`evals/gates/dealix_agent_eval_gate.yaml`).
- Kill switches active.

## Compliance posture

- PDPL-aware data handling (`docs/02_saudi_positioning/PDPL_AWARE_LANGUAGE.md`).
- CITC-awareness on communications.
- ZATCA-awareness on invoicing (`docs/finance/PAYMENT_CAPTURE_OS.md`).

## OWASP LLM Top 10 alignment

This doc maps to all ten risks at the security-policy layer. Detailed mappings are in `docs/trust/ULTIMATE_TRUST_PLANE.md`.

## NIST AI RMF alignment

- **Govern.** Policy as Code is the codified governance.
- **Map.** Agent Registry and Data Trust map the system.
- **Measure.** Observability, evals, and audits measure it.
- **Manage.** Kill switch, incident response, and exceptions manage it.

## Failure modes

- **Silent privilege escalation:** an account gains permissions outside review. Detection: quarterly access audit. Recovery: revoke; root cause.
- **Inline secret leak:** a secret committed to source. Detection: pre-commit and CI scanning. Recovery: rotate immediately; audit; root cause.
- **Outbound exfiltration:** a worker calls an endpoint outside the allowlist. Detection: network audit. Recovery: deny; incident response.

## Recovery path

If posture is in doubt, the founder triggers a Security Freeze: no new deploys, no new agents, no new access until the issue is closed.

## Metrics

- Time-since-last-rotation per secret class.
- Access-review completion per quarter.
- Dependency-vulnerability count (open).
- Incident count by P-level (target: 0 P0).

## Disclaimer

Security is engineered, not absolute. Dealix does not guarantee zero incidents. Estimated value is not Verified value.
