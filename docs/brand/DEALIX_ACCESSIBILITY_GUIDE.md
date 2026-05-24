# Dealix Accessibility Guide

> Accessibility is not an option. Every Dealix surface must meet at least WCAG 2.2 AA.

## 1. Contrast requirements

| Pair | Minimum ratio | Reference |
|---|---|---|
| Normal text on background | 4.5 : 1 | WCAG 1.4.3 |
| Large text on background | 3 : 1 | WCAG 1.4.3 |
| Non-text UI on background | 3 : 1 | WCAG 1.4.11 |
| Focus indicator on background | 3 : 1 | WCAG 1.4.11 |

Verifier: `scripts/verify_brand_system.py` parses `brand-tokens.json` and computes the contrast ratio for each declared pair.

## 2. Keyboard navigation

- Every interactive element must be focusable.
- Focus order follows reading order in both LTR and RTL.
- Focus ring uses `border.accent` at 2 px, never relies on colour alone.
- Skip-link present at the top of every console page.

## 3. Screen readers

- Every icon-only button has an `aria-label`.
- Every chart has a textual summary near it.
- Every form field has a visible label tied with `for` / `id`.

## 4. Reduced motion

- Animations cap at 200-320 ms.
- `prefers-reduced-motion: reduce` disables non-essential animation.
- Never auto-play video.

## 5. Bilingual & RTL

- Arabic surfaces set `dir="rtl"` on the relevant container.
- Padding mirrors; text alignment mirrors; logo lock-up does **not** mirror.
- Date / time / currency formatting respects locale.

## 6. Images & media

- Decorative images use `alt=""`.
- Informational images include descriptive `alt`.
- Customer logos in proof artifacts include a textual organisation name.

## 7. Forms & errors

- Errors announced via `aria-live="polite"` regions.
- Errors describe the fix, not just the failure.
- Required fields explicitly marked.

## 8. Testing

| Tool | Frequency | Owner |
|---|---|---|
| `pa11y` (config: `.pa11yrc.json`) | per build | CI |
| Lighthouse a11y | weekly | CI |
| Manual keyboard pass | on UI change | Brand Guardian |
| Screen-reader pass | on UI change | Brand Guardian |

## 9. Reporting

Accessibility regressions are first-class bugs and route through `/approvals` for fix prioritisation.
