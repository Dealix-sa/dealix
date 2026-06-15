# Dealix — دليل المؤسس اليومي (Founder Runbook)

نظام تشغيل كامل لاكتساب أول عملاء يدفعون. كل شي يجهّز نفسه — **أنت تراجع وترسل**. لا إرسال تلقائي (سياسة المراجعة البشرية، محمية باختبار `tests/test_no_auto_send.py`).

---

## ⏱️ الروتين اليومي (15–20 دقيقة)

### الصباح (10 دقائق)
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

## 🗺️ خريطة النظام
| المكوّن | الملف/الأمر | الدور |
|--------|------------|------|
| نصوص الإقناع | `data/outreach/sector_pitches.json` | ألم → حل → دعوة، لكل قطاع |
| قائمة الاستهداف | `data/outreach/saudi_target_intake.csv` | شركاتك الحقيقية (محلي، لا يُرفع) |
| محرّك الإيميلات | `make outreach` / `-f3` / `-f7` | يولّد إيميلات جاهزة |
| سجل المتابعة | `data/outreach/outreach_log.csv` | تحدّثه بعد كل إرسال |
| غرفة القيادة | `make command-room` | لوحة KPIs (مُرسل/ردود/قمع) |
| دليل الردود | `business/playbooks/REPLY_PLAYBOOK.md` | ماذا ترسل عند كل رد |
| سُلّم العروض | `business/pricing/OFFER_LADDER.md` | الأسعار الرسمية |
| العرض الرسمي | `presentations/company-profile/dealix-company-profile.html` | للإرفاق |
| كل شي مرة وحدة | `make daily` | الصباح كامل في أمر واحد |

---

## 🎯 هدف الأسبوع الأول
- [ ] 25 شركة حقيقية في `saudi_target_intake.csv` (إيميلات مؤكدة)
- [ ] 25 إيميل أولي مُرسل (5 يوميًا)
- [ ] متابعة f3 + f7 لكل من لم يرد
- [ ] 3 ردود → تشخيص مجاني
- [ ] أول مكالمة 20 دقيقة

## القاعدة الوحيدة
> أرسل 5 إيميلات حقيقية كل يوم. المتابعة تقفل أكثر من الرسالة الأولى. الاتساق > الكمال.
