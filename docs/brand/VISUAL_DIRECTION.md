# Dealix Visual Direction | التوجيه البصري

> **Visual identity direction: color palette, typography, layout, components, imagery, and data visualization.**
> Branch: `phase/startup-architecture-brand-os`
> This doc consolidates and directs. The source of truth for live design tokens is `frontend/tailwind.config.ts`.
> Related: [`COLOR_SYSTEM.md`](COLOR_SYSTEM.md), [`TYPOGRAPHY.md`](TYPOGRAPHY.md), [`VISUAL_IDENTITY.md`](VISUAL_IDENTITY.md), [`LOGO_USAGE.md`](LOGO_USAGE.md), [`BRAND_GUIDELINES_AR.md`](BRAND_GUIDELINES_AR.md)

---

## 0. Two Palette Note | تنبيه لوحي الألوان

The repo currently contains two closely related palette definitions. This section reconciles them so all new work is consistent.

| Source | Navy primary | Gold accent | Emerald (proof) |
|---|---|---|---|
| [`COLOR_SYSTEM.md`](COLOR_SYSTEM.md) + [`BRAND_GUIDELINES_AR.md`](BRAND_GUIDELINES_AR.md) + [`LOGO_USAGE.md`](LOGO_USAGE.md) | `#0c2742` | `#d4a843` | `#059669` |
| [`VISUAL_IDENTITY.md`](VISUAL_IDENTITY.md) + [`DEALIX_VISUAL_IDENTITY_AR.md`](DEALIX_VISUAL_IDENTITY_AR.md) | `#001F3F` | `#D4AF37` | `#10b981` |

**Directive:** `frontend/tailwind.config.ts` is the source of truth for live tokens. Where docs disagree, the `tailwind.config.ts` token wins for production UI. For brand documentation and print, use the [`COLOR_SYSTEM.md`](COLOR_SYSTEM.md) palette (`#0c2742` / `#d4a843` / `#059669`) as the documented brand standard, as it has the fuller scale (50–950) and WCAG tables. Reconcile `VISUAL_IDENTITY.md` tokens to match in a future cleanup task.

Both palettes share the same semantic structure: **Navy = primary/brand, Gold = accent, Emerald = proof/success only.**

---

## 1. Visual Identity Philosophy | فلسفة الهوية البصرية

From [`VISUAL_IDENTITY.md`](VISUAL_IDENTITY.md):

> Dealix is **Governed AI Operations for Saudi B2B**. The identity reflects that: composed, trustworthy, evidence-first — no noise, no hype.

The visual identity is **executive, not playful**. It expresses:
- **Institutional trust** — Navy depth, Gold restraint, evidence-first layout.
- **Operational seriousness** — dashboards, decision rooms, approval gates, proof cards. Not chat bubbles.
- **Saudi-native confidence** — Arabic-first typography, RTL-native layout, no translated-afterthought feel.
- **Proof over promise** — Emerald appears only when something is proven. Never as decoration.

---

## 2. Color Palette | لوحة الألوان

### 2.1 Primary: Navy (الكحلي)

The foundation. Trust, depth, institutional stability.

| Token | Hex | Use |
|---|---|---|
| navy-50 | `#eef3f8` | Very light backgrounds, tables |
| navy-100 | `#d4e0ed` | Light card fills, section backgrounds |
| navy-200 | `#9db8d5` | Subtle borders |
| navy-300 | `#678eb9` | Secondary text on dark |
| navy-400 | `#33649b` | Links |
| **navy-500** | **`#0c2742`** | **Brand primary ★** |
| navy-600 | `#081828` | Hover |
| navy-700 | `#040d16` | Dark surfaces |
| navy-800 | `#02050a` | Very dark sections |
| navy-900 | `#000103` | Darkest text/surfaces |

**Usage:** Hero backgrounds, navbar, primary buttons, page headings, footer, key section cards. Dark theme primary.

### 2.2 Accent: Gold (الذهبي)

