# Robots & Terms Policy — احترام robots.txt وشروط المواقع

> طبقة: Governance OS · يطبّقها: أي Discovery/Fetch provider في Targeting OS

## الدور

يضمن أن منظومة البحث في Dealix تحترم **معيار استبعاد الزواحف**
(Robots Exclusion Protocol — موثّق رسميًا في **RFC 9309**) وشروط استخدام كل
موقع. القاعدة المرفوضة صراحةً: «طالما الصفحة مفتوحة نكشطها».

## القواعد الملزمة لأي provider

1. **اقرأ `robots.txt` أولًا** واحترم `Disallow`/`Allow` و`Crawl-delay` لكل مضيف قبل أي جلب.
2. **لا تتجاوز login** ولا تتعامل مع محتوى خلف جدار اشتراك أو CAPTCHA.
3. **استخدم الصفحات العامة فقط** المخصصة للعرض العام (خدمات، عملاء، أخبار، وظائف، تواصل).
4. **عرّف نفسك** بـ User-Agent واضح وصادق عند الجلب؛ لا انتحال.
5. **حدّ المعدل** (rate-limit) واحترم زمن الانتظار؛ لا ضغط على المضيف.
6. **احترم الشروط** (Terms of Service) لأي API — وإن منع الاستخدام الآلي، نتوقف.
7. **Provider قابل للاستبدال** — لا اعتماد دائم على مزود واحد.

## ما الذي يفرضه الكود

- `targeting_compliance_gate.py` يرفض دومينات وأنماط روابط خلف login
  (`/login`, `/auth`, `/dashboard`, …) عبر [`blocked_sources.yml`](../../data/targeting/blocked_sources.yml).
- `research_targeting_os.py` يبقي **الاكتشاف معطّلًا افتراضيًا**؛ لا جلب شبكي إلا
  بـ `--allow-network` مع provider مُعتمد يحترم هذه السياسة — وهو قرار مؤسس صريح.

## روابط

- [Research Source Policy](RESEARCH_SOURCE_POLICY.md)
- RFC 9309 — Robots Exclusion Protocol (مرجع معياري)
