# Content Calendar System

The Content Calendar is the single forward view of every artifact Dealix plans to publish across every owned and earned surface.

**Source of truth:** `$PRIVATE_OPS/content_calendar.csv`
**Owner:** Marketing Lead
**Trust gate:** A1 — calendar entries become committed once the founder approves the weekly plan.

## Time horizons

| Horizon | Use |
|---------|-----|
| 1 week ahead | Committed — drafted or in draft |
| 4 weeks ahead | Planned — brief written |
| 12 weeks ahead | Themes — direction only |
| 12 months ahead | Beats — quarterly arcs |

## Row schema

```
calendar_id, planned_at, surface, format, language,
title_en, title_ar, brief_path, owner, status,
linked_offer, linked_proof, approval_class, published_at
```

`status` moves through: `theme` → `brief` → `draft` → `review` → `approved` → `published` → `archived`.

## Slot allocation

A balanced week mixes:

| Type | Share |
|------|-------|
| Founder voice | 40% |
| Sector report excerpt | 20% |
| Case-safe pattern | 15% |
| Product explanation | 15% |
| Operational note (e.g. eval result) | 10% |

If a week tips above 50% promotional content, the calendar rebalances toward sector reports and case-safe patterns.

## Cadence

- **Weekly planning:** Monday morning. Marketing Lead presents the week. Founder approves.
- **Monthly review:** first Monday of the month. Calendar measured against actual publication and lead generation.
- **Quarterly arc:** first week of quarter. Themes set for the next 12 weeks.

## Failure modes

- **Drift to "always promo":** more than 50% of a week's slots are promotional. Detection: slot audit. Recovery: rebalance with sector or case-safe content.
- **Empty slots:** scheduled slot is empty at T-24h. Detection: nightly job. Recovery: founder voice or sector excerpt is the fallback; surface stays balanced.
- **Bilingual lag:** EN published, AR scheduled days later. Detection: parity check. Recovery: AR is a publish blocker.

## Recovery path

If the calendar diverges from actual publication, the Marketing Lead resets the week to actuals and re-plans forward.

## Metrics

- Plan-vs-actual publication rate.
- Slot-balance score.
- Lead attribution by slot (estimated).
- Approval cycle time (median hours).

## Disclaimer

The calendar is intent. Publication is the founder's decision. Dealix does not guarantee revenue from any calendar entry. Estimated value is not Verified value.
