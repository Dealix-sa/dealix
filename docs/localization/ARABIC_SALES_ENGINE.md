# Arabic Sales Engine

## Doctrine Anchor
- Non-negotiables touched: #2 (no value claim without source evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: approval-first for external action.

## Purpose

Make Dealix sell naturally in Arabic and English for Saudi B2B buyers. The Arabic side is not a translation layer — it is a first-class sales motion with its own tone, vocabulary, sector-specific phrasing, and proof artifacts. Literal translation from English is a failure mode.

## Assets

| Asset | Description |
|-------|-------------|
| Arabic outreach | Sector-specific outbound drafts |
| English outreach | Counterpart drafts for English-speaking buyers |
| Bilingual proposals | Proposal pack with parallel Arabic and English |
| Arabic landing copy | Sector-specific landing pages |
| Sector-specific Arabic proof | Case studies and proof artifacts in Saudi business Arabic |
| Saudi business tone guide | Standards for register, formality, and sector-specific terms |
| Sector vocabulary lists | Industry-correct terms (financial services, healthcare, retail, manufacturing, government, etc.) |

## Tone Rules

- Arabic must sound like Saudi business communication, not Modern Standard literary Arabic and not Egyptian colloquial.
- Tone shifts by sector and buyer seniority (procurement vs CEO vs CTO).
- Honorifics and salutations follow Saudi business conventions.
- No literal translation from English structures (sentence rhythm, idioms, marketing slogans).
- Numbers and dates use the convention the reader expects in business documents.
- Brand and product names retain their English form unless an established Arabic form exists.

## Core Rules

- An Arabic asset that started as an English draft is rewritten by a native Saudi-business reader, not run through an LLM and shipped.
- A public bilingual claim is reviewed in both languages; an inconsistency between Arabic and English versions is a quality breach.
- Arabic outreach is approval-gated like any other outreach.
- Arabic feedback from buyers is logged in its original form (no translation loss).
- The bilingual tone guide is a living document; reviewers add new sector terms as they encounter them.

## Operating Cadence

| Cadence | What happens |
|---------|--------------|
| Per outbound campaign | Arabic and English drafts are both reviewed |
| Weekly | New sector terms from buyer conversations are added to the vocabulary list |
| Monthly | Tone guide review: any drift, any new register adjustments |

## Runtime Wiring

- Existing Arabic operational artifacts (cross-link): `docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md`, `docs/ops/FOUNDER_REVENUE_DAY_ONE_AR.md`, `README.ar.md`, and `_AR.md` companions across the documentation.
- Existing localization cluster: `docs/localization/` (existing).
- Existing Arabic ABM motion: `docs/commercial/operations/targeting/ABM_WAVE1_ICP_AR.md`.
- Outreach approval (Arabic drafts pass through the same Approval Center): `auto_client_acquisition/approval_center/approval_policy.py`.
- Evals (bilingual quality suite): `docs/evals/AI_EVAL_RED_TEAM_SYSTEM.md`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Bilingual quality eval pass rate | ≥ documented threshold | eval results |
| Arabic positive-reply rate vs English | tracked per sector; not expected to be equal — sectors differ | reply router |
| Inconsistencies caught between AR / EN versions | tracked; root-cause reviewed | reviewer notes |
| Sector vocabulary entries added per quarter | non-zero | tone guide |

## Cross-Links

- `docs/localization/` (existing)
- `docs/distribution/DEALIX_DISTRIBUTION_OS.md`
- `docs/distribution/EMAIL_DELIVERABILITY_SYSTEM.md`
- `docs/distribution/ABM_STRATEGIC_ACCOUNT_MACHINE.md`
- `docs/intelligence/COMPETITIVE_INTELLIGENCE_MACHINE.md`
- `docs/evals/AI_EVAL_RED_TEAM_SYSTEM.md`
- `docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md`

## Open Items

- A canonical "Saudi business tone guide" file in `docs/localization/` does not yet exist as a single source-of-truth; tone conventions live across reviewer notes.
- Sector-specific vocabulary lists are partial.
- LLM-generated Arabic drafts still benefit from a human reviewer; a documented two-step review process (LLM draft → native review → approval) is open.
- An Arabic landing-page review checklist is open.
