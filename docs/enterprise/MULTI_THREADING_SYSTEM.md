# Multi-Threading System — نظام المسارات المتعددة في الحسابات المؤسساتية

**Purpose / الغرض**
Cadence rules to keep 3+ active relationship threads alive per enterprise account. Single-thread accounts are deals waiting to die.
قواعد إيقاع لإبقاء 3 مسارات علاقة نشطة على الأقل في كل حساب مؤسساتي. الحسابات أحادية المسار صفقات تنتظر الموت.

**Owner placeholder:** Account owner = `<founder>` initially.
**Cadence:** Weekly thread audit. Daily for late-stage enterprise accounts. / تدقيق أسبوعي للمسارات. يومي للحسابات في المرحلة المتأخرة.
**KPIs:** (1) % of enterprise accounts with ≥ 3 threads touched in last 14 days, (2) thread-decay events per month, (3) median days between touches per thread per active account.
**Risk if missing / مخاطر الغياب:** A single point of contact pauses, leaves, or loses internal power — and the deal evaporates. / نقطة اتصال واحدة تتوقف أو تغادر أو تفقد نفوذها الداخلي — فتتبخّر الصفقة.

---

## EN summary

Multi-threading is the discipline of building and maintaining at least three distinct relationship threads inside each enterprise account. The system has four parts: a coverage matrix (who-talks-to-whom), cadence rules (how often), decay alerts (when a thread is starving), and escalation triggers (when to involve the founder directly). Multi-threading is not "more spam" — it is more **intentional**, **infrequent**, and **dignified** contact.

## ملخص بالعربية

المسارات المتعددة انضباط لبناء وصيانة ثلاثة مسارات علاقة متمايزة على الأقل داخل كل حساب مؤسساتي. للنظام أربعة أجزاء: مصفوفة التغطية (من يتحدث مع من)، قواعد الإيقاع (كم مرة)، تنبيهات التآكل (متى يجوع المسار)، ومحفّزات التصعيد (متى يتدخل المؤسس مباشرة). المسارات المتعددة ليست «إزعاجًا أكثر» — بل تواصلًا أكثر تعمّدًا، أقل تكرارًا، وأكثر احترامًا.

---

## مصفوفة التغطية / Coverage matrix

> الصفوف: من نحن. الأعمدة: مع من نتحدث في حساب العميل. / Rows: who we are. Columns: who we talk to in the customer account.

| Dealix role \ Customer slot | Champion | Economic buyer | Blocker | Influencer | User | Procurement | Security |
|---|---|---|---|---|---|---|---|
| Founder | primary | primary | escalation | secondary | as-needed | as-needed | escalation |
| Delivery Coordinator | secondary | as-needed | — | as-needed | primary | — | — |
| Trust/QA Reviewer | — | as-needed | secondary | — | — | — | primary |
| Saudi B2B Researcher | — | — | — | secondary | — | — | — |
| RevOps Assistant | secondary | — | — | — | as-needed | primary | — |

> `primary` = صاحب المسار. `secondary` = نسخة ملاحظة. `escalation` = يُتدخّل عند الحاجة فقط. `—` = لا تواصل مباشر.

---

## قواعد الإيقاع / Cadence rules

| Account stage | Threads required | Touch frequency per thread | Channel mix per month |
|---|---|---|---|
| Pre-pilot (discovery) | 2–3 | every 10–14 days | 1 written + 1 call/in-person |
| Pilot (active sprint) | 3–4 | every 5–7 days | 2 written + 1 call/in-person |
| Post-pilot (evaluation) | 4–5 | every 7–10 days | 1 written + 1 call + 1 artifact share |
| Renewal / expansion | 3+ | every 14 days minimum | 1 written + 1 call |
| Dormant (no active conversation) | 2 | every 30 days | 1 short written + occasional value share |

> القاعدة الأهم: كل تواصل يحمل قيمة محددة أو سؤالًا محددًا. لا «اطمئنان» بلا محتوى. / Rule above all: every touch carries a specific value or a specific question. No content-free "check-in".

---

## تنبيهات تآكل المسار / Thread-decay alerts

The thread is "decaying" when one of the following is true:

| Signal | Threshold | Action |
|---|---|---|
| No touch from thread owner | > 14 days during active pilot | Owner schedules touch within 48 hours. |
| No reply from stakeholder | > 10 business days | Bridge through champion or shift to in-person. |
| Stakeholder's stance shifted toward `opposed` or `neutral` | any change | Update `docs/enterprise/STAKEHOLDER_MAP.md` + escalate to founder. |
| Account stops opening any artifact | > 14 days | Send a short, sector-relevant value share — never a "still interested?" message. |
| Champion goes silent | > 10 business days | Multi-thread coverage absorbs it; founder reaches the economic buyer directly. |

