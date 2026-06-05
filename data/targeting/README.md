# data/targeting — Market Intelligence working data / بيانات محرك الذكاء السوقي

`out/` يحتوي مخرجات تشغيل Market Intelligence OS (مرشحون، نتائج التقييم، قائمة المؤسس المختصرة).

## Funnel (volume ceiling, not a quota) / القمع (سقف وليس هدفًا)
```
400 research candidates → 80 scored targets → 20 founder shortlist → 10 drafts → 5 manual sends
```

## Rules / القواعد
- كل هدف يحتاج `evidence_source`. لا scraping خلف تسجيل دخول. احترام robots.txt وشروط المصدر.
- المخرجات **drafts** للمراجعة — لا إرسال تلقائي، لا واتساب جماعي.
- لا تُدخل بيانات شخصية بدون أساس مشروع وموافقة (راجع `docs/03_governance/DATA_RETENTION.md`).

راجع: `docs/01_go_to_market/MARKET_INTELLIGENCE_OS.md` · `docs/01_go_to_market/TARGETING_SCORECARD.md`
