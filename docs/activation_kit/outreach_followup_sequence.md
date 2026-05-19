# Outreach Follow-up Sequence — تتابع المتابعة بعد الفتح

> Founder-led follow-up cadence that layers on top of the opening DMs already in `../ops/launch_content_queue.md`. Manual send only. No automation.

---

## القسم العربي

### القواعد قبل أي إرسال

- **إرسال يدوي فقط.** لا أداة أتمتة، لا scraping، لا أتمتة LinkedIn أو واتساب.
- **5 رسائل مُخصّصة في الساعة كحد أقصى.** كل رسالة تُكتب لشخص بعينه.
- **احترم إيقاف التواصل فوراً.** أي طلب توقّف ← غيّر الحالة إلى `opted_out` في `../ops/pipeline_tracker.csv` ولا تراسل مرة أخرى.
- **سجّل كل رسالة** في `pipeline_tracker.csv` (الحقول: `message_version`, `sent_at`, `reply_status`, `next_followup`).
- **سرعة الرد على الوارد أهم من سرعة الإرسال.** إذا رد أحد، رُد خلال 30 دقيقة.

### الجدول الزمني

| اللحظة | الغرض | الإجراء |
|---|---|---|
| D0 | الفتح | رسالة الفتح الموجودة في `launch_content_queue.md` (مع تعديل سطر العرض إلى "تشخيص مجاني 20–30 دقيقة") |
| D+2 | تذكير خفيف بسؤال واحد | المسودة أدناه |
| D+5 | قيمة + إعادة تأطير | المسودة أدناه |
| D+9 | إغلاق محترم للحلقة | المسودة أدناه |

### مسودة D+2 — سؤال واحد

```
أستاذ [الاسم]،
رسالتي قبل يومين، وأفترض الانشغال.
سؤال واحد فقط يساعدني: في فريقكم، كم يستغرق الرد الأولي على عميل محتمل جديد؟
أي إجابة مختصرة كافية. شاكر وقتك.
سامي
```

### مسودة D+5 — قيمة + إعادة تأطير

```
[الاسم]،
بدل المتابعة، أعرض شيئاً ملموساً: تشخيص مجاني 20–30 دقيقة ننظر فيه معاً
إلى كيف تستقبلون العملاء المحتملين وأين تتسرّب الفرص. ليس عرض بيع — محادثة عمل.
مخرجه ملخص مكتوب من صفحة. بدون التزام.
يناسبك 20 دقيقة هذا الأسبوع؟
سامي
```

### مسودة D+9 — إغلاق الحلقة

```
[الاسم]،
هذه آخر رسالة مني في هذا الموضوع — لا أرغب في الإلحاح.
إذا تغيّر التوقيت لاحقاً، رُد على هذه الرسالة وسأعود في نفس اليوم.
بالتوفيق لكم.
سامي
```

### بعد الرد

عند أي رد إيجابي، توقّف عن التتابع، احجز مكالمة التشخيص، وانتقل إلى [`discovery_and_close_script.md`](discovery_and_close_script.md). حدّث `reply_status` و `demo_booked_at` في المتتبّع.

---

## English Section

### Rules before any send

- **Manual send only.** No automation tool, no scraping, no LinkedIn or WhatsApp automation.
- **Max 5 personalized messages per hour.** Each message is written for a specific person.
- **Respect opt-outs immediately.** Any stop request → set status to `opted_out` in `../ops/pipeline_tracker.csv` and never message again.
- **Log every message** in `pipeline_tracker.csv` (fields: `message_version`, `sent_at`, `reply_status`, `next_followup`).
- **Speed of reply to inbound beats speed of sending.** When someone replies, respond within 30 minutes.

### The cadence

| Touch | Purpose | Action |
|---|---|---|
| D0 | Opening | The opening DM in `launch_content_queue.md` (with the offer line changed to "free 20-30 minute diagnostic") |
| D+2 | Light reminder, one question | Draft below |
| D+5 | Value + reframe | Draft below |
| D+9 | Respectful loop close | Draft below |

### D+2 draft — one question

```
Hello [Name],
My message was two days ago — I assume things are busy.
One quick question that helps me: on your team, how long does the first
reply to a new lead usually take? A short answer is plenty. Thank you for your time.
Sami
```

### D+5 draft — value + reframe

```
[Name],
Instead of just following up, here is something concrete: a free 20-30 minute
diagnostic where we look together at how you receive leads and where opportunity
leaks. Not a sales pitch — a working conversation. The output is a one-page
written summary. No commitment.
Would 20 minutes work this week?
Sami
```

### D+9 draft — close the loop

```
[Name],
This is my last message on this — I do not want to push.
If the timing changes later, reply to this message and I will respond the same day.
Wishing you well.
Sami
```

### After a reply

On any positive reply, stop the cadence, book the diagnostic call, and move to [`discovery_and_close_script.md`](discovery_and_close_script.md). Update `reply_status` and `demo_booked_at` in the tracker.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
