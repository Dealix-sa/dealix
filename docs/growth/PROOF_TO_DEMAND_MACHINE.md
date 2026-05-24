# Proof-to-Demand Machine

| Field | Value |
|---|---|
| Purpose | Route approved proof artifacts to relevant demand triggers |
| Inputs | approved proof artifacts (consent-gated), accounts in sector match |
| Outputs | `proof_to_demand_queue.csv` |
| Approval class | Founder approval; proof must already be customer-signed |
| Trust gate | Customer consent verified; sector match; suppression honoured |
| Owner | Brand Guardian + Distribution Operator |
| KPI | Reply rate when proof is cited vs. base |
| Failure mode | Consent missing → proof never cited |

## Flow

```
Approved proof (Proof Approval OS)
    ↓
Sector / persona match
    ↓
Draft cite-the-proof message
    ↓
Queue for founder approval
    ↓
Manual send
```

## Schema

```yaml
queue: proof_to_demand_queue
fields:
  - proof_id
  - account_id
  - sector_id
  - persona_id
  - draft_en
  - draft_ar
  - consent_verified         # required true
  - brand_check
  - trust_check
  - status
  - created_at
```

## Brand notes

- Only cite an outcome the customer has signed off on.
- Quote in the customer's own words when available.
- Never embellish numbers.
