# خطة استجابة فشل Railway — Dealix

هذه الخطة تختصر التعامل مع تنبيهات `Build failed` و `Deploy failed` حتى لا يتحول الفشل إلى تعطيل للنظام.

## 1) تحديد الخدمة المتأثرة

- `web` أو `cv` أو أي خدمة Frontend: راجع إعدادات Railway Root Directory. يجب أن يكون سياق البناء مطابقًا لمكان `package.json` و `Dockerfile`.
- خدمة API: يجب أن تستخدم `Dockerfile` في جذر الريبو، وتتحقق من `/healthz` بعد التشغيل.

## 2) إعدادات Railway الموصى بها

### API service

- Builder: Dockerfile
- Dockerfile path: `Dockerfile`
- Healthcheck path: `/healthz`
- Start command: اتركه فارغًا ليستخدم `CMD` من Dockerfile
- متغيرات إلزامية في الإنتاج:
  - `APP_ENV=production`
  - `APP_SECRET_KEY`
  - `JWT_SECRET_KEY`
  - `API_KEYS`
  - `ADMIN_API_KEYS`
  - `DATABASE_URL` عند استخدام Postgres

### Frontend service

- Root Directory: `frontend`
- Dockerfile path: `Dockerfile`
- Start command: اتركه فارغًا
- متغيرات عامة آمنة فقط:
  - `NEXT_PUBLIC_API_URL=https://api.dealix.me`
  - `NEXT_PUBLIC_SITE_URL=https://dealix.me`
  - `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1`

لا تضع مفاتيح Admin داخل متغيرات `NEXT_PUBLIC_*` لأنها تصبح جزءًا من حزمة المتصفح.

## 3) فحوصات بعد الإصلاح

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/ready
curl -fsS https://api.dealix.me/healthz?deep=1
```

للواجهة:

```bash
cd frontend
npm ci
npm run build
```

## 4) عند استمرار الفشل

انسخ أول خطأ حقيقي من Railway build logs، وليس عنوان الإيميل فقط. غالبًا يكون السبب واحدًا من:

- Root Directory غير صحيح.
- نقص `package-lock.json` أو استخدام أمر تثبيت غير مناسب.
- عدم وجود `output: 'standalone'` في Next.js مع Dockerfile يعتمد على `.next/standalone`.
- متغير إنتاج إلزامي مفقود يجعل التطبيق يفشل عند startup.
- preDeploy migration مفعّل بدون `DATABASE_URL` أو بدون Alembic صالح.

## 5) سياسة حماية الإنتاج

- لا يتم تجاوز فشل الأسرار في الإنتاج. أصلح المتغيرات بدل تعطيل التحقق.
- شغّل migrations فقط عندما تكون قاعدة البيانات جاهزة: `RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1`.
- أبقِ healthcheck سريعًا على `/healthz`، واستخدم الفحص العميق يدويًا بعد النشر.
