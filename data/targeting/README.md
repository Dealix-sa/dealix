# data/targeting — بيانات Targeting OS

ملفات الإعداد التي تُغذّي [`scripts/research_targeting_os.py`](../../scripts/research_targeting_os.py)
وأخواته. كلها YAML/CSV/JSONL قابلة للقراءة والمراجعة.

| الملف | الدور |
|---|---|
| `sectors.yml` | قطاعات الاستهداف (id, phase, priority, default_offer, keywords) |
| `cities.yml` | المدن حسب المرحلة |
| `signals.yml` | مكتبة إشارات الألم + الـ angles + العروض |
| `scoring_weights.yml` | أوزان السكور (100) + الخصومات + الدرجات + العتبات |
| `blocked_sources.yml` | المصادر/الأنواع الممنوعة + القطاعات الحساسة |
| `queries.txt` | queries منسّقة عالية الـ intent (research فقط) |
| `company_seed_template.csv` | قالب إدخال المؤسس (≥2 مصدر دليل لكل صف) |
| `company_master.jsonl` | عيّنة سجل شركة كامل المخطط |
| `out/` | مخرجات يومية (gitignored) — لا تُلتزم |

## ملاحظات حوكمة

- لا تُدخل بيانات خلف login أو مشتراة أو مسربة في أي ملف هنا.
- كل صف يحتاج **دليلين مستقلين على الأقل** ليتأهل لمسودة.
- المخرجات تحت `out/` لا تُلتزم في git (تُولّد يوميًا).
