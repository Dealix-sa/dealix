# DEALIX Visual Identity

**Owner:** Brand Lead
**Source of truth:** `docs/brand/brand-tokens.json`

## Identity components

The Dealix visual identity has five components, each anchored to a token in `brand-tokens.json`:

1. **Wordmark** — DEALIX set in Inter Semibold, tracked tight, all caps
2. **Growth arrow** — the upward-right vector used as a brand mark when the wordmark is unavailable
3. **Emerald swoosh** — the curved accent that signals motion / pipeline
4. **Color palette** — Deep Navy, Emerald Teal, Soft Silver, Slate, White
5. **Lockup** — wordmark + tagline composition for hero placements

## Color palette

| Role | Name | Hex | Use |
|---|---|---|---|
| Primary surface | Deep Navy | `#0B1220` | Default dark background, hero sections, deck covers |
| Primary brand | Emerald Teal | `#00D1A1` | Calls to action, growth arrow, swoosh, metric highlights |
| Secondary surface | Slate | `#0F1726` | Cards on Deep Navy, table headers |
| Neutral text | Soft Silver | `#B2BBC6` | Body text on dark, secondary labels |
| Inverse | White | `#FFFFFF` | Body text on Deep Navy, light-mode surfaces |

Off-palette colors are not permitted in customer-facing assets. Internal whiteboarding may use any color but must be re-tokenized before export.

## Gradients

Two approved gradients only:

- **Pipeline gradient** — linear, Deep Navy `#0B1220` to Slate `#0F1726`, 180deg. Default backdrop for hero surfaces.
- **Growth gradient** — linear, Emerald Teal `#00D1A1` to a 60-percent-mix of Emerald Teal and Deep Navy, 135deg. Use behind the growth arrow only.

No third gradient. No radial gradients. No multi-stop rainbows.

## Wordmark

- Family: Inter, weight 600 (Semibold)
- Tracking: -10 (tight)
- Case: all uppercase
- Color: Emerald Teal on Deep Navy; Deep Navy on White; never on Soft Silver

## Growth arrow mark

- A 45-degree upward-right vector arrow, stroke weight 2 at 24px reference size.
- Always Emerald Teal. Monochrome variants: White on Deep Navy, Deep Navy on White.
- Use as a standalone mark only when the wordmark cannot fit (favicons, avatars, watermarks).

## Emerald swoosh

- A single curved stroke, Emerald Teal, used as a decorative element behind the wordmark in hero placements.
- Never as the primary brand mark.
- Never overlapping the wordmark or making the wordmark unreadable.

## Lockup

The standard hero lockup is:

```
DEALIX
INTELLIGENT DEALS. REAL GROWTH.
```

- Wordmark at top, tagline below, both centered or both left-aligned.
- Tagline set in Inter Medium, tracked +50, 28 percent of the wordmark cap height.
- Clearspace around the lockup equals one wordmark cap height on all sides.

## Asset export pipeline

Source files live in `assets/brand/source/`. The build exports to:

```
assets/brand/logo/
assets/brand/icon/
assets/brand/wordmark/
assets/brand/monochrome/
assets/brand/social/
assets/brand/favicons/
```

See `assets/brand/source/README.md` for the manual upload step.

## Failure mode

- Stretched or rotated wordmark.
- Off-palette accent color (orange, red, purple) inside a Dealix surface.
- Two gradients in the same composition.
- Growth arrow used at an angle other than 45 degrees.

## Recovery path

Replace the offending asset with the latest export from `assets/brand/`. If the source design is broken, request a re-export from Brand Lead before reuse.

## Disclaimer

Visual treatments do not constitute claims about deliverables. All performance language in branded surfaces must follow `docs/brand/DEALIX_BRAND_VOICE.md` and avoid guaranteed-result phrasing.
