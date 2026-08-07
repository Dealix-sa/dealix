# 00 — Media & Social OS

نظام الإعلام والسوشل ميديا — تخطيط ونشر يدوي فقط. لا أتمتة نشر، لا API نشر، لا تفاعل مصطنع.
The media & social operating system — **planning + manual posting only**. No auto-post, no
platform API posting, no synthetic engagement.

## Principles
- **Plan, don't post.** Tools generate a calendar; a human posts each item.
- **Founder-led brand.** Founder POV drives reach; company posts support.
- **Claim-safe.** Forbidden claims are rejected at planning time.
- **Bilingual.** AR + EN, alternating by audience.

## Content pillars
1. Category education — Revenue Intelligence for Saudi B2B.
2. Saudi B2B proof & data (anonymized).
3. Approval-first AI doctrine.
4. Founder POV / lessons.
5. Customer outcomes (anonymized, consented).

## Cadence (per week)
- 5 founder posts
- 3 company posts
- 1 long-form

## Config & generation
- Config: [`config/media_social_calendar.json`](../../config/media_social_calendar.json) (`auto_post: false`)
- Generate: `python scripts/media_social_calendar_generate.py`
- Verify: `python scripts/media_social_verify.py`
- Output: `outputs/media_social/calendar_30_day.json`

## Components
- Content calendar (30-day) — generated.
- Press kit — `docs/BRAND_PRESS_KIT.md`.
- Ads readiness gate — [`15_ADS_READINESS_GATE.md`](15_ADS_READINESS_GATE.md).
- Founder brand pillars — this document.

## Guardrails (NO-GO)
- No auto-posting / scheduling bots.
- No platform API posting from this repo.
- No buying engagement; no synthetic interactions.
- No paid ads live launch before the ads gate.
