# Dealix Draft Approval Runbook — دليل الموافقة والإرسال اليدوي

دورة يومية قصيرة للمؤسس. **الإرسال يدوي دائمًا.**

## الخطوات

1. **شغّل اليوم**
   ```bash
   make distribution-day
   ```
   تحقق من `DEALIX_DISTRIBUTION_DAY=PASS`. إن كان `FAIL`، عالج بوابة الجودة أولًا
   (`make draft-quality`).

2. **افتح قائمة الموافقة**
   ```bash
   make draft-queue
   ```
   تُكتب أيضًا في `reports/distribution/DRAFT_QUEUE_REVIEW.md`.

3. **راجع كل مسودة** عبر SOAEN:
   - Source موثّق · Owner محدد · Approval · Evidence · Next Action واحد.

4. **اعتمد / عدّل / ارفض**
   ```bash
   python scripts/review_draft_queue.py --approve draft_xxxx
   python scripts/review_draft_queue.py --reject  draft_yyyy --reason "off-ICP"
   ```

5. **انسخ وأرسل يدويًا** عبر القناة المناسبة (email/WhatsApp/LinkedIn يدوي)، ثم:
   ```bash
   python scripts/review_draft_queue.py --mark-copied draft_xxxx
   ```

6. **سجّل النتيجة لاحقًا**
   ```bash
   python scripts/win_loss_learning.py --record --company "…" --outcome won|lost|no_response|nurture --reason "…"
   ```

## قواعد ثابتة
- لا إرسال خارجي تلقائي — أبدًا.
- لا وعود مضمونة ولا أرقام غير مثبتة.
- لا تعتمد مسودة فشلت في بوابة الجودة.
- اعتمد الأعلى ملاءمة (priority القطاع + جاهزية الحساب) أولًا.
