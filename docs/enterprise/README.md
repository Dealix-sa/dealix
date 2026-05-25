# Enterprise documents

Customer-facing governance and security documents produced by the
`dealix/hermes/` layer. Each document is generated from the same source
of truth that powers the runtime decisions — there is no separate
"marketing version".

| Document | Purpose | Backing module |
| --- | --- | --- |
| [SECURITY_OVERVIEW.md](SECURITY_OVERVIEW.md) | High-level security posture | `dealix.hermes.security` |
| [AI_GOVERNANCE_MODEL.md](AI_GOVERNANCE_MODEL.md) | The agentic governance model | `dealix.hermes.agent_lifecycle`, `dealix.hermes.identity` |
| [DATA_BOUNDARIES.md](DATA_BOUNDARIES.md) | Where data lives and who can read/write it | `dealix.hermes.identity.workspace_scope`, `dealix.hermes.provenance` |
| [AGENT_REGISTRY_SAMPLE.md](AGENT_REGISTRY_SAMPLE.md) | Sample agent registry entries | `dealix.hermes.agent_lifecycle.registry` |
| [TOOL_PERMISSION_MATRIX.md](TOOL_PERMISSION_MATRIX.md) | Which agents can call which tools | `dealix.hermes.identity.capability_scope` |
| [EVIDENCE_PACK_SAMPLE.md](EVIDENCE_PACK_SAMPLE.md) | What a delivered evidence pack contains | `dealix.hermes.delivery.quality_checklists` |
| [ROI_MEASUREMENT.md](ROI_MEASUREMENT.md) | How verified revenue + attribution work | `dealix.hermes.money`, `dealix.hermes.growth.attribution` |
| [INCIDENT_RESPONSE.md](INCIDENT_RESPONSE.md) | Red-team playbooks | `dealix.hermes.security.red_team` |
