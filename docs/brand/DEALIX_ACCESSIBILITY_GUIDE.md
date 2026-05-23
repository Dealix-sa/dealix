# Dealix Accessibility Guide | دليل إمكانية الوصول

> Accessibility is a trust commitment. Every Dealix surface meets WCAG 2.2 AA, supports RTL, and is operable by keyboard alone.

---

## 1. Standard | المعيار

- **Target:** WCAG 2.2 **Level AA** for all customer-facing surfaces (web app, marketing site, emails, decks where rendered as PDF, in-product help).
- **Stretch target:** AAA contrast for body text on the marketing site.
- **Scope:** Includes English (LTR) and Arabic (RTL) parity.

---

## 2. Color & Contrast | اللون والتباين

- Body text: minimum **4.5:1** against its background.
- Large text (≥18pt, or ≥14pt bold): minimum **3:1**.
- Non-text UI components (form borders, icons, focus rings): minimum **3:1**.
- See `DEALIX_COLOR_SYSTEM.md` §5 for verified pairs.
- **Never** put White on Emerald Teal — it fails AA. Use Deep Navy on Emerald Teal instead.
- Never rely on color alone to convey state. Always pair with a label, icon, or text.

---

## 3. Typography | الطباعة

- Minimum body size: **16px** on web, **14pt** in PDF, **9pt** in print.
- Line height: ≥ 1.5 for body; ≥ 1.6 for Arabic body.
- Line length: 60–75 chars (Latin), 50–65 chars (Arabic).
- Letter spacing: ≥ 0.12em for tracked all-caps.
- Avoid justified Arabic paragraphs (creates inconsistent word spacing).
- Honor `prefers-contrast` and `prefers-reduced-motion` user settings.

---

## 4. Focus States | حالات التركيز

- Every interactive element must show a visible focus indicator.
- Default focus ring: **2px Emerald Teal** outer + **2px Deep Navy** inner halo, offset 2px.
- Focus rings are **always visible** on keyboard focus; do not suppress with `outline: none`.
- Skip-to-content link is the first focusable element on every page.
- Focus order matches visual order (top→bottom in LTR, top→bottom right→left in RTL).

---

## 5. Keyboard Operability | تشغيل الكيبورد

- All actions reachable by keyboard (no mouse-only interactions).
- Modal dialogs trap focus while open and restore focus on close.
- Tab order is logical; `tabindex` ≥ 0 only when necessary, never > 0.
- Approval prompts and destructive actions require explicit confirmation (Enter or Space, never click-anywhere-to-confirm).

---

## 6. RTL Support | دعم RTL

- Set `dir="rtl"` and `lang="ar"` on Arabic pages.
- Use **logical CSS properties** (`margin-inline-start`, `padding-inline-end`, `inset-inline-start`).
- Mirror directional icons (arrows, chevrons) in RTL. Do **not** mirror brand marks or logos.
- Numbers and Latin terms inside Arabic prose use bidi isolation (`<bdi>` or CSS `unicode-bidi: isolate`).
- Test scroll, drag, and swipe gestures in RTL — many libraries default to LTR-only.

---

## 7. Screen Readers | قارئات الشاشة

- Use semantic HTML first; ARIA only to fill gaps.
- Every image has meaningful `alt` text. Decorative images use `alt=""`.
- Form fields are labeled with `<label for>` or `aria-labelledby`.
- Errors are announced with `aria-live="polite"`; critical alerts use `aria-live="assertive"`.
- Loading states and async updates announce status to screen readers.
- Tested with VoiceOver (macOS/iOS), NVDA (Windows), and TalkBack (Android), in both English and Arabic.

---

## 8. Forms & Inputs | النماذج

- Visible labels always; placeholder is **not** a label.
- Error messages name the field and the fix.
- Required fields marked with both text ("required") and visual cue.
- Inputs have a minimum touch target of 44×44 px.
- Autocomplete attributes set where appropriate (`autocomplete="email"`, `autocomplete="tel"`).

---

## 9. Motion & Animation | الحركة

- Honor `prefers-reduced-motion`: replace transforms with opacity transitions.
- No motion exceeding 5Hz (avoid seizure triggers).
- No auto-playing video with sound.
- No looping animations on marketing pages.

---

## 10. Media | الوسائط

- Videos include captions (Arabic + English).
- Audio clips include a transcript.
- Charts include a text alternative (data table or summary).
- Decorative SVGs have `aria-hidden="true"`; informative SVGs have `<title>` and `<desc>`.

---

## 11. Approval Flows & Microcopy | تدفقات الموافقة

Because Dealix is approval-gated, every approval prompt must be **unambiguous and accessible**:

- Title states the action ("Approve outbound draft?").
- Body lists what will happen if approved **and** if declined.
- Two clearly labeled buttons: "Approve" (Emerald Teal) and "Decline" (Slate). Never "OK / Cancel."
- Destructive or irreversible actions require a typed confirmation.
- All of the above readable by screen reader, operable by keyboard, and translated for Arabic.

---

## 12. Testing & QA | الاختبار

- **Automated:** axe-core or Lighthouse in CI; zero AA violations to merge.
- **Manual:** keyboard-only walkthrough of every new page before release.
- **Screen reader:** VoiceOver pass on top 10 customer-facing flows per release.
- **RTL:** Every page reviewed in `dir="rtl"` before release.
- **Quarterly audit:** sample 20 production screens; remediate any AA violations within the sprint.

---

## 13. Owner & KPI | الملكية والمؤشرات

- **Owner:** Design Systems Lead + Engineering Quality Lead.
- **KPI:** Zero AA violations on shipped customer surfaces.
- **KPI:** 100% bilingual parity on KSA-facing surfaces.
- **KPI:** 100% of approval prompts pass keyboard + screen reader test.

---

## 14. Related Documents | مراجع

- `DEALIX_COLOR_SYSTEM.md`
- `DEALIX_TYPOGRAPHY.md`
- `DEALIX_VISUAL_IDENTITY.md`
- `DEALIX_BRAND_VOICE.md`
