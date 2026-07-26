# جسر Dealix إلى Obsidian — Second Brain آمن ومثبت بالمصادر

## القرار التنفيذي

نستفيد من فكرة `claude-obsidian` كواجهة معرفة محلية قابلة للبحث والربط، لكن **لا ننسخ Runtime المشروع الخارجي داخل Production Dealix**.

Dealix يملك أصلًا Knowledge Graph وKnowledge Base وKnowledgeAccumulator وProof/Approval layers، بينما المشروع الخارجي يفترض مستخدمًا واحدًا وVault واحدًا وجهازًا واحدًا، وقد يتضمن تنزيل Plugins وAuto-commit. لذلك نعتمد الفكرة المعمارية فقط:

```text
Dealix canonical repository Markdown
        ↓
Local deterministic exporter
        ↓
Obsidian-compatible read-only projection
        ↓
Obsidian / Claude Code / local operator
```

يمكن إدخال KnowledgeAccumulator JSON **محليًا وبشكل صريح فقط** بعد مراجعة التصنيف والخصوصية. لا يقرأه الأمر الافتراضي ولا الـWorkflow الأسبوعي.

الـVault الناتج ليس قاعدة البيانات الرسمية، وليس بديلًا لـPostgreSQL، ولا يرسل شيئًا، ولا يغيّر Production.

## القيمة المباشرة

- ذاكرة مؤسسية قابلة للتصفح عبر Markdown وWiki links.
- `CLAUDE.md` يفرض الاستشهاد بالمصدر والفصل بين الحقيقة والاستنتاج والتوصية.
- `manifest.json` يسجل ما دخل إلى الـVault.
- `proof-log.json` يسجل SHA-256 لكل ملف ويثبت `network_calls=0` و`external_actions=0`.
- يمكن تشغيله محليًا دون Network أو Plugins أو Auto-commit.

## الحزمة

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

## التشغيل الافتراضي الآمن

من جذر الريبو:

```bash
python scripts/knowledge/export_dealix_knowledge_vault.py --clean
```

المخرج الافتراضي:

```text
artifacts/dealix-knowledge-vault/
```

هذا الأمر يصدّر مصادر Markdown المعتمدة فقط. لا يقرأ `data/knowledge/accumulated_intel.json` تلقائيًا.

## إدخال Knowledge JSON محليًا — Opt-in

بعد التأكد أن الملف:

- داخل ريبو Dealix؛
- ليس داخل `private/` أو `secrets/`؛
- لا يحتوي أسرارًا أو بيانات عميل غير مصرح بها؛
- لا يتجاوز الحد المسموح؛
- حصل على المراجعة البشرية المطلوبة؛

يمكن تشغيل:

```bash
python scripts/knowledge/export_dealix_knowledge_vault.py \
  --knowledge-json data/knowledge/accumulated_intel.json \
  --output artifacts/dealix-knowledge-vault \
  --clean
```

عند عدم تمرير `--knowledge-json` تكون القيم التالية مثبتة في الـManifest والـProof Log:

```text
knowledge_json = null
knowledge_json_opt_in = false
knowledge_entries = 0
```

## مصادر Markdown الافتراضية

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

يستبعد التصدير تلقائيًا المسارات التي تحتوي أجزاء مثل:

- `.git`
- `.venv`
- `venv`
- `node_modules`
- `__pycache__`
- `secrets`
- `private`

ويقبل ملفات Markdown حتى 2MB، وKnowledge JSON اختياريًا حتى 5MB.

## عقد `--clean`

لا ينفذ exporter حذفًا عامًا. عند أول إنشاء يضع marker:

```text
.dealix-knowledge-vault.json
```

وعند `--clean`:

1. يرفض Repository root وHome وfilesystem root.
2. يرفض symlink output.
3. يرفض أي مجلد موجود لا يحمل marker ملكية صحيحًا.
4. يرفض output داخل أي source root لمنع self-export والحذف المتداخل.
5. يحذف ويعيد إنشاء Vault مولّدًا ومملوكًا للأداة فقط.

## عقد CI والـArtifact

الـWorkflow الأسبوعي واليدوي:

- يثبت الاختبارات المركزة؛
- يصدّر Markdown العام الموجود أصلًا في الريبو العام؛
- **لا يمرر `--knowledge-json`**؛
- يتحقق أن Knowledge entries تساوي صفرًا؛
- يتحقق من marker والـManifest والـProof Log؛
- يرفع artifact لمدة محدودة للمراجعة.

لا يجوز تحويل الـWorkflow إلى تصدير بيانات عميل أو Snapshot داخلي دون Data classification وRedaction وTenant isolation وموافقة صريحة.

## حدود السلامة

### مسموح تلقائيًا

- قراءة Markdown المعتمد داخل الريبو.
- إنشاء Vault محلي أو artifact يحتوي مصادر الريبو العامة فقط.
- إنشاء الفهارس والروابط والـManifest والـProof Log.
- تنظيف output مولّد ومملوك للأداة فقط.

### يحتاج موافقة منفصلة

- إدخال Knowledge JSON يحوي بيانات عميل حقيقية.
- رفع Vault إلى خدمة خارجية أو مشاركته مع طرف ثالث.
- تشغيل Cloud Sync.
- ربط Gmail أو CRM أو Drive بمحتوى عميل.
- نشر أي Knowledge page للعامة خارج محتوى الريبو العام.

### ممنوع

- نسخ `.env` أو Secrets أو Tokens.
- قراءة Knowledge JSON خارج الريبو أو من `private/` و`secrets/`.
- خلط بيانات Tenants.
- اعتبار Knowledge entry حقيقة دون المصدر والثقة.
- Auto-commit إلى `main`.
- جعل Obsidian قاعدة الإنتاج.
- حذف مجلد غير مملوك للـexporter.

## اختبارات السلامة

الاختبارات تثبت:

1. بناء Vault مستشهد بالمصادر.
2. عدم إدخال Knowledge JSON افتراضيًا.
3. رفض تنظيف Repository root.
4. رفض تنظيف مجلد موجود غير مملوك.
5. تنظيف Vault مملوك فقط.
6. رفض Knowledge JSON خارج الريبو.
7. رفض output داخل source root.
8. الفشل المغلق عند تصادم identifiers بعد normalization.

## التطوير التالي

بعد اعتماد Knowledge storage وخصوصية الـPilot يمكن إضافة:

- Redaction policy قابلة للتكوين.
- Adapter آمن إلى Knowledge OS API.
- Snapshot من PostgreSQL بعد تصنيف البيانات.
- Incremental export based on content hashes.
- Vault منفصل لكل Tenant مع retention وdelete/export requests.

## مرجع الفكرة الخارجية

- Repository: `AgriciDaniel/claude-obsidian`
- License: MIT
- لم يتم نسخ Runtime أو Plugins أو hooks؛ استُخدمت الفكرة المعمارية فقط مع تنفيذ مستقل متوافق مع Dealix.
