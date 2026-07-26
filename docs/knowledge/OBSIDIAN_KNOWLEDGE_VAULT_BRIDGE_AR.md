# جسر Dealix إلى Obsidian — Second Brain آمن ومثبت بالمصادر

## القرار التنفيذي

نستفيد من فكرة `claude-obsidian` كواجهة معرفة محلية قابلة للبحث والربط، لكن **لا ننسخ Runtime المشروع الخارجي داخل Production Dealix**.

السبب:

- Dealix لديه أصلًا Knowledge Graph وKnowledge Base وKnowledgeAccumulator وProof/Approval layers.
- المشروع الخارجي مصمم افتراضيًا لـ **مستخدم واحد + Vault واحد + جهاز واحد**.
- إعداد المشروع الخارجي يتضمن تنزيل Plugin من الإنترنت، Community Plugins، وAuto-commit hook لمسارات المعرفة.
- هذه الافتراضات مناسبة لدفتر معرفة شخصي، وليست مناسبة مباشرة لمنصة متعددة العملاء أو CI مشترك أو بيانات شركات حساسة.

لذلك نستخدمه كـ **Sidecar / Projection**:

```text
Dealix canonical sources
  ├─ repository Markdown
  ├─ KnowledgeAccumulator snapshot
  ├─ proof metadata
  └─ source paths
          ↓
Local deterministic exporter
          ↓
Obsidian-compatible vault
  ├─ HOME.md
  ├─ wiki/sources/repo/
  ├─ wiki/sources/knowledge/
  ├─ wiki/entities/
  ├─ wiki/concepts/
  ├─ manifest.json
  └─ proof-log.json
          ↓
Obsidian / Claude Code / local agent
```

الـVault الناتج ليس قاعدة البيانات الرسمية، وليس بديلًا لـPostgreSQL، ولا يرسل شيئًا، ولا يغيّر Production.

## القيمة المباشرة للمشروع

### 1. ذاكرة مؤسسية قابلة للتصفح

كل وثائق Dealix المهمة تُعرض داخل Vault واحد مع روابط وفهارس، بدل الاعتماد على البحث اليدوي داخل آلاف الملفات.

### 2. إجابات Claude Code من مصادر Dealix الفعلية

الـVault يولد `CLAUDE.md` يفرض:

- البدء من `HOME.md`.
- الاستناد إلى الملفات الأصلية المنسوخة.
- ذكر `dealix_source_path` لكل ادعاء مهم.
- الفصل بين الحقيقة والاستنتاج والتوصية.
- منع اختراع عملاء أو إيراد أو Proof أو حالة Production.

### 3. تحويل KnowledgeAccumulator إلى Graph مفهوم

عند وجود `data/knowledge/accumulated_intel.json`، كل Entry تتحول إلى صفحة تحتوي:

- المصدر.
- الفئة.
- الشركة.
- القطاع.
- الوسوم.
- درجة الثقة.
- تاريخ الإنشاء والانتهاء.

ثم يُنشأ تلقائيًا:

- صفحة لكل شركة في `wiki/entities/`.
- صفحة لكل قطاع في `wiki/concepts/`.
- روابط للمعرفة المرتبطة.

### 4. Proof by construction

كل Export ينتج:

- `manifest.json`: ما الذي دخل إلى الـVault.
- `proof-log.json`: SHA-256 لكل ملف، وعدد Network Calls وExternal Actions وكلاهما صفر.
- `wiki/meta/Export Manifest.md`: فهرس بشري.
- `wiki/meta/Proof Index.md`: Knowledge entries مع المصدر والثقة.

### 5. أصل قابل لإعادة الاستخدام مع العملاء

لاحقًا يمكن إنشاء Vault منفصل لكل Tenant أو Pilot، لكن فقط بعد إضافة:

- Tenant isolation.
- Data classification.
- PDPL retention rules.
- Redaction before export.
- Encryption at rest.
- Explicit client approval.

لا يجوز خلط معرفة عميلين في Vault واحد.

## التنفيذ الحالي

### الحزمة

```text
dealix/knowledge_vault/
  __init__.py
  exporter.py

scripts/knowledge/
  export_dealix_knowledge_vault.py

tests/
  test_knowledge_vault_exporter.py

.github/workflows/
  knowledge-vault-export.yml
```

### أمر التشغيل

من جذر الريبو:

```bash
python scripts/knowledge/export_dealix_knowledge_vault.py --clean
```

المخرج الافتراضي:

```text
artifacts/dealix-knowledge-vault/
```

افتح هذا المجلد في Obsidian كـVault، أو افتح Claude Code من داخله.

### تخصيص المصادر

