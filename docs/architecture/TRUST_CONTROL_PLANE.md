# Trust Control Plane

The Trust Control Plane is the layer that makes Dealix sellable to
enterprises. Every agent, every tool, every action is registered,
permissioned, audited, and reviewed.

## Registries

### Agent Registry (`trust/agent_registry.py`)

Every agent runs as a registered `AgentCard`:

```python
AgentCard(
    agent_id="proposal_factory",
    owner="Sami",
    domain="money",
    mission="Generate structured commercial proposals.",
    max_sovereignty_level=SovereigntyLevel.S1_INTERNAL,
    allowed_tools=["read_opportunity", "read_offer_library", "draft_proposal"],
    forbidden_tools=["send_external", "sign_contract", "export_data"],
    kpis=["proposals_drafted", "proposal_acceptance_rate"],
)
```

51 default cards live in `agents/registry_cards.py`.

### Tool Registry (`trust/tool_registry.py`)

Every tool is declared with risk, scope, owner, audit requirement:

```python
ToolCard(
    tool_id="send_external",
    owner="Sami",
    risk_level=ToolRisk.high,
    enabled=False,        # default DISABLED
    requires_approval=True,
    data_scope="explicit_recipient_only",
    audit_required=True,
    pdpl_relevant=True,
)
```

17 default tool cards seed via `config/tools_seed.py`. Dangerous tools
(`send_external`, `transfer_money`, `sign_contract`, `export_data`,
`publish_landing`, `publish_pricing`) are disabled by default and require
approval to invoke.

## Permission Matrix

`trust/permission_matrix.py` checks (agent, tool, workspace) tuples:

1. Explicit deny? → block.
2. Agent or tool unknown? → block.
3. Agent inactive or tool disabled? → block.
4. Tool on agent's forbidden list? → block.
5. Tool not on agent's allow list? → block.
6. Tool has `allowed_agents` and agent not in it? → block.
7. Otherwise → allow.

## Trust Check

`trust/trust_check.py` is the master gate every agent action passes
through. It blocks:

- Overclaim phrases (`"guaranteed"`, `"100% accuracy"`, `"infallible"`)
- Partnership claims without an approved partner record
- PII in external content (`contains_pii && audience=="external"`)
- Pricing changes without approval
- External commitments without approval
- Missing evidence pack when one is required

Plus a `PolicyEngine` for custom rules.

## Evidence Packs

`trust/evidence.py` — every tier-A/B decision ships with a pack
containing sources, model used, and an AR+EN bilingual memo.

## Audit, Risks, Incidents

- `trust/audit.py` — append-only audit log; `MCPGateway.invoke` writes
  on every call.
- `trust/risk_register.py` — open risks with `severity * likelihood`
  scoring; sortable by score.
- `trust/incident_response.py` — incidents with state transitions
  (open → triaged → contained → resolved → postmortem_done).

## Controls Catalog

`trust/controls.py` — named safety mechanisms cross-referenced to
external frameworks (e.g. NIST AI RMF Govern/Map/Measure/Manage).
