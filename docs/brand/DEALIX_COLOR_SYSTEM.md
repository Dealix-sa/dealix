# DEALIX Color System

**Owner:** Brand Lead
**Source of truth:** `docs/brand/brand-tokens.json`

## Primary palette

| Token | Hex | Role |
|---|---|---|
| `colors.deepNavy` | `#0B1220` | Primary background, hero surfaces |
| `colors.emeraldTeal` | `#00D1A1` | Primary brand accent, CTAs |
| `colors.slate` | `#0F1726` | Secondary surface, card background on Deep Navy |
| `colors.softSilver` | `#B2BBC6` | Body text on dark, secondary labels |
| `colors.white` | `#FFFFFF` | Inverse surface, body text on Deep Navy |

## Semantic palette

These are derived from the primary palette and used for state communication.

| Role | Token name | Hex | Use |
|---|---|---|---|
| Success | `semantic.success` | `#00D1A1` | Deal won, sprint complete, KPI met (= Emerald Teal) |
| Warning | `semantic.warning` | `#F5B544` | Approval pending, deadline near |
| Risk | `semantic.risk` | `#E5484D` | Policy breach, missed gate, trust violation |
| Info | `semantic.info` | `#5BA9FF` | Neutral note, system message |
| Muted | `semantic.muted` | `#5C6675` | Disabled, archived, low-signal |

Risk red is reserved. Never use it for decoration. Its presence means a trust or governance breach.

## Contrast ratios (WCAG AA)

All text-on-surface combinations must meet AA. AAA is preferred for body text.

| Foreground | Background | Ratio | AA pass |
|---|---|---|---|
| White `#FFFFFF` | Deep Navy `#0B1220` | 17.8:1 | AAA |
| Soft Silver `#B2BBC6` | Deep Navy `#0B1220` | 9.4:1 | AAA |
| Emerald Teal `#00D1A1` | Deep Navy `#0B1220` | 9.1:1 | AAA |
| Deep Navy `#0B1220` | White `#FFFFFF` | 17.8:1 | AAA |
| Deep Navy `#0B1220` | Emerald Teal `#00D1A1` | 9.1:1 | AAA |
| Emerald Teal `#00D1A1` | White `#FFFFFF` | 2.0:1 | Fail — never use |
| Soft Silver `#B2BBC6` | White `#FFFFFF` | 1.9:1 | Fail — never use |

The two failing combinations are common mistakes. Avoid them.

## State pairs

| State | Surface | Text |
|---|---|---|
| Default | Deep Navy | White |
| Card on Default | Slate | White |
| Hover (dark) | Slate (+4 percent lighten) | White |
| Active CTA | Emerald Teal | Deep Navy |
| Disabled | Slate | Soft Silver (50 percent opacity) |
| Risk surface | `#1E0B0D` (Deep Navy mix with Risk) | Risk red |

## Data visualization

Default chart palette, in order:

1. Emerald Teal `#00D1A1`
2. Soft Silver `#B2BBC6`
3. Info Blue `#5BA9FF`
4. Warning Amber `#F5B544`
5. Risk Red `#E5484D` (only when the data point is itself a risk)

Never use more than five distinct colors in a single chart. Use opacity steps if more series are needed.

## Dark-mode default

Dealix is a dark-first brand. Light-mode is supported but secondary. All product UI defaults to Deep Navy with Emerald Teal accents.

## Failure mode

- Emerald Teal text on White (contrast fail).
- Soft Silver text on White (contrast fail).
- Off-palette gradient stops.
- Risk red used for a non-risk highlight.

## Recovery path

1. Re-check the asset against the contrast table.
2. Swap to a passing pair.
3. If a designer needs an off-palette color, escalate to Brand Lead. Do not invent.

## Disclaimer

The color system carries the brand promise of trust. Misusing risk red — for example, to draw attention to a normal feature — erodes the signal. Treat it as a load-bearing semantic, not a decoration.
