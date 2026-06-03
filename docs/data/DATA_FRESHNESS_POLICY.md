# Data Freshness Policy

## Purpose
Define how recent each data source must be before it can drive a decision.

## Freshness targets
| Entity | Maximum staleness | Refresh cadence |
|---|---|---|
| Pipeline tracker | 7 days | After every founder action |
| Revenue action log | 1 day | After every action |
| Cash collected | 1 day | After every confirmed payment |
| Proposal tracker | 3 days | After every proposal touch |
| MRR tracker | 30 days | Monthly close |
| Expenses | 30 days | Monthly close |
| Approval log | 1 day | After every approval decision |
| Risk register | 7 days | Weekly review |
| Evidence ledger | 1 day | After every evidence event |
| Business score | 7 days | Weekly close |

## Stale-data behavior
If a source is past its freshness window:
- Verifiers warn.
- Mission control and control tower brief mark the source as `STALE`.
- The founder must refresh before relying on the data for a major decision.

## How freshness is measured
- For CSVs: the `last_touch` column or the file's modified timestamp, whichever is more recent.
- For generated reports: the report header includes a `Generated on:` line; staleness is now - header.

## Manual refresh checklist
1. Open the file.
2. Update or append rows.
3. Touch the `last_touch` column.
4. Save.
5. Run the relevant verifier or report regeneration command.

## Exceptions
None. If a source is irrelevant, retire it from the architecture rather than letting it go stale.
