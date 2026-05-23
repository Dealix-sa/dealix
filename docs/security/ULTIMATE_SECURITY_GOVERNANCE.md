# Ultimate Security and Governance — الأمن والحوكمة الشاملة

Status: v1
Owner: Founder

## 1. Purpose — الغرض

A single document that anchors security and governance for Dealix. Concrete controls, mapped to NIST AI RMF and PDPL-aligned posture.

وثيقة واحدة تُرسي الأمن والحوكمة في Dealix. ضوابط ملموسة مرتبطة بمعايير NIST AI RMF وموقف متوافق مع PDPL.

## 2. Governance Pillars — أعمدة الحوكمة

1. Policy-as-code (`policies/dealix_control_policy.yaml`).
2. Agent registry (`registries/agent_registry.yaml`).
3. Trust Guardian (runtime enforcement).
4. Eval Gate (release enforcement).
5. Audit log (append-only).
6. Approvals (founder in the loop).
7. Kill switches (per agent, per swarm, per worker, per provider).
8. Control Plane (observable state).

## 3. NIST AI RMF Mapping — ربط NIST

- Govern — pillars 1, 2, 6, 7.
- Map — pillars 2, 3.
- Measure — pillars 3, 4, 5, 8.
- Manage — pillars 3, 6, 7, 8.

## 4. LLM Risk Controls — ضوابط مخاطر النماذج

| Risk | Control |
|---|---|
| Prompt injection | Input quarantining + `prompt_injection` eval suite + Guardian markers |
| Excessive agency | Tool allowlist per agent + `tool_misuse` eval suite |
| Sensitive data leakage | Restricted tier excluded from prompts + `sensitive_data_leakage` suite |
| Insecure output handling | Output schema validation + downstream renderer escaping |
| Overreliance | Evidence-required eval + claim source mandatory in console |
| Model DoS | Token caps per agent and provider + budget cutoffs |
| Authorization confusion | Class system + Guardian + approvals identity binding |

## 5. Identity and Access — الهوية والوصول

- Founder identity: SSO with MFA, IP allowlist, device binding.
- Internal services: short-lived service tokens; rotation enforced.
- Agents: per-agent identity with scoped tool and storage access.
- Customers (when applicable): scoped tokens with rate limits.
- Break-glass: founder-only, time-bound, audited, paged on use.

## 6. Network Security — أمن الشبكة

- TLS everywhere; HSTS on public surfaces.
- WAF on public site and APIs.
- Internal API not exposed to internet without the auth gate.
- Outbound egress denied by default at runtime; allowlisted destinations only.

## 7. Data Protection — حماية البيانات

- Classification: public / internal / confidential / restricted.
- Encryption at rest for all storage tiers.
- Encryption in transit for all traffic.
- Key management via managed KMS; per-agent key isolation for LLM providers.
- Retention enforced by job; no orphan data.

## 8. PDPL Posture — موقف PDPL

- Data subject rights operable end-to-end (access, rectification, deletion).
- Cross-border transfer addendum in place for any non-KSA processor.
- Breach response plan tested.
- Data processing register maintained.

## 9. Supply Chain — سلسلة التوريد

- Dependencies pinned and scanned on every PR.
- SBOM produced on every release.
- Container base images pinned by digest.
- Provider keys rotated on a schedule and on any incident.

## 10. Incident Response — الاستجابة للحوادث

- Severity classes P0..P3.
- P0 includes any external action sent without approval (must be impossible by design; any detection is a P0).
- Runbooks per class; postmortems blameless and stored in audit.
- DORA MTTR measures recovery; every P0/P1 contributes.

## 11. Change Management — إدارة التغيير

- Branch protection on main with required checks (see Branch Protection doc).
- Trust Guardian label required on policy/registry/agent changes.
- Production deploys carry release tags and audit entries.

## 12. Non-Negotiables — خطوط حمراء

- No bypass of the Guardian.
- No write without an audit entry.
- No external send.
- No public claim without evidence.
- No A3 action without founder approval.

## 13. References — مراجع

- `docs/security/PRODUCTION_SECURITY_GATE.md`
- `docs/security/INTERNAL_API_AUTH_GATE.md`
- `docs/security/BRANCH_PROTECTION_REQUIRED_CHECKS.md`
- `docs/ai/TRUST_GUARDIAN_AGENT.md`
