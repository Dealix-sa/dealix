# DEALIX Accessibility Guide

> Wordmark: **DEALIX**
> Tagline: **INTELLIGENT DEALS. REAL GROWTH.**

This document defines the accessibility commitments that bind every Dealix
surface. It covers contrast, focus, motion, RTL/LTR, semantics, and
assistive technology. It is the practical complement to
`DEALIX_COLOR_SYSTEM.md` and `DEALIX_TYPOGRAPHY.md`.

Dealix targets **WCAG 2.1 AA** as the floor and **AAA where reasonable**.
Accessibility is treated as a feature of the brand, not an afterthought.

---

## 1. Why this matters

Saudi B2B buyers include senior decision-makers across age and ability.
Investors, regulators, and board members review our surfaces. An
inaccessible surface is a sign of sloppy engineering, and the brand
cannot afford that signal.

Beyond the brand argument, PDPL-adjacent Saudi regulations expect a
defensible accessibility posture for enterprise software. We exceed the
floor on purpose.

---

## 2. Contrast

### 2.1 Targets

| Element | Minimum ratio | Notes |
| --- | --- | --- |
| Body text | 4.5:1 | WCAG AA |
| Large text (24 px+ or 18.66 px bold) | 3.0:1 | WCAG AA |
| Non-text UI (icons, focus rings, inputs) | 3.0:1 | WCAG AA |
| Graphical objects in a chart | 3.0:1 | WCAG AA |

### 2.2 Sanctioned pairs

The canonical color pairs in `DEALIX_COLOR_SYSTEM.md` (section 5) all
clear AA for body text. They are the default. If a designer composes a
new pair, run it through a contrast checker.

### 2.3 Forbidden pairs

- Emerald Teal text on White surface (~2:1, fails AA).
- Soft Silver text on White surface.
- Soft Silver text on Emerald Teal surface.

When these collisions are forced by a layout, change the foreground or
darken the background — do **not** ship a failing pair.

---

## 3. Focus

Every interactive element receives a visible focus ring.

- Ring color: Emerald Teal `#00D1A1`.
- Ring width: 2 px outside the element border.
- Ring offset: 2 px gap between element and ring.
- Border-radius: matches the element's radius.
- Visible on **all** interactive elements: buttons, links, inputs,
  selects, checkboxes, radios, tabs, dropdown items, cards-as-links.

Focus visibility is not optional, not opt-in, and not removed by a global
`* { outline: none; }`. That CSS pattern is forbidden in Dealix code.

Keyboard navigation:
- `Tab` moves focus forward.
- `Shift+Tab` moves focus backward.
- `Enter` / `Space` activates focused button or link.
- `Esc` closes the topmost modal or dropdown.
- Custom widgets (tabs, comboboxes) follow WAI-ARIA Authoring
  Practices.

---

## 4. Motion

Dealix surfaces favor stillness. Animation is a feature, not a
decoration.

### 4.1 Sanctioned motion
- Logo swoosh sweep on first paint (one quarter-second).
- Button hover/active state transitions (≤ 150 ms).
- Modal/drawer enter/exit (≤ 200 ms).
- Toast notifications fade-in (≤ 200 ms).
- Status chip pulse for "Live" or "In progress" (low amplitude, 2 s
  cycle).

### 4.2 Forbidden motion
- Auto-playing background video on a hero.
- Looping parallax scroll on the marketing site.
- Carousels that auto-advance.
- Bouncy "spring" easings on text.
- Confetti, fireworks, or celebratory animations on closed deals.
  (The CRM-level outcome is the celebration.)

### 4.3 Reduced motion
We respect `prefers-reduced-motion: reduce`. When the user has it set:
- Skip the logo swoosh sweep.
- Skip the chip pulse.
- Reduce transitions to opacity-only fades at ≤ 80 ms.

In CSS:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 5. RTL and LTR

Dealix is bilingual. RTL is a first-class layout direction, not a
translated afterthought.

### 5.1 Direction
- Set `dir="rtl"` on Arabic blocks; the page direction follows the
  active locale.
- Use logical CSS properties: `margin-inline-start`, `padding-inline-end`,
  `inset-inline-start`, `border-inline-start-width`.
- Avoid `margin-left` and `padding-right` outside legacy code paths.

### 5.2 Mirroring
- Directional icons (arrows, chevrons, breadcrumbs) mirror in RTL.
- Decorative shapes do not mirror.
- The Dealix mark does not mirror — only its anchor moves.

### 5.3 Numerals
- Arabic prose uses Arabic-Indic numerals.
- Tables, KPIs, machine-readable surfaces use ASCII numerals.

### 5.4 Mixed content
- Bidirectional text uses `<bdi>` or the `unicode-bidi: isolate` rule
  for embedded names, URLs, or codes.

---

## 6. Semantics and ARIA

