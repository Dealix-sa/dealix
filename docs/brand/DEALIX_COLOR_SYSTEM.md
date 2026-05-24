# Dealix Color System | نظام الألوان

> Color signals trust before words do. Dealix uses a tight, high-contrast palette tuned for dashboards, decks, and bilingual reading.

---

## 1. Core Palette | اللوحة الأساسية

| Token | Name | Hex | Role |
|---|---|---|---|
| `color.bg.primary` | Deep Navy | `#0B1220` | Primary background, hero, app shell |
| `color.bg.secondary` | Slate | `#0F1726` | Cards, panels, elevated surfaces |
| `color.brand.accent` | Emerald Teal | `#00D1A1` | Brand accent, CTAs, "Dealix outcome" data series |
| `color.fg.muted` | Soft Silver | `#B2BBC6` | Muted text, dividers, baselines, captions |
| `color.fg.inverse` | White | `#FFFFFF` | Primary text on dark, inverse surfaces |

These five colors carry 95% of all Dealix surfaces. Anything beyond them must be added through the semantic layer below.

---

## 2. Semantic Layer | الطبقة الدلالية

| Token | Hex | Use |
|---|---|---|
| `color.semantic.success` | `#00D1A1` | Approvals, positive deltas, healthy KPIs |
| `color.semantic.warning` | `#F2B544` | Pending approval, attention required |
| `color.semantic.danger` | `#E5484D` | Blocked, error, escalation needed |
| `color.semantic.info` | `#5EB1FF` | Informational notes, neutral system messages |
| `color.semantic.neutral` | `#B2BBC6` | Baselines, secondary chips |

Semantic colors are used **sparingly** and **never** as decorative accents. They earn their place by carrying meaning.

---

## 3. Surface Tokens | طبقات الأسطح

| Token | Hex | Notes |
|---|---|---|
| `surface.0` | `#0B1220` | App background |
| `surface.1` | `#0F1726` | Card |
| `surface.2` | `#172033` | Elevated card / modal |
| `surface.3` | `#1F2A40` | Popover / tooltip |
| `border.subtle` | `#1F2A40` | Hairline divider |
| `border.strong` | `#2E3A52` | Card border, input border |

---

## 4. Text Tokens | طبقات النص

| Token | Hex | Use |
|---|---|---|
| `text.primary` | `#FFFFFF` | Headings & body on dark |
| `text.secondary` | `#B2BBC6` | Body, descriptions |
| `text.tertiary` | `#7A8597` | Captions, helper text |
| `text.inverse` | `#0B1220` | Text on white/light surfaces |
| `text.accent` | `#00D1A1` | Inline emphasis (used sparingly) |

---

## 5. Contrast Pairs (WCAG 2.2 AA) | أزواج التباين

Dealix targets **WCAG 2.2 AA**: **4.5:1** for body text, **3:1** for large text (≥18pt or ≥14pt bold) and non-text UI components.

| Foreground | Background | Ratio | Verdict |
|---|---|---|---|
| White `#FFFFFF` | Deep Navy `#0B1220` | ~17.9:1 | Pass AAA |
| White `#FFFFFF` | Slate `#0F1726` | ~16.3:1 | Pass AAA |
| Soft Silver `#B2BBC6` | Deep Navy `#0B1220` | ~9.4:1 | Pass AAA |
| Soft Silver `#B2BBC6` | Slate `#0F1726` | ~8.5:1 | Pass AAA |
| Emerald Teal `#00D1A1` | Deep Navy `#0B1220` | ~9.0:1 | Pass AAA |
| Deep Navy `#0B1220` | White `#FFFFFF` | ~17.9:1 | Pass AAA |
| Deep Navy `#0B1220` | Emerald Teal `#00D1A1` | ~9.0:1 | Pass AAA |
| White `#FFFFFF` | Emerald Teal `#00D1A1` | ~2.0:1 | FAIL — do not use |

**Hard rule:** Never put white text on Emerald Teal. Use Deep Navy text on teal.

---

## 6. Color Use by Surface | استخدام الألوان حسب السطح

| Surface | Primary | Secondary | Accent |
|---|---|---|---|
| Marketing site | Deep Navy | White | Emerald Teal |
| Product app | Deep Navy / Slate | White | Emerald Teal |
| Decks (light) | White | Deep Navy text | Emerald Teal |
| Decks (dark) | Deep Navy | White text | Emerald Teal |
| Email | White | Deep Navy text | Emerald Teal (CTA only) |
| Print | White | Deep Navy text | Emerald Teal (accent only) |

---

## 7. Data Visualization | تصور البيانات

- **Primary series ("Dealix outcome"):** Emerald Teal `#00D1A1`.
- **Baseline / comparison series:** Soft Silver `#B2BBC6`.
- **Grid & axis lines:** `#2E3A52` on dark, `#E5E8EC` on light.
- **Annotations:** Warning `#F2B544` for "pending approval"; Danger `#E5484D` for "blocked."
- **Categorical palette (when more than two series are needed):** Emerald Teal, Soft Silver, Info Blue, Warning Amber — in that order. Avoid rainbow palettes.

---

## 8. Don'ts | ما لا نفعله

- Do not introduce new brand hues without Brand Lead approval.
- Do not use Emerald Teal for warnings, errors, or anything negative.
- Do not use red or amber as decoration — they always carry semantic meaning.
- Do not use gradients on text.
- Do not pair Emerald Teal with white text.
- Do not use opacity to fake new colors — use the surface tokens.

---

## 9. Token Naming Convention | تسمية الرموز

```
color.<scope>.<role>.<variant?>
```

Examples: `color.bg.primary`, `color.brand.accent`, `color.semantic.warning`, `text.secondary`.

Tokens live in `tokens/colors.json` and are the only allowed source for color in product code.

---

## 10. Governance | الحوكمة

- **Owner:** Brand Lead + Design Systems Lead.
- **Audit:** Quarterly contrast audit on top 20 customer-facing screens.
- **Change gate:** New color → token PR → Brand Lead approval → token release.
- **KPI:** Zero WCAG AA failures on shipped customer surfaces.

---

## 11. Related Documents | مراجع

- `DEALIX_VISUAL_IDENTITY.md`
- `DEALIX_ACCESSIBILITY_GUIDE.md`
- `DEALIX_TYPOGRAPHY.md`