Value, distinction, success accent. Used sparingly.

| Token | Hex | Use |
|---|---|---|
| gold-50 | `#fdf8ee` | Very light gold highlight |
| gold-100 | `#fcf1db` | Accent fills |
| gold-200 | `#f5dfa3` | Light gold borders |
| gold-300 | `#edc967` | Badges |
| gold-400 | `#e2b032` | Gold hover |
| **gold-500** | **`#d4a843`** | **Brand accent ★** |
| gold-600 | `#b48b2a` | Gold text on light |
| gold-700 | `#916d16` | Active state |
| gold-800 | `#6b4e0a` | High contrast gold |
| gold-900 | `#423004` | Darkest gold |

**Usage:** Secondary buttons, feature/service icons, accent borders, badges, `pulse-gold` on the single primary CTA, accent lines, glow on important elements.

**Guardrail:** Never use Gold for large background fills. (See [`BRAND_GUARDRAILS.md`](BRAND_GUARDRAILS.md) §4.1.)

### 2.3 Proof/Success: Emerald (الزمردي)

Proof, success, verified results. Never a brand color.

| Token | Hex | Use |
|---|---|---|
| emerald-50 | `#ecfdf5` | Light success background |
| emerald-100 | `#d1fae5` | Success fill |
| emerald-200 | `#93efc0` | Success icons |
| emerald-300 | `#51df99` | Green borders |
| emerald-400 | `#1ac771` | Bright emerald |
| **emerald-500** | **`#059669`** | **Success accent ★** |
| emerald-600 | `#037448` | Hover |
| emerald-700 | `#02522d` | Success text on light |

**Usage:** Approved status, success indicators, checkmarks, proof pack indicators, positive numbers, active service status.

**Guardrail:** Emerald is for proof/success only. Never use as a primary brand color. (See [`BRAND_GUARDRAILS.md`](BRAND_GUARDRAILS.md) §4.1.)

### 2.4 Neutral / Slate

| Token | Use | Hex (light) | Hex (dark) |
|---|---|---|---|
| Background | Page background | `#fafbfc` | `#0a0f1c` |
| Surface | Cards, forms | `#ffffff` | `#0f172a` |
| Border | Dividers, frames | `#e2e8f0` | `#1e293b` |
| Text primary | Headings, main text | `#0c2742` | `#f1f5f9` |
| Text secondary | Helper text | `#364558` | `#cbd5e1` |
| Text muted | Hints, placeholders | `#64748b` | `#94a3b8` |

### 2.5 Semantic colors

| Color | Hex | Use |
|---|---|---|
| Success | `#059669` (emerald-500) | Confirmation, completion |
| Warning | `#d97706` | Alert, attention |
| Error / Destructive | `#dc2626` | Error, rejection, rejected status |
| Info | `#2563eb` | Notice, guidance |

### 2.6 Dark mode

Dealix is a **dark-theme-primary** brand. The default executive presentation is dark Navy backgrounds with Gold accents and white/light text. Light mode exists for reading-heavy surfaces (blog, docs, long-form).

| Variable | Light | Dark |
|---|---|---|
| Background | `#fafbfc` | `#0a0f1c` |
| Surface | `#ffffff` | `#0f172a` |
| Border | `#e2e8f0` | `#1e293b` |
| Text primary | `#0c2742` | `#f1f5f9` |
| Text secondary | `#364558` | `#cbd5e1` |
| Brand primary | `#0c2742` (Navy) | `#d4a843` (Gold as accent on dark) |
| Accent | `#d4a843` (Gold) | `#d4a843` (Gold) |

### 2.7 WCAG compliance

All pairings must meet AA (4.5:1 small text, 3:1 large text). Safe pairings (from [`COLOR_SYSTEM.md`](COLOR_SYSTEM.md) §5):

