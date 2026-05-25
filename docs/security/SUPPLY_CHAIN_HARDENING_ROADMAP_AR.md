# خارطة طريق تصلّب سلسلة التوريد

> النسخة الإنجليزية القانونية: [`SUPPLY_CHAIN_HARDENING_ROADMAP.md`](./SUPPLY_CHAIN_HARDENING_ROADMAP.md).

## مرجع الدوكترين
- الالتزامات: #3، #4، #5.
- القرارات المثبّتة: سكربتات التحقق مانعة للإصدار.

## الغرض

تصلّب Dealix ضد مخاطر سلسلة توريد البرمجيات على مراحل، باستخدام OpenSSF Scorecard كنقطة مرجعية خارجية، و SLSA-aligned build provenance كهدف، مع البناء على أدوات الأمان الحالية.

## السطح الأمني الحالي

- فحص الأسرار: `gitleaks`, `detect-secrets`, `trufflehog`.
- التحليل الستاتيكي: `bandit`.
- CORS, rate limits, تدوير المفاتيح: في `docs/security/`.
- التحقق من Moyasar webhook HMAC: `docs/BILLING_MOYASAR_RUNBOOK.md`.
- أنماط Docker بدون root.
- pre-commit hooks: `make pre-commit-install`, `make pre-commit-run`.
- فحوصات أمان: `make security`.

## المراحل

### المرحلة 1 — فحوصات وحالة CI أساسية

- Required status checks على الفروع المحمية.
- Dependency review على كل PR.
- فحص الأسرار مفروض.
- OpenSSF Scorecard على جدول، النتائج منشورة.

### المرحلة 2 — تصلّب البناء

- تثبيت GitHub Actions على commit SHA.
- توليد SBOM لكل إصدار.
- توقيع الـ artifacts.
- توليد provenance للإصدارات.

### المرحلة 3 — خط أنابيب متوافق مع SLSA

- خط أنابيب متوافق مع SLSA لأي artifact يصل الإنتاج.
- نشر OIDC (لا أوراق اعتماد سحابية طويلة العمر).
- least-privilege لـ GitHub tokens.
- موافقات بيئة لنشر الإنتاج.

## القواعد الجوهرية

- Required status checks غير قابلة للتفاوض على الفروع المحمية.
- pre-commit hooks ما تُتخطى (`--no-verify`) بدون موافقة مؤسس صريحة في الـ PR.
- فشل فحص الأسرار يمنع merge.
- إصدار بدون مسار رجوع موثّق ليس إصدارًا.
- تبعية طرف ثالث جديدة تحتاج مراجعة مسجّلة.

## الإيقاع

- لكل PR: dependency review + فحص أسرار + lint + security scan.
- أسبوعي: نتائج Scorecard.
- لكل إصدار: SBOM + provenance.
- ربع سنوي: مراجعة أرضية التبعيات.

## الربط بالتشغيل

- `make pre-commit-install`, `pre-commit-run`, `make security`.
- `.github/workflows/`.
- `docs/security/`, `SECURITY.md`.

## روابط ذات صلة

- `SECURITY.md`
- `docs/security/`
- `docs/BILLING_MOYASAR_RUNBOOK.md`
- `docs/transformation/01_doctrine_lock.md`
- [`../engineering/OBSERVABILITY_SLO_SYSTEM_AR.md`](../engineering/OBSERVABILITY_SLO_SYSTEM_AR.md)

## بنود مفتوحة

- OpenSSF Scorecard مذكور لكن ما هو مجدول بعد كـ workflow.
- توليد SBOM والـ provenance (المرحلة 2): خارطة طريق.
- خط الأنابيب SLSA (المرحلة 3): خارطة طريق، يعتمد على المرحلة 2.
- ملف سياسة dependency-review allowlist: غير مكتوب.
