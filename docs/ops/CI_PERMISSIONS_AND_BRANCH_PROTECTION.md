# CI Permissions, Branch Protection & Environments / صلاحيات CI وحماية main والبيئات
<!-- PHASE: Launch | Owner: Founder | Date: 2026-06-07 -->
<!-- Arabic primary — العربية أولاً -->

> least-privilege لكل workflow + حماية main + بيئات بموافقة. الجزء داخل الريبو نُفِّذ؛
> أجزاء GitHub-UI يطبّقها المؤسس. The in-repo part is done; the GitHub-UI parts are founder steps.

---

## 1. ما نُفِّذ داخل الريبو / Done in this repo (least-privilege permissions)

أصل المشكلة: workflow بلا `permissions:` يرث الافتراضي المتساهل للمستودع. كان **13 من 51**
workflow بلا أي `permissions:` block. أُضيف لكلٍّ منها **أقل صلاحية** تطابق خطواته الفعلية
(فحص لكل ملف — لا `contents: read` أعمى). الـ 38 الباقية تُعلن صلاحياتها أصلًا وتُركت كما هي
(تقليلها يكسر release/SBOM/CodeQL).

| Workflow | الصلاحية المضافة | السبب |
|---|---|---|
| `scheduled_healthcheck.yml` | `contents: read` + `issues: write` | ينشئ issue عبر `github.rest.issues.create` عند فشل الإنتاج |
| الـ 12 الأخرى* | `contents: read` | checkout + فحوص + upload-artifact / نشر عبر سر خارجي (SSH_KEY/RAILWAY_TOKEN) — لا يحتاج كتابة `GITHUB_TOKEN` |

\* `business_now_snapshot`, `commercial-expand-weekly`, `cto_weekly_anchor`, `deploy`,
`design-system`, `enterprise-control-plane`, `founder_complete_autonomous_weekly`,
`founder_strongest_ops_daily`, `global-ai-transformation`, `railway_deploy`,
`reliability_drills_scorecard`, `staging-smoke`.

تحقّق: كل ملفات `.github/workflows/*.yml` تُحلَّل YAML بنجاح بعد التعديل.

```bash
python -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('.github/workflows/*.yml')]"
```

---

## 2. أقوى ضبط للصلاحيات (GitHub-UI — مؤسس) / Repo-wide default (founder)

أقوى ضابط least-privilege هو الافتراضي على مستوى المستودع، وهو **تبديل في الإعدادات** لا يُنفَّذ من الريبو:

```
Settings → Actions → General → Workflow permissions
  ◉ Read repository contents and packages permissions   (default = read-only)
  ☐ Allow GitHub Actions to create and approve pull requests   (اتركه مُطفأ ما لم يلزم)
```

بعد ذلك تبقى الـ workflows التي تحتاج كتابة (release/docker/codeql) لأنها تعلن `permissions:`
الخاصة بها صراحةً.

---

## 3. حماية main / Branch protection ruleset (GitHub-UI — مؤسس)

```
Settings → Rules → Rulesets → New ruleset
Name: main-production-protection      Target: main      Enforcement: Active
```

فعّل: Require PR before merging · Require approvals: 1 · Dismiss stale approvals ·
Require status checks · Require branches up to date · Require conversation resolution ·
Require linear history · Block force pushes · Block deletions · Do not allow bypassing.

**Required status checks — استخدم أسماء الفحوص الفعلية من الـ workflows، لا تسميات `make`:**
من `ci.yml`: `python-checks`, `web-build`, `frontend-build`, `railway-docker-builds`؛
ومن الأمن/الإصدار: `CodeQL`, `Dependency Review`, `Docker Build`.

> تنبيه دقّة: الخطة الملصقة سردت "make doctor / make env-check…" كـ required checks — هذه أوامر
> داخل الوظائف، وليست أسماء فحوص في GitHub. اختر الأسماء كما تظهر في تبويب Checks على PR فعلي.
> ولا تجعل CI أخضر شرطًا قبل إغلاق عائق `make security-smoke` (انظر
> `OFFICIAL_PRIVATE_LAUNCH_DECISION.md` §3.1) وقرار free-tier money-safety في PR #650.

---

## 4. البيئات / Environments (GitHub-UI — مؤسس)

```
Settings → Environments → New environment
```

- **staging:** Deployment branches = `main` only.
- **production:**
  - Required reviewers: Founder (Sami / VoXc2).
  - Prevent self-review: ON (إن متاح).
  - Allow administrators to bypass: OFF (إن متاح).
  - Deployment branches: `main` only.
  - أسرار الإنتاج تُربط بالبيئة (لا ملفات) — انظر `PRODUCTION_ENV_TEMPLATE.md` /
    `PRODUCTION_SECRETS_CHECKLIST.md`.

> required reviewers يحمون أسرار البيئة: لا يصلها workflow قبل موافقة بشرية صريحة.

---

## 5. صلاحيات قوالب لمراجعها / Reference permission templates

```yaml
# قاعدة افتراضية لأي workflow جديد:
permissions:
  contents: read

# نشر إنتاج عبر OIDC (إن استُخدم):
permissions:
  contents: read
  deployments: write
  id-token: write
```

مرجع: مبدأ least-privilege لـ `GITHUB_TOKEN`، وحماية الفروع، والبيئات بموافقة — موثّقة في GitHub Docs.
