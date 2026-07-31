# 009 — Sanitize exception detail returned to API clients

- **Finding:** `api/main.py:294-298`'s `AICompanyError` exception handler
  returns `str(exc)` verbatim as the `"detail"` field of every 400 response:
    ```python
    @app.exception_handler(AICompanyError)
    async def ai_company_error_handler(_: Request, exc: AICompanyError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error": exc.__class__.__name__, "detail": str(exc)},
        )
    ```
  `core/errors.py:6-36`'s `AICompanyError` subclasses are plain marker
  classes with no message sanitization, and call sites across the repo
  (e.g. `integrations/whatsapp.py:51`, `integrations/calendar.py:123`,
  `core/agents/base.py:275,318`) raise them with interpolated strings.
  Today's raise sites only embed variable names or truncated LLM text (no
  concrete secret leak found), but the pattern — any exception message
  reaching an HTTP client unfiltered — is a latent risk: a future raise
  that includes a stack trace fragment, a DB connection string, or a
  provider error body (which can itself contain request headers) would
  leak straight to the caller. For a product marketing itself as an "AI
  Trust & Compliance OS," this class of error-handling hygiene matters to
  a security-conscious buyer's due diligence.
- **Category:** security
- **Wave:** maintenance
- **Effort:** S   **Confidence:** MED
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read api/main.py before editing
```

## Context (inlined)
- File in scope: `api/main.py`
- Current state (`api/main.py:294-298`, exact excerpt above).
- `core/logging.py` already has a `get_logger` helper used repo-wide — use
  it here rather than inventing a new logging pattern.
- Repo convention: never print secret values to logs either (per
  `.claude/rules/dealix-safety.md` "Secrets"), so the fix must not just move
  the raw string from the HTTP response into a log line that itself gets
  shipped somewhere unsafe — logging via the standard `core.logging.get_logger`
  path is the existing sanctioned sink.

## Steps
1. In `api/main.py`, change the handler to log the full exception detail
   server-side (for debugging) but return a generic, error-class-scoped
   message to the client, keeping the exception's `__class__.__name__` (not
   a security-sensitive value) visible so API consumers can still branch on
   error type:
    ```python
    from core.logging import get_logger

    _api_error_log = get_logger("api.errors")

    @app.exception_handler(AICompanyError)
    async def ai_company_error_handler(_: Request, exc: AICompanyError) -> JSONResponse:
        _api_error_log.warning("AICompanyError: %s", exc, exc_info=exc)
        return JSONResponse(
            status_code=400,
            content={
                "error": exc.__class__.__name__,
                "detail": "Request could not be processed. Contact support with this error type if it persists.",
            },
        )
    ```
   **Gate:** `python3 -m compileall -q api` → exit 0.
2. Check whether any existing test asserts on the current `str(exc)` detail
   text being returned verbatim (a test that would now need updating
   because it's testing the old leaky behavior, not a doctrine guard):
   `grep -rln "ai_company_error_handler\|AICompanyError" tests/`
   For each match, read it — if it asserts on the *generic* detail message
   only conceptually (e.g. checks status code 400, checks `error` field),
   it should still pass. If it asserts on the literal old message text,
   update the assertion to match the new generic message (this is
   expected, not a doctrine violation — no doctrine guard test is in this
   list per `references/dealix-gates.md`).
   **Gate:** `python3 -m pytest <matching test files> -q` → all pass.

## Done criteria (machine-checkable)
- [ ] `python3 -m pytest tests/ -k "error_handler or AICompanyError" -q` → passes (or "no tests ran")
- [ ] `python3 scripts/ops/security_smoke_ci.py` → exit 0
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not change `core/errors.py`'s exception class hierarchy.
- Do not change any raise site (`integrations/whatsapp.py`,
  `integrations/calendar.py`, `core/agents/base.py`, etc.) — this plan only
  fixes the single response-serialization point in `api/main.py`.
- Do not add exception detail to response headers as a workaround —
  the goal is removing the leak surface, not relocating it.

## STOP conditions
- If `api/main.py:294-298` no longer matches the excerpt above → STOP,
  re-run drift check.
- If an existing test relies on the client seeing the specific exception
  message for legitimate UX reasons (e.g. a validation error that must
  show the user which field is invalid) → STOP and report; do not blanket-
  genericize a message that a real user-facing form depends on for
  usability. Prefer a per-exception-subclass allowlist of safe messages
  over one universal generic string if this STOP condition triggers.
