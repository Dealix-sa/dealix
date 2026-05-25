# Security Overview

Dealix runs agentic AI inside a sovereign control plane. The plane
enforces nine independent defenses in depth, so that no single failure
can produce unauthorized action, data leakage, or unsupported claims.

| # | Defense | Module |
| --- | --- | --- |
| 1 | Context isolation per agent identity | `dealix.hermes.identity` |
| 2 | Data classification | `dealix.classifications` |
| 3 | Prompt sanitization | `dealix.hermes.agent_comms.message_sanitizer` |
| 4 | Tool permissioning | `dealix.hermes.identity.capability_scope`, `dealix.hermes.mcp.gateway` |
| 5 | Output validation | `dealix.hermes.security.output_sanitizer`, `dealix.hermes.security.data_loss_prevention` |
| 6 | Human approval gates | `dealix.governance.approvals` |
| 7 | Append-only audit trails | `dealix.trust.audit` |
| 8 | Kill switch | `dealix.hermes.mcp.kill_switch` |
| 9 | Incident response playbooks | `dealix.hermes.security.red_team` |

## Hard rules

1. **No outbound sends without approval.** External messages, contract
   signing, refunds, exports, and production-config changes go through
   `dealix.governance.approvals.ApprovalGate`. Auto-approval is disabled
   by default for these actions.
2. **No untrusted source can issue instructions.** Anything tagged
   `TrustLevel.UNTRUSTED` or `QUARANTINED` is treated as data, never as
   a command. Enforced in `dealix.hermes.provenance.downstream_validation`.
3. **No lower-privilege agent can delegate externally-visible actions
   to a higher-privilege agent.** Enforced in
   `dealix.hermes.agent_comms.delegation_policy`.
4. **No MCP server is enabled without S4 Sovereign Approval.** Enforced
   in `dealix.hermes.mcp.server_allowlist`.
5. **No marketing or proposal text ships with absolute or unsupported
   claims.** Enforced in `dealix.hermes.security.claim_verifier`.

## Threat model

The plane is designed against:

- **Direct prompt injection** (override, persona swap, role spoof,
  privilege escalation, prompt exfiltration).
- **Indirect / second-order prompt injection** via documents, tool
  outputs, or cross-agent messages — see
  `dealix.hermes.security.indirect_injection_detector`.
- **MCP tool poisoning and shadowing** — see
  `dealix.hermes.mcp.manifest_review` + `descriptor_scan` + `semantic_vetting`.
- **Data loss** of PII, IBAN, national-ID, and credential tokens — see
  `dealix.hermes.security.data_loss_prevention`.
- **Agent-washing overclaim** in customer-facing surfaces — see
  `dealix.hermes.security.claim_verifier`.

## SLAs

- Approval-gate decision SLA: p95 ≤ 4 hours during business hours.
- Trust-incident triage SLA: 1 hour to acknowledgement.
- Kill switch trip time: immediate (in-process boolean flip).
