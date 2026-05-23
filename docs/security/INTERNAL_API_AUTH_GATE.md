# Internal API Auth Gate

The internal API (`/api/v1/internal/*`) is gated by a single shared
secret: `DEALIX_INTERNAL_TOKEN`.

## Behaviour

| `DEALIX_INTERNAL_TOKEN` set? | Header required? | Mode |
|---|---|---|
| yes | yes (`X-Dealix-Internal-Token`) | `enforced` |
| no | no | `dev_unprotected` |

`dev_unprotected` is intended for local dev only. The Founder Console
surfaces the current mode at `/security` and `/control-plane`. The
production gate refuses to certify a deploy in `dev_unprotected` mode.

## Rotation

1. Generate a new strong random token.
2. Set `DEALIX_INTERNAL_TOKEN` in the deploy environment.
3. Set `DEALIX_INTERNAL_TOKEN` in the Founder Console environment.
4. Wait for the next config rollout.
5. Smoke-test with `make smoke-internal-api`.

## Implementation

`api/internal/auth.py` exposes `require_internal_token` as a FastAPI
dependency. The Founder Console router includes it via
`dependencies=[Depends(require_internal_token)]` at router-construction
time, so every endpoint inherits the gate automatically.
