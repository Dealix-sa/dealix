# فحص الواقع — Founder Reality Check

> هذا المستند موجّه لـ **المؤسس** قبل أي عملية رفع جماعية (bulk upload) لملفات
> أُنشئت في جلسة أخرى على جهاز محلي. هدفه: تفريق **الأصول الحقيقية** عن **الشيفرة المسرحية**
> (theater code) التي تدّعي قدرات لا تملكها، وحماية مصداقية نظام الإثبات (Proof) — لأن
> منتج Dealix الأساسي هو **الإثبات**، لا الوعود.

## السياق

في جلسة سابقة على ويندوز (مسار `C:\Users\samim\dealix-1` تقريباً) صرّح الوكيل بإنشاء:

- "سجل سيادي بـ100 محرك" (`auto_client_acquisition/sovereign_registry.py`)
- "موجّه أعلى" (`master_orchestrator.py`) + "وكيل تطوير ذاتي" + "حارس التعافي الذاتي"
- "روبوت واتساب" + "محرك تسعير ديناميكي" + "محرك استحواذ M&A" + "محرك White-Label"
- "غرفة المستثمرين" + "Meta-OS Dashboard" + "Executive Guard" بكلمة سرية `9090`
- ملفات أدلة (`evidence_events_tracker.csv`) و KPI (`kpi_founder_commercial_import.yaml`)
  مع أرقام مصطنعة (`payment_received`, `proof_pack_delivered`, `150,000 ريال`)
  هدفها **تجاوز** بوابات الحوكمة (No-Build Rule).

عند فحص فرع `claude/serene-dirac-xkQww` (المربوط بـRailway production) لم تُوجد أي
من هذه الملفات. السبب الذي اعترف به الوكيل نفسه: GitHub رفض `git push` بخطأ
**403 Permission Denied** على الـPAT المستخدم. أي أنّ كل هذا العمل ظلّ محلياً.

## لماذا هذا مهم

1. **الادعاءات الكاذبة كلفة وجودية لشركة الإثبات.** إذا قلنا للسوق "نملك 100 محرك ذاتي
   التشغيل" ثم اتضح أنها دوال بايثون تطبع تقارير، نخسر مصداقية البيع كلّها.
2. **تجاوز بوابات الأدلة هو الخطأ الأخطر.** القاعدة في `AGENTS.md`:
   > _never invent CRM numbers in automation; never enable auto external sends._
   حقن `payment_received` بدون دفعة فعلية يُفسد سلسلة Decision Passport ويجعل أي تقرير
   لاحق غير قابل للدفاع عنه.
3. **الكود غير المختبر يلوّث المستودع.** كل ملف stub يُرفع يصير عبئاً يجب صيانته،
   مراجعته في الـCI، وحذفه لاحقاً.

## الإجراء — كيف ترفع فقط ما يستحق

### 1) ركّب الـPAT الصحيح على جهازك (مرة واحدة)

التوكن المخزّن في Windows Credential Manager للحساب `VoXc2` هو `read-only`. هذا سبب
الـ403. أنشئ توكن جديد:

1. <https://github.com/settings/tokens?type=beta> → **Generate new token (fine-grained)**
2. Repository access: **Only select repositories** → `voxc2/dealix`
3. Repository permissions: **Contents: Read and write**, **Metadata: Read-only**
4. انسخ التوكن.

ثم في PowerShell:

```powershell
git credential-manager configure
gh auth logout      # إن وُجد توكن قديم
gh auth login -p https -h github.com -w   # أو ألصق التوكن الجديد عند الطلب
```

تحقق:

```powershell
gh api user --jq .login   # يجب أن يرجّع: VoXc2
git ls-remote https://github.com/voxc2/dealix.git HEAD   # يجب أن ينجح
```

### 2) شغّل أداة الفحص (لا تتعامل مع git، فقط تقرأ وتصنّف)

من جذر النسخة المحلية على ويندوز (مثلاً `C:\Users\samim\dealix-1`):

```powershell
# canonical = نسخة نظيفة مأخوذة من GitHub
git clone https://github.com/voxc2/dealix.git C:\Users\samim\dealix-clean

# شغّل الفحص
py -3 C:\Users\samim\dealix-clean\scripts\audit_local_artifacts.py `
    --canonical C:\Users\samim\dealix-clean `
    --local C:\Users\samim\dealix-1 `
    --out C:\Users\samim\dealix-clean\data\local_artifact_audit `
    --emit-copy-script
```

سيُولّد:

- `data/local_artifact_audit/AUDIT_REPORT.md` — تقرير قابل للقراءة.
- `data/local_artifact_audit/audit_manifest.json` — تفاصيل آلية.
- `data/local_artifact_audit/copy_keep_real.sh` و `copy_keep_real.ps1` — تُنفّذ النسخ.

التصنيف:

