# Capital Ledger

Track **which capital** each project compounded. IDs: `C-###`.

## Capital types

```text
Service
Product
Knowledge
Trust
Market
```

## Minimum per project

```text
1 Trust Asset
+ 1 Knowledge أو Product Asset
```

Examples:

- **Trust:** anonymized proof pack, QA’d deliverable narrative
- **Knowledge:** playbook delta, objection, sector insight
- **Product:** script, internal tool, feature candidate shipped or specified

| ID | Project | Capital Type | Asset Created | Reusable? | Owner | Next Use |
|----|---------|--------------|---------------|-----------|-------|----------|
| C-001 | Lead Sprint A | Trust | anonymized proof pack | Yes | | sales deck |
| C-002 | Lead Sprint A | Product | import preview script | Yes | | all lead sprints |
| C-003 | Clinic Sprint | Knowledge | clinics playbook update | Yes | | clinic outreach |
| C-004 | M3 Sprint Dry-Run (synthetic/internal) | Trust | 14-section Proof Pack v2 example (`proof_example` / `cap_29ff323baca1`) — `data/proofs/m3_dryrun_internal_proof_pack.json` | Yes | dealix | delivery QA reference + anonymized sales-deck proof |
| C-005 | M3 Sprint Dry-Run (synthetic/internal) | Knowledge | Saudi B2B account-scoring heuristic delta (`sector_insight` / `cap_68d9e7d86716`) — warm + tier-1 city + recency dominate; 8-way score-tie issue logged | Yes | dealix | account scoring tiebreaker fix; clinic/logistics outreach |

**M3 Dry-Run note (2026-05-18):** C-004/C-005 produced by the M3 Delivery Engine readiness test on synthetic data only. JSONL source of truth: `var/capital-ledger.jsonl`, engagement `m3_dryrun_internal_2026_05_18`. No real customer data. The orchestrator also auto-registered a `scoring_rule` asset (`cap_e77d3d212e13`); gap logged — `step7_capital_assets` registers only one default asset and does not enforce the "1 Trust + 1 Knowledge/Product" minimum.

**Parent model:** [`DEALIX_CAPITAL_MODEL.md`](../company/DEALIX_CAPITAL_MODEL.md).
