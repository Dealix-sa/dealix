# Enterprise Stakeholder Map — خريطة أصحاب القرار في المؤسسات

**Purpose / الغرض**
Per-account template that names every role in an enterprise buying group, their stance, and the next action. Without this map, deals depend on one human relationship — and one human leaves.
قالب لكل حساب يسمّي كل دور في مجموعة الشراء داخل المؤسسة، موقفه، والإجراء التالي. بدون هذه الخريطة، تعتمد الصفقات على علاقة بشرية واحدة — وذلك الإنسان قد يغادر.

**Owner placeholder:** Account owner = `<founder>` initially.
**Cadence:** Refreshed after every customer interaction. Full review weekly for active enterprise accounts. / تُحدَّث بعد كل تفاعل مع العميل. مراجعة كاملة أسبوعيًا للحسابات النشطة.
**KPIs:** (1) % of accounts with ≥ 3 mapped stakeholders, (2) % of accounts with ≥ 3 stakeholders touched in the last 14 days, (3) count of accounts with no champion identified.
**Risk if missing / مخاطر الغياب:** Deals die when the single contact rotates, leaves, or stops championing. PII becomes the only memory. / تموت الصفقات حين يتحرّك جهة الاتصال الوحيدة أو تغادر أو تتوقّف عن المساندة. تصبح بيانات الشخص الذاكرة الوحيدة.

---

## EN summary

For each enterprise account, you map seven role slots: champion, economic buyer, blocker, influencer, user, procurement, and security. Each slot is filled with a labelled placeholder (no PII in this doc), the person's stance (supportive / neutral / opposed), the last touch date, the next action, and the multi-thread status. The map is the single source of truth for who knows what about Dealix in this account.

## ملخص بالعربية

لكل حساب مؤسساتي، تُملأ سبع خانات أدوار: champion، المشتري الاقتصادي، المعارض، المؤثر، المستخدم، المشتريات، الأمن. كل خانة تأخذ تسمية placeholder (دون PII)، الموقف (داعم/محايد/معارض)، تاريخ آخر تواصل، الإجراء التالي، وحالة المسارات المتعددة. الخريطة هي مصدر الحقيقة الوحيد لمن يعرف ماذا عن Dealix في هذا الحساب.

---

## الأدوار السبعة / The seven roles

| Slot | الدور | Description |
|---|---|---|
| `champion` | المُؤيِّد الداخلي | الشخص الذي يبيع نيابة عنا داخل المؤسسة عندما لا نكون في الغرفة. |
| `economic_buyer` | المشتري الاقتصادي | الشخص الذي يمكنه قول «نعم» للسعر النهائي. |
| `blocker` | المعارض | الشخص الذي يمكنه قول «لا» وحده ويفسد الصفقة. |
| `influencer` | المؤثر | يوصي ولا يقرر، لكن صوته مسموع. |
| `user` | المستخدم | من سيستخدم المخرجات في عمله اليومي. |
| `procurement` | المشتريات | الفريق الذي يمتلك مسار الشراء، الفواتير، البائعين. |
| `security` | الأمن / الحوكمة | فريق المخاطر، الأمن، الحماية، الامتثال (PDPL). |

> ليس كل حساب يحتاج 7 ملفّات. لكن أي خانة مُحدَّدة لكنها فارغة هي إشارة احمر. / Not every account needs 7 names. But any slot marked relevant yet empty is a red flag.

---

## مخطّط الحقول لكل صاحب قرار / Per-stakeholder schema

```yaml
account_label: <opaque label, e.g., riyadh-mfg-A>      # no PII at company level
slot: champion | economic_buyer | blocker | influencer | user | procurement | security
name_placeholder: <role-tag>                            # e.g., "Ops Director"
title_placeholder: <title only, no full name>
stance: supportive | neutral | opposed
confidence_in_stance: low | med | high
last_touch_date: YYYY-MM-DD
last_touch_channel: in-person | call | email | written-doc | event
next_action: <one line, with owner and due date>
next_action_due: YYYY-MM-DD
multi_thread_status: covered | exposed
notes: |
  <one paragraph; never store PII; refer to permission status>
permission_to_quote: yes | no | not-asked
```

- `name_placeholder` يستخدم تسمية دور، ليس اسمًا. التسمية تفصل تواصل العمل عن سجل الـ CRM الذي يحوي PII.
- `multi_thread_status: exposed` تعني هذه الخانة معتمدة على شخص واحد فقط.
- `permission_to_quote: no` تعني لا اقتباس عام ولا استشهاد في Trust Pack.

---

## مثال مُعبَّأ — مصنّع افتراضي في الرياض / Filled example — hypothetical Riyadh manufacturer

> هذا حساب افتراضي. القالب فقط. أي تشابه مع شركة حقيقية مصادفة. / Hypothetical account. Template only. Any resemblance to a real entity is coincidental.