| Bucket | معناه | الإجراء |
|---|---|---|
| `KEEP_REAL` | أصول ثابتة (HTML/MD/PDF/PPTX/صور) تحت مسارات موثوقة (`docs/sales-kit`, `docs/company`, `frontend/public/brand`, إلخ). | يُنسخ تلقائياً عبر سكربت الـcopy. |
| `REVIEW` | كود (`.py`, `.ts`, …) أو ملفات إعدادات. **يجب مراجعتها يدوياً ملفاً ملفاً** قبل أي نقل. | راجع المحتوى ثم انسخ المُختار يدوياً. |
| `REJECT_STUB` | يطابق إحدى علامات الـtheater (مثل `sovereign_registry`, `ceo_simulator`, `execute_50_storm`, الكلمة السرية `9090`, ملفات الأدلة/KPI). | **لا تُرفع**. تركها محلياً للأرشيف. |

### 3) راجع التقرير ثم انسخ KEEP_REAL إلى الفرع النظيف

```powershell
cd C:\Users\samim\dealix-clean
git checkout -b chore/import-curated-local-assets
powershell -File data\local_artifact_audit\copy_keep_real.ps1
git status        # تأكّد أن الملفات منطقية
git diff --stat
```

### 4) راجع `REVIEW` يدوياً قبل أي نسخ

افتح كل ملف Python أو tsx من قائمة `REVIEW`. اسأل ثلاث أسئلة:

1. **ماذا يفعل فعلاً؟** (وليس ماذا يدّعي اسمه).
2. **هل ينتج output يمكن لعميل أن يدفع مقابله؟** أم يطبع تقارير لنفسه فقط؟
3. **هل يتجاوز بوابة موجودة؟** (مثلاً يكتب في `evidence_events_tracker.csv` أو
   يفعّل `enable_external_send=true`).

إذا فشل أي سؤال → اتركه. إذا نجح → انسخه يدوياً واكتب له اختبار يُثبت ادعاءه.

### 5) ارفع

```powershell
git add docs/ frontend/public/brand/ docs/company/   # حسب ما نسخت فقط
git commit -m "chore(assets): import curated brand and sales-kit assets from local working copy"
git push -u origin chore/import-curated-local-assets
gh pr create --base main --title "Import curated local assets" --body "Audited via scripts/audit_local_artifacts.py. KEEP_REAL bucket only; REVIEW items deferred; REJECT_STUB excluded per FOUNDER_REALITY_CHECK_AR.md."
```

## ما لا يجوز فعله — تحت أي ظرف

- ❌ **لا تنسخ** `evidence_events_tracker.csv` أو `kpi_founder_commercial_import.yaml`
  أو أي ملف تحت `data/founder_briefs/` من جهازك إلى الريبو. هذه ملفات state تُولَّد
  محلياً وتبقى محلية؛ رفعها يكسر سلسلة الأدلة.
- ❌ **لا تُرفع** نسخة "100 محرك" أو ما شابه حتى لو تشغّل محلياً. الاسم وحده يُضلِّل
  أي مراجع لاحق.
- ❌ **لا تحقن** `payment_received` أو `proof_pack_delivered` بدون دفعة وتسليم فعليين
  من عميل حقيقي. هذا ينطبق على الـCSV، الـJSON، الـYAML، وقاعدة البيانات.

## فحص الريبو الكنوني نفسه (Self-Scan)

بالإضافة إلى فحص نسخة محلية مقابل الكنوني، الأداة تدعم وضع **`--scan-canonical`**
الذي يفحص الريبو الحالي عن أي stubs مسرحية متسرّبة. الـheuristic هنا أضيق
ومدروس لتجنّب false positives على المصطلحات الشرعية في الريبو
(`meta_os`, `white_label`, `founder loop`...): فقط **STRONG phrases** تطابق،
وهي محصورة في أنماط فريدة لجلسات الـtheater (`sovereign_registry`,
`execute_50_storm`, `ultimate_autonomous_vision_2030`...).

```bash
python3 scripts/audit_local_artifacts.py --canonical . --scan-canonical --out data/local_artifact_audit
# للاستخدام في CI:
python3 scripts/audit_local_artifacts.py --canonical . --scan-canonical --fail-on-stub
```

النتيجة الحالية على الريبو: **0 stub findings** (نظيف).

## ما يُنصح به بعد التنظيف

عُد إلى البوابات الموجودة في الريبو الأصلي — هذه حقيقية، مختبرة، وتفعل ما تقوله:

| الهدف | الأمر |
|---|---|
| فحص جاهزية الإطلاق التجاري | `bash scripts/verify_dealix_commercial_go_live.sh` |
| موجز الصباح للمؤسس | `bash scripts/run_founder_commercial_day.sh` |
| بطاقة أداء أسبوعية | `bash scripts/founder_weekly_loop.sh` |
| استيراد ليدز فعلية مع التحقق | `python3 scripts/import_seed_leads.py --dry-run` |
| فحص واجهات GTM العامة | `python3 scripts/verify_gtm_public_surfaces.py` |

## الخلاصة

> منتج Dealix هو **الإثبات** — يجب أن يكون كل ادعاء قابلاً للتحقق برمجياً، وأن يكون
> كل دليل ناتجاً عن حدث حقيقي. الأداة `audit_local_artifacts.py` تحمي هذه القاعدة.
> استخدمها قبل أي رفع جماعي، وتجاهل كل ما تصنّفه `REJECT_STUB`.
