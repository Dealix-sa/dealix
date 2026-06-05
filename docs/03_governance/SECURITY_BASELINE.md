# Security Baseline

> **Status:** CANONICAL · **Owner:** Founder · **Last reviewed:** 2026-06-05
>
> NCA-aligned controls. We say "aligned," never "certified."

---

## 1. Configuration & secrets

- All configuration via `.env`; never commit secrets.
- Secrets use `SecretStr` patterns; pre-commit runs gitleaks + detect-secrets.
- CI: CodeQL, dependency review, secret + filesystem vulnerability scans,
  OpenSSF Scorecard.
- Local/CI security smoke: `python scripts/security_smoke.py` / `make security-smoke`.

## 2. GitHub Actions least privilege

Default token to read-only; elevate per-job only when needed.

```yaml
permissions:
  contents: read
```

Elevate only where required:

```yaml
permissions:
  contents: write
  pull-requests: write
  issues: write
```

GitHub recommends `GITHUB_TOKEN` have the least privileges possible (read-only by
default, elevated only on jobs that need it) and warns against storing secrets as
plaintext or relying on redaction.

## 3. GitHub App permissions (current stage)

| Permission | Level |
|---|---|
| Contents | Read/Write |
| Pull requests | Read/Write |
| Issues | Read/Write |
| Actions | Read |
| Checks | Read |
| Commit statuses | Read |
| Metadata | Read |
| Workflows | Write only if it edits workflows |
| Administration / Organization / Account | None |

Least sufficient privilege is the correct decision at Dealix's current stage.

## 4. Runtime & deploy

- Docker hardening (non-root container, multi-stage build).
- Webhook signature verification where implemented.
- Protected admin/customer/privileged routes (API-key or future RBAC boundary).

## 5. Verification gates

```bash
make env-check
python scripts/security_smoke.py
python -c "import api.main; print('api import OK')"
make prod-verify
```

## 6. NCA alignment

NCA publishes official cybersecurity controls and guidelines (social-media
accounts, remote work, critical systems, e-commerce, and more). Dealix maps its
controls to these as **NCA-aligned**. Certification claims require an actual
certification.

## 7. Enterprise readiness (before enterprise pilots)

security-smoke PASS · prod-verify PASS · privacy pages ready · DPA draft ·
incident response · access control · audit logs · case study · support SLA.
