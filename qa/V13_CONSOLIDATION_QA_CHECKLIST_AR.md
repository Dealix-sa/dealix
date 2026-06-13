# V13 QA Checklist

## قبل الدمج

- [ ] Makefile موجود ويعمل.
- [ ] master readiness يعمل.
- [ ] launch decision يعطي Controlled Preview GO.
- [ ] migration order واضح.
- [ ] workflow inventory لا يظهر صلاحيات خطرة.
- [ ] env example لا يحتوي أسرار حقيقية.
- [ ] V11 first revenue sprint موجود.
- [ ] V12 scale plan موجود.

## بعد الدمج

- [ ] افتح PR منفصل.
- [ ] راجع الملفات المتكررة.
- [ ] شغل CI.
- [ ] شغل security smoke.
- [ ] لا تطلق self-serve قبل إغلاق أول managed clients.