### 6.1 HTML semantics
- One `<h1>` per page.
- Section structure with `<header>`, `<main>`, `<nav>`, `<footer>`.
- Lists use `<ul>` / `<ol>`; tables use `<table>` with `<thead>` and
  `<tbody>`.
- Forms use `<label>` linked via `for` to inputs.
- Buttons use `<button>`; links use `<a href>`. We do not stub a
  `<div>` and bolt `onClick` onto it.

### 6.2 ARIA usage
- ARIA is a fallback for cases where HTML semantics fall short.
- Use `aria-label` only when a visible label is impossible.
- `aria-live="polite"` for non-urgent status changes (toasts).
- `aria-live="assertive"` for urgent errors.
- `aria-current="page"` for the active nav item.
- `aria-expanded` and `aria-controls` for disclosure widgets.

### 6.3 Language attributes
- `<html lang="ar">` or `<html lang="en">` per page locale.
- Inline language switches use `<span lang="...">` so screen readers
  pick the correct voice.

---

## 7. Forms

- Every input has a visible label. Placeholder text is **not** a label.
- Required fields marked with both an asterisk and an `aria-required`.
- Errors named in plain language, attached to the input via
  `aria-describedby`.
- Validation runs on blur and on submit, not on every keystroke.
- Submit buttons name the action: "Submit pilot brief", not "Submit".

---

## 8. Images and media

- Every `<img>` carries `alt` text. Decorative images use `alt=""`.
- ALT text describes the image in plain language, in the surface's
  locale.
- SVG icons use `role="img"` with `aria-label` when carrying meaning;
  decorative SVGs use `aria-hidden="true"`.
- Video has captions and a transcript. Auto-play is forbidden.
- Audio has a transcript.

---

## 9. Tables and dashboards

- Tables use `<th scope="col|row">` for headers.
- Long tables include a `<caption>` summarizing what they show.
- Sortable columns expose their state via `aria-sort`.
- KPI numbers use `font-variant-numeric: tabular-nums` so they align.
- Empty states explain what is missing, not what was empty.

---

## 10. Modals and overlays

- Focus is trapped inside the open modal.
- `Esc` closes the modal.
- The trigger element receives focus when the modal closes.
- A modal includes a visible close button labeled "Close" (or the
  Arabic equivalent), not just an X icon.
- Modals announce themselves via `aria-modal="true"` and `role="dialog"`.

---

## 11. Touch and pointer

- Tap targets are at least 44×44 px (iOS) and 48×48 px (Android).
- Hit areas extend to include the visible focus ring.
- Hover-only interactions have a touch fallback.

---

## 12. Internationalization beyond direction

- Dates are formatted with the locale's calendar:
  `Intl.DateTimeFormat('ar-SA')` for Arabic surfaces (Umm al-Qura
  available where required).
- Numbers are formatted with `Intl.NumberFormat`.
- Currency: SAR shown as either "ر.س" or "SAR" depending on locale.
- Time zones default to `Asia/Riyadh` for Saudi customers.

---

## 13. Testing

The accessibility floor is verified by:

| Tool | What it checks |
| --- | --- |
| `pa11y` (CI) | Automated WCAG checks per page |
| `axe-core` (Storybook) | Component-level a11y rules |
| Manual keyboard pass | One pass per PR touching UI |
| Screen reader pass | One pass per release |
| Reduced motion | Manual toggle, one pass per release |

A surface that fails the automated CI checks does not merge.

---

## 14. Known constraints we accept

- Some PDF exports lose semantic structure. We mitigate with
  PDF/A-1b export and explicit tagging.
- Some embedded video providers do not expose captions API. We host
  captions as side-car files when this happens.

---

## 15. Bilingual note — العربية

إمكانية الوصول جزء من العلامة، لا إضافة لاحقة. كل سطح يجب أن يجتاز
WCAG 2.1 AA كحد أدنى. لكل عنصر تفاعلي حلقة تركيز مرئية باللون الأخضر
التركوازي. نَحترم تفضيل المستخدم لتقليل الحركة، ونستخدم خصائص CSS
المنطقية لدعم RTL تلقائياً. الأرقام في النص الجاري عربية-هندية،
وفي الجداول لاتينية. كل صورة تحمل نصاً بديلاً واضحاً بلغة السطح. كل
نموذج له تسمية مرئية، ورسائل الخطأ مكتوبة بلغة بشرية لا برموز
تقنية. هذه ليست رفاهيّة، بل دفاع عن سمعة المنتج أمام مشترٍ سعودي
متطلّب.

---

## 16. Escalation

If a feature cannot meet the accessibility floor:

1. Document the gap and the why.
2. Propose a remediation plan with an owner and a date.
3. Get brand director sign-off.
4. Surface the gap in the changelog so customers and reviewers know.

We do not ship a quietly inaccessible surface and hope no one notices.
