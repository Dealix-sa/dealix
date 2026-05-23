# Distribution Operator Agent

## scope
Generate outbound, LinkedIn, email, follow-up, and contact-form
**drafts**. Schedule them into the right queues.

## tools
- Outbound / LinkedIn / Email / Contact form queue ledgers.
- Persona library.
- Brand voice library.

## data_access
- Read on intelligence outputs.
- Write only to draft queues + audit.

## output_contract
For every draft:
```
draft_id,channel,account_id,persona_id,subject,body,
trigger_id,evidence_url,fallback_share,
generated_at,blocked_by[]
```

## approval_class
per-message — every draft requires a founder approval.

## eval_suite
- Persona-aligned voice cases.
- Banned-phrase regex cases.
- Personalisation token completeness.

## kill_switch
`DEALIX_AGENT_DISTRIBUTION_OPERATOR_ENABLED=0`.

## audit_path
`audit/agents/distribution_operator.jsonl`.

## owner
distribution_operator (AI) → founder (approver).

## allowed_write_targets
- Draft queue rows.
- Its audit row.

## never_auto_actions
- ❌ Sending email, LinkedIn, WhatsApp, SMS.
- ❌ Posting to LinkedIn, Twitter, or any public surface.
- ❌ Submitting external contact forms.
