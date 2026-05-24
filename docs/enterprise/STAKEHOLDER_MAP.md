# Stakeholder Map

For every enterprise account in active motion, a stakeholder map. No
single-thread deals.

## Map template

```
Account: <name>
Sector: <ERP / cyber / ... — must match docs/strategy/BEACHHEAD_SECTOR_SCORECARD.md>

Economic buyer:
  Name, title:
  Authority:
  Concerns:
  Touchpoint cadence:

Champion:
  Name, title:
  Why they win if we win:
  Internal authority:
  Touchpoint cadence:

User (operator):
  Name, title:
  Day-to-day impact:
  Touchpoint cadence:

Procurement:
  Name, title:
  Standard requirements:
  Status:

Security / IT:
  Name, title:
  Review depth required:
  Status:

Legal:
  Name, title:
  Status (MSA, DPA):

Detractors:
  - Name, title: <why they might block>

Coach:
  Name: <internal coach, may or may not be the champion>
```

## Cadence

- New strategic account: map filled within first 14 days
- Monthly: re-confirm names + status (people change jobs)
- Stage gate: every transition in [`ENTERPRISE_SALES_MOTION`](ENTERPRISE_SALES_MOTION.md) requires the map to be current

## Storage

Inside [`docs/ops/CEO_TOP50_TRACKER.csv`](../ops/CEO_TOP50_TRACKER.csv) as
linked entries, or in a per-account markdown file under
`docs/ops/accounts/<account_slug>.md` (gitignored if it contains PII).

## Cross-references

- [ENTERPRISE_SALES_MOTION](ENTERPRISE_SALES_MOTION.md)
- [MULTI_THREADING_SYSTEM](MULTI_THREADING_SYSTEM.md)
- [`docs/enterprise/ENTERPRISE_DECISION.md`](ENTERPRISE_DECISION.md)
- [`docs/strategy/STRATEGIC_ACCOUNT_LIST.md`](../strategy/STRATEGIC_ACCOUNT_LIST.md)

## Non-negotiables

Touchpoint cadence respects the approval-center gates and the customer's
stated preferences. No external contact occurs outside the documented
channels. See [`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
