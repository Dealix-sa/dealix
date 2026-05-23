# Dealix Accessibility Guide

The Dealix brand is built to **WCAG 2.1 AA** at minimum, with AAA targets for body text on default brand surfaces.

## 1. Why accessibility is part of the brand

A brand-led design system is only credible if it works for every operator who needs it. The Saudi B2B market includes operators with reduced vision, age-related vision loss, colour-blindness, and screen-reader users. Dealix surfaces respect those operators.

## 2. Contrast targets

| Element                       | WCAG AA target | Dealix policy |
|-------------------------------|----------------|---------------|
| Body text                     | ≥ 4.5:1        | AAA (≥ 7:1) on default brand surfaces |
| Large text                    | ≥ 3:1          | ≥ 4.5:1       |
| UI components                 | ≥ 3:1          | ≥ 3:1         |
| Graphical objects (icons)     | ≥ 3:1          | ≥ 3:1         |
| Focus indicator               | ≥ 3:1 against adjacent colours | ≥ 3:1, never colour-only |

## 3. Colour pair table (verified)

See `DEALIX_COLOR_SYSTEM.md` § 3 for the full contrast pair table. Key results:

- White on Deep Navy: ~17.5:1 (AAA body)
- Soft Silver on Deep Navy: ~9.8:1 (AAA body)
- Emerald Teal on Deep Navy: ~9.2:1 (AAA body)
- Emerald Teal on White: ~2.3:1 (large text only — never body)

## 4. Don't rely on colour alone

- Status: always pair colour with an icon and a text label.
- Errors: red ring + error icon + plain-language text. Not red alone.
- Charts: encode with both colour and shape/pattern.

## 5. Focus & keyboard

- Every interactive control has a visible focus ring at ≥ 3:1 contrast against its background.
- The focus ring is 2px Emerald Teal with 1px Deep Navy outline for legibility on light surfaces.
- Tab order follows visual order. No `tabindex > 0` traps.
- Skip-link at the top of every page: "Skip to main content".

## 6. Motion

- Respect `prefers-reduced-motion: reduce`. Disable swoosh animation, parallax, and any non-essential motion.
- No flashing > 3Hz (epilepsy safety).
- No autoplay video with sound.

## 7. Forms

- Every form input has a `<label>` (not a placeholder masquerading as a label).
- Error messages are programmatically linked to the input via `aria-describedby`.
- Required fields are marked in both text ("required") and via `aria-required`.

## 8. RTL / Arabic

- Set `dir="rtl"` on `<html>` for AR pages.
- Use logical properties (`margin-inline-start`) — not `margin-left`.
- Test with a real screen reader in Arabic. Auto-translate does not count.

## 9. Tooling

- Use `pa11y` (already configured in `.pa11yrc.json`) for automated checks.
- Use Lighthouse a11y in CI.
- Manual screen-reader sweep on every release (VoiceOver + NVDA, EN + AR).

## 10. References

- WCAG 2.1 — https://www.w3.org/TR/WCAG21/
- WCAG quick ref — https://www.w3.org/WAI/WCAG21/quickref/
