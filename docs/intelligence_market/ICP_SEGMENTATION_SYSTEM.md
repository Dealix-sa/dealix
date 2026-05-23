# ICP Segmentation System

How Dealix turns "Saudi B2B" into operable sub-segments.

## 1. Segmentation axes

Each segment is defined on six axes:

1. **Sector** — from `SECTOR_RANKING_SYSTEM.md`.
2. **Size band** — headcount + revenue band.
3. **Maturity** — founder-led, scale-up, mature.
4. **Compliance posture** — light, regulated, audit-led.
5. **Buyer profile** — founder, CRO, head of ops, head of growth.
6. **Channel posture** — warm-only, mixed, openly-marketed.

## 2. Segment ID convention

`SEG-{sector}-{size}-{maturity}-{compliance}`
e.g. `SEG-erp-100to500-scaleup-regulated`.

## 3. Output

`growth/target_segments.csv` with columns:

```
segment_id,sector_id,size_band,maturity,compliance_posture,
buyer_role,channel_posture,persona_id,score,sample_account_count,
note,collected_at,source
```

## 4. Rules

- Every segment links to **one persona** (see Buyer Persona System).
- No segment ships with < 12 named example accounts.
- A segment with > 30 % fallback rows is `provisional` — not eligible
  for outbound until refreshed.

## 5. Use in distribution

- Outbound draft machines pick a segment, then a sub-list inside it.
- The trust gate enforces that segment-level approvals exist before
  any draft is generated.

## 6. Refresh

Quarterly review with the offer_architect agent + a founder check.
