# خطة الدمج الرئيسية — Dealix V13

## الهدف

تجميع V1 إلى V12 في طبقة واحدة مفهومة وقابلة للتشغيل، بدون أن يضيع الفريق بين عشرات السكربتات والمجلدات.

## قواعد الدمج

1. لا تدمج كل شيء عشوائيًا بدون فرع مستقل.
2. لا ترفع أسرار أو مفاتيح حقيقية.
3. لا تشغل outbound تلقائي.
4. كل workflow يبقى read-only إلا لو كان job نشر مقيدًا ببيئة production وموافقة بشرية.
5. كل migration له ترتيب واضح.
6. كل claim تسويقي يحتاج proof item.
7. كل عميل له client room أو CRM record.
8. كل أسبوع له operating review.

## ترتيب الدمج

1. انسخ الحزمة إلى الريبو.
2. شغل فحص V13 master readiness.
3. شغل فحص env contract.
4. شغل migration plan.
5. شغل security smoke.
6. شغل launch decision.
7. افتح PR واحد باسم consolidation.
8. راجع الملفات الكبيرة والتكرارات.
9. ادمج بعد نجاح CI.

## نتيجة الدمج المتوقعة

Dealix يصبح عنده: موقع، عروض، CRM، acquisition، revenue sprint، delivery، trust center، agents، SaaS model، production bridge، scale cadence، وmaster command surface.
