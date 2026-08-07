# Vercel Python bundle budget

## Current evidence

- The observed Preview build reported **458.49 MB** uncompressed.
- The repository source tree is about **83 MB** before function exclusions.
- Vercel's Python runtime has no automatic tree-shaking and documents a standard
  **500 MB uncompressed** function limit.

The risk is therefore real: the current function has little growth headroom.

## Controls added

1. `vercel.json` excludes tests, CI metadata, reports, presentations, duplicate
   frontends, caches, and archive hand-off files from the Python function.
2. Test-only packages were removed from `requirements.txt`; test workflows now
   install `requirements-dev.txt` explicitly.
3. `scripts/measure_vercel_source_payload.py` enforces a 60 MB source-input
   budget. This is intentionally not presented as the final function size.

## Acceptance gate

The next Preview must prove all of the following before merge:

- Python 3.12 build is `READY`.
- Uncompressed function size is below **425 MB** (target) and below 500 MB
  (hard standard-runtime limit).
- `/health` and `/api/v1/commercial-intelligence/status` return success.
- No import or missing-file error appears in runtime logs.
- The proposal PDF endpoint remains checked because that asset is deliberately
  not excluded.

If the bundle remains above 425 MB, create a separate, evidence-led dependency
split: trace startup imports first, then move genuinely optional integrations
to a worker/service boundary. Do not remove operational SDKs by guesswork.