```yaml
account_label: riyadh-mfg-hypo-01

stakeholders:

  - slot: champion
    name_placeholder: ops-director
    title_placeholder: Operations Director
    stance: supportive
    confidence_in_stance: high
    last_touch_date: 2026-05-22
    last_touch_channel: in-person
    next_action: send Revenue Intelligence sprint scope draft (founder)
    next_action_due: 2026-05-26
    multi_thread_status: covered
    notes: |
      Driving the internal narrative on revenue visibility.
      Has direct access to the CFO weekly.
    permission_to_quote: not-asked

  - slot: economic_buyer
    name_placeholder: cfo
    title_placeholder: Chief Financial Officer
    stance: neutral
    confidence_in_stance: med
    last_touch_date: 2026-05-15
    last_touch_channel: call
    next_action: arrange 30-minute walkthrough of unit economics
    next_action_due: 2026-06-01
    multi_thread_status: exposed
    notes: |
      Has not seen any written proof artifact yet.
      Risk: champion may oversell internally.
    permission_to_quote: no

  - slot: blocker
    name_placeholder: it-director
    title_placeholder: IT Director
    stance: opposed
    confidence_in_stance: high
    last_touch_date: 2026-05-10
    last_touch_channel: email
    next_action: book security review session, share trust pack section on data handling
    next_action_due: 2026-05-31
    multi_thread_status: exposed
    notes: |
      Concern centered on data residency and access scopes.
      Reference docs/governance/PDPL_DATA_RULES.md before this meeting.
    permission_to_quote: no

  - slot: influencer
    name_placeholder: head-of-bd
    title_placeholder: Head of Business Development
    stance: supportive
    confidence_in_stance: med
    last_touch_date: 2026-05-20
    last_touch_channel: in-person
    next_action: share two reference points from comparable sector (case-safe summaries only)
    next_action_due: 2026-05-29
    multi_thread_status: covered
    notes: |
      Useful internal amplifier for the champion.
      Wants to see proof, not promises.
    permission_to_quote: not-asked

  - slot: user
    name_placeholder: revenue-ops-analyst
    title_placeholder: Revenue Operations Analyst
    stance: neutral
    confidence_in_stance: low
    last_touch_date: 2026-05-12
    last_touch_channel: call
    next_action: share short demo recording of the proof events flow
    next_action_due: 2026-06-03
    multi_thread_status: exposed
    notes: |
      Will receive the daily outputs. Needs to feel the workflow is dignified.
    permission_to_quote: no

  - slot: procurement
    name_placeholder: procurement-lead
    title_placeholder: Procurement Lead
    stance: neutral
    confidence_in_stance: low
    last_touch_date: 2026-05-08
    last_touch_channel: email
    next_action: deliver standard SOW + payment terms aligned with docs/revenue/INVOICE_FLOW.md
    next_action_due: 2026-05-30
    multi_thread_status: exposed
    notes: |
      Likely to push for Net-30 or longer.
      Pre-route any deviation through docs/revenue/DEAL_DESK_SYSTEM.md.
    permission_to_quote: no

  - slot: security
    name_placeholder: ciso
    title_placeholder: CISO
    stance: opposed
    confidence_in_stance: med
    last_touch_date: 2026-05-18
    last_touch_channel: written-doc
    next_action: deliver trust pack section + governance runtime overview
    next_action_due: 2026-05-28
    multi_thread_status: exposed
    notes: |
      Aligned with IT Director's concerns; treat them as one thread.
      Reference docs/14_trust_os/TRUST_PACK.md.
    permission_to_quote: no
```

---

## القواعد التي لا تُكسر / Hard rules

### EN

- No PII (full name, phone, email, national ID) is stored in this doc. Use role tags. PII belongs in the gated CRM only.
- A stakeholder with `permission_to_quote: not-asked` is never quoted in marketing, sales decks, or trust pages.
- An account with 5+ slots marked `exposed` is escalated as a single-thread risk in the next weekly review.
- A `blocker` marked `opposed` with `confidence_in_stance: high` cannot be ignored — schedule a direct conversation or accept the deal will not close.
- A `champion` who suddenly goes silent for > 10 business days is treated as a thread loss; multi-thread coverage must absorb it.

### AR

- لا PII (اسم كامل، هاتف، بريد، هوية) في هذا المستند. استخدم وسوم الأدوار. PII في CRM المُقيَّد فقط.
- صاحب القرار مع `permission_to_quote: not-asked` لا يُقتبس أبدًا في التسويق أو عروض البيع أو صفحات الثقة.
- الحساب الذي به 5 خانات أو أكثر `exposed` يُصعَّد كمخاطرة مسار واحد في المراجعة الأسبوعية.
- `blocker` بحالة `opposed` وثقة `high` لا يُتجاهل — حدد محادثة مباشرة أو اقبل أن الصفقة لن تُغلق.
- `champion` يصمت فجأة لأكثر من 10 أيام عمل = خسارة مسار. على المسارات المتعددة استيعابها.

---

## ربط مع الأنظمة الأخرى / Ties

- إيقاع المسارات المتعددة وقواعد الاتصال: `docs/enterprise/MULTI_THREADING_SYSTEM.md`.
- نص الإحالة وقالب الرسائل: `docs/sales-kit/v5/dealix_multi_stakeholder_outreach.md`.
- الحوكمة والأمن في الأسئلة: `docs/governance/PDPL_DATA_RULES.md`، `docs/14_trust_os/TRUST_PACK.md`.
- المقترح: `docs/29_sales_os/PROPOSAL_OS.md`.
- الانحراف عن الشروط القياسية: `docs/revenue/DEAL_DESK_SYSTEM.md`.

---

## Disclosure / إفصاح

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
The filled example is a hypothetical, case-safe template. No real entity, role, or person is named.

## Related canonical docs

- `docs/enterprise/MULTI_THREADING_SYSTEM.md`
- `docs/sales-kit/v5/dealix_multi_stakeholder_outreach.md`
- `docs/29_sales_os/PROPOSAL_OS.md`
- `docs/governance/PDPL_DATA_RULES.md`
- `docs/14_trust_os/TRUST_PACK.md`
- `docs/revenue/DEAL_DESK_SYSTEM.md`
