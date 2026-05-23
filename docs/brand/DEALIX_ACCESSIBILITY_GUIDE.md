# Dealix Accessibility Guide

The brand is only as strong as the most constrained user can read it.

## 1. Contrast baselines

We target **WCAG 2.2 AA** as the floor and **AAA** wherever feasible.

| Foreground | Background | Ratio | Status |
|---|---|---|---|
| White `#FFFFFF` | Deep Navy `#0B1220` | 17.0 : 1 | AAA |
| Soft Silver `#B2BBC6` | Deep Navy `#0B1220` | 8.4 : 1 | AAA |
| Emerald Teal `#00D1A1` | Deep Navy `#0B1220` | 8.6 : 1 | AAA |
| White `#FFFFFF` | Slate `#0F1726` | 15.8 : 1 | AAA |
| Soft Silver `#B2BBC6` | Slate `#0F1726` | 7.7 : 1 | AAA |

`scripts/verify_brand_system.py` re-computes these on every change
and fails CI if any combination drops below 4.5 : 1 for body or
3 : 1 for large display text.

## 2. Focus and keyboard

- Every interactive element ships a visible focus ring
  (`--dlx-shadow-focus`). Never `outline: none` without replacing it.
- Tab order matches DOM order; no `tabIndex` higher than `0`.
- Skip-link is present on every shell layout.

## 3. RTL / bilingual

- All shells set `dir` and `lang` correctly.
- Numerals stay LTR inside Arabic paragraphs (`<bdo dir="ltr">`).
- Icons that imply direction (arrows, growth lines) flip in RTL.

## 4. Motion

- All motion respects `prefers-reduced-motion: reduce`.
- No animation lasts longer than 320 ms in the product UI.
- No flashing or pulsing more frequently than 3 Hz.

## 5. Forms

- Every input has an associated `<label>` or `aria-label`.
- Errors are announced via `aria-live="polite"` and are colour-coded
  with `--dlx-danger` **plus** an icon and text — never colour alone.

## 6. Imagery and icons

- Decorative icons set `aria-hidden="true"`.
- Meaningful icons have a `<title>` or `aria-label`.
- Brand mark uses `role="img"` with the documented `aria-label`.

## 7. Targets

- Minimum interactive target size: **44 × 44 px** (per WCAG 2.5.5).
- Adjacent CTAs are separated by at least 8 px.
