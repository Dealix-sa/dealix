# 008 — Wire IP allowlist + privileged-audit middleware into the app

- **Finding:** `api/middleware/ip_allowlist.py` (`IPAllowlistMiddleware`) and
  `api/middleware/privileged_audit.py` (`PrivilegedAuditMiddleware`) are
  fully implemented, self-contained, and already default-safe (`ip_allowlist.py:73`:
  `self._enabled = os.getenv("IP_ALLOWLIST_ENABLED", "false").lower() == "true"`
  — a no-op unless explicitly turned on), but neither is ever registered via
  `app.add_middleware(...)` in `api/main.py` (confirmed: `grep -n
  "add_middleware" api/main.py` only lists CORS, SecurityHeaders,
  RateLimitHeaders, ETag, AuditLog, RequestID, APIKey — lines 268-280).
  This is real, tested, disabled-by-default enterprise-compliance tooling
  (PDPL Article 18 / NCA ECC-11 / SOC 2 audit trail per
  `privileged_audit.py:6-7`) sitting unused — a gap for the "AI Trust &
  Compliance OS" product line, which needs exactly this kind of control to
  be credible to an enterprise buyer.
- **Category:** security
- **Wave:** maintenance (serves AI Trust & Compliance OS)
- **Effort:** S   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read api/main.py before editing
```

## Context (inlined)
- Files in scope: `api/main.py`
- Current state (`api/main.py:268-280`):
    ```python
    app.add_middleware(
        CORSMiddleware,
        ...
    )
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimitHeadersMiddleware)
    app.add_middleware(ETagMiddleware)
    app.add_middleware(AuditLogMiddleware)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(APIKeyMiddleware)
    ```
- `IPAllowlistMiddleware.__init__` (`api/middleware/ip_allowlist.py:43-73`)
  takes `(app, global_allowlist=None, trusted_proxies=None)` and is a no-op
  unless `IP_ALLOWLIST_ENABLED=true`.
- `PrivilegedAuditMiddleware.__init__` (`api/middleware/privileged_audit.py:52-61`)
  takes only `(app)`; it always audits `/admin/` and `/api/v1/admin/`
  paths into an in-memory list (`self._audit_log`, capped at 100,000
  entries) — this one is **not** gated by an env flag, so wiring it changes
  behavior immediately (adds audit logging on admin paths; does not block
  any request).
- Starlette applies `add_middleware` in reverse order (last added = outermost
  first executed on the way in), so placement matters for correctness.

## Steps
1. In `api/main.py`, import both middlewares near the other middleware
   imports and add them to the chain. Add `IPAllowlistMiddleware` early
   (it's a hard reject and should run before more expensive middleware) and
   `PrivilegedAuditMiddleware` after `APIKeyMiddleware` (so it can see
   `request.state.user` if the key middleware sets it):
    ```python
    from api.middleware.ip_allowlist import IPAllowlistMiddleware
    from api.middleware.privileged_audit import PrivilegedAuditMiddleware

    app.add_middleware(
        CORSMiddleware,
        ...
    )
    app.add_middleware(IPAllowlistMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimitHeadersMiddleware)
    app.add_middleware(ETagMiddleware)
    app.add_middleware(AuditLogMiddleware)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(APIKeyMiddleware)
    app.add_middleware(PrivilegedAuditMiddleware)
    ```
   **Gate:** `python3 -m compileall -q api` → exit 0.
2. Confirm `IPAllowlistMiddleware` stays a no-op by default (no env var set)
   by running the existing test suite for it, if one exists:
   `find tests -iname "*ip_allowlist*"` — if a test file exists, run it;
   if not, note that in the PR description rather than writing a new test
   in this plan (out of scope, see below).
   **Gate:** `python3 -m pytest tests/ -k ip_allowlist -q` → passes or "no tests ran" (both acceptable — this step only confirms nothing broke).
3. Start the app locally in a smoke test (no network calls) to confirm the
   middleware chain still constructs without error:
   `python3 -c "from api.main import create_app; create_app()"`
   **Gate:** exits 0, no exception.

## Done criteria (machine-checkable)
- [ ] `python3 -c "from api.main import create_app; create_app()"` → exit 0
- [ ] `grep -c "add_middleware(IPAllowlistMiddleware)\|add_middleware(PrivilegedAuditMiddleware)" api/main.py` → `2`
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not set `IP_ALLOWLIST_ENABLED=true` anywhere (env files, Railway
  config, tests) — wiring the middleware class is safe; flipping it on is
  a founder decision requiring real allowlist entries first.
- Do not write a new test suite for either middleware in this plan — if
  none exists, report that as a separate finding (test-coverage category)
  rather than expanding scope here.
- Do not modify `PrivilegedAuditMiddleware`'s in-memory storage to a real
  DB — that's a larger persistence change, out of scope.

## STOP conditions
- If `api/main.py:268-280` no longer matches the excerpt above → STOP,
  re-run drift check — the middleware chain may have already changed.
- If adding either middleware causes any existing test in
  `tests/test_full_repo_matrix_contract.py` or `tests/test_growth_sales_cards.py`
  to fail → STOP, do not modify those tests; report the conflict instead.
- If `create_app()` raises on import of either middleware module → STOP,
  report the import error rather than debugging the middleware's internals.
