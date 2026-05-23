# Conversion Diagnostics

For every drop in a KPI, ask in order:

## 1. Source

- Is the upstream ledger fresh?
- Has any provider gone fallback-only?

## 2. Voice

- Did the brand guardian block more drafts than usual?
- Did approval rate dip on a specific persona / sector?

## 3. Personalisation

- Are required tokens missing on a specific channel?
- Is one persona over-represented in blocks?

## 4. Cadence

- Did follow-up density spike?
- Are we asking the same account twice in a week?

## 5. Trust

- Did the trust guardian block any rows? Why?
- Any PDPL opt-out that propagated?

## 6. Buyer changes

- Did a sector trigger expire en masse?
- Are buyers cycling roles?

## 7. Output

For each drop, the diagnostic produces:

```
diagnostic_id,kpi,drop_size,suspected_layer,
evidence_ledger_rows[],recommended_experiment_id
```
