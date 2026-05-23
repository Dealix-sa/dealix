# Dealix Color System

## 1. Primary palette

| Token | Hex | Role |
|---|---|---|
| Deep Navy | `#0B1220` | Page background, mark panel, primary surface. |
| Emerald Teal | `#00D1A1` | Accent, growth, success, CTA fill. |
| Soft Silver | `#B2BBC6` | Secondary text, dividers, mark outline. |
| Slate | `#0F1726` | Card surface, panel inset. |
| White | `#FFFFFF` | Primary text on dark, mark inversion. |

The palette is intentionally narrow — four anchors plus white. Anything
else is a derived semantic token, not a new brand colour.

## 2. Semantic tokens

```
--dlx-bg              #0B1220   page background
--dlx-surface         #0F1726   card / panel
--dlx-surface-alt     #121C30   raised / hover surface
--dlx-border          #1B2740   hairlines, dividers
--dlx-text-primary    #FFFFFF   headings, key numbers
--dlx-text-secondary  #B2BBC6   body, captions
--dlx-accent          #00D1A1   primary CTA, growth, success
--dlx-accent-pressed  #00B98D   pressed / focus
--dlx-warning         #F2C84B   warning surface
--dlx-danger          #FF5A5F   destructive, kill switch
--dlx-info            #5AB0FF   informational
```

## 3. Data visualization order

`#00D1A1` → `#5AB0FF` → `#F2C84B` → `#FF8A65` → `#B2BBC6` → `#A78BFA`

Use sequential teal-to-silver for funnels. Use the categorical order
above for bars / pies / segments.

## 4. Contrast targets

- Body text on `--dlx-bg` ≥ **4.5 : 1** (WCAG AA normal text).
- Large display text ≥ **3 : 1**.
- Accent on navy: `#00D1A1` on `#0B1220` ≈ 8.6 : 1 — passes AA + AAA.
- Soft silver on navy: `#B2BBC6` on `#0B1220` ≈ 8.4 : 1 — passes AAA.

Run `python scripts/verify_brand_system.py` to re-check contrast on
every change.

## 5. Banned colour patterns

- ❌ Pure black `#000000` as a UI surface.
- ❌ Bright red CTAs (we reserve red for destructive only).
- ❌ Yellow-on-white text (fails contrast).
- ❌ Custom one-off hex codes inside components — always reference a
  semantic token.
