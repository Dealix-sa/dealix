# Railway Secret Handling

The certification layer treats anything that names a secret as toxic
if it lands in: (a) a file the repo can commit, (b) the frontend
bundle, (c) a log line. This doc is the operating rule for Railway.

## 1. Where secrets live

- **Railway → Variables**: the only canonical store.
- **Local dev**: `.env` (gitignored). Never commit even a sample with
  real values.
- **CI**: GitHub Actions secrets, only when a workflow truly needs
  them. The certification workflow does NOT need any.

## 2. What is forbidden, automatically

`scripts/verify_railway_readiness.py` greps `Dockerfile` and
`railway.toml` for the regex below and fails if a match is found:

```
\b(MOYASAR_SECRET_KEY|GREEN_API_TOKEN|JWT_SECRET_KEY|DEALIX_INTERNAL_TOKEN|HUBSPOT_ACCESS_TOKEN|GROQ_API_KEY|SMTP_PASSWORD|GOOGLE_SEARCH_API_KEY)\s*=\s*[\w.-]+
```

`scripts/verify_live_send_safety.py` scans `apps/web/**/*.{ts,tsx,js,jsx}`
for the same secret names and for direct calls to
`api.green-api.com`, `api.moyasar.com`, `api.hubapi.com`,
`graph.facebook.com`.

`scripts/verify_production_env.py` refuses any
`NEXT_PUBLIC_*` variable whose name contains `TOKEN | SECRET | KEY |
PASSWORD`. Anything `NEXT_PUBLIC_*` ships to the browser.

## 3. Rotation cadence

| Secret | Cadence | Trigger |
|---|---|---|
| `DEALIX_INTERNAL_TOKEN` | quarterly | also: any contractor offboard |
| `JWT_SECRET_KEY` | quarterly | also: any session-leak suspicion |
| `MOYASAR_SECRET_KEY` | yearly | also: any vendor incident |
| `GREEN_API_TOKEN` | yearly | also: provider notice |
| `SMTP_PASSWORD` | yearly | also: deliverability incident |
| `HUBSPOT_ACCESS_TOKEN` | yearly | also: scope change |

Use `scripts/rotate_secrets.sh` (already present) to generate new
random values and stage them; rotate in Railway, then revoke the old.

## 4. What goes in logs

Never log: the value, the first 8 chars, the last 8 chars, a base64
copy, or a hash. The codebase uses `core.config.settings.SecretStr`
fields for a reason — they `str()` to `**********`.

The audit writer (`api/internal/audit_writer.py`) scrubs any key
matching `TOKEN|SECRET|API_KEY|ACCESS_KEY|PASSWORD|PRIVATE_KEY|CLIENT_SECRET`
to `***` before writing.

## 5. If a secret leaks

1. Rotate immediately in Railway.
2. Revoke the old at the provider.
3. Force-rotate `JWT_SECRET_KEY` as well — assume sessions are
   compromised.
4. Open an incident in `private_ops/trust/incidents.csv`.
5. File a `friction_log` entry so the root cause is captured.
6. If the leak is in git history, contact the provider and treat the
   value as burned permanently; rewriting history is rarely effective
   for credentials.
