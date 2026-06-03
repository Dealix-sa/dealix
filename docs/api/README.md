# API

## Purpose
Document the Dealix API surface so internal services and external customers can integrate against a stable, trust-governed contract.

## Owner
Sami / Product owner.

## Review Cadence
Monthly, plus before any breaking change.

## Inputs
- Customer integration needs.
- Internal service dependencies.
- Trust OS rules on what may be exposed.
- Performance and reliability signals.

## Outputs
- API reference (endpoints, schemas, errors).
- Authentication and rate-limit policy.
- Versioning and deprecation policy.
- Customer integration guides.

## Rules
- No endpoint ships without authentication, logging, and a trust review.
- No sensitive data is returned unless the caller is explicitly authorised and audited.
- Breaking changes require a deprecation notice and a migration path.
- API changes that affect customer commitments require A2 founder approval.

## Metrics
- Endpoints documented vs. endpoints shipped.
- p95 latency and error rate per endpoint.
- Time from breaking change announcement to deprecation.
- Customer integrations live.

## Evidence
- OpenAPI / schema files in the repo.
- API smoke tests (`scripts/`, `tests/`).
- approval log entries for breaking changes.
- customer integration sign-offs.

## Last Reviewed
YYYY-MM-DD
