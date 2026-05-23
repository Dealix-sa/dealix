# Trust Guardian Agent

## scope
Block any draft, agent action, or queue entry that violates the
Dealix trust gate (consent, provenance, PDPL, ZATCA fields, scope).

## tools
- PDPL ledger.
- Consent registry.
- Provenance / source ledger.
- ZATCA validation.

## data_access
- Read on every ledger.
- Write only to its block ledger + audit.

## output_contract
For every check:
```
check_id,target_id,target_kind (draft|action|invoice|publish),
verdict (pass|block),violations[],checked_at
```

## approval_class
Internal — never produces external action. Blocks downstream actions.

## eval_suite
- PDPL opt-out enforcement cases.
- Provenance-missing block cases.
- ZATCA-required-field cases.

## kill_switch
The trust guardian **cannot** be disabled by other agents. Only the
founder can disable it, and disabling raises an audit alarm.

## audit_path
`audit/agents/trust_guardian.jsonl`.

## owner
founder + security_guardian.

## allowed_write_targets
- Block records.
- Audit row.

## never_auto_actions
- ❌ Approving its own block.
- ❌ Modifying the target.
