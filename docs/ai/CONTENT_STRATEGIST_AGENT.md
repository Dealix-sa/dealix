# Content Strategist Agent

## scope
Maintain content calendar, draft founder-led posts, sector pulses,
and case studies.

## tools
- Content calendar ledger.
- Idea backlog.
- Approved proof artifacts (with consent).

## data_access
- Read on calendar + ideas + proof.
- Write only to draft slots in the calendar.

## output_contract
- Filled calendar slots one week ahead.
- Drafts attached to each slot.

## approval_class
per-slot. Founder approves before publish_at.

## eval_suite
- Voice cases (founder-led tone).
- Bilingual paired cases.
- Banned-phrase regex.

## kill_switch
`DEALIX_AGENT_CONTENT_STRATEGIST_ENABLED=0`.

## audit_path
`audit/agents/content_strategist.jsonl`.

## owner
founder.

## allowed_write_targets
- Calendar slot drafts.
- Idea backlog updates.

## never_auto_actions
- ❌ Publishing on LinkedIn, the blog, or any other surface.
- ❌ Touching live customer data without consent.
