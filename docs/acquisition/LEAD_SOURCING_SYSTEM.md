# Lead Sourcing System

> Where leads come from, how they're captured, and how they enter qualification.

## Sources (allow-listed)

1. **Public LinkedIn search** (founder-driven, allow-listed filters)
2. **Public company websites** (about pages, hiring pages, press)
3. **Public registries** (chambers of commerce, trade associations, official rosters)
4. **Sector publications** (Aleqtisadiah, Argaam, sector reports)
5. **Personal network** (warm intros, referrals, advisor network)
6. **Inbound** (LinkedIn DMs, website form, content engagement)
7. **Partner referrals** (per partner agreement)

## Forbidden Sources

- Purchased lists
- Scraped contact databases
- Leaked datasets
- Anything that can't be cited publicly
- Anything from a competitor's customer list (even if visible)

## Daily Sourcing Volume

- Target: 25 new sourced leads per week (5/day, Sun–Thu)
- Quality bar: each lead has a real company + a real role + a real signal
- Stored in `pipeline/lead_sources.md` (private) with source URL

## Per-Lead Capture Schema

```yaml
lead_id: L-2026-NNNN
captured_at: 2026-MM-DD
source: linkedin | website | registry | publication | network | inbound | partner
source_url: https://...
company:
  name: ...
  sector: ...
  size_employees: ...
  revenue_band: SAR ...
  city: Riyadh | Jeddah | Dammam | ...
buyer:
  name: ...
  role: ...
  authority_level: founder | head_of_sales | other
trigger_signal: |
  Concrete reason we noticed them today
warm_path: true | false (with intro person name if true)
fit_signals: []
risk_signals: []
```

## Sourcing Discipline

- Every captured lead has a source URL (audit-traceable)
- Every lead is added to the pipeline tracker the same day
- Every lead gets a fit score within 24 hours
- Every lead either qualifies, nurtures, or suppresses within 48 hours

## Tools Used

- LinkedIn (manual + Sales Navigator if subscribed)
- Public registries (free)
- Sector publications (RSS / manual)
- `dealix/agents/lead_finder_agent.py` (when present) — wraps allow-listed sources, never scrapes

## Tools NOT Used

- Apollo / Lusha / ZoomInfo for contact data without prior consent
- Scrapers of any kind
- Buying lists from "Saudi B2B" vendors
- Anyone offering "enriched" data without source citations

## When Sourcing Stalls

If weekly target missed for 2 weeks:
1. Check source mix — are we leaning too hard on one channel?
2. Check ICP definition — too narrow?
3. Check the sector playbooks — are we sourcing where buyers are?
4. Add one new allow-listed source after research; do not lower the quality bar

## Inbound Handling

Inbound is precious — treat it differently:
- Reply within 24 hours
- Auto-qualify with extra weight on intent (`+15` to fit score for inbound)
- Skip Free Diagnostic step if appropriate; go directly to Sprint conversation
- Log inbound source in detail — what content drew them?

## Sourcing Review Cadence

- Daily: 5 leads sourced (logged before EOD)
- Weekly: source mix + quality audit
- Monthly: source channel ROI — which sources convert?

## What This System Refuses

- Volume without quality (quality wins long-term)
- Anonymous leads (every lead has a real buyer name)
- Cross-border sourcing this quarter (Saudi only)
- "Maybe in 6 months" sources (they go to nurture, not pipeline)