| Pairing | Ratio | Level |
|---|---|---|
| Navy `#0c2742` + White `#ffffff` | 14.2:1 | AAA ✓ |
| White `#ffffff` + Navy `#0c2742` | 14.2:1 | AAA ✓ |
| Gold `#d4a843` + Navy `#0c2742` | 5.1:1 | AA ✓ |
| Emerald `#059669` + White `#ffffff` | 4.2:1 | AA ✓ |
| Navy `#0c2742` + Light Gold `#edc967` | 5.7:1 | AA ✓ |

**Unsafe (do not use):**
| Pairing | Ratio | Problem |
|---|---|---|
| Gold `#d4a843` + White `#ffffff` | 2.8:1 | Not readable for small text |
| Light Gold `#edc967` + White | 1.6:1 | Not readable at all |

---

## 3. Typography | الطباعة

### 3.1 Font stack

| Role | Arabic (primary) | English (mirror) | CSS variable |
|---|---|---|---|
| Display / Headings | Noto Kufi Arabic, Cairo | Poppins | `--font-heading`, `--font-display` |
| Body | Noto Naskh Arabic, Noto Sans Arabic, Tajawal | Inter | `--font-body` |
| Code / Mono | IBM Plex Mono | JetBrains Mono | `--font-mono` |
| General Arabic | Cairo, Noto Sans Arabic | — | `--font-arabic` |

```css
--font-arabic:   "Noto Kufi Arabic", "Noto Naskh Arabic", "Cairo", "IBM Plex Sans Arabic", system-ui, sans-serif;
--font-display:  "Cairo", "Noto Kufi Arabic", "Poppins", system-ui, sans-serif;
--font-body:     "Inter", "Noto Sans Arabic", "Tajawal", system-ui, sans-serif;
--font-mono:     "JetBrains Mono", "IBM Plex Mono", "Fira Code", monospace;
--font-heading:  "Noto Kufi Arabic", "Cairo", "Inter", system-ui, sans-serif;
```

### 3.2 Size scale (modular, 1.25 Major Third)

| Name | rem | px | Line height | Letter spacing | Weight |
|---|---|---|---|---|---|
| 7xl | 4.5rem | 72px | 1.05 | -0.03em | 700 |
| 6xl | 3.75rem | 60px | 1.05 | -0.025em | 700 |
| 5xl | 3rem | 48px | 1.1 | -0.02em | 700 |
| 4xl | 2.25rem | 36px | 1.15 | -0.015em | 700 |
| 3xl | 1.875rem | 30px | 1.2 | -0.01em | 600 |
| 2xl | 1.5rem | 24px | 1.3 | 0 | 600 |
| xl | 1.25rem | 20px | 1.35 | 0 | 600 |
| lg | 1.125rem | 18px | 1.5 | 0 | 400 |
| base | 1rem | 16px | 1.6 | 0 | 400 |
| sm | 0.875rem | 14px | 1.5 | 0 | 400 |
| xs | 0.75rem | 12px | 1.5 | 0.02em | 500 |

### 3.3 Responsive typography

```css
h1 { font-size: clamp(2rem, 5vw, 3.75rem); }
h2 { font-size: clamp(1.5rem, 3.6vw, 2.75rem); }
h3 { font-size: clamp(1.25rem, 2.5vw, 1.875rem); }
h4 { font-size: clamp(1.125rem, 1.8vw, 1.5rem); }
```

| Device | h1 | h2 | h3 | Body |
|---|---|---|---|---|
| Small mobile (320px) | 32px | 24px | 20px | 14px |
| Large mobile (414px) | 36px | 28px | 22px | 15px |
| Tablet (768px) | 44px | 32px | 26px | 16px |
| Desktop (1280px) | 52px | 38px | 28px | 16px |
| Large screen (1536px) | 60px | 44px | 30px | 18px |

### 3.4 Typography rules

