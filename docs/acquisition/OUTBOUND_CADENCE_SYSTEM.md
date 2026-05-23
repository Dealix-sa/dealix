# Outbound Cadence System

## Purpose
Define the pace and shape of founder-led outbound so it stays personal, controlled, and respectful.

## Cadence shape (per lead)
- Touch 1: hand-written DM / email referencing one specific signal about the company.
- Touch 2 (3–5 days later, if no reply): a short follow-up with one extra angle.
- Touch 3 (10–14 days later, if no reply): an "is this the wrong time?" close.
- Touch 4: no further outbound for 90 days unless lead engages.

## Daily volume cap
- Maximum 10 brand-new outbound touches per day.
- Maximum 10 follow-up touches per day.
- Maximum 20 outbound interactions total per day.

This cap protects quality and avoids spam patterns.

## Channel order
1. Warm intro / referral (always first if available).
2. Email.
3. LinkedIn DM.
4. WhatsApp (only if the contact has shared their number willingly).
5. Phone (only after a written reply).

## Content rules
- Personalized opener (no copy-paste body).
- One clear ask per message.
- Proof level must match `docs/content/PROOF_LEVEL_POLICY.md`.
- No fabricated stats, no name-dropping without permission.

## Logging
- Every touch goes into `revenue/revenue_action_log.csv`.
- Reply rate and conversion are summarized in `acquisition/message_performance.csv`.

## Automation policy
- No automated sending. No mail-merge tools.
- Drafting can be assisted by an AI sub-agent; sending is always by the founder.

## Failure modes
- Volume > cap → quality drops → reply rate falls.
- Templated opener → recipient flags as spam → reputational damage.
- Mismatched proof claims → Trust workflow violation.
