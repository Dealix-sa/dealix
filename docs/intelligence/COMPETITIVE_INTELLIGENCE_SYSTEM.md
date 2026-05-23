# Competitive Intelligence System

> The mechanism by which Dealix tracks, reframes, and learns from competitors. Never disparages.

## 1. Tracked categories

| Category | Examples (illustrative; refreshed in registry) |
|---|---|
| CRM | HubSpot, Salesforce, Zoho |
| Sales engagement | Outreach, Salesloft, Apollo Engage |
| Marketing automation | Marketo, HubSpot Marketing |
| AI SDR | Artisan, 11x.ai |
| Lead generation | Apollo, Cognism |
| Local KSA consultancies / agencies | (named per engagement; not published) |
| Custom builds | In-house RevOps teams |

## 2. Per-competitor record

```yaml
id: competitor_xxx
name: <public>
category: <one of §1>
geo_presence_ksa: yes / no
buyer_perception: <one paragraph>
their_best_frame: <quote>
our_reframe: <one line from COMPETITIVE_NARRATIVE.md>
proof_to_show: <link>
pricing_posture: <link to PRICING_GUARDRAILS.md>
last_updated: <date>
source: signal | fallback
```

## 3. Surfaces

- Read-only dashboard inside `/growth`.
- Battle cards delivered to the founder via the daily brief.
- Drafted reframes recorded in `growth/competitor_reframes.csv`.

## 4. Rules

- We never name a competitor in marketing without founder + Brand Guardian approval.
- We never quote a competitor without source.
- We never make a price-comparison claim without a current matched-spec table.

## 5. Cadence

- Monthly competitor scan.
- Quarterly reframe refresh.
- Ad-hoc on lost-deal escalation.

## 6. Trust posture

Competitive intel never triggers an action; it informs the founder.
