# Decision Maker Personas

> **Status:** Default personas, calibrated for the agency wedge.
> **Adjust** after the first 5 deals based on who actually said yes.

## Persona 1 — "The Owner-Operator" (default for week 1)

- **Role:** Founder / co-founder / owner.
- **Age:** 28–45.
- **Background:** 5+ years in the agency, knows the craft, hates admin.
- **Mindset:** "I want to grow. I am the bottleneck."
- **Triggers:** lost a big client, end of quarter underperformance, scaling pain.
- **Fears:** another tool nobody uses; another consultant who doesn't understand agencies.
- **What they read:** WhatsApp, LinkedIn, Twitter, agency newsletters.
- **Best channel to reach:** warm intro, then email, then LinkedIn.
- **Best time to reach:** Sunday evening (week planning) or Tuesday morning.
- **Tone to use:** peer-to-peer, no jargon, direct.
- **Forbidden in copy:** "best practice", "synergy", "leverage", "AI will transform".

## Persona 2 — "The Head of Sales"

- **Role:** Sales lead, head of business development, VP sales.
- **Age:** 30–45.
- **Background:** came from sales at a larger company; runs the agency's growth.
- **Mindset:** "I have a number to hit. I need leverage."
- **Triggers:** missed quota, lost competitive deal, board pressure.
- **Fears:** missing targets; being seen as the bottleneck.
- **What they read:** LinkedIn, sales newsletters, podcasts.
- **Best channel:** LinkedIn DM (they live there), then email.
- **Best time:** Monday morning (planning) or Thursday morning (mid-week reset).
- **Tone to use:** peer-to-peer; numbers-friendly.
- **Forbidden in copy:** "AI is the future", generic "transformation" language.

## Persona 3 — "The General Manager"

- **Role:** GM, COO, ops director.
- **Age:** 35–50.
- **Background:** grew up in the agency, now manages the owner.
- **Mindset:** "I keep the trains running. Anything that makes my day easier is welcome."
- **Triggers:** team turnover, missed delivery, escalation from a client.
- **Fears:** being caught off-guard; losing control of the team.
- **What they read:** ops newsletters, WhatsApp groups, occasional LinkedIn.
- **Best channel:** email (formal) or WhatsApp (after consent).
- **Best time:** Sunday evening or early morning.
- **Tone to use:** respectful, formal, structured.
- **Forbidden in copy:** slang, "hustle", "grind".

## Persona 4 — "The Founder's Spouse / Partner"

- **Role:** Co-founder, often runs finance or operations.
- **Age:** 30–50.
- **Background:** married to or partnered with the founder; runs the back office.
- **Mindset:** "I see the numbers. I see the lost follow-ups. The founder is too busy."
- **Triggers:** monthly financial close, an angry client, a missed invoice.
- **Fears:** financial exposure; brand damage from a missed client.
- **What they read:** WhatsApp, occasional LinkedIn, banking apps.
- **Best channel:** warm intro from the founder; otherwise email.
- **Best time:** Sunday evening.
- **Tone to use:** respectful, calm, numbers-friendly.
- **Forbidden in copy:** "AI is smarter than your team" (this is insulting to them).

## Persona 5 — "The Skeptic" (you will meet this person)

- **Role:** Any of the above, but skeptical of "AI tools".
- **Age:** any.
- **Background:** been burned by tools or consultants.
- **Mindset:** "Show me, don't tell me."
- **Triggers:** they feel the pain themselves.
- **Fears:** wasting time on a demo that goes nowhere.
- **What they read:** peer reviews, case studies, anything with receipts.
- **Best channel:** referral from a peer; otherwise a low-friction email with a one-line offer.
- **Best time:** any, but keep the message very short.
- **Tone to use:** zero fluff. "3-day audit. 1-page report. If it's not useful, walk away."
- **Forbidden in copy:** any superlative ("amazing", "transformative", "guaranteed").

## How personas drive the copy

For each outreach draft, the script `outreach_draft_factory_dry_run.py` looks at the persona field and picks the tone, length, and CTA:

- **Owner-Operator:** 4-line email, peer tone, "free audit" CTA.
- **Head of Sales:** 6-line email, numbers-friendly, "pilot" CTA.
- **GM:** 8-line email, structured, "discovery call" CTA.
- **Spouse/Partner:** 5-line email, calm, "audit" CTA.
- **Skeptic:** 3-line email, zero fluff, "3-day audit" CTA.

Every draft is checked by `trust_preflight_dry_run.py` before it goes to the founder for review.

## When to update

- Every 10 deals, look at who actually said yes.
- If a persona is over-represented in conversions, lean into it.
- If a persona is under-represented, rewrite the copy or drop the persona.
- After 30 deals, retire the personas that did not work and add the ones that emerged.
