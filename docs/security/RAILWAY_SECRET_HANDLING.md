# Railway secret handling

## Principles

1. **Names in code, values in Railway.** Settings field names live in
   `core/config/settings.py`. Values live in Railway Variables. Never
   commit values to git.
2. **Never print secrets.** Verifiers and logs report `set` / `missing`
   only. Use `SecretStr` in pydantic for any field that holds a secret.
3. **Seal where possible.** Use Railway's variable-sealing feature for
   anything not needed at build time. Sealed variables are still
   available at runtime but cannot be re-read from the UI.
4. **Rotate on incident.** Documented at `docs/security/KEY_ROTATION.md`.

## Adding a new secret

1. Add the field to `Settings` in `core/config/settings.py`. Use
   `SecretStr` if the value should never appear in logs/serialisation.
2. Add the name to `docs/security/PRODUCTION_ENVIRONMENT_VARIABLES.md`.
3. If required in production, add the name to `REQUIRED` in
   `scripts/verify_production_env.py`.
4. Set the value on Railway.
5. Run `make production-env-check` locally (CI mode by default).

## Reading a secret in code

```python
from core.config.settings import get_settings

settings = get_settings()
api_key = settings.require_secret("hubspot_access_token")  # raises if missing/empty
```

`require_secret` raises a clear `ValueError` rather than silently passing
`"change-me"` through to a third-party API. Never use `os.getenv()`
directly for secret values — go through `Settings` so the field schema is
the single source of truth.

## What `verify_production_env.py` checks

- Variable **names** are declared in `Settings` (CI mode).
- In live mode, the env var is non-empty.
- Contradictory flags trip a `FAIL` (e.g. `WHATSAPP_ALLOW_LIVE_SEND=true`
  AND `WHATSAPP_MOCK_MODE=true`).

## What it does **not** do

- Validate value format (length, regex). That belongs in the pydantic
  validator on the field itself.
- Network probes. See `scripts/verify_railway_production_config.py`.
