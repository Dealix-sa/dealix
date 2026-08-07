# OIDC and Secret Policy
## سياسة OIDC والأسرار

**Document Type:** Security Policy
**Version:** 1.0
**Owner:** Agent #5 — Security Red Team
**Last Updated:** 2026-06-03

---

## 1. Purpose

This policy defines how Dealix uses OIDC (OpenID Connect) for cloud authentication and handles secrets in CI/CD.

---

## 2. OIDC Authentication

### 2.1 Preferred Over Static Secrets

OIDC is preferred over static secrets for cloud authentication because:
- No long-lived credentials
- Automatic token rotation
- Scope-limited permissions
- Time-bound access

### 2.2 Implementation

```yaml
# Example: Azure authentication via OIDC
- name: Azure Login
  uses: azure/login@v2
  with:
    creds: ${{ secrets.AZURE_CREDENTIALS }}
    # OIDC token from GitHub Actions
```

### 2.3 When OIDC is Required

| Environment | OIDC Required | Notes |
|-------------|----------------|-------|
| Production | Yes | No static secrets |
| Staging | Recommended | OIDC preferred |
| Development | Optional | Local credentials OK |

---

## 3. Secret Management

### 3.1 Secret Storage Hierarchy

1. **GitHub Secrets** — For CI/CD credentials
2. **Environment Variables** — For runtime configuration
3. **Vault (future)** — For centralized secret management

### 3.2 Secret Access Rules

1. **Untrusted events get NO secrets** — PRs from forks
2. **Minimal secrets for minimal trust** — Only what's needed
3. **Production secrets require approval** — Founder approval
4. **Log all secret access** — Audit trail

---

## 4. Related Documents

| Document | Purpose |
|----------|---------|
| `SECRETS_HANDLING_POLICY.md` | General secrets policy |
| `GITHUB_ACTIONS_SECURITY_POLICY.md` | GitHub Actions security |

---

*Policy maintained by Agent #5 — Security Red Team*
