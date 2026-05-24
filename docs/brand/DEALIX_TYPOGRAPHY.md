# Dealix Typography

## 1. Families

| Role | Latin family | Arabic family | Weight |
|---|---|---|---|
| Display | Inter Tight | IBM Plex Sans Arabic | 700-800 |
| Heading | Inter | IBM Plex Sans Arabic | 600 |
| Body | Inter | IBM Plex Sans Arabic | 400-500 |
| Mono | JetBrains Mono | JetBrains Mono | 400-500 |

System fallback stack: `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`.

Arabic and English are always **typographically equal**: same weight, same optical size, same line-height when shown side-by-side.

## 2. Type scale (rem)

| Token | Size | Use |
|---|---|---|
| `xs` | 0.75 | micro labels |
| `sm` | 0.875 | small body, captions |
| `md` | 1 | body |
| `lg` | 1.125 | emphasis body |
| `xl` | 1.25 | sub-section |
| `2xl` | 1.5 | section heading |
| `3xl` | 1.875 | page heading |
| `4xl` | 2.25 | dashboard hero |
| `5xl` | 3 | landing hero |
| `6xl` | 3.75 | top-of-page hero, deck cover |

## 3. Line-height tokens

| Token | Value | Use |
|---|---|---|
| `tight` | 1.20 | Hero headings |
| `snug` | 1.35 | Sub-heads |
| `normal` | 1.50 | Body |
| `relaxed` | 1.65 | Long-form, blog |

## 4. Tracking

- Display: `-0.01em`
- Eyebrows / overlines: `0.18 - 0.24em` uppercase
- Body: default
- Mono: default

## 5. Hierarchy

| Element | Token | Weight |
|---|---|---|
| Page eyebrow | `xs` | 700, uppercase |
| Page title (h1) | `3xl-4xl` | 700 |
| Section title (h2) | `2xl` | 600 |
| Card title (h3) | `lg` | 600 |
| Body | `md` | 400 |
| Labels | `sm` | 500 |
| Caption | `xs` | 500 |

## 6. Bilingual rules

- Right-to-left containers must mirror padding, not text.
- Numbers in Arabic surfaces use Western digits by default unless the customer's contract states otherwise.
- Mixed-script paragraphs use the AR family as the dominant family.

## 7. Files

| Surface | Source |
|---|---|
| Founder Console | `apps/web/styles/brand.css`, `apps/web/lib/brand-tokens.ts` |
| Landing | `landing/styles.css` |
| Marketing decks | `templates/dealix-deck.theme.json` (TBD by Brand Guardian) |
