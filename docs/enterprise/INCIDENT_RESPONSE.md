# Incident Response

Dealix ships four standing red-team playbooks. They are codified in
[`dealix/hermes/security/red_team.py`](../../dealix/hermes/security/red_team.py)
so the runbook and the code never drift apart.

## 1. Suspected prompt injection

**Trigger:** `message_sanitizer` or `indirect_injection_detector` returns
findings.

1. Quarantine the affected `ProvenanceObject`
   (`TrustLevel.QUARANTINED`).
2. Restrict the receiving agent to `DRAFT_ONLY` for the next 24h.
3. Open an Approval Center ticket with the sanitized message attached.
4. Run the standard prompt-injection test vectors
   (`dealix.hermes.security.prompt_injection_tests`) against the
   responsible tool/route to confirm coverage.
5. If a downstream action was taken before detection, roll it back and
   notify the workspace owner.

## 2. MCP anomaly

**Trigger:** `dealix.hermes.mcp.anomaly_detection` severity in
`{warn, critical}`.

1. Trip the MCP kill switch for the affected server.
2. Compare current `manifest_sha256` against the allowlist entry — if
   it drifted, disable the server.
3. Snapshot the last 100 calls (request + response previews) for
   review.
4. Schedule a manifest re-review before re-enabling.

## 3. DLP secret leak

**Trigger:** `data_loss_prevention.findings` contains `secret_token:*`
or `pii:possible_*`.

1. Block the outbound payload at the boundary.
2. Rotate the leaked credential (if any) within 1 hour.
3. Trace the lineage via `ProvenanceLedger` to the originating
   `object_id`.
4. Add a regression test vector to `prompt_injection_tests` with the
   offending shape.

## 4. Overclaim in marketing

**Trigger:** `claim_verifier.flagged_phrases != []`.

1. Block the asset from publishing.
2. Route the asset to the approved-claims editor
   (`dealix.hermes.partners.program.approved_claims`).
3. Update the offending template with safe alternatives.

## On-call

Incident response is owned by the founder during the bootstrap phase.
The kill-switch trip and the approval gate are both single-actor
operations. The on-call rotation will expand once a second engineer is
onboarded; until then, the founder is the named first responder for
every incident class above.
