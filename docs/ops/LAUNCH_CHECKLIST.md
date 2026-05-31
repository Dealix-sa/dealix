# Dealix Launch Checklist — 2026-05-30

## خطوة صفر: أمان (أنت تنفذها الآن)

- [ ] ألغِ GitHub Token القديم: https://github.com/settings/tokens
- [ ] أنشئ GitHub Token جديداً بصلاحيات: `repo, workflow, write:packages`
- [ ] ألغِ Railway Token القديم من لوحة التحكم
- [ ] أنشئ Railway Token جديداً

---

## اليوم 1: GitHub Secrets (أنت تضيفها)

انتقل إلى: https://github.com/dealix-sa/dealix/settings/secrets/actions

- [ ] `RAILWAY_TOKEN` = التوكن الجديد من Railway
- [ ] `DEALIX_API_BASE` = `https://api.dealix.me`
- [ ] `DEALIX_ADMIN_API_KEY` = ← شغّل: `make gen-secrets`
- [ ] `RESEND_API_KEY` = من resend.com dashboard
- [ ] `DEALIX_FOUNDER_EMAIL` = `bassam.m.assiri@gmail.com`
- [ ] `ANTHROPIC_API_KEY` = من console.anthropic.com

---

## اليوم 1: Railway Environment Variables (أنت تضيفها)

افتح Railway dashboard → dealix-api service → Variables

**Generated (شغّل `make gen-secrets` للحصول عليها):**
- [ ] `SECRET_KEY`
- [ ] `JWT_SECRET_KEY`
- [ ] `ADMIN_API_KEY`

**Manual:**
- [ ] `DATABASE_URL` = `${{Postgres.DATABASE_URL}}` (استخدم Reference Variable)
- [ ] `ENVIRONMENT` = `production`
- [ ] `APP_URL` = `https://api.dealix.me`
- [ ] `BASE_URL` = `https://api.dealix.me`
- [ ] `CORS_ORIGINS` = `https://dealix.me,https://app.dealix.me`
- [ ] `MOYASAR_SECRET_KEY` = من Moyasar dashboard
- [ ] `MOYASAR_WEBHOOK_SECRET` = كلمة سر تختارها (ضعها أيضاً في Moyasar webhook settings)
- [ ] `RUN_RAILWAY_PRE_DEPLOY_MIGRATE` = `1`
- [ ] `SMTP_HOST` = `smtp.sendgrid.net`
- [ ] `FROM_EMAIL` = `noreply@dealix.sa`

**للـ founder-os-worker service:**
- [ ] `AGENT_APPROVAL_MODE` = `required`
- [ ] `AUTO_SEND_ENABLED` = `false`
- [ ] `EXTERNAL_OUTREACH_ENABLED` = `false`

---

## اليوم 1: النشر التلقائي (Claude يُشغّله)

بعد إضافة RAILWAY_TOKEN، أرسل push لـ main أو شغّل:
```
GitHub Actions → Deploy to Railway → Run workflow
```

---

## اليوم 1: التحقق بعد النشر (Claude يُشغّله)

```bash
make deploy-and-verify BASE_URL=https://api.dealix.me
```

---

## اليوم 2: Moyasar Webhook Setup (أنت تفعله)

1. افتح https://dashboard.moyasar.com → Webhooks
2. أضف Webhook URL: `https://api.dealix.me/api/v1/webhooks/moyasar`
3. اختر Events: `payment_paid`, `payment_failed`, `invoice_paid`
4. Secret Token = نفس `MOYASAR_WEBHOOK_SECRET` الذي وضعته في Railway

---

## اليوم 2: Moyasar KYC (أنت تفعله)

- [ ] ارفع Commercial Registration (السجل التجاري)
- [ ] ارفع هوية المؤسس
- [ ] ارفع IBAN / حساب بنكي
- [ ] انتظر 1-3 أيام للموافقة

---

## اليوم 3: إرسال رسائل LinkedIn (أنت تفعله — 5 دقائق)

الرسائل جاهزة في: `docs/ops/linkedin_outreach_tracker.md`

- [ ] Obada Allahham — Teryaq Marketing Agency
- [ ] Mohammed Alhamed — Above Limits (ابحث في LinkedIn)
- [ ] مؤسس Bytes Future (افتح Company Page → People)

---

## KPIs — الأسبوع الأول

| المقياس | الهدف |
|---------|-------|
| Healthcheck يرد 200 | ✓ |
| 22-point verify = green | ✓ |
| اختبار دفع 1 SAR ناجح | ✓ |
| رسائل LinkedIn مُرسلة | 3 |
| أول رد على LinkedIn | 1+ |
| أول Free Diagnostic | 1 |

---

*للمساعدة التقنية: `make cockpit` أو `make v5-status`*
