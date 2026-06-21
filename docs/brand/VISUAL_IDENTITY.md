# Dealix — Visual Identity / الهوية البصرية

> دليل الهوية البصرية الموحّد. مصدر الحقيقة للرموز (tokens): [`frontend/tailwind.config.ts`](../../frontend/tailwind.config.ts). هذه الوثيقة تشرح وتنظّم؛ لا تُعدّل الكود.
> The consolidated visual-identity guide. The source of truth for tokens is [`frontend/tailwind.config.ts`](../../frontend/tailwind.config.ts). This doc explains and organizes; it does not change code.

Dealix هي **عمليات ذكاء اصطناعي محوكمة لقطاع الأعمال السعودي**. الهوية تعكس ذلك: رصينة، موثوقة، قائمة على الدليل — لا صخب ولا مبالغة. Dealix is **Governed AI Operations for Saudi B2B**. The identity reflects that: composed, trustworthy, evidence-first — no noise, no hype.

---

## 1. الشعار / Logo

- **المسافة الآمنة / Clear space:** اترك مسافة لا تقل عن ارتفاع حرف "D" حول الشعار من كل جهة. Keep clear space of at least the cap-height of the "D" on all sides.
- **أقل مقاس / Minimum size:** 24px ارتفاعًا للشاشة، 12mm للطباعة. 24px tall on screen, 12mm in print.
- **الخلفيات / Backgrounds:** الشعار الذهبي على Navy الداكن (الأساسي)، أو Navy على أبيض. Gold logo on dark Navy (primary), or Navy on white.
- **ممنوع / Don't:** لا تمطّط، لا تُدِر، لا تُضِف ظلًا، لا تستخدم ألوانًا خارج اللوحة، لا تضعه على صورة مزدحمة. No stretching, rotating, drop shadows, off-palette colors, or busy photo backgrounds.

---

## 2. لوحة الألوان / Color Palette

اللون الأساسي **Navy `#001F3F`**، التمييز **Gold `#D4AF37`**، ولون النجاح/الإثبات **Emerald `#10b981`**. السلالم الكاملة معرّفة في `tailwind.config.ts`.

### Navy — الأساس / Primary

| Token | Hex | الاستخدام / Use |
|---|---|---|
| navy-50 | `#e6edf5` | خلفيات فاتحة جدًا / very light backgrounds |
| navy-100 | `#ccdaeb` | خلفيات بطاقات فاتحة / light card fills |
| navy-200 | `#99b5d7` | حدود خفيفة / subtle borders |
| navy-300 | `#6690c3` | نص ثانوي على داكن / secondary text on dark |
| navy-400 | `#336baf` | روابط / links |
| **navy-500** | **`#001F3F`** | **اللون الأساسي / brand primary** |
| navy-600 | `#001832` | تحويم / hover |
| navy-700 | `#001226` | خلفيات داكنة / dark surfaces |
| navy-800 | `#000c19` | أقسام داكنة جدًا / very dark sections |
| navy-900 | `#00060d` | نص أساسي داكن / darkest text |
| navy-950 | `#000306` | أعمق درجة / deepest shade |

### Gold — التمييز / Accent

| Token | Hex | الاستخدام / Use |
|---|---|---|
| gold-50 | `#fdfbf0` | تمييز فاتح جدًا / very light highlight |
| gold-100 | `#faf4d0` | خلفيات تمييز / accent fills |
| gold-200 | `#f4e89f` | حدود ذهبية فاتحة / light gold borders |
| gold-300 | `#edd463` | شارات / badges |
| gold-400 | `#e4bf2e` | تحويم على الذهبي / gold hover |
| **gold-500** | **`#D4AF37`** | **لون التمييز / brand accent** |
| gold-600 | `#b8861a` | نص ذهبي على فاتح / gold text on light |
| gold-700 | `#956414` | حالة نشطة / active state |
| gold-800 | `#7a4f14` | تباين عالٍ / high contrast |
| gold-900 | `#664116` | أغمق ذهبي / darkest gold |
| gold-950 | `#3a2108` | حدّي / extreme |

### Emerald — النجاح والإثبات / Success & Proof

يُستخدم لإشارات الإثبات والنجاح فقط (حزمة إثبات مكتملة، حالة معتمَدة). لا يُستخدم كلون أساسي. Used only for proof and success signals (Proof Pack complete, approved status). Never as a primary color.

| Token | Hex | الاستخدام / Use |
|---|---|---|
| emerald-100 | `#d1fae5` | خلفية حالة نجاح / success fill |
| emerald-400 | `#34d399` | أيقونة معتمَد / approved icon |
| **emerald-500** | **`#10b981`** | **لون النجاح / success accent** |
| emerald-700 | `#047857` | نص نجاح على فاتح / success text on light |

> الألوان الدلالية (`background`, `foreground`, `primary`, `destructive` …) مربوطة بمتغيّرات CSS (`hsl(var(--…))`) في `tailwind.config.ts` لدعم الوضع الداكن. Semantic colors are wired to CSS variables for dark mode in `tailwind.config.ts`.

---

## 3. الخطوط / Typography

| الدور / Role | الخط / Family (من `tailwind.config.ts`) |
|---|---|
| العرض / Display | `font-display` → Poppins / Cairo |
| المتن / Body | `font-body` → Inter / Tajawal |
| العربية / Arabic | `font-arabic` → Noto Sans Arabic / IBM Plex Arabic |
| الأكواد / Mono | `font-mono` → IBM Plex Mono |

