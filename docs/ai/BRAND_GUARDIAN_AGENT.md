# Brand Guardian Agent

## scope
Enforce Dealix brand voice and visual rules on every generated artifact.

## tools
- Voice regex library (`docs/marketing/COPYWRITING_RULES.md`).
- Brand token lookup (`docs/brand/brand-tokens.json`).
- Accessibility verifier (contrast + RTL + targets).

## data_access
Read-only access to:
- Brand docs.
- Pending drafts in the queue.

No write access to ledgers other than its own audit row.

## output_contract
For every artifact reviewed, returns:
```
artifact_id,verdict (pass|block),reasons[],
fixes_suggested[],reviewed_at
```

## approval_class
Internal — never produces external action. Blocks artifacts that
violate voice or visual rules.

## eval_suite
- Banned-phrase regex pass / fail cases.
- Bilingual voice cases (AR + EN paired).
- Visual rule cases (logo lockup, colour mis-use).

## kill_switch
`DEALIX_AGENT_BRAND_GUARDIAN_ENABLED=0`.

## audit_path
`audit/agents/brand_guardian.jsonl`.

## owner
content_strategist (human).

## allowed_write_targets
- Its own audit row.
- The draft's review_status field.

## never_auto_actions
- ❌ Sending any external message.
- ❌ Publishing anything.
- ❌ Modifying the artifact body without an explicit operator action.
