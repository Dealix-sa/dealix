# Trigger Event System

> Watches for events in the world that make an account momentarily more receptive.

## 1. Tracked event types

| Event | Source | Signal weight |
|---|---|---|
| New funding | Public announcements | 0.8 |
| Senior hire (CEO, CRO, COO, Head of Growth) | Public registries, news | 0.7 |
| New office / expansion | News, registries | 0.6 |
| Tech adoption (CRM switch, new ERP) | Job posts, RFPs | 0.6 |
| Regulatory move | Government, news | 0.5 |
| Product launch | Company news | 0.4 |
| Award / certification | Industry signal | 0.3 |
| Customer-stated trigger | Intake form / sales note | 1.0 |

## 2. Per-event record

```yaml
event_id: evt_xxxx
account_id: acc_xxxx
type: funding | hire | expansion | tech | regulatory | launch | award | customer
description: <one line>
date: YYYY-MM-DD
weight: 0.0-1.0
source: <url or signal>
trust_check_passed: true
```

## 3. Surfaces

- Daily feed at `/growth`.
- Per-account view in Sales Cockpit.
- Drives account scoring composite.

## 4. Outputs

`growth/trigger_events.csv` columns:

```
event_id, account_id, type, description, date, weight, source
```

## 5. Cadence

- Daily refresh (05:00 KSA).
- Old events decay at 0.9 / day after 14 days.

## 6. Trust posture

A trigger never sends an outreach. It raises the score and may be cited in a draft.
