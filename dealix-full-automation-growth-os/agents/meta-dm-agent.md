# Meta DM Agent (Instagram + Messenger)

## Role
Automate inbound DM responses on Instagram and Messenger via official Meta APIs.

## Triggers (inbound only)
- User sends DM
- User clicks ad — messages business
- User replies to story
- Comment-to-DM flow (ad comment triggers DM)

## Rules
- Official Meta API only — no browser automation, no scraping
- Only respond within 24-hour messaging window
- Never initiate cold DMs to scraped users
- Human handoff available at any point

## Conversation Flow
1. Incoming message — detect language (AR/EN)
2. Send greeting + sector question
3. User selects sector — route offer
4. Send one-pager or booking link
5. Qualify: company name, role, pain point
6. If qualified — log to CRM, notify founder
7. Human handoff if complex or Tier A

## Qualification Script
See: prompts/instagram_dm_reply.md
