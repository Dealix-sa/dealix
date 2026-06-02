# Renewal Engine — محرّك التجديد — Renewal Engine

> Purpose — الغرض: يشرح هذا المستند سلّم التجديد ومحفّزاته. التجديد والترقية يُولَّدان كمسودات `pending_approval` فقط؛ لا يُرسل النظام عرض تجديد تلقائيًا، ولا يُجدّد اشتراكًا أو يخصم مبلغًا من تلقائه.
>
> This document explains the renewal ladder and its triggers. Renewal and upsell are generated as `pending_approval` drafts only; the system never sends a renewal offer automatically, nor renews a subscription or charges on its own.

Cross-link — روابط: [PROPOSAL_FACTORY_AR.md](./PROPOSAL_FACTORY_AR.md) · [PAYMENT_HANDOFF_AR.md](./PAYMENT_HANDOFF_AR.md) · [WIN_LOSS_LEARNING_AR.md](./WIN_LOSS_LEARNING_AR.md) · [../08_value_os/VALUE_OS.md](../08_value_os/VALUE_OS.md) · [../03_commercial_mvp/RETAINER_PATH.md](../03_commercial_mvp/RETAINER_PATH.md).

---

## 1. القاعدة الحاكمة — The governing rule

محرّك التجديد **يولّد** مسودة `renewal_upsell` للموافقة، ولا **يجدّد** شيئًا. القرار النهائي بشري، والدفع يتبع تسليم الدفع نفسه (راجع [PAYMENT_HANDOFF_AR.md](./PAYMENT_HANDOFF_AR.md)). لا تجديد تلقائي ولا خصم تلقائي.

The renewal engine generates a `renewal_upsell` draft for approval; it renews nothing. The final decision is human, and payment follows the same handoff path. No auto-renew, no auto-charge.

تُخزَّن سجلّات التجديد في `data/revenue_execution/renewals.jsonl` (قابل للتجاوز عبر `DEALIX_REVX_RENEWALS_PATH`).

---

## 2. سلّم التجديد — The renewal ladder

التجديد يرتقي على السلّم التجاري الخماسي حسب القيمة المُثبتة. المسار النموذجي صعودًا:

Renewal climbs the 5-rung commercial ladder according to proven value. The typical upward path:

| من — From | إلى — To | المنطق — Logic |
|---|---|---|
| Rung 1 (Sprint 499) | Rung 3 (Managed 2,999–4,999/mo) | السبرنت أثبت القيمة → تشغيل مُدار |
| Rung 2 (Data Pack 1,500) | Rung 3 (Managed) | البيانات جُهّزت → إدارة مستمرّة |
| Rung 3 (Managed) | Rung 3 أعلى أو Rung 4 (Custom 5k–25k) | حاجة أعمق → خدمة مخصّصة |
| Rung 4 (Custom) | Enterprise (Governance Review 25k–50k) | نضج مؤسسي → مراجعة حوكمة |

الأسعار من السلّم القانوني فقط (راجع [PROPOSAL_FACTORY_AR.md](./PROPOSAL_FACTORY_AR.md)). لا تُخترَع أسعار تجديد خارجه.

Prices come only from the canonical ladder; no renewal prices are invented outside it.

---

## 3. المحفّزات — Triggers

| المُحفِّز — Trigger | المسودة المُولَّدة — Generated draft | التوقيت — Timing |
|---|---|---|
| نافذة التجديد — Renewal window | `renewal_upsell` | يوم 21–30 من الاشتراك |
| قيمة مُثبتة كافية — Sufficient proven value | `renewal_upsell` لدرجة أعلى | عند بلوغ عتبة القيمة |
| اقتراب نهاية اشتراك — Subscription nearing end | تذكير تجديد للمؤسس | قبل التجديد بأسبوع |
| طلب توسّع من العميل — Customer expansion ask | عرض ترقية | عند الطلب |

كل محفّز يُنتج مسودة `pending_approval` تظهر في حلقة المؤسس اليومية (راجع [DRAFT_APPROVAL_RUNBOOK_AR.md](./DRAFT_APPROVAL_RUNBOOK_AR.md)).

Every trigger produces a `pending_approval` draft appearing in the founder's daily loop.

---

## 4. شروط الترقية — Upsell conditions

لا يُقترَح صعود درجة دون أساس من القيمة:

A rung climb is not proposed without a value basis:

- قيمة مُلاحَظة أو مُتحقَّقة مسجّلة في `value_os` (لا تقدير وحده).
- Proof Pack مكتمل للمشروع السابق (البند 10).
- علاقة عمل نشطة ومالك سير عمل مُسمّى مستمرّ (البند 9).

> لا ترقية بادعاء قيمة غير مسنود — No upsell on an unsupported value claim. القيمة المذكورة في عرض التجديد تتبع تمييز Estimated/Observed/Verified (البند 4، 5).

---

## 5. الاحتفاظ مقابل التجديد — Retention vs renewal

التجديد ليس تلقائيًا حتى للعميل الراضي؛ كل دورة تجديد فرصة لإعادة إثبات القيمة. إن لم تُثبَت القيمة، الأنزه اقتراح إغلاق نظيف لا تجديد بالعطالة (راجع [RETAINER_PATH.md](../03_commercial_mvp/RETAINER_PATH.md)).

Renewal is not automatic even for a satisfied customer; each cycle is a chance to re-prove value. If value is not proven, the honest move is a clean close, not a renewal by inertia.

---

## 6. ما لا يفعله المحرّك — What the engine will not do

- لا يجدّد اشتراكًا تلقائيًا.
- لا يخصم مبلغًا تلقائيًا (الدفع يتبع تسليم الدفع اليدوي).
- لا يرسل عرض تجديد دون موافقة المؤسس (البند 8).
- لا يَعِد بنتائج التجديد كحقيقة (البند 5).

The engine will not: auto-renew; auto-charge; send a renewal offer without founder approval; or promise renewal outcomes as fact.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
