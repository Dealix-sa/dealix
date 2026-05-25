# Data Boundaries

## Workspaces

Every record in Dealix is tagged with a `workspace_scope`. An agent
identity scoped to `dealix_internal` cannot read or write a record
tagged `customer_xyz`, regardless of its capability scope.

Enforced in
[`dealix/hermes/identity/workspace_scope.py`](../../dealix/hermes/identity/workspace_scope.py).

| Workspace | Examples |
| --- | --- |
| `dealix_internal` | Dealix proposal templates, internal knowledge base |
| `customer_<id>` | A specific customer engagement |
| `partner_<id>` | A specific partner relationship |
| `public` | Published marketing surfaces |

## Data classification

Data is classified S1 → S4 (`dealix.classifications`).

| Class | Examples | Allowed without approval |
| --- | --- | --- |
| S1 | Public marketing copy | yes |
| S2 | Internal ops notes | yes (internal workspace only) |
| S3 | Personal data (PDPL scope) | no — requires PDPL lawful-basis check |
| S4 | Production secrets, signed contracts | never (kill-switch territory) |

## Provenance

Every prompt fragment, agent message, and tool output carries provenance
metadata (`dealix.hermes.provenance`):

```json
{
  "object_id": "msg_001",
  "object_type": "agent_message",
  "source": "external_website",
  "source_trust_level": "untrusted",
  "created_by": "market_radar_agent",
  "used_by": ["proposal_factory"],
  "sanitized": true,
  "policy_notes": ["external source cannot issue instructions"]
}
```

Hard rule: untrusted or quarantined data is never used as instructions
for any agent, regardless of risk band. Enforced in
[`downstream_validation.py`](../../dealix/hermes/provenance/downstream_validation.py).

## Cross-region

Dealix is operated from the KSA region by default. PDPL applies. Any
cross-region transfer requires explicit consent and is logged in the
audit trail.
