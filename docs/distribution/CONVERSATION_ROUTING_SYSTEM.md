# Conversation Routing System

## Purpose
Route every reply into the correct next action.

## Reply Types

### Positive
Action: Prepare sample or book call.

### Asked for More Info
Action: Send one-page explanation or mini sample.

### Pricing Question
Action: Qualify and send price band or proposal draft.

### Not Now
Action: Move to nurture.

### Not Interested
Action: Add to suppression or lost.

### Referral
Action: Ask for right contact.

### Objection
Action: Classify objection and respond.

## Rules
- No reply left without `next_action`.
- Positive replies get same-day action.
- Objections update `objection_patterns.md`.
- Lost leads update `win_loss_log.md`.

## Evidence
- `private-ops/outreach/reply_log.csv`
- `private-ops/sales/objection_patterns.md`
- `private-ops/sales/win_loss_log.md`
- `private-ops/outreach/suppression_list.csv`
