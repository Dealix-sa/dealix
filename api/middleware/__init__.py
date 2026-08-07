"""API middleware modules — Wave 12.6 §33.2.6 hardening + http_stack.

This package contains FastAPI middleware + dependencies that enforce
cross-cutting safety invariants:

- ``http_stack``: request ID, security headers, PDPL audit logging, ETag,
  rate-limit headers (shared HTTP layer used by ``api.main``).

- ``tenant_isolation``: repository-layer assertions — given the request's
  tenant and the object's tenant, refuse a mismatch (defense against
  OWASP API1:2023 BOLA — Broken Object-Level Authorization). It does
  **not** resolve the tenant; that is ``api/security/tenant_scope.py``,
  which derives it from verified identity rather than from a header.

- ``bopla_redaction``: Pydantic response-model decorator that filters
  sensitive fields (bank_account, personal_email, phone) by role
  (defense against OWASP API3:2023 BOPLA — Broken Object Property-Level
  Authorization).

Re-exports the 5 http_stack classes so `api/main.py` imports stay
stable: ``from api.middleware import (
    AuditLogMiddleware, ETagMiddleware, ...
)``.

Article 11: composes existing api/security/ (RBAC + JWT + api_key) —
doesn't duplicate.
"""

from api.middleware.http_stack import (
    AuditLogMiddleware,
    ETagMiddleware,
    RateLimitHeadersMiddleware,
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
)

__all__ = [
    "AuditLogMiddleware",
    "ETagMiddleware",
    "RateLimitHeadersMiddleware",
    "RequestIDMiddleware",
    "SecurityHeadersMiddleware",
]