- **Arabic:** line-height 1.7–1.8 (larger than English). No italic. No letter-spacing. RTL.
- **English:** line-height 1.5–1.6 body, 1.05–1.3 headings. Negative letter-spacing for large headings. LTR.
- **Never mix RTL and LTR in one paragraph.**
- **Use CSS logical properties** (`margin-inline-start`, not `margin-left`).
- **Numbers:** tabular figures for data tables and KPI comparisons.
- **Paragraph width:** 45–75 characters for readability.

(See [`TYPOGRAPHY.md`](TYPOGRAPHY.md) for the full system.)

---

## 4. Layout Principles | مبادئ التخطيط

### 4.1 Spacing scale

4 / 8 / 12 / 16 / 24 / 32 / 48 / 64px. Stick to multiples. No arbitrary pixel values.

### 4.2 Section rhythm

- **Major section vertical spacing:** 64–96px.
- **Card internal padding:** 24px.
- **Component internal spacing:** 8 / 12 / 16px per the scale.

### 4.3 Grid

- **Desktop:** 12-column grid, max content width 1280px, gutter 24px.
- **Tablet:** 8-column grid, gutter 16px.
- **Mobile:** 4-column grid, gutter 16px.

### 4.4 RTL / LTR

- Arabic pages: `dir="rtl"`, text-align right, layout flows right-to-left.
- English pages: `dir="ltr"`, text-align left, layout flows left-to-right.
- Use CSS logical properties throughout (`margin-inline-start`, `padding-inline-end`, etc.).
- Never hardcode `left`/`right` in CSS; use `inline-start`/`inline-end`.

### 4.5 Radius

Driven by `--radius` tokens (`lg`, `md`, `sm`) in `tailwind.config.ts`. No arbitrary border-radius values.

---

## 5. Component Style | نمط المكوّنات

### 5.1 Buttons

| Type | Style | Usage |
|---|---|---|
| **Primary** | Navy fill, white text. `pulse-gold` animation on the single primary CTA only. | Main CTA per page (e.g., "Book a diagnosis"). |
| **Secondary** | Navy outline, Navy text. | Secondary actions (e.g., "Explore the 14 OSes"). |
| **Accent** | Gold fill, Navy text. | Highlight actions (sparingly). |
| **Success** | Emerald fill, white text. | Success confirmations only. |
| **Destructive** | Red (`#dc2626`) fill, white text. | Reject, delete, cancel. |

**Rules:**
- One primary CTA per page. `pulse-gold` only on that one button.
- Buttons use Inter SemiBold (EN) / Cairo SemiBold (AR).
- Hover states: darken fill by one shade (e.g., navy-500 → navy-600).
- No drop shadows on buttons except a subtle Gold glow on the primary CTA.

### 5.2 Cards

| Property | Value |
|---|---|
| Background | Light surface (`#ffffff`) or dark surface (`#0f172a`) in dark mode |
| Border | `navy-100` (`#d4e0ed`) light / `#1e293b` dark |
| Radius | `md` |
| Shadow | Soft, subtle |
| Padding | 24px internal |
| Hover | Gold border accent on interactive cards |

### 5.3 Badges / Status

| Status | Color | Arabic | English |
|---|---|---|---|
| Approved / Proof | Emerald | معتمَد | Approved |
| Pending approval | Gold | بانتظار الاعتماد | Pending |
| Rejected | Destructive red | مرفوض | Rejected |
| Draft only | Light Navy | مسودة فقط | Draft only |
| Neutral info | Light Navy fill | معلومة | Info |

### 5.4 Navigation

- **Navbar:** Navy background (dark theme), white text, Gold accent on active item, logo per [`LOGO_USAGE.md`](LOGO_USAGE.md).
- **Footer:** Navy background, white/light text, disclosure line present.
- **Sticky header:** Navy with slight opacity/glassmorphism on scroll.

### 5.5 Motion

| Animation | Use | Duration |
|---|---|---|
| `fade-in` | Element entrance | 0.2–0.4s |
| `slide-in-right` | Lists, menus | 0.3s |
| `pulse-gold` | Single primary CTA | Subtle pulse |

