# Proof-Safe Asset Policy

> The single policy every sales / authority / partner asset must
> obey. Owned by the founder; enforced by verifiers and by the
> approval flow.

## The five rules

1. **No claim without a source.** Any quantitative claim ("Saudi B2B
   buyers respond X% faster…") must cite a source or be removed.
2. **No promise without a guardrail.** Outcomes are described with
   the upstream activities required, not as guarantees.
3. **No customer data without permission.** Logos, names, quotes,
   screenshots — all require a permission row in the proof-pack
   registry.
4. **No off-ladder pricing or terms.** Pricing lives in
   `docs/company/PRICING.md`. Assets that imply different prices are
   rejected.
5. **No automation that bypasses approval.** No asset says "click
   here, our AI takes over." Approval-first is a feature, not a bug.

## Banned phrases

- "guaranteed leads"
- "guaranteed revenue"
- "100% success"
- "always wins"
- "risk-free"
- "AI does it for you, no humans needed"
- "we promise"
- "we will deliver X customers"

The verifier (`scripts/verify_market_attack_system.py`) scans new
docs and asset files for these phrases and flags them.

## Audit

Every asset has an audit row when published:

```
audit_id,asset_id,approver,approved_at,proof_pack_ref,scope,notes
```

stored in `<PRIVATE_OPS>/sales_assets/approval_log.csv`.
