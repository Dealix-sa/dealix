# Growth Experiments — Dealix Self-Growth OS

النمو لا يُبنى عشوائيًا. كل أسبوع ننفّذ حتى **10 تجارب صغيرة**، كل واحدة
بمقياس واحد وقاعدة قرار.

> القاعدة: **لا رأي بدون تجربة. لا تجربة بدون metric. لا metric بدون قرار.**

> المصدر الحي: [`data/growth/experiments.jsonl`](../../data/growth/experiments.jsonl).
> الـ backlog: `python3 scripts/growth/generate_experiment_backlog.py`
> → [`reports/growth/EXPERIMENT_BACKLOG.md`](../../reports/growth/EXPERIMENT_BACKLOG.md).

---

## بنية التجربة (حقول `experiments.jsonl`)

`id` · `hypothesis` · `channel` · `metric` · `status` · `effort` (S/M/L) ·
`loop` · `owner` · `created`.

---

## أمثلة من الـ backlog

| التجربة | المقياس |
|---|---|
| CTA pain-led مقابل product-led | conversion |
| Sample Command Pack قبل السعر | diagnostic bookings |
| صفحة قطاعية مقابل عامة | reply rate |
| Revenue Leakage Calculator مقابل Business OS Score | qualified leads |
| nurture 7 أيام مقابل متابعة واحدة | diagnostic bookings |
| build-log مقابل framework على LinkedIn | tool clicks |
| honest scarcity (3 sprints/شهر) | close rate |
| pricing 3-tier مع "Recommended" | average order value |

---

## الدورة الأسبوعية

1. اختر حتى 10 تجارب من الـ backlog.
2. لكل تجربة: حدّد المقياس الواحد وقاعدة القرار **قبل** البدء.
3. شغّلها أسبوعًا.
4. **رابح** → رقّيه إلى الـ loop المناسب (free-tools / conversion / content...).
5. **خاسر** → أرشفه مع التعلّم (لا تكرّره).

---

## القنوات المغطّاة

landing · seo · free-tools · email · linkedin · sales · partner ·
proof-to-content.

---

## الحوكمة

- لا تجربة تتضمن spam، cold WhatsApp، scraping، أو fake scarcity.
- "Honest scarcity" مسموح فقط إن كان حقيقيًا (سعة التسليم فعلًا محدودة).
- المقاييس تُقرأ من الأنظمة الفعلية — لا أرقام مُختلقة.
