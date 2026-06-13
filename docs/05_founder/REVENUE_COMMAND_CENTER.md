<!-- Wave 6 | Owner: Founder | Arabic-first — العربية أولاً -->

# Dealix Revenue Command Center — مركز قيادة الإيراد

**Purpose / الغرض:** Track the full revenue-to-proof path in one place:
Target → Outreach → Reply → Diagnostic → Offer → Paid Sprint → Delivery → Proof Pack → Upsell.

**هذا الملف هو المصدر الوحيد لمخطط (schema) ملفات `data/revenue/*.jsonl`.**

---

## القواعد غير القابلة للتفاوض / Doctrine rules

> مرجع: `docs/00_foundation/NON_NEGOTIABLES.md` و `docs/DEALIX_OPERATING_CONSTITUTION.md`.

- **no auto-send** — لا إرسال آلي لأي رسالة خارجية.
- **manual outreach only** — كل تواصل يدوي.
- **founder approval required** — كل رسالة خارجية تحتاج موافقة المؤسس قبل الإرسال.
- **no fake proof** — لا إثبات مفبرك. كل ادعاء يحتاج evidence.
- **no guaranteed revenue** — لا ضمان إيراد. نستخدم إطار "KPI commitment".
- **no customer names without approval** — لا أسماء عملاء علنية بدون إذن كتابي.
- **no scraping / no cold WhatsApp / no LinkedIn automation.**
- **revenue truth** — الإيراد يُحتسب فقط بعد دليل دفع (payment evidence). مسودة فاتورة أو
  اهتمام شفهي ليست إيرادًا.

---

## Pipeline stages — مراحل المسار

ترتيب المراحل (قيمة الحقل `stage`):

| # | stage | الوصف |
|---|-------|-------|
| 1 | `research` | بحث أولي عن الشركة |
| 2 | `qualified` | مطابقة ICP + نقاط ألم محتملة |
| 3 | `founder_reviewed` | راجعها المؤسس |
| 4 | `draft_ready` | مسودة رسالة جاهزة |
| 5 | `sent_manually` | أُرسلت يدويًا بعد موافقة |
| 6 | `reply` | وصل رد |
| 7 | `diagnostic_booked` | حُجز موعد تشخيص |
| 8 | `diagnostic_done` | تم التشخيص |
| 9 | `offer_sent` | أُرسل عرض Command Sprint |
| 10 | `paid` | تم الدفع (payment evidence) |
| 11 | `delivery_started` | بدأ التسليم / Workspace |
| 12 | `proof_pack_delivered` | سُلّم Proof Pack |
| 13 | `upsell_offered` | عُرض Upsell |
| 14 | `managed_os_closed` | أُغلق Managed Business OS |
| — | `nurture` | متابعة لاحقة |
| — | `rejected` | غير مناسب |

---

## Record schema — مخطط السجل

كل سطر في `data/revenue/*.jsonl` كائن JSON واحد، snake_case، تواريخ ISO-8601، ويتضمن **على الأقل**:

| field | type | example |
|-------|------|---------|
| `date` | string (ISO date) | `"2026-06-05"` |
| `company` | string | `"Example Agency"` |
| `sector` | string | `"b2b_marketing_agency"` |
| `source` | string | `"warm_intro"` / `"referral"` |
| `stage` | enum (above) | `"qualified"` |
| `owner` | string | `"founder"` |
| `next_action` | string | `"draft personalized message"` |
| `due_date` | string (ISO date) | `"2026-06-07"` |
| `evidence` | string (url/ref) | `"https://..."` |
| `risk` | string | `"no clear contact path"` |
| `notes` | string | `"met at event"` |

سجلات خاصة بكل ملف تضيف حقولًا فوق ما سبق:
- `outreach_queue.jsonl` → `person_or_role`, `evidence_url`, `pain_hypothesis`, `message`,
  `cta`, `approval_status` (`draft`/`approved`/`rejected`/`sent`), `founder_review_notes`,
  `sent_date`. **لا يُسمح بـ `sent` إلا إذا `approval_status = approved`.**
- `diagnostics.jsonl` → `score`, `top_blockers`, `os_fit`, `sprint_fit_score`,
  `outcome` (`not_fit`/`nurture`/`command_sprint_offer`/`partner_path`), `no_fit_reason`.
- `offers.jsonl` → `scope`, `deliverables`, `timeline`, `price_sar`, `payment_status`,
  `what_not_included`, `next_step`.
- `payments.jsonl` → `amount_sar`, `payment_status`, `payment_evidence`, `paid_date`.
- `upsells.jsonl` → `proof_pack_ref`, `recommended_upsell`
  (`none`/`starter_command`/`business_ops`/`executive_os`), `mrr_sar`, `decision`.

> **مهم — البيانات لا تُرفع إلى Git:** ملفات `data/revenue/*.jsonl`،
> `data/customers/customer_health.jsonl`، و `data/growth/first_30_targets.csv` هي **حالة
> تشغيل محلية** وتقع تحت `.gitignore` (القاعدة: لا تُرفع أي بيانات عملاء أو أسماء عملاء إلى
> المستودع). تبدأ **فارغة** وتُنشأ تلقائيًا عبر
> `python scripts/verify_wave6_revenue_rhythm.py` إن لم تكن موجودة. لا بيانات مفبركة.

---

## Daily operating loop — الدورة اليومية

1. `python scripts/founder_daily_command.py` → يولّد `reports/founder/daily_command.md`.
2. راجع `reports/revenue/outreach_approval_queue.md` ووافق على المسودات قبل أي إرسال يدوي.
3. حدّث المرحلة (`stage`) لكل شركة بعد كل تفاعل.
4. أي `payment_status = paid` → `python scripts/create_customer_workspace.py --name <slug>`.
5. تابع التسليم عبر `reports/delivery/daily_delivery_brief.md`.
6. بعد Proof Pack → سجّل قرار Upsell في `data/revenue/upsells.jsonl`.

## Related artifacts
- Targets: `docs/06_growth/FIRST_30_TARGETS_PLAYBOOK.md`, `data/growth/first_30_targets.csv`
- Diagnostic: `sales/DIAGNOSTIC_SCRIPT.md`, `sales/DIAGNOSTIC_SCORECARD.md`
- Offer: `sales/COMMAND_SPRINT_TERMS.md`, `sales/PROPOSAL_TEMPLATE.md`
- Delivery: `docs/04_delivery/PAID_SPRINT_HANDOFF.md`, `docs/04_delivery/DELIVERY_DAILY_RHYTHM.md`
- Upsell: `docs/04_delivery/PROOF_TO_UPSELL_PLAYBOOK.md`, `sales/MANAGED_BUSINESS_OS_OFFER.md`
- Weekly: `docs/05_founder/WEEKLY_CEO_REVIEW.md`
- Verify: `python scripts/verify_wave6_revenue_rhythm.py`
