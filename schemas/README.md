# schemas/ — Revenue Execution OS entity schemas

JSON Schema (draft 2020-12) definitions for the `distribution_os` entities.
Field names match the dataclasses in
`auto_client_acquisition/distribution_os/` exactly, and the bilingual specs in
[`docs/distribution/`](../docs/distribution/).

| Schema | Entity | Module |
|--------|--------|--------|
| `prospect.schema.json` | Prospect | `distribution_os/prospect.py` |
| `draft.schema.json` | Draft | `distribution_os/draft_factory.py` |
| `followup.schema.json` | Followup | `distribution_os/followup.py` |
| `proposal.schema.json` | Proposal | `distribution_os/proposal.py` |
| `proof_pack.schema.json` | ProofPack | `distribution_os/proof_pack.py` |
| `payment_handoff.schema.json` | PaymentHandoff | `distribution_os/payment_handoff.py` |
| `delivery_handoff.schema.json` | DeliveryHandoff | `distribution_os/delivery_handoff.py` |
| `renewal.schema.json` | RenewalSchedule | `payment_ops/renewal_scheduler.py` |
| `win_loss.schema.json` | WinLoss | `distribution_os/win_loss.py` |

## Doctrine reflected in these schemas

- `draft.governance_status` is one of `pending_approval` / `needs_edit` /
  `blocked` — never an "auto-sent" state set by AI.
- `proposal` / `payment_handoff` / `delivery_handoff` reference a `product_id`
  from the existing catalog — prices are never invented.
- `payment_handoff.approvals` requires all six flags before `status` can be
  `approved`; AI never charges.
- evidence levels are integers `0`–`5` (L0–L5).

Validate a JSONL store against a schema (example):

```bash
python -c "import json,jsonschema,sys; s=json.load(open('schemas/draft.schema.json')); \
[jsonschema.validate(json.loads(l), s) for l in open('var/drafts.jsonl') if l.strip()]"
```
