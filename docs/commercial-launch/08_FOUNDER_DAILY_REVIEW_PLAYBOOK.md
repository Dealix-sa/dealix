# Founder Daily Review Playbook

> AI drafts and ranks. **You** review and approve. The system never sends.

## Morning (20–30 min)
1. Run `python scripts/commercial_generate_400_drafts.py --target 400`.
2. Open `outputs/commercial_launch/<today>/top_50_priority.md`.
3. Confirm `safety_audit.json` shows `verdict: PASS`.
4. Approve the top 20–50 drafts manually (your judgement, your account).
5. Note any draft that needs research before contact.

## Midday
- Manually copy/paste approved drafts (email/LinkedIn) — **you** send, not the system.
- Update CRM stages (`config/crm_pipeline_schema.json`).
- Update the suppression list for anyone who asks to stop.

## Evening
- Classify replies (positive/negative) into `daily_metrics.json` as manual input.
- Capture new objections into `11_OBJECTION_HANDLING.md`.
- Pick tomorrow's vertical focus and update `next_actions.md`.

## Approval rules
- Every draft is `requires_founder_approval=true`; nothing is `send_allowed`.
- A rejected draft carries a `rejection_reason` and never re-enters the send path.
- If a draft mentions a prior touch ("following up"), confirm that touch truly happened.

## Daily safety check
Run `python scripts/commercial_safety_audit.py` — it must return PASS before you
act on any draft.
