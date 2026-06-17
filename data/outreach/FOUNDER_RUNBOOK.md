# Dealix — دليل المؤسس اليومي (Founder Runbook)

نظام تشغيل كامل لاكتساب أول عملاء يدفعون. كل شي يجهّز نفسه — **أنت تراجع وترسل**. لا إرسال تلقائي (سياسة المراجعة البشرية، محمية باختبار `tests/test_no_auto_send.py`).

---

## ⏱️ الروتين اليومي (15–20 دقيقة)

### الصباح — أمر واحد (2 دقيقة)
```bash
make daily-ops           # أولوياتك اليوم بالكامل — AR+EN
```
يقرأ من `outreach_log.csv` و`contract_log.csv` ويطبع قائمة عمل مرتّبة حسب الأولوية (🔴→🟠→🟡→🟢).

### الصباح الموسّع (10 دقائق)
```bash
# 1) حدّث قائمة شركاتك الحقيقية (أضف 3–5 شركات بإيميل مؤكد)
nano data/outreach/saudi_target_intake.csv

# 2) ولّد إيميلات اليوم الجاهزة
make outreach            # → reports/outreach/<اليوم>/

# 3) ولّد لوحة غرفة القيادة
make command-room        # → reports/command_room/index.html
```
افتح كل إيميل، تأكد من عنوان المستلم، **أرسل بنفسك**، ثم سجّل في `data/outreach/outreach_log.csv` (status = sent).

### بعد العصر (5 دقائق) — المتابعات
```bash
make outreach-f3         # متابعة لطيفة لمن لم يرد بعد 3 أيام
make outreach-f7         # متابعة أخيرة لمن لم يرد بعد 7 أيام
```

### عند أي رد
افتح `business/playbooks/REPLY_PLAYBOOK.md` → جهّز الرد المناسب → أرسل → حدّث السجل (reply / meeting).

---

## 🗺️ خريطة النظام الكاملة

### مرحلة 1 — Outreach (التواصل)
| الأمر | الدور |
|-------|------|
| `make daily-ops` | أولوياتك الصباحية — يقرأ pipeline + عقود + مقترحات |
| `make outreach` | يولّد إيميلات اليوم (مسودات جاهزة للإرسال اليدوي) |
| `make outreach-f3` | متابعة يوم 3 |
| `make outreach-f7` | متابعة يوم 7 |
| `make outreach-tracker COMPANY="..." STATUS="sent"` | تسجيل حدث في سجل التواصل |
| `make outreach-tracker-summary` | ملخص pipeline (مُرسل/ردود/اجتماعات/فوز) |
| `make outreach-tracker-list SECTOR="logistics"` | عرض السجل مُصفّى |

### مرحلة 2 — Discovery (الاستكشاف)
| الأمر | الدور |
|-------|------|
| `make diagnostic COMPANY="..." SECTOR="..."` | يولّد التشخيص المجاني (30 نقطة) |
| `make reply-classify COMPANY="..." TEXT="..."` | يصنّف الرد الوارد ويقترح الخطوة التالية |
| `make meeting COMPANY="..." SECTOR="..."` | يولّد agenda مكالمة الاستكشاف (AR+EN) |

### مرحلة 3 — Proposal (العرض)
| الأمر | الدور |
|-------|------|
| `make proposal COMPANY="..." SECTOR="..." TIER="sprint"` | يولّد عرض سعر بالعربي (مسودة — لا يُرسل تلقائياً) |
| `make proposal COMPANY="..." SECTOR="..." --dry-run` | معاينة بدون حفظ ملف |
| `make proposal --list-sectors` | عرض القطاعات والباقات الموصى بها |

**تدرّج الباقات:**
- `sprint` — 499 SAR إعداد (التشخيص السريع 7 أيام)
- `review_os` — 12,000 SAR + 3,500/شهر
- `revenue_os` — 18,000 SAR + 5,000/شهر
- `delivery_os` — 25,000 SAR + 6,000/شهر
- `command_center` — 35,000 SAR + 9,000/شهر

