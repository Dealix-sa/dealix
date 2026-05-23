# Production Security Gate

Before declaring the Operating Layer production-ready:

1. `DEALIX_INTERNAL_TOKEN` is set in the runtime environment.
2. `DEALIX_PRIVATE_OPS` points to a writable path that is **not** inside
   the public repo.
3. Branch protection requires the `dealix-ultimate-operating-layer`
   workflow on `main`.
4. `make ultimate-operating-layer` passes locally and in CI.
5. `apps/web` builds with `npm run build`.
6. No secrets are present in committed files
   (`scripts/verify_prompt_output_quality.py` is the basic check).

A "PASS" claim from this gate must point to a green CI run; it is not a
self-attestation.