```bash
python scripts/knowledge/export_dealix_knowledge_vault.py \
  --source-root README.md \
  --source-root docs/knowledge \
  --source-root docs/commercial \
  --knowledge-json data/knowledge/accumulated_intel.json \
  --output artifacts/dealix-knowledge-vault \
  --clean
```

## مصادر التصدير الافتراضية

- `README.md`
- `AGENTS.md`
- `docs/knowledge/`
- `docs/knowledge_base/`
- `docs/company/`
- `docs/playbooks/`
- `docs/commercial/`
- `docs/ops/`
- `docs/agents/`
- `reports/final/`
- `data/knowledge/accumulated_intel.json` عند وجوده

التصدير يقرأ ملفات Markdown فقط، ويستبعد تلقائيًا مجلدات مثل:

- `.git`
- `.venv`
- `node_modules`
- `secrets`
- `private`

كما يرفض الملفات الأكبر من 2MB افتراضيًا.

## لماذا لم نستخدم `bash bin/setup-vault.sh` مباشرة؟

الـSetup الخارجي ينفذ أشياء لا نحتاجها في Dealix Core:

- ينشئ بنية Vault شخصية.
- ينزل Excalidraw `main.js` عبر `curl`.
- يوصي بتثبيت Community Plugins.
- يفترض تشغيلًا محليًا أحادي المستخدم.

وفي سياسة الأمان للمشروع الخارجي توجد ملاحظات مهمة:

- Lock release يعتمد على filesystem trust.
- Auto-commit hook يضيف تلقائيًا مسارات `wiki/` و`.raw/` و`.vault-meta/`.
- النموذج الأمني يفترض جهازًا ومستخدمًا واحدًا.

لذلك أخذنا الفكرة النافعة فقط: Plain Markdown + Wiki links + Graph + Source ownership، وأبقينا Dealix هو مصدر الحقيقة.

## قواعد الحوكمة

### مسموح تلقائيًا

- قراءة ملفات Markdown المعتمدة.
- إنشاء Vault محلي أو CI artifact.
- إنشاء الفهارس والروابط.
- توليد Manifest وProof Log.
- حذف مجلد Output المحدد فقط عند `--clean`.

### يحتاج موافقة منفصلة

- إدخال بيانات عميل حقيقية.
- رفع Vault إلى خدمة خارجية.
- مشاركة Vault مع طرف ثالث.
- تشغيل مزامنة سحابية.
- ربط Gmail/CRM/Drive بمحتوى عميل.
- نشر أي Knowledge page للعامة.

### ممنوع

- نسخ `.env` أو Secrets.
- تصدير Credentials أو Tokens.
- خلط بيانات Tenants.
- اعتبار Knowledge entry حقيقة دون مراعاة `source` و`confidence`.
- استخدام Auto-commit إلى `main`.
- جعل Obsidian قاعدة الإنتاج.

## مسار التطوير التالي

### P0 — تم في هذه الحزمة

- Exporter محلي deterministic.
- مصدر موثق لكل صفحة.
- Company/Sector maps.
- Manifest + SHA-256 Proof Log.
- Focused tests.
- GitHub artifact أسبوعي ويدوي.

### P1 — بعد اعتماد Knowledge storage

- Adapter يقرأ من Knowledge OS API بصلاحية Admin داخل بيئة آمنة.
- Snapshot export من PostgreSQL بدون بيانات حساسة.
- Redaction policy قابلة للتكوين.
- Incremental export based on content hashes.

### P2 — Client Pilot

- Vault منفصل لعميل واحد.
- Company Brain + meeting notes + approved proposals + Proof Pack.
- Retention policy وDelete/Export request.
- قياس زمن الوصول للمعلومة وجودة الاستشهاد.

### P3 — Product capability

- واجهة داخل Dealix تعرض Knowledge Graph نفسه بدون اشتراط Obsidian.
- Obsidian يبقى Export/Operator interface، وليس dependency للعميل.

## معايير النجاح

الحزمة ناجحة عندما:

1. الاختبارات المركزة تنجح.
2. الـWorkflow ينتج Artifact.
3. `manifest.json` يحتوي مصادر فعلية.
4. `proof-log.json` يثبت `network_calls=0` و`external_actions=0`.
5. فتح `HOME.md` يقود إلى المصادر والشركات والقطاعات.
6. أي إجابة من Claude يمكن ربطها بملف أو Knowledge source واضح.

## مرجع الفكرة الخارجية

- Repository: `https://github.com/AgriciDaniel/claude-obsidian`
- License: MIT
- لم يتم نسخ Runtime المشروع أو Plugins؛ استُخدمت الفكرة المعمارية فقط مع تنفيذ مستقل متوافق مع Dealix.
