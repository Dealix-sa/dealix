# Dealix Visual Identity System — نظام الهوية البصرية

> Status: LIVE · Audience: Internal (design + web) · Owner: Founder
> Source tokens: `frontend/tailwind.config.ts` · `design-systems/dealix/tokens/` · `DESIGN_SYSTEM.md`
> Related: [BRAND_IDENTITY_SYSTEM.md](BRAND_IDENTITY_SYSTEM.md) · [MESSAGING_HOUSE.md](MESSAGING_HOUSE.md)

This document **formalizes** the palette and type system already present in the repo. It does not introduce new colors. Where older brand notes disagree, the tokens in `frontend/tailwind.config.ts` are canonical.

---

## EN — Visual System

### Color palette (hex + usage)
Canonical brand families and their 500 anchors, from `frontend/tailwind.config.ts`.

| Token | Hex (500) | Role | Usage |
|---|---|---|---|
| Navy | `#001F3F` | Primary | Backgrounds, headers, navy surfaces, primary buttons base |
| Gold | `#D4AF37` | Accent | CTAs, active states, focus rings, gradient highlights |
| Emerald | `#10B981` | Success | Verified states, "LIVE", positive deltas |
| Coral / red | `#EF4444` | Error | Failures, BLOCKED, destructive actions |
| Amber | `#F59E0B` | Warning | Pending, BETA, attention |
| Ocean | `#0066FF` | Info | Links, informational notes |

Each family ships a full 50–950 scale in the config. Use tints (50–300) for surfaces and text-on-navy, shades (600–950) for depth. Navy is the canvas; gold is the single accent; emerald, coral, amber, ocean are semantic only — never decorative.

### Typography
| Layer | Stack | Class |
|---|---|---|
| Display (headings) | Poppins, Cairo | `font-display` |
| Body | Inter, Tajawal | `font-body` |
| Arabic-led | Noto Sans Arabic, IBM Plex Arabic | `font-arabic` |
| Mono (schemas/IDs) | IBM Plex Mono | `font-mono` |

Headings 700–900 weight. Body 400–600. Mono only for JSON schemas, status tokens, and identifiers — never for prose.

### Spacing & contrast principles
- Generous negative space; one idea per band.
- Contrast targets: Navy + White ≈ 12.6:1 (AAA); Gold + Navy ≈ 7.4:1 (AAA). Keep AA minimum everywhere.
- Focus ring is gold (`ring`), always visible for keyboard navigation.

### RTL rules
- Arabic pages set `dir="rtl"`; layout, icons, and progress flow mirror.
- AR and EN blocks are parallel and equal in weight — never AR as a smaller afterthought.
- Numerals and SAR pricing follow the active locale; keep alignment consistent within a block.

### Component look
- **Cards**: `bg-white/5`, `border-white/10`, gold glow on hover. Flat, no heavy shadow.
- **CTA bands**: navy surface, single gold button, one message. Exactly one main CTA per page.
- **Badges / status**: emerald = LIVE, amber = BETA, slate = INTERNAL/DOCS_ONLY, ocean = FUTURE, coral = BLOCKED, strikethrough/muted = DEPRECATED. Gold = premium label only.

### Dark executive direction
Premium dark Saudi/GCC enterprise look: navy canvas, restrained gold, emerald for verified. The system signals authority and trust, not consumer playfulness.

### What to avoid
- Childish or "AI rainbow" color schemes; neon purples/teals.
- Gradient overload — gold gradient on text only, sparingly.
- Clutter: multiple CTAs, competing accents, dense decoration.
- Off-palette colors (e.g. generic blue-700) and low-contrast gray text on white.

---

## AR — النظام البصري

### لوحة الألوان (HEX + الاستخدام)
العائلات المعتمدة ومراسيها عند 500، من `frontend/tailwind.config.ts`.

| الرمز | HEX (500) | الدور | الاستخدام |
|---|---|---|---|
| Navy | `#001F3F` | أساسي | الخلفيات، الترويسات، الأسطح، أساس الأزرار |
| Gold | `#D4AF37` | لمسة | CTAs، الحالات النشطة، حلقة التركيز، التظليل |
| Emerald | `#10B981` | نجاح | حالات مُتحقَّقة، «LIVE»، الفروق الإيجابية |
| Coral | `#EF4444` | خطأ | الإخفاقات، BLOCKED، الإجراءات الهدّامة |
| Amber | `#F59E0B` | تحذير | قيد الانتظار، BETA، الانتباه |
| Ocean | `#0066FF` | معلومة | الروابط، الملاحظات |

كل عائلة تأتي بسلّم كامل 50–950. الفواتح للأسطح والنصوص على الـ Navy، والغامقة للعمق. الـ Navy هو القماش، والـ Gold هو اللمسة الوحيدة، وبقية الألوان دلالية فقط لا زخرفية.

### الخطوط
| الطبقة | المجموعة | الفئة |
|---|---|---|
| العناوين | Poppins، Cairo | `font-display` |
| النصوص | Inter، Tajawal | `font-body` |
| العربية | Noto Sans Arabic، IBM Plex Arabic | `font-arabic` |
| الكود | IBM Plex Mono | `font-mono` |

العناوين بوزن 700–900، النصوص 400–600، والـ Mono للمخططات والمعرّفات فقط.

### المسافات والتباين
- فراغ سخي؛ فكرة واحدة لكل شريط.
- Navy + أبيض ≈ 12.6:1 (AAA)، Gold + Navy ≈ 7.4:1 (AAA). الحد الأدنى AA في كل مكان.
- حلقة التركيز ذهبية وظاهرة دوماً للتنقل بلوحة المفاتيح.

### قواعد RTL
- الصفحات العربية `dir="rtl"`؛ التخطيط والأيقونات والتقدّم تنعكس.
- العربي والإنجليزي متوازيان ومتساويان في الوزن — لا يكون العربي إضافة أصغر.
- الأرقام وتسعير SAR تتبع اللغة الفعّالة مع محاذاة متّسقة.

### مظهر المكوّنات
- **البطاقات**: `bg-white/5`، `border-white/10`، توهّج ذهبي عند المرور؛ مسطّحة بلا ظلال ثقيلة.
- **أشرطة CTA**: سطح Navy، زر ذهبي واحد، رسالة واحدة. دعوة رئيسية واحدة لكل صفحة.
- **الشارات**: emerald = LIVE، amber = BETA، رمادي = INTERNAL/DOCS_ONLY، ocean = FUTURE، coral = BLOCKED، باهت/مشطوب = DEPRECATED. الذهبي = شارة تميّز فقط.

### الاتجاه التنفيذي الداكن
مظهر مؤسسي خليجي فاخر داكن: قماش Navy، ذهبي مقتصد، emerald للتحقّق. يوحي بالسلطة والثقة لا بالعبث الاستهلاكي.

### ما يجب تجنّبه
- ألوان طفولية أو «قوس قزح AI»؛ بنفسجي/فيروزي صارخ.
- إفراط في التدرّجات — التدرّج الذهبي للنص فقط وباعتدال.
- الفوضى: دعوات متعددة، لمسات متنافسة، زخرفة كثيفة.
- ألوان خارج اللوحة ونصوص رمادية منخفضة التباين على أبيض.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
