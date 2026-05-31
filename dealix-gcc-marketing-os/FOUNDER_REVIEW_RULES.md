# Founder Review Rules

## The Core Rule
**You review. You decide. You approve. The system never sends without you.**

Every draft has `send_allowed: false` until you change it to `true`.

## What the System Delivers to You Daily

- Ranked list of 150–300 founder-ready drafts
- Each with: company brief, pain angle, offer, language, channel, quality score
- Top 25 highlighted with full draft text
- Risk flags for anything needing extra care
- Send recommendations by channel

## How to Review

1. Open `outputs/reports/founder_report_YYYY-MM-DD.md`
2. Start from Priority 1 (highest score)
3. Read the draft — is it accurate? Does it feel right for this company?
4. If yes: set `send_allowed: true` in the corresponding queue record
5. If no: add a note and it goes to `rejected/` for learning

## What Makes a Draft Worth Sending

- The company context is specific and accurate
- The pain angle feels real for this sector
- The language sounds natural (not translated)
- The offer is clear and low-risk
- The CTA is one simple ask
- The opt-out is present
- You would be comfortable if this person called you about it

## Red Flags — Send With Extra Care or Hold

- Personal employee email (not role-based)
- Law firm or healthcare company without privacy-first language
- Company in Qatar, Oman — high consent requirement countries
- Score below 75
- Any draft flagged by compliance gate

## Sending Rate Guidance

| Week | Max Email Sends/Day | Notes |
|---|---:|---|
| Week 1 | 50–100 | Best drafts only |
| Week 2 | 100–200 | If bounce < 3% |
| Week 3 | 200–300 | Segmented by country |
| Week 4 | 300–500 | If reputation is clean |

**These are maximums, not targets.** Send fewer with better targeting.

## Multi-Channel Distribution

Don't put all sends on email. Distribute:
- 40% email
- 27% LinkedIn drafts
- 17% website contact forms
- 10% WhatsApp Business (published business contacts only)
- 7% referral/intro requests

## Suppression

Any contact who opts out → immediately added to suppression.jsonl → never contacted again.
Check `memory/suppression.jsonl` regularly.
