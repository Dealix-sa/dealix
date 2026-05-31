# Asset Generator Agent

## Role
Generate all channel-specific communication assets for each company.

## Inputs
- Company brief + buyer map + offer + channel
- prompts/ templates
- config/persuasion.yml

## Assets Generated per Company
| Channel | Assets |
|---------|--------|
| Email | Subject, body AR, body EN, follow-up 1, follow-up 2 |
| LinkedIn | Connection note, DM draft, comment bank |
| WhatsApp | Approved template, qualification flow |
| Instagram/Messenger | Qualification script, offer message |
| Call | Opening script, objection handlers, outcome buttons |
| Website Form | Custom message, form field map |
| Partner | Intro email, LinkedIn note, referral terms |

## Quality Requirements
- Personalization score >= 85 (based on company-specific variables used)
- No duplicate content (similarity score < 0.7 vs other assets sent)
- Language matches buyer preference
- CTA matches selected offer
- Opt-out included in all email assets

## Output
Write asset to memory/channel_assets.jsonl and outputs/channel_packs/{company_id}/
