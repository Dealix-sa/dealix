# Post Deployment Smoke Test

## Smoke 10 دقائق
1. افتح الصفحة الرئيسية.
2. افتح services/pricing/custom-ai/contact/diagnostic.
3. أرسل lead وهمي.
4. تأكد من دخول lead في ledger أو webhook.
5. شغّل pipeline report.
6. شغّل security smoke.
7. راجع logs.

## فشل شائع
- env ناقص.
- API route لا يكتب بسبب permissions.
- NEXT_PUBLIC_SITE_URL خطأ.
- CORS إذا كان backend منفصل.
