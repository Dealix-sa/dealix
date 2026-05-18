# Dealix — الرواية والسعر الرسميان · Canonical Narrative & Price

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18
**وثائق مرافقة / Companion docs:** `MASTER_LAUNCH_OS.md` · `../COMMERCIAL_WIRING_MAP.md` · `../commercial/COMMERCIAL_CONTROL_TOWER.md`

---

## الغرض · Purpose

هذه الوثيقة هي المصدر الوحيد للحقيقة الذي يجب أن يطابقه كل أصل من أصول Dealix — صفحة هبوط، عرض تقديمي، بريد، منشور، أو مسودة تواصل. عند أي تعارض، **هذه الوثيقة تفوز**.

This document is the single source of truth that every Dealix asset must conform to — a landing page, a deck, an email, a post, or an outreach draft. On any conflict, **this document wins**.

---

## سلّم السعر الرسمي · The Canonical Price Ladder

السجل التالي مطابق لـ[`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md). أي رقم آخر خاطئ.

| `service_id` | الاسم · Name (AR / EN) | السعر · Price (SAR) | الإيقاع · Cadence | الدور · Role |
|---|---|---|---|---|
| `free_mini_diagnostic` | التشخيص المجاني / Free Mini Diagnostic | 0 | one_time | اكتشاف · discovery |
| `revenue_proof_sprint_499` | سبرنت إثبات الإيرادات / Revenue Proof Sprint | **499** | one_time | **عرض الدخول — الإسفين · THE entry wedge** |
| `data_to_revenue_pack_1500` | حزمة من البيانات إلى الإيراد / Data-to-Revenue Pack | 1,500 | one_time | توسّع · expansion |
| `growth_ops_monthly_2999` | عمليات النمو الشهرية / Growth Ops Monthly | 2,999 | per_month | retainer شهري · monthly retainer |
| `support_os_addon_1500` | إضافة دعم العمليات / Support OS Add-on | 1,500 | per_month | إضافة · add-on |
| `executive_command_center_7500` | غرفة قيادة الإدارة / Executive Command Center | 7,500 | per_month | تنفيذي · executive |
| `agency_partner_os` | منصة شركاء الوكالات / Agency Partner OS | مخصّص · custom | — | قناة · channel |

**قواعد ثابتة · Firm rules:**

- **`revenue_proof_sprint_499` عند 499 ريال هو عرض الدخول الوحيد — الإسفين.** كل تواصل بارد ودافئ يقود إليه.
- **"1 ريال" وضع اختبار فقط، وليس سعراً للعميل أبداً.** لا يظهر في أي أصل يواجه العميل.
- أرقام V14 ("Sector Sprint 5,000 ريال" و"Managed AI Partner 12,000 ريال") **معاد تأطيرها على الرتب الأعلى** من السجل — حزمة البيانات، عمليات النمو، التنفيذي، أو المخصّص. هي ليست سعر الدخول.

- **`revenue_proof_sprint_499` at 499 SAR is the only entry offer — the wedge.** Every cold and warm touch leads to it.
- **"1 SAR" is test mode only, never a customer price.** It appears in no customer-facing asset.
- The V14 figures ("Sector Sprint 5,000 SAR" and "Managed AI Partner 12,000 SAR") are **reframed onto the higher rungs** of the registry — Data-to-Revenue Pack, Growth Ops, Executive, or custom. They are not the entry price.

---

## الرواية الرسمية للمنتج · The Canonical Product Narrative

### ما هو Dealix · What Dealix IS

Dealix هو **رادار عمليات إيراد يبدأ بالموافقة (approval-first revenue-operations radar)**. يحضّر المسودات والتشخيصات والـProof Packs، ويصفّها للمراجعة. **المؤسس يوافق على كل إجراء خارجي** قبل تنفيذه.

Dealix is an **approval-first revenue-operations radar**. It prepares drafts, diagnostics, and Proof Packs, and queues them for review. **The founder approves every external action** before it executes.

### ما هو ليس · What Dealix IS NOT

- ليس bot يردّ تلقائياً على الـleads. · Not a bot that auto-replies to leads.
- ليس أداة تحجز demos تلقائياً. · Not a tool that auto-books demos.
- ليس خدمة تَعِد بإيراد أو ROI مضمون. · Not a service that promises guaranteed revenue or ROI.
- لا يرسل رسائل خارجية نيابة عن العميل دون موافقة صريحة. · Does not send external messages on the customer's behalf without explicit approval.

---

## قائمة الادعاءات الممنوعة · Forbidden Claims List

| الادعاء الممنوع · Forbidden claim | البديل المعتمد · Approved replacement | المرتبط بـ · Tied to non-negotiable |
|---|---|---|
| "يرد خلال 45 ثانية" / "45 second auto-reply" | "يجهّز متابعة مُسجَّلة ومُسوَّدة خلال دقائق لموافقة المؤسس" · "prepares a scored, drafted follow-up within minutes for founder approval" | `no_live_send` |
| "يحجز demo تلقائياً" / "يحجز demos" / auto-booking | "يجهّز مسودة حجز جاهزة لموافقة المؤسس" · "prepares a booking-ready draft for founder approval" | `no_live_send` |
| "Pilot بـ 1 ريال" / "1 SAR pilot" | "سبرنت إثبات الإيرادات بـ 499 ريال" · "Revenue Proof Sprint at 499 SAR" | `no_hidden_pricing` |
| "نضمن ROI / إيراد" / "guaranteed ROI / revenue" | "فرص مُثبتة بأدلة" · "evidenced opportunities" | `no_unverified_outcomes` |
| أي إرسال خارجي آلي · any automated external send | "تحضير + صفّ + موافقة بشرية" · "preparation + queuing + human approval" | `no_live_send`, `no_unbounded_agents` |

---

## قاعدة المطابقة · Conformance Rule

كل أصل جديد أو معدَّل — markdown، صفحة هبوط، قالب، منشور — يجب أن يطابق هذه الوثيقة قبل النشر. عند أي تعارض بين أصل وهذه الوثيقة، **هذه الوثيقة تفوز** ويُصحَّح الأصل. لا استثناءات.

Every new or edited asset — markdown, landing page, template, post — must conform to this document before publication. On any conflict between an asset and this document, **this document wins** and the asset is corrected. No exceptions.

---

## سجل المصالحة · Reconciliation Backlog

أصول لا تزال تحمل الرواية القديمة ("45 ثانية" / "1 ريال"). تُصحَّح بالترتيب التالي.

### Tier 1 — مواجِه للعميل ونشط، يُصحَّح أولاً · Active customer-facing, fix first

- [`../ops/today_send_queue.md`](../ops/today_send_queue.md)
- [`../ops/strategic_send_queue.md`](../ops/strategic_send_queue.md)
- [`../ops/partner_send_queue.md`](../ops/partner_send_queue.md)
- [`../sales-kit/dealix_pitch_deck.md`](../sales-kit/dealix_pitch_deck.md)
- [`../sales-kit/dealix_onepager.md`](../sales-kit/dealix_onepager.md)
- `../sales-kit/dealix_onepager.html`
- `../../landing/index.html`
- `../../landing/founder.html`
- `../../landing/roi.html`
- `../../landing/case-study.html`

### Tier 2 — جسم عدّة المبيعات · Sales-kit body

- مدوّنات `docs/sales-kit/dealix_*` · the `docs/sales-kit/dealix_*` blog posts
- تسلسلات الـdrip · drip sequences
- سكربتات الـdemo · demo scripts
- سكربتات الفيديو · video scripts

### Tier 3 — أرشيفي/تاريخي، يُترك كسجل مؤرَّخ ولا يُعاد كتابته · Archival/historical, leave as a dated record

- [`DEALIX_LAUNCH_NOW_BUNDLE.md`](DEALIX_LAUNCH_NOW_BUNDLE.md)
- [`FINAL_LAUNCH_INSTRUCTIONS.md`](FINAL_LAUNCH_INSTRUCTIONS.md)
- [`../ops/LAUNCH_DAY_ONE_KIT.md`](../ops/LAUNCH_DAY_ONE_KIT.md)
- ملفات بيانات `docs/ops/lead_machine/` · the `docs/ops/lead_machine/` data files

**ملاحظة · Note:** ملف [`../ops/launch_content_queue.md`](../ops/launch_content_queue.md) **مُصالَح في هذا التغيير نفسه** — لم يعد يحمل الرواية القديمة.

The file [`../ops/launch_content_queue.md`](../ops/launch_content_queue.md) is **reconciled in this same change** — it no longer carries the old narrative.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
