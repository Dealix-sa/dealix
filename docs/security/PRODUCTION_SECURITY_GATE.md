# Production Security Gate

The gate that any change must pass before it influences production behavior, customer-facing surfaces, or money flow.

## Checks

1. **Secret hygiene.** No secret committed; all env-var references resolve through the runtime secret manager.
2. **Auth posture.** All `/api/v1/internal/*` routes require `X-Dealix-Internal-Token`; tenant-scoped routes require tenant-bound JWT.
3. **PDPL compliance.** PII fields are detected and gated by `auto_client_acquisition/governance_os/`; cross-border transfers are blocked unless covered by the addendum.
4. **Destructive-op guard.** Schema migrations, deletes, drops, and IAM changes route through founder approval (per `destructive_operation_requires_escalation`).
5. **Key rotation.** Key rotation log under `docs/security/key_rotation_log.md` reflects an entry within the documented rotation window.
6. **Rate limits.** Rate-limit configuration in `docs/security/RATE_LIMITS.md` is the active production config.
7. **Incident drill.** Most recent incident-response drill is no older than the documented cadence.

## Owner

Security Guardian agent (advisory) + Founder (approver). Status is recorded in `security/security_status.csv`.

## Failure mode

Any failed check blocks release; the verifier `verify_sovereign_operating_stack.py` includes this gate as a required component and will exit non-zero.
