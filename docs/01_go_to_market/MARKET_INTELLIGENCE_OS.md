# Market Intelligence OS — عدسة النمو — The Growth Lens

## دور هذه الوثيقة

هذه هي **العدسة التسويقية (GTM lens)** لمحرّك ذكاء السوق: كيف يخدم النمو والبحث ودورة المبيعات. النسخة الأعمق على مستوى الأنظمة موجودة في [../02_operating_systems/](../02_operating_systems/) — هنا نصفه كأداة نمو، لا كهندسة.

> Market Intelligence ليست أداة تنقيب جماعي. هي مُولِّد فرص مُثبتة بأدلة، مُخرَجه مسودّات تنتظر موافقة المؤسس.

## ماذا يفعل — What It Does

1. **يبحث** عن شركات ضمن قطاع/معيار مُحدَّد.
2. **يُصفّي** حسب ملاءمة الـ ICP.
3. **يُسجّل الدليل** — كل مرشّح يُرفق بـ `evidence_source` (مصدر علني مسموح).
4. **يُقيّم** عبر [TARGETING_SCORECARD.md](TARGETING_SCORECARD.md).
5. **يحدّد نقطة الضعف التشغيلية** (pain signal) من دليل مرئي.
6. **يقترح زاوية استهداف** (angle) مبنية على الألم لا على الافتراض.
7. **يبني مسودّات (DRAFTS)** للمراجعة البشرية — **لا يرسل شيئًا**.

## قاعدة القُمع — The Funnel Rule

| المرحلة | العدد | البوّابة |
|---|---|---|
| Research candidates | 400 | مصدر دليل علني لكل مرشّح |
| Scored targets | 80 | اجتاز التقييم الأساسي |
| Founder shortlist | 20 | اختيار يدوي من المؤسس |
| Drafts | 10 | لكل مسودّة `evidence_source` |
| Manual sends | 5 | موافقة المؤسس + إرسال يدوي |

القُمع يضيق عمدًا: من 400 بحث إلى 5 إرسالات يدوية. الجودة فوق الحجم. الـ 5 إرسالات يدوية بالكامل — لا أتمتة إرسال.

## القواعد الصلبة — Hard Rules (مفروضة في كل دورة)

- **كل هدف يحتاج `evidence_source`** قبل أي مسودّة. لا دليل = لا هدف.
- **لا scraping خلف تسجيل دخول.** نحترم شروط المصدر و `robots.txt`.
- **المُخرَج مسودّات للموافقة**، لا يُرسَل تلقائيًا أبدًا.
- **لا واتساب جماعي، لا outreach بالجملة.**
- **لا استخدام لأي بيانات في تدريب نموذج.**

راجع: [../05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md) و [../02_saudi_positioning/WHATSAPP_BOUNDARY.md](../02_saudi_positioning/WHATSAPP_BOUNDARY.md).

## حلقة الرادار — The Market Radar Loop

```
market signals  →  pattern detection  →  product roadmap input
       ↑__________________________________________|
```

إشارات السوق المتكرّرة (ألم مشترك بين مرشّحين) تتحوّل إلى مُدخَل لخارطة المنتج: ما يطلبه السوق أكثر من مرّة يصبح ميزة، ثم منتجًا.

## حلقة التشخيص-إلى-البيانات — Diagnostic-to-Data Loop

```
diagnostic pain data  →  sharper ICP  →  better targeting  →  higher score quality
       ↑__________________________________________________________|
```

كل تشخيص يكشف ألمًا حقيقيًا. هذا الألم يُغذّي تعريف الـ ICP، فيرتفع جودة التقييم في الدورة التالية. المحرّك يتعلّم من الواقع، لا من الافتراض.

## ما يُسلّمه هذا المحرّك للـ GTM

- **Company Intelligence Brief** داخل الـ [COMMAND_SPRINT_OFFER.md](COMMAND_SPRINT_OFFER.md).
- **shortlist يومية** للمؤسس ضمن الـ [SALES_PLAYBOOK.md](SALES_PLAYBOOK.md).
- **مسودّات موثّقة بالدليل** فقط — لا إرسال، لا وعود.

## روابط مرجعية — Cross-links

- [TARGETING_SCORECARD.md](TARGETING_SCORECARD.md)
- [SALES_PLAYBOOK.md](SALES_PLAYBOOK.md)
- [COMMAND_SPRINT_OFFER.md](COMMAND_SPRINT_OFFER.md)
- [../02_operating_systems/](../02_operating_systems/) — النسخة الأعمق على مستوى الأنظمة (cross-link to verify)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