### السلّم / Scale

| الاستخدام / Use | الحجم / Size | الوزن / Weight |
|---|---|---|
| H1 | 40–56px | 600 |
| H2 | 30–36px | 600 |
| H3 | 22–26px | 500 |
| متن / Body | 16–18px | 400 |
| تسمية / Caption | 13–14px | 400 |

- العربية تتطلب ارتفاع سطر أكبر قليلًا (1.7–1.8) وحجمًا مكافئًا أو أكبر بقليل من الإنجليزية. Arabic needs slightly larger line-height (1.7–1.8) and equivalent-or-larger size than English.
- اتجاه RTL للعربية، LTR للإنجليزية؛ لا تخلط الاتجاهين في فقرة واحدة. RTL for Arabic, LTR for English; never mix directions in one paragraph.

---

## 4. المسافات والزوايا / Spacing & Radius

- **سلّم المسافات / Spacing scale:** 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64px. التزم بالمضاعفات. Stick to the multiples.
- **الزوايا / Radius:** عبر `--radius` (`lg`, `md`, `sm`) في الإعداد. Driven by `--radius` (`lg`/`md`/`sm`) in config.
- **الإيقاع / Rhythm:** قسم رئيسي 64–96px رأسيًا؛ بطاقة 24px حشو داخلي. Major section 64–96px vertical; card 24px inner padding.

---

## 5. الصوت والنبرة / Voice & Tone

هادئ، موثوق، B2B سعودي، قائم على الدليل، بلا مبالغة. ممنوع: "حوّل عملك"، "خارق"، "مدعوم بالذكاء الاصطناعي" كشعار. Calm, authoritative, Saudi B2B, evidence-first, no hype. Banned: "transform your business", "supercharge", "AI-powered" as a slogan.

| ✗ تجنّب / Avoid | ✓ استخدم / Use |
|---|---|
| "نضمن لك مبيعات" | "فرص مُثبتة بأدلة" |
| "guaranteed sales" | "evidenced opportunities" |
| "حلّ ثوري مدعوم بالذكاء" | "عمليات محوكمة مع إثبات قابل للتدقيق" |
| "revolutionary AI-powered solution" | "governed operations with auditable proof" |
| "نتائج مذهلة فورًا" | "قيمة تقديرية موثّقة المصدر" |
| "instant amazing results" | "source-backed estimated value" |

كل نص عام يفصح: **القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.** Every public copy discloses this.

---

## 6. أنماط مكوّنات الواجهة / UI Component Patterns

- **الأزرار / Buttons:** أساسي = خلفية Navy ونص أبيض؛ ثانوي = حدّ Navy ونص Navy؛ تمييز = خلفية Gold ونص Navy. استخدم `pulse-gold` فقط لدعوة الإجراء الرئيسية. Primary = Navy fill, white text; secondary = Navy outline; accent = Gold fill, Navy text. Reserve `pulse-gold` for the single primary CTA.
- **البطاقات / Cards:** خلفية فاتحة، حدّ `navy-100`، زاوية `md`، ظل خفيف. Light surface, `navy-100` border, `md` radius, soft shadow.
- **الشارات / Badges:** الإثبات والنجاح بـ Emerald؛ التمييز التجاري بـ Gold؛ المعلومة المحايدة بـ Navy فاتح. Proof/success in Emerald; commercial highlight in Gold; neutral info in light Navy.
- **الحركة / Motion:** `fade-in` للظهور، `slide-in-right` للقوائم. هادئة وقصيرة (0.2–0.4s). لا حركة مشتّتة. Quiet and short (0.2–0.4s). No distracting motion.
- **حالات الإثبات / Proof states:** "معتمَد / Approved" = Emerald؛ "بانتظار الاعتماد / Pending approval" = Gold؛ "مرفوض / Rejected" = `destructive`. كل إجراء خارجي يمرّ ببوابة اعتماد مرئية. Every external action passes a visible approval gate.

---

## 7. افعل / لا تفعل / Do & Don't

| ✓ افعل / Do | ✗ لا تفعل / Don't |
|---|---|
| استخدم Navy أساسًا و Gold بقتصاد. / Navy as base, Gold sparingly. | لا تجعل الذهب لونًا للخلفيات الكبيرة. / No Gold for large fills. |
| اجعل العربية والإنجليزية متوازيتين بنفس الوزن. / Keep AR and EN parallel and equal-weight. | لا تترجم نصفًا وتترك النصف. / Don't half-translate. |
| التزم بسلّم المسافات. / Stick to the spacing scale. | لا تستخدم قيمًا عشوائية. / No arbitrary pixel values. |
| استخدم Emerald للإثبات فقط. / Emerald for proof only. | لا تستخدم Emerald كلون علامة. / Don't use Emerald as a brand color. |
| أبقِ سطر الإفصاح في كل صفحة عامة. / Keep the disclosure on every public page. | لا تحذف الإفصاح أبدًا. / Never drop the disclosure. |

---

### روابط ذات صلة / Related docs

- [`docs/LAUNCH_MASTER_PLAN.md`](../LAUNCH_MASTER_PLAN.md)
- [`frontend/tailwind.config.ts`](../../frontend/tailwind.config.ts) — رموز التصميم الحيّة / live design tokens

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
