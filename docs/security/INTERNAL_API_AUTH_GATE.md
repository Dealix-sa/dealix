# Internal API Auth Gate

Source: `api/internal/auth.py`.
Env var: `DEALIX_INTERNAL_TOKEN`.
Header: `X-Dealix-Internal-Token`.

## Modes

- **production / staging** — env var is set; every internal endpoint
  requires the header. Unauthorised requests return 401.
- **local dev** — env var is unset; requests are allowed and the auth
  gate logs a warning. `is_production_token_set()` returns `False` and
  the Security page renders `production_token_set: false`.

## How to set in production

```
export DEALIX_INTERNAL_TOKEN="$(python -c 'import secrets;print(secrets.token_urlsafe(48))')"
```

Set the same value in the frontend's environment as
`NEXT_PUBLIC_DEALIX_INTERNAL_TOKEN` (for server-rendered pages only —
do not ship a token to untrusted browsers).