**Rules:** Quiet and short. No distracting, flashy, or bouncy motion. No parallax. No autoplay video.

### 5.6 Proof states (critical to the brand)

Every external action passes a visible approval gate. In UI:

```
[Draft generated] → [Pending approval: Gold] → [Approved: Emerald] → [Sent]
                                                    or
                                                 [Rejected: Red]
```

This visual flow IS the brand. It must be visible in every product UI, not hidden in a settings menu.

---

## 6. Imagery Direction | توجيه الصور

### 6.1 What to use

| Type | Direction |
|---|---|
| **Product screenshots** | Real screenshots of the product UI. No exaggerated phone/device frames. |
| **Data visualizations** | Real data, clean charts in brand colors (Navy, Gold, Emerald for positive). |
| **Decision rooms / command centers** | Abstract or stylized visuals of a revenue command room, decision desk, approval queue. |
| **Revenue maps / pipeline flows** | Visual representations of pipeline, approval gates, proof flow. |
| **Patterns** | Fine grid lines, gold dot accents, subtle Navy-to-darker gradients. |
| **Proof cards** | Visual representations of Proof Packs: baseline → after → delta. |

### 6.2 What NOT to use (from [`VISUAL_IDENTITY.md`](VISUAL_IDENTITY.md), [`BRAND_GUIDELINES_AR.md`](BRAND_GUIDELINES_AR.md))

| Prohibited | Why |
|---|---|
| Generic AI robot imagery | Chatbot positioning, not OS. |
| Stock photos | Inauthentic, off-brand. |
| Stereotypical "AI" visuals (brains, neural nets as decoration) | Cliché, non-differentiating. |
| Overly colorful icons | Off-brand. |
| Low-quality images | Unprofessional. |

### 6.3 Filters and effects

| Effect | Use |
|---|---|
| Navy-to-Gold gradient | Hero backgrounds (subtle, dark-dominant) |
| Glassmorphism | Key cards on dark backgrounds |
| Gold glow | Primary CTA and important elements (subtle) |
| Dark backgrounds with fine gold dots | Section backgrounds, footer |
| Grid pattern | Hero overlay, subtle |

---

## 7. Data Visualization Style | نمط تصور البيانات

### 7.1 Principles

1. **Real data only.** No fabricated metrics in public-facing visualizations. If showing a demo, label it "demo data / بيانات تجريبية."
2. **Brand colors.** Navy for primary series, Gold for highlight/accent series, Emerald for positive deltas, red (`#dc2626`) for negative deltas.
3. **Clean over dense.** Prefer one clear insight over ten crowded metrics. White space is a feature.
4. **Tabular figures.** Use tabular numbers for all data displays so digits align.
5. **Disclosure.** Any chart showing estimated value carries the disclosure: "القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value."

### 7.2 Chart types by use case

| Use case | Chart type | Color |
|---|---|---|
| Pipeline value over time | Line chart | Navy line, Gold for the highlighted point |
| Approval queue status | Stacked bar or status list | Emerald (approved), Gold (pending), Red (rejected) |
| Baseline vs after (Proof Pack) | Paired bar or before/after comparison | Navy (baseline), Emerald (after, if positive) |
| Revenue scenario range | Range bar with confidence band | Navy range, Gold marker for the scenario point |
| KPI summary | Large number + label | Navy number, Gold label, Emerald if positive delta |
| Audit trail / decision log | Timeline or table | Navy primary, Gold for decision points, Emerald for approved |

### 7.3 Dashboard layout (Command Room)

The Revenue Command Room OS dashboard is the flagship visual expression of the brand. Layout:

