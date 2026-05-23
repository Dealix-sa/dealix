# Content Calendar System

> The weekly cadence that turns themes into shipped content.

## 1. Surfaces

| Surface | Format | Cadence |
|---|---|---|
| LinkedIn (founder) | Short post (90-220 words) | 3 × per week |
| LinkedIn (Dealix) | Long post / carousel | 1 × per week |
| Newsletter | Sector or operating insight | 1 × per 2 weeks |
| Landing | New section or proof block | 1 × per 2 weeks |
| Sector report | Long-form PDF / HTML | 1 × per month |

## 2. Slot definition

```yaml
slot:
  date: YYYY-MM-DD
  surface: linkedin_founder | linkedin_dealix | newsletter | landing | sector_report
  theme: Built on Trust | Driven by Growth | ...
  language: en | ar | bilingual
  status: idea | draft | brand_check | trust_check | scheduled | published
  proof_required: yes / no
  owner: founder | brand_guardian | content_strategist
  source: signal | fallback
```

## 3. CSV file

`marketing/content_calendar.csv` columns:

```
slot_id, date, surface, theme, language, status, proof_required, owner, draft_link, source
```

## 4. Brand & trust gates

- Brand check before drafts move to `scheduled`.
- Trust check (claims have evidence; no guarantees) before drafts move to `scheduled`.
- Audit event on `published`.

## 5. Cadence

- Sunday: weekly plan.
- Daily: drafting and review.
- Friday: review what shipped vs. plan; record learnings.
