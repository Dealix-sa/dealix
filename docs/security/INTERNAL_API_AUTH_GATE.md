# Internal API Auth Gate

`api/internal/auth.py` implements the token gate.

Behavior:

- If `DEALIX_INTERNAL_TOKEN` is set, every internal endpoint requires
  the `X-Dealix-Internal-Token` header to match.
- If `DEALIX_INTERNAL_TOKEN` is unset (typical local dev), requests are
  allowed without the header.

The frontend reads `NEXT_PUBLIC_DEALIX_INTERNAL_TOKEN` and sends it on
every call from `lib/dealix-runtime.ts` and `lib/dealix-actions.ts`.

> Production must set `DEALIX_INTERNAL_TOKEN`. The deployment is
> considered insecure until it is set.