```
┌────────────────────────────────────────────────────────────┐
│  Navbar (Navy, logo left, Gold active accent)               │
├────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  KPI: 42    │  │  KPI: 18    │  │  KPI: 3     │         │
│  │  فرص عالية  │  │  مسودات     │  │  موافقات    │         │
│  │  Emerald    │  │  Navy       │  │  Gold       │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │  Pipeline chart      │  │  Approval queue      │        │
│  │  (Navy line, Gold)   │  │  (status badges)     │        │
│  └──────────────────────┘  └──────────────────────┘        │
├────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────┐          │
│  │  CEO Brief (daily)                            │          │
│  │  Navy heading, body text, Gold section divs  │          │
│  └──────────────────────────────────────────────┘          │
├────────────────────────────────────────────────────────────┤
│  Footer (Navy, disclosure line)                             │
└────────────────────────────────────────────────────────────┘
```

### 7.4 KPI card style

| Element | Style |
|---|---|
| Number | 5xl (48px), Poppins SemiBold (EN) / Cairo Bold (AR) |
| Label | sm (14px), regular weight, text secondary color |
| Positive delta | Emerald, with ↑ arrow |
| Negative delta | Red (`#dc2626`), with ↓ arrow |
| Neutral | Navy or text secondary |
| Card | Light surface, navy-100 border, md radius, soft shadow |

---

## 8. Accessibility | إمكانية الوصول

From [`BRAND_GUIDELINES_AR.md`](BRAND_GUIDELINES_AR.md) §9 and [`COLOR_SYSTEM.md`](COLOR_SYSTEM.md) §5:

### 8.1 Contrast

- All color pairings must meet WCAG 2.1 AA.
- Small text (<18px): 4.5:1 minimum.
- Large text (>18px bold or >24px): 3:1 minimum.
- UI components: 3:1 minimum.

### 8.2 Structure

- Use semantic HTML (`nav`, `main`, `section`, `article`).
- Provide alt text for images (in Arabic on Arabic pages).
- Ensure keyboard navigation.
- Use `aria-labels` for interactive elements.
- Provide a skip-to-content link.

(See [`BRAND_GUIDELINES_AR.md`](BRAND_GUIDELINES_AR.md) §9 for the full accessibility guide.)

---

## 9. Do & Don't Summary | افعل ولا تفعل

| ✓ Do | ✗ Don't |
|---|---|
| Navy as base, Gold sparingly. | No Gold for large fills. |
| Arabic and English parallel and equal-weight. | No half-translation. |
| Stick to the spacing scale. | No arbitrary pixel values. |
| Emerald for proof only. | Don't use Emerald as a brand color. |
| Disclosure on every public page. | Never drop the disclosure. |
| Real product screenshots and data viz. | No stock photos or AI robot imagery. |
| Dark Navy backgrounds for executive surfaces. | No light, playful backgrounds for executive surfaces. |
| Visible approval gates in every product UI. | No hidden approval flows. |
| Tabular figures for data. | No proportional figures in data tables. |
| RTL for Arabic, LTR for English. | Never mix directions in one paragraph. |

---

## 10. Related Documents | وثائق ذات صلة

- [`COLOR_SYSTEM.md`](COLOR_SYSTEM.md) — full color palette with WCAG tables
- [`TYPOGRAPHY.md`](TYPOGRAPHY.md) — full font system, size scale, RTL/LTR rules
- [`VISUAL_IDENTITY.md`](VISUAL_IDENTITY.md) — consolidated visual identity guide
- [`LOGO_USAGE.md`](LOGO_USAGE.md) — logo usage, clear space, incorrect uses
- [`BRAND_GUIDELINES_AR.md`](BRAND_GUIDELINES_AR.md) — comprehensive Arabic brand guidelines (v2.0)
- [`DEALIX_VISUAL_IDENTITY_AR.md`](DEALIX_VISUAL_IDENTITY_AR.md) — Arabic visual identity summary
- [`BRAND_GUARDRAILS.md`](BRAND_GUARDRAILS.md) — visual guardrails (§4)
- `frontend/tailwind.config.ts` — live design tokens (source of truth)

---

> **آخر تحديث**: 1 يونيو 2026 | **الإصدار**: 1.0 | **اللغة الأساسية**: العربية
> **Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة**