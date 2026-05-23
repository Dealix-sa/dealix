# Dealix Typography

## 1. Stacks

- **Latin:** `Inter, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`
- **Arabic:** `"IBM Plex Sans Arabic", "Noto Sans Arabic", Tahoma, sans-serif`

We default to system fallbacks so the product loads instantly even on
constrained networks. Web font loading is a `font-display: swap`
concern, never a brand correctness concern.

## 2. Scale

| Token | Size | Use |
|---|---|---|
| `display` | 44 px | Landing hero, founder console eyebrow. |
| `h1` | 32 px | Section heading. |
| `h2` | 24 px | Card heading. |
| `h3` | 18 px | Inline subsection. |
| `body` | 15 px | Default paragraph. |
| `small` | 13 px | Captions, helper text. |
| `caption` | 12 px | Pill labels, metric eyebrows. |

## 3. Weights

- `400` regular — body paragraphs.
- `500` medium — labels, secondary buttons.
- `600` semibold — UI emphasis, button labels.
- `700` bold — h1 / h2 headings, key metric values.
- `800` extrabold — `DEALIX` wordmark only.

## 4. Letter-spacing

- Headings: `-0.01em` to feel tight and confident.
- Wordmark `DEALIX`: `+0.04em` to feel architectural.
- Uppercase eyebrows: `+0.10em` to read as labels, not words.

## 5. Bilingual rules

- Arabic always sets right-to-left (`dir="rtl"`).
- Headings can stack Arabic above Latin with the same accent rule
  (silver above white, or white above teal accent).
- Never mix the two stacks in the same line of marketing copy unless
  a single proper noun (`Dealix`) appears inside an Arabic sentence.

## 6. Forbidden patterns

- ❌ Italic body text (we never italicise for tone).
- ❌ Font-family overrides inside individual components.
- ❌ Sub-13-px body copy on dark backgrounds.
- ❌ Hand-drawn / handwritten / display fonts anywhere.
