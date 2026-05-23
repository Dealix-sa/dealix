# Dealix Typography | الطباعة

> Type carries the Dealix voice. We use two families — one Latin, one Arabic — chosen to read with equal authority in dashboards, decks, and contracts.

---

## 1. Type Families | عائلات الخطوط

| Script | Family | Weights in use | Source |
|---|---|---|---|
| Latin | **Inter** | 400, 500, 600, 700 | rsms.me/inter |
| Arabic | **IBM Plex Sans Arabic** | 400, 500, 600, 700 | IBM Plex |
| Mono (UI numerals, code) | **JetBrains Mono** | 400, 500 | jetbrains.com/mono |

- Inter pairs cleanly with IBM Plex Sans Arabic at matched x-height.
- JetBrains Mono is reserved for tabular numerals in dashboards and inline code blocks.
- No other fonts are permitted on customer-facing surfaces.

---

## 2. Bilingual Pairing | الإقران الثنائي

| Use | Latin | Arabic |
|---|---|---|
| Display | Inter Semibold | IBM Plex Sans Arabic Semibold |
| Heading | Inter Semibold | IBM Plex Sans Arabic Semibold |
| Body | Inter Regular | IBM Plex Sans Arabic Regular |
| Emphasis | Inter Medium | IBM Plex Sans Arabic Medium |
| Caption | Inter Medium | IBM Plex Sans Arabic Medium |

- Arabic text is **never** Inter. Latin text is **never** IBM Plex Sans Arabic.
- Mixed strings (e.g., "Q3 لقاءات") use the correct script per character via font-family fallback chain.

---

## 3. Type Scale | السلم الطباعي

Base size: **16px** (1rem). Modular scale: **1.25** (major third), trimmed for UI density.

| Token | Size (px / rem) | Line height | Use |
|---|---|---|---|
| `display-2xl` | 64 / 4.0 | 1.05 | Hero |
| `display-xl` | 48 / 3.0 | 1.1 | Section hero |
| `display-lg` | 36 / 2.25 | 1.15 | Page title |
| `heading-xl` | 28 / 1.75 | 1.2 | H1 |
| `heading-lg` | 24 / 1.5 | 1.25 | H2 |
| `heading-md` | 20 / 1.25 | 1.3 | H3 |
| `heading-sm` | 18 / 1.125 | 1.35 | H4 |
| `body-lg` | 18 / 1.125 | 1.55 | Long-form body |
| `body-md` | 16 / 1.0 | 1.55 | Default body |
| `body-sm` | 14 / 0.875 | 1.5 | Secondary body |
| `caption` | 13 / 0.8125 | 1.45 | Captions, labels |
| `micro` | 12 / 0.75 | 1.4 | Legal, microcopy |

Arabic line heights are **+5% over Latin** for diacritics breathing room. Apply `line-height: 1.6` for `body-md` in Arabic surfaces.

---

## 4. Weight & Style Rules | قواعد الوزن

- **Headings:** Semibold (600). Never Bold (700) unless the heading is set on a busy photo.
- **Body:** Regular (400). Use Medium (500) only for emphasis within a paragraph.
- **All-caps:** Reserved for the tagline lockup and small eyebrow labels. Track +6%. Never set body in all-caps.
- **Italics:** Avoid in Latin; Arabic has no italic — use Medium for emphasis instead.

---

## 5. Numerals | الأرقام

- **Default:** Tabular numerals (`font-variant-numeric: tabular-nums`) in dashboards, tables, and KPIs.
- **Arabic numerals:** Use Western Arabic numerals (0–9) in product UI for cross-locale legibility. Eastern Arabic numerals (٠–٩) are reserved for Arabic long-form editorial only, on approval.
- **Currency:** SAR symbol or "ر.س" placed per locale convention; never both in one surface.

---

## 6. Line Length & Rhythm | طول السطر والإيقاع

- **Latin body:** 60–75 characters per line.
- **Arabic body:** 50–65 characters per line (denser script).
- **Vertical rhythm:** Use the 8px spacing scale; never freehand margins.
- **Paragraph spacing:** 0.75× line-height between paragraphs.

---

## 7. RTL & LTR | اليمين والشمال

- Arabic surfaces are RTL by default; the entire layout mirrors.
- Numbers, code, and English brand terms remain LTR inside RTL paragraphs via bidi isolation.
- Use logical CSS properties (`margin-inline-start`, `padding-inline-end`) — never `margin-left` / `padding-right` directly.
- Icons that imply direction (arrows, chevrons) mirror in RTL; brand marks and logos do **not** mirror.

---

## 8. Web Implementation | التطبيق الويب

```
font-family: "Inter", "IBM Plex Sans Arabic", system-ui, -apple-system, "Segoe UI", sans-serif;
```

- Self-host both families with `font-display: swap`.
- Preload only the weights actually used on the page (typically 400 + 600).
- Subset Arabic to the Arabic + extended ranges; subset Latin to Latin + Latin Extended-A.

---

## 9. Print & Decks | الطباعة والعروض

- Decks use the same scale, mapped to: Display 44 / Heading 28 / Body 18 / Caption 14.
- Print body never below 9pt. Captions never below 7pt.
- Arabic deck pages use IBM Plex Sans Arabic at the matched scale.

---

## 10. Do / Don't | افعل / لا تفعل

**Do**
- Pair Inter + IBM Plex Sans Arabic in every bilingual surface.
- Use the scale tokens — not arbitrary pixel values.
- Use tabular numerals in tables and KPIs.
- Respect logical CSS properties for RTL.

**Don't**
- Don't introduce a third typeface.
- Don't render Arabic in Inter (it will fall back to a system font and look wrong).
- Don't set body text in all-caps.
- Don't justify Arabic paragraphs — left/right alignment only, per direction.
- Don't use decorative or display fonts in product UI.

---

## 11. Governance | الحوكمة

- **Owner:** Design Systems Lead.
- **Source of truth:** `tokens/typography.json` + Figma "Dealix Type" library.
- **Change gate:** New scale step or weight requires Brand Lead + Design Systems Lead approval.

---

## 12. Related Documents | مراجع

- `DEALIX_VISUAL_IDENTITY.md`
- `DEALIX_COLOR_SYSTEM.md`
- `DEALIX_ACCESSIBILITY_GUIDE.md`
