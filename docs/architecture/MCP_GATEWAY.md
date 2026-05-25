# MCP Gateway

No agent talks to MCP directly. Every MCP call goes:

```
agent → MCPGateway.invoke()
       → server registry check (is the server approved?)
       → permission matrix check (is the agent allowed this tool?)
       → runtime guardrails
       → anomaly detection
       → audit
```

## Components (`dealix/hermes/mcp/`)

### `gateway.py`
The single ingress. Constructs an `MCPCallResult` with `allowed`,
`blocked_reasons`, and (if allowed and an executor is wired) `output`.
Every call writes an `AuditEntry` regardless of outcome.

### `server_registry.py`
`MCPServerCard` rows with state: `pending | approved | blocked | deprecated`.
Only `approved` servers pass the gateway. `approve()` records the
manifest hash and whether the manifest was signed.

### `manifest_review.py`
`review_manifest(manifest_dict)` returns:
- `passed: bool`
- `reasons: tuple[str]` (missing owner, missing tools list, missing data_scope, manifest not signed)
- `manifest_hash` (SHA-256 of the canonical JSON)

### `descriptor_scan.py`
Scans tool descriptors for prompt-injection phrases (`"ignore previous"`,
`"system prompt:"`, `"exfiltrate"`, `"<|system|>"`, etc.) and suspicious
keywords (`"password"`, `"private_key"`, `"os.system"`).

### `semantic_vetting.py`
Compares declared purpose vs observed side effects. A `read_users`
declared tool that emits a `delete_users` side effect is flagged.
Parameter surfaces larger than 25 fields are also flagged.

### `runtime_guardrails.py`
Three default rails:
- `no_external_send_without_approval`
- `no_unregistered_tool`
- `no_silent_failure` (every action must write audit)

### `anomaly_detection.py`
- Rate spikes (per server × tool) over `call_threshold`
- Sensitive payloads (`password`, `private_key`) in arguments

## API

`POST /api/v1/hermes/trust/mcp-review`

```json
{
  "manifest": {"owner": "Sami", "tools": [], "data_scope": "internal", "signed": true},
  "descriptors": [{"name": "read_x", "description": "..."}]
}
```

Returns manifest pass/fail, descriptor findings, combined verdict.

## Doctrine

- A server is **pending** until manifest review + descriptor scan + semantic
  vetting all pass and Sami approves.
- A tool descriptor that fails the scan is **blocked** outright.
- An anomaly during runtime triggers the kill switch on the server.
