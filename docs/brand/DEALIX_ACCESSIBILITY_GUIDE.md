# DEALIX Accessibility Guide

**Owner:** Brand Lead + Product Engineering
**Source of truth:** `docs/brand/DEALIX_COLOR_SYSTEM.md` + WCAG 2.2 AA

## Principle

Accessibility is part of the trust promise. A Dealix surface that excludes a user is a broken surface, not an edge case.

## Targets

- WCAG 2.2 AA for all customer-facing surfaces.
- AAA where the cost of meeting it is low (body text contrast).
- Full keyboard operability on all interactive surfaces.
- Full RTL parity for Arabic content.

## Contrast

All text-on-surface combinations must pass AA (4.5:1 for body, 3:1 for large text). Reference table in `DEALIX_COLOR_SYSTEM.md`. Run an automated check (e.g., axe, Lighthouse) before publishing any UI.

The two failing pairs to remember:

- Emerald Teal on White — contrast 2.0:1, fails AA.
- Soft Silver on White — contrast 1.9:1, fails AA.

Use these only for non-text decorative elements.

## Focus rings

- Visible focus ring on every interactive element.
- Ring color: Emerald Teal `#00D1A1`, 2px outline, 2px offset from the element edge.
- Never remove the focus ring with `outline: none` without an equivalent replacement.

## Hit targets

- Minimum 44 x 44 px for any tap target on touch surfaces.
- Minimum 32 x 32 px for mouse-only surfaces.
- Spacing: at least 8 px between adjacent tap targets.

## Motion

- Honor `prefers-reduced-motion`. Disable swoosh entries, parallax, and gradient animation when the user prefers reduced motion.
- No motion longer than 400 ms for UI transitions.
- No infinite-loop animations on content surfaces.

## RTL support

When `dir="rtl"` is set:

- Layout mirrors automatically through logical properties (`padding-inline-start`, `margin-inline-end`).
- Icons that imply direction (arrows, chevrons) mirror.
- Icons that are bidi-neutral (search, info, settings) do not mirror.
- Numbers remain LTR inside RTL prose. Use the Unicode bidi algorithm rather than forcing direction.
- Tables align numeric columns to the trailing edge in both directions.

## Screen reader

- Every image has alt text. Decorative images carry `alt=""`.
- Every form input has a `<label>` associated by `for` attribute.
- Every interactive element has an accessible name reachable through `aria-label` or visible text.
- Headings nest in order. Skipping levels breaks screen-reader navigation.
- Live regions for queue updates use `aria-live="polite"`. Never `assertive` for non-critical updates.
- Tables of data use `<th scope="col">` and `<th scope="row">` so screen readers can announce cell context.

## Forms

- Required fields marked with both color and an explicit `*` or `required` label.
- Error states use Risk red and an icon and text. Never color alone.
- Error text appears immediately after the offending field, not at the top of the form.
- Each error references the field by name.

## Keyboard

- Tab order follows visual order.
- Skip-link present on every page-level surface.
- All modal dialogs trap focus and return focus to the trigger on close.
- All custom widgets follow ARIA Authoring Practices patterns.

## Language attributes

- `<html lang="en">` on English surfaces, `<html lang="ar" dir="rtl">` on Arabic surfaces.
- Inline language switches: `<span lang="ar">…</span>` inside Latin prose, and vice versa.

## PDF and document accessibility

- Tagged PDFs only. Untagged PDFs are inaccessible to screen readers.
- Reading order matches visual order.
- Tables have header rows tagged.
- Form fields, if any, have tooltips set to the visible label.

## Failure mode

- Customer proposal exported as untagged PDF.
- Focus ring removed in product UI for a "cleaner" look.
- Arabic page rendered without `dir="rtl"`, producing right-padded but logically-mirrored content.
- Error state communicated by red color alone.

## Recovery path

1. Re-export PDFs with tags.
2. Restore focus rings using the standard token.
3. Add `dir="rtl"` and re-test RTL layout.
4. Add icon and text to error states.

## Disclaimer

Accessibility is a non-negotiable. A surface that fails AA is not approved for customer release regardless of timeline pressure.