### مرحلة 4 — Contract (العقد)
| الأمر | الدور |
|-------|------|
| `make contract COMPANY="..." SECTOR="..." TIER="sprint"` | يولّد عقد خدمة رسمي (AR+EN) |
| `make contract-dry COMPANY="..." SECTOR="..." TIER="sprint"` | معاينة العقد |
| `make contract-tiers` | عرض الباقات والأسعار |

### مرحلة 5 — Onboarding (الاستقبال)
| الأمر | الدور |
|-------|------|
| `make onboard COMPANY="..." SECTOR="..."` | حزمة استقبال العميل الجديد |

### مرحلة 6 — Customer Success (نجاح العميل)
| الأمر | الدور |
|-------|------|
| `make pilot-report COMPANY="..." SECTOR="..."` | تقرير نتائج التشغيل التجريبي 7 أيام |
| `make customer-monthly-report COMPANY="..." SECTOR="..." MONTH="2026-06"` | تقرير شهري للعميل |
| `make renewal-check` | تنبيهات العقود المنتهية خلال 30/60 يوم |
| `make renewal-summary` | ملخص MRR + العقود النشطة + المعرّضة للخطر |

### أدوات المراجعة الأسبوعية
| الأمر | الدور |
|-------|------|
| `make weekly-review` | تقرير GTM الأسبوعي الكامل |
| `make command-room` | لوحة KPIs تفاعلية |
| `make targets-merge` | دمج قوائم الاستهداف |

---

## 📋 خريطة الملفات والمخرجات

| المكوّن | المسار | الحالة |
|--------|--------|--------|
| نصوص الإقناع | `data/outreach/sector_pitches.json` | Git-tracked |
| قائمة الاستهداف | `data/outreach/saudi_target_intake.csv` | **محلي فقط** (gitignore) |
| سجل التواصل | `data/outreach/outreach_log.csv` | **محلي فقط** (gitignore) |
| سجل العقود | `data/contracts/contract_log.csv` | **محلي فقط** (gitignore) |
| المقترحات المولّدة | `reports/proposals/<date>/` | **محلي فقط** (gitignore) |
| العقود المولّدة | `reports/contracts/<date>/` | **محلي فقط** (gitignore) |
| تقارير الـ Pilot | `reports/pilot_reports/<date>/` | **محلي فقط** (gitignore) |
| تقارير العملاء | `reports/customer_reports/<month>/` | **محلي فقط** (gitignore) |
| Agenda الاجتماعات | `reports/meetings/<date>/` | **محلي فقط** (gitignore) |
| دليل الردود | `business/playbooks/REPLY_PLAYBOOK.md` | Git-tracked |
| سُلّم العروض | `business/pricing/OFFER_LADDER.md` | Git-tracked |

---

## 🎯 هدف الأسبوع الأول
- [ ] 25 شركة حقيقية في `saudi_target_intake.csv` (إيميلات مؤكدة)
- [ ] 25 إيميل أولي مُرسل (5 يوميًا) — `make outreach`
- [ ] متابعة f3 + f7 لكل من لم يرد
- [ ] 3 ردود → `make diagnostic` + `make meeting`
- [ ] أول عقد → `make proposal` ثم `make contract`

## 🎯 هدف الأسبوع الثاني
- [ ] أول عميل يدفع — `make contract` + `make onboard`
- [ ] تشغيل تجريبي 7 أيام → `make pilot-report`
- [ ] تفعيل تقرير شهري → `make customer-monthly-report`
- [ ] مراقبة تجديد العقد → `make renewal-check`

## القاعدة الوحيدة
> أرسل 5 إيميلات حقيقية كل يوم. المتابعة تقفل أكثر من الرسالة الأولى. الاتساق > الكمال.

---

*آخر تحديث: 2026-06 — يغطي الـ pipeline الكامل: Outreach → Discovery → Proposal → Contract → Onboarding → Customer Success → Renewal*
