# Internal API Auth Gate

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Built on Trust.

The Internal API Auth Gate is the mechanism that protects the
Founder Console internal endpoints (`/api/v1/internal/*`). It is
defined in `api/internal/auth.py` and used by every endpoint in
`api/routers/founder_console_internal.py`.

## How it works

The gate is a FastAPI dependency:

```python
async def require_internal_token(
    x_dealix_internal_token: str | None = Header(default=None, alias="x-dealix-internal-token"),
) -> AuthMode:
    expected = os.getenv("DEALIX_INTERNAL_TOKEN")
    if expected is None:
        return "dev_unprotected"
    if not x_dealix_internal_token or x_dealix_internal_token != expected:
        raise HTTPException(status_code=401, detail="invalid_or_missing_internal_token")
    return "enforced"
```

The gate returns one of two modes:

| Mode               | Trigger                                  | Behavior                                                          |
| ------------------ | ---------------------------------------- | ----------------------------------------------------------------- |
| `enforced`         | `DEALIX_INTERNAL_TOKEN` set in environment  | Header must match exactly; missing or mismatched returns HTTP 401.|
| `dev_unprotected`  | `DEALIX_INTERNAL_TOKEN` unset             | Console renders; every response carries `auth_mode: "dev_unprotected"`.|

`auth_mode()` is a helper that surfaces the current mode without
performing any auth.

## The `DEALIX_INTERNAL_TOKEN` environment variable

`DEALIX_INTERNAL_TOKEN` is the single secret that controls Founder
Console access. The discipline:

| Discipline                                       | Practice                                                       |
| ------------------------------------------------ | -------------------------------------------------------------- |
| Set in production                                 | Always. Production deploys without this set fail the security gate. |
| Length and entropy                                | At least 64 bytes of random, URL-safe characters.              |
| Source                                            | Generated locally by the founder; stored in the secrets store.  |
| Distribution                                      | Only the founder and the deployment automation hold it.        |
| Rotation                                          | Quarterly at minimum, immediately after any suspected exposure. |
| Logging                                           | Never logged. Filtered at the logger middleware level.          |
| Response surface                                  | Never returned in API responses.                                |
| Local development                                  | Unset. The dev_unprotected mode is surfaced visibly.            |

## Rotation procedure

| Step                                              | Owner            |
| ------------------------------------------------- | ---------------- |
| Generate a new token of sufficient length.         | Founder.         |
| Update the secrets store.                          | Founder.         |
| Update the application environment (deployment).   | Engineering.     |
| Restart the application.                            | Engineering.    |
| Smoke-test with the new token.                      | Engineering.    |
| Record the rotation in the audit ledger.            | Founder.        |

The audit row carries `action: token_rotation`, `risk: medium`.

## Failure modes the gate handles

| Failure                                             | Response                                                                    |
| --------------------------------------------------- | --------------------------------------------------------------------------- |
| Missing header in production                         | HTTP 401, `detail: invalid_or_missing_internal_token`.                       |
| Wrong header value                                   | HTTP 401, same detail string.                                                |
| Token leaked (suspected)                             | Immediate rotation; incident opened.                                         |
| Token leaked (confirmed in logs)                     | Immediate rotation; incident opened; log redaction audit.                     |
| Token unset in production                            | Production security gate fails; deploy reverted.                              |
| Token unset in dev                                   | `auth_mode: "dev_unprotected"` surfaced in every response.                    |

## Surface in responses

Every Founder Console internal endpoint response includes
`auth_mode` in the envelope. This is deliberate. We do not want a
silently unprotected deploy. The UI displays a visible warning when
`auth_mode == "dev_unprotected"`.

Example response envelope:

```json
{
  "data": { ... },
  "auth_mode": "enforced",
  "fetched_at": "2026-05-23T08:00:00+00:00"
}
```

## Header conventions

| Aspect                  | Convention                                          |
| ----------------------- | --------------------------------------------------- |
| Header name             | `x-dealix-internal-token`                            |
| Case                    | Lowercase preferred; HTTP is case-insensitive.       |
| Whitespace              | None; the value is compared character-for-character. |
| Encoding                | URL-safe characters only.                            |

## Server-side handling

The token is read from `os.getenv("DEALIX_INTERNAL_TOKEN")` once per
request via the FastAPI dependency. It is never copied into logs,
into local variables intended for serialization, or into audit
payloads.

The eval gate suite `sensitive_data_leakage` includes a regex deny
for the literal string `x-dealix-internal-token` to prevent any
draft from accidentally revealing the header name in customer-facing
text (it is not secret, but its presence in any draft is a signal of
sloppy redaction).

## Client-side handling

The Founder Console UI:

- Reads the token from a secure local store (operator's password
  manager or environment variable).
- Sends the token with every request.
- Shows a visible warning when the response shows
  `auth_mode: "dev_unprotected"`.

## Suspected exposure response

If the token is suspected exposed:

1. Rotate immediately.
2. Update all clients.
3. Open an incident.
4. Review logs for unexpected access patterns.
5. Confirm no audit ledger writes occurred during the suspected
   exposure window from unfamiliar callers.

## Discipline

1. Set the token in production. Always.
2. Rotate quarterly. Always.
3. Never log the token. Never.
4. Surface `auth_mode` in every response.
5. Treat unset-token in production as a security incident, not a
   developer convenience.

## Cross-references

- `ULTIMATE_SECURITY_GOVERNANCE.md` for the security model.
- `PRODUCTION_SECURITY_GATE.md` for the production posture check.
- `FOUNDER_CONSOLE_TRUST_GATE.md` for the trust-side enforcement.
- `INCIDENT_RESPONSE_OS.md` for handling a suspected exposure.
