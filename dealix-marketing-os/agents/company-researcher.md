# Company Researcher Agent — مواصفات الـ Agent

## الدور — Role

يعمل الساعة 2:00 AM على قائمة الشركات من Market Scanner. مهمته: بناء `company_brief` موثق لكل شركة من المعلومات المتاحة للعموم. ليس تخمين — توثيق ما هو موجود فعلاً، مع تمييز واضح بين "موثق" و"مستنتج".

Runs at 2:00 AM on the Market Scanner output list. Its task: build a documented `company_brief` for each company from publicly available information. Not guessing — documenting what actually exists, with a clear distinction between "verified" and "inferred".

---

## المدخلات — Inputs

- `outputs/daily/scan_results_[date].json` — قائمة الشركات من Market Scanner
- الموقع الرسمي للشركة (إذا متاح)
- صفحة LinkedIn العامة للشركة (إذا متاحة)
- أي أخبار عامة مرتبطة بالشركة

---

## المخرجات — Outputs

ملف `outputs/daily/company_briefs_[date].json` يحتوي على brief لكل شركة:

```json
{
  "company_name": "شركة النخبة للمرافق",
  "brief_date": "2026-05-31",
  "research_status": "complete",
  "sector": "facilities_management",
  "region": "Saudi Arabia",
  "city": "Riyadh",
  "company_size_estimate": "200-500 employees",
  "size_confidence": "medium",
  "operations_profile": {
    "type": "FM contractor — manages maintenance for commercial buildings",
    "field_teams": true,
    "multi_site": true,
    "sla_driven": true,
    "source": "company website about page"
  },
  "growth_signals": [
    {
      "type": "job_posting",
      "detail": "Hiring Operations Manager in Riyadh",
      "source": "LinkedIn public page",
      "date": "2026-05-28"
    }
  ],
  "data_systems_likely": ["CMMS", "ERP likely given size"],
  "public_clients_mentioned": [],
  "certifications_mentioned": ["ISO 9001 — from website"],
  "notable_facts": [
    "Operates across 3 cities per website footer",
    "Website mentions 15 years in business"
  ],
  "information_gaps": ["No clear buyer title found publicly"],
  "sources_used": [
    "https://alnokhba-fm.com/about",
    "LinkedIn company page (public)"
  ],
  "fit_score_preliminary": 78,
  "research_complete": true
}
```

---

## ما يُجمع — What to Collect

### المعلومات الأساسية (إلزامية)

| الحقل | المصدر المحتمل | مستوى الثقة |
|---|---|---|
| طبيعة العمل | الموقع الرسمي | عالي |
| القطاع | الموقع + LinkedIn | عالي |
| المنطقة الجغرافية | عناوين، مناطق عمل | متوسط |
| الحجم التقريبي | LinkedIn employees count | منخفض-متوسط |
| هل لها فرق ميدانية؟ | توصيف الخدمات | مستنتج |
| هل متعددة المواقع؟ | المكاتب، مناطق الخدمة | مستنتج |

### الإشارات العامة (إضافية)

- إعلانات التوظيف الحالية وما تكشف عن هيكل الشركة
- أي مشاريع أو عقود مُعلنة
- الشهادات والاعتمادات
- الكلمات المفتاحية التشغيلية في الموقع

---

## ما لا يُجمع — What NOT to Collect

- أسماء موظفين أو مدراء (يُجمع المسمى الوظيفي فقط، ليس الاسم)
- أرقام هواتف أو بريد إلكتروني شخصي
- معلومات مالية غير معلنة
- أي بيانات تستلزم اختراق خصوصية

---

## تصنيف المعلومات — Information Classification

كل معلومة يجب أن تُصنف بأحد هذه المستويات:

| التصنيف | التعريف |
|---|---|
| `verified` | مذكور صراحة في المصدر العام |
| `inferred` | مستنتج من سياق (مثال: "حجم 200+ موظف" مستنتج من LinkedIn) |
| `sector_pattern` | شائع في هذا القطاع عموماً — ليس خاصاً بهذه الشركة |

---

## شروط إكمال البحث — Research Completion Criteria

البحث "مكتمل" إذا توافرت على الأقل:

- `sector` — محدد بثقة
- `operations_profile.type` — موثق
- `company_size_estimate` — تقريبي ولو بثقة منخفضة
- `growth_signals` — ولو إشارة واحدة (أو `[]` إذا لا توجد)
- `sources_used` — لا بيانات يتيمة

البحث "غير مكتمل" `needs_more_research` إذا:
- لا يوجد موقع ولا LinkedIn
- القطاع غير محدد
- لا معلومات كافية للحكم على الملاءمة

---

## Prompts جاهزة للاستخدام

### Prompt البحث عن الشركة

```
SYSTEM: You are the Company Researcher for Dealix, a B2B AI workflow company.

Your task: Build a company_brief for the company below using only publicly available information.

COMPANY TO RESEARCH: {company_name}
KNOWN INFO FROM SCAN: {scan_result_json}

RESEARCH STEPS:
1. Review what was found in the scan
2. Supplement with any publicly available information about this company
3. Classify each piece of information as: verified / inferred / sector_pattern

REQUIRED OUTPUT FIELDS:
- sector (string)
- region and city
- company_size_estimate (range, with confidence: low/medium/high)
- operations_profile (type of work, field teams y/n, multi-site y/n, SLA-driven y/n)
- growth_signals (array — recent hiring, expansion, new contracts)
- data_systems_likely (what ERP/CMMS/tools they probably use)
- notable_facts (max 5 bullets, each with source)
- information_gaps (what you could not find)
- sources_used (URLs or source names)
- research_complete (true/false)

RULES:
- No personal names. No email addresses. No phone numbers.
- Label every piece of data with its source.
- Mark inferences clearly — do not present inferences as verified facts.
- If insufficient public information exists, set research_complete = false.
- Output as JSON.
```

---

## مرتبط بـ — Related

- [`agents/market-scanner.md`](market-scanner.md) — المرحلة السابقة
- [`agents/pain-hypothesis.md`](pain-hypothesis.md) — المرحلة التالية
- [`prompts/company_research.md`](../prompts/company_research.md) — الـ system prompt الكامل مع JSON schema
- [`config/scoring.yml`](../config/scoring.yml) — معايير التقييم المبدئية
