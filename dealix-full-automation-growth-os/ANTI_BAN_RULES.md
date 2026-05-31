# Dealix Anti-Ban Rules

هذه القواعد غير قابلة للتجاوز. أي agent يخالفها يُوقف فوراً.

## Email Health Thresholds

| المقياس | حد التحذير | الإجراء |
|---------|-----------|---------|
| Bounce rate | > 3% | تقليل الإرسال 50% |
| Unsubscribe rate | > 2% | إيقاف الـ segment + مراجعة النص |
| Spam complaint | أي شكوى | إيقاف الـ inbox فوراً |

## Platform-Specific Rules

### LinkedIn
- أول warning — إيقاف كل النشاط فوراً
- لا auto-connect، لا auto-DM، لا scraping

### WhatsApp
- انخفاض quality rating — إيقاف templates فوراً
- لا إرسال بدون opt-in
- معالجة STOP keywords خلال ثانية

### X/Twitter
- Official API only
- No duplicate posts
- No bulk unsolicited DMs

## Similarity Guard

لا ترسل رسائل متشابهة في نفس الدفعة.

Variables الإلزامية للتمييز:
- company_name
- sector
- pain_point
- offer
- buyer_title
- country
- language
- cta_variant

إذا similarity score > 0.7 — أعد التوليد بزاوية مختلفة.

## Account Warmup

كل inbox جديد يمر بـ 14 يوم warmup:
- الأيام 1-7: 10 رسائل/يوم
- الأيام 8-14: +10/يوم
- ما بعد الـ warmup: controlled auto-send فقط

## Watchdog

Anti-Ban Guardian يشتغل كل 15 دقيقة.
يراقب: bounce، unsubscribe، spam، API errors، platform warnings.
ينبّه المؤسس فوراً عند أي مشكلة.
