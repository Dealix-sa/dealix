# Market Production OS — Schemas — مخططات البيانات

جزء من: Dealix Market Production OS — انظر [docs/market_os/MARKET_PRODUCTION_OS_AR.md](../docs/market_os/MARKET_PRODUCTION_OS_AR.md)

These JSON Schemas (draft 2020-12) define the machine-readable objects that flow through the
Market Production OS. They are the contract between the docs (`docs/`), the runtime working data
(`data/`, gitignored except templates), and the verifier (`scripts/verify_market_production_os.py`).

| Schema | Object | Used by |
|---|---|---|
| `prospect.schema.json` | Researched prospect + weighted score + lifecycle state | Prospect Research OS |
| `outreach_draft.schema.json` | One personalized cold-email draft (250/day factory) | Cold Email Draft Factory |
| `email_account.schema.json` | Sending identity + SPF/DKIM/DMARC + warmup + health | Compliance & Deliverability Gate, Sending Ramp OS |
| `sending_batch.schema.json` | Staged, founder-approved send batch | Sending Ramp OS |
| `suppression.schema.json` | Address/domain that must never be contacted | Compliance Gate, Reply Handling OS |
| `approval_action.schema.json` | Founder decision on a draft | Founder Approval Queue |
| `reply.schema.json` | Classified inbound reply + next action | Reply Handling OS |
| `job_signal.schema.json` | Buying signal from a public job ad (manual, founder-approved) | Job Signal OS |

## Doctrine encoded in these schemas

- **No send without unsubscribe** — `outreach_draft.unsubscribe_included` and `email_account.one_click_unsubscribe`.
- **No send without approval** — `approval_action.decision = approve` is required; `sending_batch.approved_by` is mandatory before `status = sending`.
- **No scraping** — `prospect.source` and `job_signal.source_url` are founder-supplied / public, manually reviewed.
- **No committed PII** — raw emails live only in gitignored runtime data; `suppression` prefers `email_sha256`.
- **Every output carries governance** — `outreach_draft.governance_decision`.

## Examples (synthetic, no PII)

Schema-conformant samples used as founder templates and as test fixtures live under
`data/templates/market_os_*_example.jsonl`. Real prospect / reply / suppression records are
runtime data under `data/prospects/`, `data/signals/`, `data/partners/` — gitignored by policy.

## Validation

```bash
python3 scripts/verify_market_production_os.py
```

Prints `DEALIX_MARKET_PRODUCTION_OS_VERDICT=PASS|FAIL`. The same checks run under
`tests/test_market_production_os.py`.
