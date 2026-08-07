# خطة المؤسس — 72 ساعة القادمة

> ملف عملي بحت. لا استراتيجيات فضفاضة.

---

## اليوم 1 — التحقق والنشر

| الوقت | المهمة | الأمر/الإجراء |
|-------|--------|---------------|
| صباح | تحقق من الفرع | `git checkout launch/kimi-final-readiness-20260614` |
| صباح | راجع FINAL_VERDICT.md | `cat reports/kimi_final_launch_execution/FINAL_VERDICT.md` |
| صباح | راجع سلم العروض | `cat docs/commercial/DEALIX_FINAL_OFFER_LADDER_AR.md` |
| ظهر | شغل بناء الـ Frontend | `cd frontend && npm install && npm run build` |
| ظهر | شغل اختبارات بايثون | `APP_ENV=test pytest -q --no-cov` |
| عصر | راجع العمليات اللازمة | `cat reports/kimi_final_launch_execution/FOUNDER_ONLY_ACTIONS.md` |
| مساء | ابعت warm intro لـ 3 شركات | LinkedIn/WhatsApp يدوي |

---

## اليوم 2 — التشخيص والمكالمات

| الوقت | المهمة | الأمر/الإجراء |
|-------|--------|---------------|
| صباح | شغل cockpit | `make cockpit` |
| صباح | جهز قائمة 10 شركات | `docs/commercial/operations/targeting/agency_accounts_seed.csv` |
| ظهر | اتصل بـ 2-3 شركات من القائمة | اعرض التشخيص المجاني |
| عصر | ارسل عروض ليوم أمس | Email/WhatsApp يدوي |
| مساء | راجع نتائج التشخيصات | `GET /api/v1/diagnostic/intent` |

---

## اليوم 3 — إغلاق أول بايلوت مدفوع

| الوقت | المهمة | الأمر/الإجراء |
|-------|--------|---------------|
| صباح | تابع مكالمات أمس | Warm follow-up |
| ظهر | ارسل عرض بايلوت (2,500-5,000 ريال) | Use: `POST /api/v1/leads` + manual proposal |
| عصر | أغلق أول صفقة مدفوعة | signed agreement + Moyasar payment link |
| مساء | سجل النتيجة | `make cockpit` + CRM update |

---

## قائمة التحقق السريعة

- [ ] `cd frontend && npm run build` يشتغل بدون أخطاء
- [ ] `APP_ENV=test pytest -q` يمر
- [ ] `make doctor` يمر
- [ ] warm intro 3+ شركات يوم 1
- [ ] مكالمة 2+ شركة يوم 2
- [ ] عرض بايلوت مرسل يوم 3
- [ ] أول دفعة مستلمة

## إذا واجهت مشكلة

| المشكلة | الحل |
|---------|------|
| Frontend build fails | `cd frontend && npm run typecheck` → شوف الخطأ |
| pytest fails | `pytest -x -v` → أول test يفشل |
| `make doctor` fails | شوف `reports/kimi_final_launch_execution/VERIFICATION_LADDER.md` |
| محتاج مساعدة تقنية | راجع `AGENTS.md` → `docs/architecture/DEALIX_FUTURE_FILE_SYSTEM_AR.md` |

## ملاحظة مهمة
**لا ترسل رسائل WhatsApp آلية بدون موافقة.**  
**لا تشغل الدفع المباشر (live Moyasar) إلا بعد تفعيل ZATCA.**  
**لا تكشف أسرار API في أي مكان.**