---

## محفّزات التصعيد / Escalation triggers

تُصعَّد الحالات التالية إلى المؤسس مباشرة (ولا يُكتفى بتذكرة داخلية):

1. **خروج محدّد:** champion ترك المؤسسة أو غيّر دوره.
2. **اعتراض حوكمي حاد:** Security أو Procurement رفع شرطًا غير مرن بشكل قاطع.
3. **اقتراح مالي خارج النطاق:** طلب الخصم > 20% أو شروط دفع > Net-45.
4. **تأخّر القرار > 60 يومًا** من أول عرض رسمي.
5. **ظهور منافس واضح** يُسمَّى داخل حوار العميل.

> Escalation directly to founder. Not via internal ticket queue.

---

## كل تواصل يحمل قيمة / Every touch carries value

نوع المحتوى المقبول في كل تواصل (لا يُكسر إلا بإذن مكتوب من المؤسس):

| Touch type | Acceptable content |
|---|---|
| Written (email, formal note) | A sector-relevant question, a short artifact share, a meeting proposal with explicit agenda. |
| Call | Pre-shared agenda, ≤ 3 questions, ≤ 30 minutes by default. |
| In-person | Joint working session on a specific decision or artifact. |
| Artifact share | A trust-pack section, a case-safe summary, a methodology doc — never a generic "sell" deck. |

غير مقبول:
- «بس أبي أطمئن» (Just checking in) — رسالة بلا قيمة.
- إرسال جماعي أتمتاتي إلى عدة جهات في نفس الحساب.
- استخدام WhatsApp للمتابعة بدون قبول مسبق مكتوب.
- ذكر منافس بشكل مهين.

Not acceptable: empty check-ins; automated bulk to multiple stakeholders in the same account; WhatsApp follow-up without prior written acceptance; disparaging a competitor by name.

---

## نموذج تدقيق مسارات أسبوعي / Weekly thread audit template

```yaml
audit_week: 2026-W21
accounts_reviewed:

  - account_label: riyadh-mfg-hypo-01
    threads_active: 3
    threads_required: 4
    decay_alerts:
      - slot: cfo
        last_touch_days_ago: 12
        owner: founder
        action: schedule walkthrough by 2026-06-01
    escalations: []
    next_week_priority: confirm CFO walkthrough; book security session

  - account_label: jeddah-clinic-hypo-02
    threads_active: 2
    threads_required: 3
    decay_alerts:
      - slot: ciso
        last_touch_days_ago: 18
        owner: trust-qa
        action: send trust pack section + propose 30-min session
    escalations:
      - reason: blocker objection escalating
        next_step: founder direct call within 72h
    next_week_priority: stabilize security thread before procurement starts
```

---

## ربط مع الأنظمة الأخرى / Ties

- خريطة أصحاب القرار: `docs/enterprise/STAKEHOLDER_MAP.md`.
- صياغة الرسائل وتوزيعها على الأدوار: `docs/sales-kit/v5/dealix_multi_stakeholder_outreach.md`.
- صياغة الاعتراضات بحسب الدور: `docs/29_sales_os/OBJECTION_HANDLING.md`.
- تصعيدات تخص النطاق أو السعر: `docs/revenue/DEAL_DESK_SYSTEM.md`.
- مراجعة فوز/خسارة بعد الإغلاق: `docs/revenue/WIN_LOSS_REVIEW.md`.

---

## قواعد لا تُكسر / Non-negotiables

- لا أتمتة تواصل خارجي. كل رسالة يراها بشري من Dealix قبل الإرسال، ويعتمدها المؤسس عند تجاوز عتبة الحوكمة.
- لا اقتباس عميل في تواصل مع صاحب قرار آخر دون إذن مكتوب.
- لا «ذكر اسم» منافس في حوار العميل. التركيز على ما نقدمه نحن.
- لا تواصل WhatsApp إلا بعد قبول مسبق مكتوب من الشخص، مع التزام السياسة في `docs/02_saudi_positioning/WHATSAPP_BOUNDARY.md`.

> No outreach automation. No customer quote shared cross-stakeholder without written permission. No naming a competitor in customer conversation. No WhatsApp without prior written opt-in.

---

## Disclosure / إفصاح

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

## Related canonical docs

- `docs/sales-kit/v5/dealix_multi_stakeholder_outreach.md`
- `docs/enterprise/STAKEHOLDER_MAP.md`
- `docs/29_sales_os/OBJECTION_HANDLING.md`
- `docs/revenue/DEAL_DESK_SYSTEM.md`
- `docs/revenue/WIN_LOSS_REVIEW.md`
- `docs/02_saudi_positioning/WHATSAPP_BOUNDARY.md`
