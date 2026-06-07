# بوابة دمج PR

قبل دمج أي PR متعلق بـ Dealix launch:

1. لا secrets داخل الملفات.
2. كل workflow يحتوي permissions محددة.
3. migrations مرتبة وغير مكسورة.
4. readiness checks تمر.
5. صفحات الموقع لا تحتوي وعود دخل مضمونة.
6. outbound messaging drafts فقط.
7. أي route يكتب بيانات يجب أن يملك tenant/session guard في V10+.
8. لا service role في frontend.
9. لا self-serve launch flag قبل approval.
10. يوجد rollback plan.

قرار الدمج: merge فقط إذا كان Controlled Preview scope واضحًا.
