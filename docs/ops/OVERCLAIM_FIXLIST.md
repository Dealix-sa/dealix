# Overclaim Fix-List — قائمة تصحيح المبالغات

**Status: AWAITING FOUNDER REVIEW**
**Compiled:** 2026-05-18
**Owner:** Workstream A — Narrative unification & overclaim cleanup

> This file is an **audit**, not an applied change. It lists every overclaim
> found outside `docs/ops/launch_content_queue.md` (which was rewritten in
> the same workstream). Landing HTML is **not** edited here — the founder
> reviews and applies these fixes. Every replacement is doctrine-true under
> [`docs/CANONICAL_PRODUCT_NARRATIVE.md`](../CANONICAL_PRODUCT_NARRATIVE.md)
> and [`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md).

## Overclaim patterns being retired

| Pattern | Why it is wrong |
|---|---|
| "45 ثانية" / "45-second reply" | Implies an SLA Dealix does not commit to; implies auto-reply. Dealix drafts; the founder approves before sending. |
| "مندوب مبيعات AI" / "AI sales rep" | Positions Dealix as an autonomous rep. It is an approval-first revenue-ops radar. |
| "يحجز / يحجز اجتماعات تلقائياً" / auto-book | Constitution Article II — no agent makes an external commitment on its own. Booking is human-approved. |
| "1 ريال" / "1 SAR pilot" | Not a real ladder price. Entry = Free Diagnostic; first paid step = 499 SAR Sprint. |
| "صفر code" / "zero code" | Not a doctrine claim; reads as marketing fluff. |
| "يرسل / Outreach Agent safe auto" | Implies auto-send. Every external message requires founder approval. |

---

## Fixes — landing/ HTML (DO NOT auto-edit; founder applies)

### `landing/founder.html`

- **Line 7** (`<meta name="description">`)
  - Offending: `... لخدمة الشركات السعودية بـ AI sales rep بالعربي الخليجي.`
  - Replacement: `... لخدمة الشركات السعودية برادار عمليات إيراد بموافقة المؤسس بالعربي الخليجي.`
- **Line 10** (`<meta property="og:description">`)
  - Offending: `... بـ AI sales rep بالعربي الخليجي.`
  - Replacement: `... برادار عمليات إيراد بموافقة المؤسس بالعربي الخليجي.`
- **Line 64**
  - Offending: `Dealix هو الجواب: AI sales rep بالعربي الخليجي يجلس فوق CRM الحالي ويرد على inbound خلال 45 ثانية — قبل أن يبرد الـ lead.`
  - Replacement: `Dealix هو الجواب: رادار عمليات إيراد بموافقة المؤسس بالعربي الخليجي يجلس فوق CRM الحالي، يكشف فرص الـ inbound المتسربة ويصيغ مسودات تواصل — وأنت تعتمد كل رسالة قبل إرسالها.`

### `landing/index.html`

- **Line 218** (chat-demo bot bubble)
  - Offending: `... Dealix مندوب مبيعات AI بالعربي الخليجي، يرد على leads شركتك ويؤهّلهم ويحجز demos ...`
  - Replacement: `... Dealix رادار عمليات إيراد بموافقة المؤسس بالعربي الخليجي، يقرأ leads شركتك ويصيغ مسودات تأهيل ومتابعة تعتمدها قبل الإرسال ...`
- **Line 222** (chat-demo bot bubble)
  - Offending: `... Dealix يختصر هذا لـ ٤٥ ثانية + يؤهّل تلقائي. أقدر أحجز لك demo ...`
  - Replacement: `... Dealix يكشف هذه الفرص المتسربة ويصيغ مسودة المتابعة — وأنت تعتمدها. تحب نرتّب لك تشخيص مجاني 15 دقيقة؟`
- **Line 459** — `قد يستغرق 15-45 ثانية` describes a page-render/processing time, **not** a reply SLA. Lower priority; acceptable if reworded to avoid the "45 ثانية" token, e.g. `قد يستغرق بضع ثوانٍ`. Founder discretion.

### `landing/pricing.html`

- **Line 234** (comparison table header)
  - Offending: `Pilot 1 ريال`
  - Replacement: `Free Diagnostic` / `التشخيص المجاني` — and align the column body to the Free Diagnostic scope. The first paid column should be `Sprint 499`.

### `landing/marketers.html`

- **Line 464** (CTA button)
  - Offending: `ابدأ بـ 1 ريال`
  - Replacement: `ابدأ بتشخيص مجاني`
- **Line 662**
  - Offending: `ادفع شهرياً أو سنوياً — ابدأ بـ 1 ريال لـ 7 أيام.`
  - Replacement: `ابدأ بتشخيص مجاني — ثم Sprint إثبات الإيراد 499 ريال لـ 7 أيام.`

### `landing/roi.html`

- **Line 173** (comparison table row)
  - Offending: `زمن الرد | 45 ثانية بالعربي`
  - Replacement: change the row to a doctrine-true metric, e.g. `سرعة كشف الفرص | مسودة متابعة جاهزة للاعتماد خلال دقائق`. Remove the "45 ثانية" reply-SLA framing.

### `landing/case-study.html`

- **Line 95**
  - Offending: `Dealix يرد بالعربي الخليجي خلال 45 ثانية`
  - Replacement: `Dealix يصيغ مسودة رد بالعربي الخليجي يعتمدها فريقك قبل الإرسال`
- **Line 139**
  - Offending: `... قبل ما يحجز معاينة. الموظف البشري يصله lead جاهز ...`
  - Replacement: `... ويصيغ مسودة دعوة لمعاينة يعتمدها الموظف. الموظف البشري يصله lead جاهز ...`
  - Note: this is a case study — confirm it is labeled "Hypothetical / case-safe" and contains no real customer PII.

### `landing/case-study-pilot-example.html`

- **Line 94**
  - Offending: `... AI يقترح رد بـ ≤ 45 ثانية. فريقك يعتمد بكبسة زر ...`
  - Replacement: `... AI يقترح مسودة رد. فريقك يراجع ويعتمد بكبسة زر — أو يعدّل أولاً.`
  - Remove the "45 ثانية" timing claim; keep the approval-first framing.

### `landing/command-center.html`

- **Line 405** (Outreach Agent)
  - Offending: `Outreach Agent | يرسل عبر القناة المثلى | badge: safe auto`
  - Replacement: relabel to draft-and-approve, e.g. `يصيغ مسودة التواصل عبر القناة المثلى` and change the badge from `safe auto` to `approval`. Auto-send is not doctrine-true.
- **Line 407** (Meeting Agent)
  - Offending: `Meeting Agent | يحجز اجتماعات تلقائياً | badge: approval`
  - Replacement: `يصيغ مسودة دعوة اجتماع للاعتماد` (badge `approval` is already correct; the description must not say "تلقائياً").

### `landing/autopilot.html`

- **Line 97**
  - Offending: `11 AI Agents يعملون لك 24/7 — ... يرسلون بعد موافقتك ... يحجزون الاجتماعات ...`
  - Replacement: `11 AI Agents يصيغون لك مسودات على مدار الساعة — يكتشفون الشركات السعودية، يفهمون الإشارات، يكتبون مسودات رسائل عربية مخصصة، يفحصون PDPL، ويجهّزون كل شيء لاعتمادك. لا إرسال ولا حجز إلا بموافقتك الصريحة لكل رسالة.`
  - Note: "يرسلون بعد موافقتك" is borderline — keep only if it clearly means per-message approval, never bulk auto-send.

### `landing/verticals.html`

- **Line 197**
  - Offending: `عملاؤكم يطلبون "AI sales rep بالعربي" — لا تملكون`
  - Replacement: `عملاؤكم يطلبون "رادار عمليات إيراد بالعربي" — لا تملكون`

### `landing/compare.html`

- **Line 142** — comparison cell `⚠️ Sales rep` refers to a competitor category, not a Dealix self-claim. **No change required**; listed for completeness.

### `landing/personal-operator.html`

- **Lines 28, 47** — describe the operator that "يحجز اجتماعات" / "يحجز بموافقتك". The "بموافقتك" qualifier is present, so these are doctrine-aligned. **Low priority** — optionally reword "يحجز" to "يصيغ مسودة حجز" for consistency. Founder discretion.

---

## Investment deck — status

- `landing/investor.html` and `docs/sales-kit/dealix_investor_faq.md` were
  scanned for all six overclaim patterns. **No overclaim hits found** in the
  investor surfaces. (`dealix_investor_faq.md` line 121 mentions a "Sales Rep"
  hire in a headcount plan — that is an HR role, not a product claim. No change.)

---

## Broader repo — flagged for a later pass (out of this workstream's edit scope)

A repo-wide grep surfaced the same patterns across ~150 files, heavily in
`docs/sales-kit/`, `docs/business/`, `docs/ops/lead_machine/`, and older
launch docs. These are sales-asset content and should be reconciled to the
canonical narrative in a dedicated follow-up workstream. They are listed here
as a pointer, not itemized — the priority fixes are the customer-facing
landing pages above. Notable clusters:

- `docs/sales-kit/` — multiple files use "AI sales rep", "45 ثانية",
  "1 ريال", and the `dealix_1_riyal_test.sh` script name.
- `docs/business/` — launch kits and press releases (`PRESS_RELEASE_AR.md`,
  `PRESS_RELEASE_EN.md`, `FOUNDER_LAUNCH_KIT.md`) carry the old narrative.
- `docs/ops/FIRST_REVENUE_GUARANTEE_PLAYBOOK.md` — the filename itself uses
  "GUARANTEE"; review for guaranteed-outcome language.
- `docs/ops/lead_machine/` — pre-generated message JSON/CSV may embed the
  old "45 ثانية" / "يحجز" copy.

---

## Cross-links the founder should resolve

- The repo has no `alembic/` directory; the persistence migration is at
  `db/migrations/versions/20260518_013_launch_persistence.py` (revision 013).
  The `no_overclaim.yaml` evidence paths were set to this real path.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
