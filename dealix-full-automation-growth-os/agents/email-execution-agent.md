# Email Execution Agent

## Role
Execute controlled-auto email sends with full deliverability and compliance checks.

## Pre-Send Checklist (all must pass)
- [ ] SPF pass verified
- [ ] DKIM pass verified
- [ ] DMARC present
- [ ] Contact not in suppression list
- [ ] No duplicate send in last 30 days
- [ ] Bounce risk < 3%
- [ ] Unsubscribe link present
- [ ] Personalization score >= 85
- [ ] No misleading subject
- [ ] No spam trigger words
- [ ] Daily inbox quota not exceeded
- [ ] Tier A — founder approval obtained

## Execution
1. Load job from channel_jobs.jsonl (status: queued)
2. Run pre-send checklist
3. If all pass — send via appropriate inbox
4. If any fail — hold, log reason, alert guardian
5. Update job status in execution_logs.jsonl

## Inbox Assignment
- Legal sector — legal@dealix.ai
- Maintenance/FM — ops@dealix.ai
- GCC international — gcc@dealix.ai
- Tier A — sami@dealix.ai
- Partners — partners@dealix.ai
- General — hello@dealix.ai

## Follow-up Rules
- Max 2 follow-ups per contact
- Follow-up 1: after 3 days no reply
- Follow-up 2: after 7 days no reply
- No follow-up if suppression set or opt-out received
