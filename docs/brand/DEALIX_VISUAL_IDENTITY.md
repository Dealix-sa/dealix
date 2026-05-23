# Dealix Visual Identity | الهوية البصرية

> The visual identity is how Dealix is recognized before a single word is read. It must say "operator," "trust," and "growth" — in that order.

---

## 1. Identity Components | مكونات الهوية

| Component | Role |
|---|---|
| Wordmark "Dealix" | Primary identifier across all surfaces |
| Monogram "D" | Compact mark for avatars, favicons, app icons |
| Lockup | Wordmark + tagline, used in formal/launch contexts |
| Grid | 8pt base grid, 4pt half-step, with 12-column layout |
| Color | See `DEALIX_COLOR_SYSTEM.md` |
| Type | See `DEALIX_TYPOGRAPHY.md` |

---

## 2. Wordmark | الشعار الكتابي

- **Spelling:** "Dealix" — always capitalized D, lowercase rest. Never "DEALIX" except in tagline lockup.
- **Type:** Inter Semibold (English), IBM Plex Sans Arabic Semibold ("ديليكس") for Arabic lockups.
- **Tracking:** -1% optical for English; default for Arabic.
- **Minimum size:** 16px on screen, 12mm in print.

---

## 3. Monogram "D" | الرمز المختصر

- Used only where the full wordmark cannot breathe (favicons, app icons, social avatars, small UI badges).
- Always rendered with Emerald Teal on Deep Navy, or White on Deep Navy.
- Never tilted, outlined, or filled with gradients.
- Minimum size: 24px.

---

## 4. Tagline Lockup | قفل الشعار + العبارة

- Formal lockup pairs the wordmark with **"INTELLIGENT DEALS. REAL GROWTH."** set in Inter Medium, all caps, tracked +6%.
- Arabic lockup uses **"صفقات ذكية. نمو حقيقي."** in IBM Plex Sans Arabic Medium.
- Tagline sits below the wordmark at 25% of wordmark cap-height.
- Tagline lockup is reserved for: launch creative, investor decks, formal partner agreements, and the homepage hero.

---

## 5. Layout Grid | الشبكة

- **Base unit:** 8px. Half-step 4px allowed for icon work only.
- **Web grid:** 12 columns, 80px max gutter at 1440 viewport, scaling down to 16px at 360.
- **Print grid:** 12 columns on A4, 18mm margin, 6mm gutter.
- **Vertical rhythm:** 8/16/24/32/48/64/96 spacing scale only.
- **Cards & sections:** 16px radius for cards, 8px for buttons, 4px for chips.

---

## 6. Logo on Backgrounds | الشعار على الخلفيات

| Background | Permitted mark |
|---|---|
| Deep Navy #0B1220 | White wordmark, or Emerald Teal monogram |
| Slate #0F1726 | White wordmark |
| White #FFFFFF | Deep Navy wordmark, or Emerald Teal monogram |
| Soft Silver #B2BBC6 | Deep Navy wordmark only |
| Emerald Teal #00D1A1 | Deep Navy wordmark only — never white on teal |
| Photography | White wordmark over a 40% Deep Navy overlay |

---

## 7. Imagery Direction | الاتجاه البصري

- **Photography:** Real Saudi operators, real desks, real meetings. No stock-AI imagery, no glowing brains, no holographic earths.
- **Illustration:** Geometric, line-based, 1.5px stroke, Emerald Teal accents on Deep Navy.
- **Data visualization:** Restrained. Emerald Teal for the "Dealix outcome" series; Soft Silver for baselines; Slate for grid lines.
- **Iconography:** 24px grid, 1.5px stroke, rounded joins, no fills.

---

## 8. Motion | الحركة

- **Easing:** `cubic-bezier(0.2, 0.8, 0.2, 1)` for entrances; `cubic-bezier(0.4, 0, 1, 1)` for exits.
- **Duration:** 150–250ms for UI, 400–600ms for hero reveals.
- **Reduce motion:** Honor `prefers-reduced-motion`; replace with opacity-only transitions.
- **No looping animations** in marketing pages — they undermine trust.

---

## 9. Sound | الصوت

- Dealix has no sonic logo today.
- If introduced, it must be a single tonal mark, ≤ 800ms, neutral, and approval-gated by Brand Lead.

---

## 10. Asset Naming Convention | تسمية الملفات

```
dealix-<surface>-<variant>-<lang>-<size>.<ext>
```

Examples:
- `dealix-wordmark-navy-en-512.svg`
- `dealix-monogram-teal-ar-128.png`
- `dealix-og-hero-en-1200x630.jpg`

---

## 11. Governance | الحوكمة

- **Owner:** Brand Lead.
- **Source of truth:** Figma "Dealix Identity" library + this folder.
- **Versioning:** Semantic — `v1.0`, `v1.1`, etc., with a dated changelog entry per release.
- **Approval gate:** Any new mark, illustration style, or motion pattern requires Brand Lead sign-off before use in customer-facing surfaces.

---

## 12. Related Documents | مراجع

- `DEALIX_LOGO_USAGE.md`
- `DEALIX_COLOR_SYSTEM.md`
- `DEALIX_TYPOGRAPHY.md`
- `DEALIX_MARKETING_ASSET_GUIDE.md`
