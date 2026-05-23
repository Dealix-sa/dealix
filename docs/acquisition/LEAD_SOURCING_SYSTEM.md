# Lead Sourcing System

## Purpose
Generate qualified leads ethically and at a controlled pace.

## Allowed sources
1. **Founder warm list** — people Sami already knows and has reason to contact.
2. **Public business directories** — chambers of commerce, sector associations.
3. **Conferences and events** — face-to-face conversations.
4. **Partner referrals** — through formal partner agreements.
5. **Inbound** — content-driven inbound from `docs/content/CONTENT_TO_PIPELINE_SYSTEM.md`.

## Forbidden sources
- LinkedIn scraping or bulk scraping of any platform.
- Purchased contact lists.
- Cold WhatsApp / SMS to numbers harvested without consent.
- Scraping competitor customer logos for prospect mining.

## Process
1. Identify a sector from the Primary ICP.
2. Hand-pick 10 companies per session.
3. Add each to `pipeline/pipeline_tracker.csv` with stage=New, priority=B (default).
4. Promote to priority=A only after a positive signal (intro, prior conversation, public buying signal).
5. Update `acquisition/source_performance.csv` weekly.

## Volume targets
- Week 1: add 25 leads.
- Week 2–4: keep pipeline ≥ 50 active opportunities.
- Once 1 paying customer: focus on lookalikes of that customer.

## Hygiene
- No duplicate companies in the tracker.
- Stale leads (no touch for 30 days) are moved to `Closed-lost` or promoted with a new next_action.
- Personal data: minimum necessary (name, role, email or phone).
