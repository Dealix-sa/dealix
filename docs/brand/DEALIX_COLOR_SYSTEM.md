# Dealix Colour System

The Dealix palette is **dark, enterprise, premium**. One bold accent (Emerald Teal), one neutral mid-tone (Soft Silver), and a navy/slate foundation.

## 1. Core palette

| Token             | HEX        | RGB              | Use                                              |
|-------------------|------------|------------------|--------------------------------------------------|
| Deep Navy         | `#0B1220`  | `11, 18, 32`     | Primary background, brand surfaces, dark mode    |
| Emerald Teal      | `#00D1A1`  | `0, 209, 161`    | Primary accent, CTA, growth/success indicators   |
| Soft Silver       | `#B2BBC6`  | `178, 187, 198`  | Secondary text, dividers, muted icons            |
| Slate             | `#0F1726`  | `15, 23, 38`     | Card surfaces, modals, secondary background      |
| White             | `#FFFFFF`  | `255, 255, 255`  | Primary text on dark surfaces, headings          |

## 2. Semantic tokens

Semantic tokens are what the application/console references — they map onto the core palette and provide an indirection layer so we can refine the palette without rewriting every component.

| Semantic token        | Maps to        | Use                                              |
|-----------------------|----------------|--------------------------------------------------|
| `--dealix-bg`         | Deep Navy      | Page / shell background                          |
| `--dealix-surface`    | Slate          | Card, modal, section background                  |
| `--dealix-accent`     | Emerald Teal   | CTA, links, focus rings, growth indicators       |
| `--dealix-text`       | White          | Primary text on dark surfaces                    |
| `--dealix-text-muted` | Soft Silver    | Secondary text, labels, hints                    |
| `--dealix-border`     | rgba silver    | Subtle borders, dividers                         |
| `--dealix-success`    | Emerald Teal   | Success states (mirrors accent)                  |
| `--dealix-warning`    | `#F6B73C`      | Warning states (amber, used sparingly)           |
| `--dealix-danger`     | `#FF5C7A`      | Error / refusal / kill switch                    |
| `--dealix-muted`      | Slate          | Disabled controls, deferred items                |

## 3. Contrast (WCAG)

Every text-on-background pair must meet WCAG **2.1 AA** contrast:

- **Body text**: ≥ 4.5:1
- **Large text** (≥ 18.66px bold or ≥ 24px regular): ≥ 3:1
- **UI components & graphical objects**: ≥ 3:1

Verified core combinations:

| Foreground   | Background    | Ratio   | Pass               |
|--------------|---------------|---------|--------------------|
| White        | Deep Navy     | ~17.5:1 | AAA body           |
| White        | Slate         | ~16.4:1 | AAA body           |
| Soft Silver  | Deep Navy     | ~9.8:1  | AAA body           |
| Soft Silver  | Slate         | ~9.2:1  | AAA body           |
| Emerald Teal | Deep Navy     | ~9.2:1  | AAA body           |
| Emerald Teal | White         | ~2.3:1  | **Large text only** — never use teal-on-white for body |
| Deep Navy    | White         | ~17.5:1 | AAA body           |
| Deep Navy    | Emerald Teal  | ~9.2:1  | AAA body — teal CTA fill, navy label                   |

**Never** use Soft Silver on White (≈1.9:1) for body. **Never** use Emerald Teal on White for body — only on large display text where the contrast is acceptable and the size is verified.

## 4. Usage rules

- **One accent** — Emerald Teal is the only accent. Do not introduce a secondary accent without founder approval.
- **Backgrounds are dark by default** — light/white backgrounds are reserved for invoices, press kits, and partner co-branding.
- **Status colours are reserved** — amber `#F6B73C` and red `#FF5C7A` are for warning/danger only. They are not decorative.
- **Gradients** — only one gradient is approved: a 12° linear from Deep Navy to Slate, used as the landing hero background.

## 5. Founder Console application

| Surface                    | Token                              |
|----------------------------|------------------------------------|
| App shell background       | `--dealix-bg` (Deep Navy)          |
| Nav rail background        | `--dealix-surface` (Slate)         |
| Active nav item            | `--dealix-accent` (Emerald Teal)   |
| Body text                  | `--dealix-text` (White)            |
| Secondary text             | `--dealix-text-muted` (Soft Silver)|
| Card                       | `--dealix-surface` (Slate)         |
| Card border                | `--dealix-border` (silver alpha)   |
| Primary CTA fill           | `--dealix-accent` (Emerald Teal)   |
| Primary CTA label          | `--dealix-bg` (Deep Navy)          |
| Kill-switch button         | `--dealix-danger`                  |

## 6. Marketing / proposal application

- Hero section: gradient navy → slate.
- Section dividers: 1px Soft Silver at 12% alpha.
- Quote / highlight cards: Slate with Emerald Teal left border (2px).
- Pricing table accent column: Emerald Teal at 10% alpha tint.

## 7. Tokens in code

The TypeScript source of truth: `apps/web/lib/brand-tokens.ts`.
The JSON mirror (for external tools, designers, partners): `docs/brand/brand-tokens.json`.
The CSS variable source of truth: `apps/web/styles/brand.css`.

All three must agree. The brand verifier checks consistency.
