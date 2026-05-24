## CHANGELOG — Revenue Marketing Engine Content Layer

### 2026-05-24 — Initial release

Initial release of Revenue Marketing Engine content layer — positioning, offers ladder, content factory, message variants, landing pages, outreach playbook, case study template, partner kit, market radar brief, trust marketing, dashboard glossary, anti-vanity rules.

**Files included:**

- `README.md` (bilingual overview + folder index)
- `positioning.md` (bilingual positioning matrix, taglines, trust pillars, anti-claims)
- `offers_ladder.md` (five-rung offer ladder, 17 offers, full bilingual table)
- `content_factory.md` (10 content pillars, content card template, anti-vanity rules)
- `message_variants.md` (3 angles per core offer × 6 core offers)
- `landing_pages/revenue-hunter.md` (Revenue Hunter Pilot landing copy)
- `landing_pages/ai-trust-kit.md` (AI Trust Kit landing copy)
- `landing_pages/agency-white-label.md` (Agency White-label landing copy)
- `outreach_playbook.md` (founder-led, manual, no automation)
- `case_study_template.md` (bilingual, with Jinja2 placeholders + sample filled)
- `partner_kit.md` (agency/consultant/training-partner kit)
- `market_radar_brief.md` (Saudi/MENA market signal radar)
- `trust_marketing.md` (4 trust messages + 5 trust assets + anti-claims)
- `dashboard_glossary.md` (16 metrics with bilingual definitions)
- `anti_vanity_rules.md` (pairing rule + forbidden solo celebrations)
- `CHANGELOG.md` (this file)

**Items flagged for founder review:**

- Public publication of starting prices in `offers_ladder.md` and landing pages.
- Final `{{partner_share_pct}}` values, `{{min_partner_share_pct}}`, `{{max_partner_share_pct}}` in `partner_kit.md`.
- Naming any customer in `case_study_template.md` (default is case-safe).
- Activating the 999 SAR Revenue Hunter Pilot checkout link (depends on Moyasar activation per `DEALIX_COMPANY_OPERATIONAL_STATE.md`).

**Cross-links to engineer scope (do not edit):**

- `dealix/revenue_marketing/scoring.py` (referenced from `outreach_playbook.md`, `dashboard_glossary.md`)
- `api/routers/revenue_marketing.py` (referenced indirectly from dashboard glossary)
- `dealix/revenue_marketing/seeds/` (seed YAML for offers + content cards, engineer-owned)

**Conventions applied:**

- AR primary, EN parallel, in every customer-facing file.
- Every customer-facing file ends with the disclosure line: "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".
- No real customer names. All numbers in placeholders.
- No forbidden anti-claims (see `trust_marketing.md`).
- All file names lowercase with hyphens, except `README.md` and `CHANGELOG.md` per repo convention.

---

**Disclosure / إفصاح:** Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
