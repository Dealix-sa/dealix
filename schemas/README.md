# Schemas — Market Production OS value objects

JSON Schema (draft-07) definitions for the governed market-production
pipeline. Generated from
`auto_client_acquisition/market_production_os/schemas.py` via:

```bash
python3 scripts/generate_market_production_schemas.py
```

CI (`.github/workflows/gtm-quality-gate.yml`) regenerates and fails if these
drift from the dataclasses.

| Schema | Object | Notes |
|---|---|---|
| `prospect.schema.json` | Prospect | `source` must be lawful; scraping/purchased_list/cold_whatsapp/linkedin_automation are rejected downstream |
| `outreach_draft.schema.json` | OutreachDraft | `send_status` is always `draft` from the factory; carries `governance_decision` + `evidence_level` |
| `job_signal.schema.json` | JobSignal | public/founder-supplied job postings → matched offer |
| `company_signal.schema.json` | CompanySignal | website / careers / launch signals |
| `reply.schema.json` | Reply | classification + routing; unsubscribe/angry/bounce → suppress |
| `sending_batch.schema.json` | SendingBatch | ramp-capped plan only; `planned_sends` ≤ 250 |
| `suppression.schema.json` | SuppressionEntry | permanent do-not-contact list |
| `approval_action.schema.json` | ApprovalAction | founder decision on a draft |
| `email_account.schema.json` | EmailAccount | deliverability posture (SPF/DKIM/DMARC, warmup, cap) |

See the layer overview: [`docs/market_production_os/00_MARKET_PRODUCTION_OS_MASTER_AR.md`](../docs/market_production_os/00_MARKET_PRODUCTION_OS_MASTER_AR.md).
