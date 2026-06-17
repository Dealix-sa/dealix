# سير عمل 100 شركة/يوم

## الهدف

الوصول إلى قدرة على التواصل مع 100 شركة/يوم دون spam ودون انتهاك الامتثال.

## المبدأ

جودة أولًا. كل شركة يجب أن يكون لها:
- `source_url` عام
- `verification_status`
- `confidence` 0.5+
- `pain_hypothesis` واضحة

## الخطوات

### 1. Research Queue

```bash
python3 scripts/revenue/find_targets_manual_workflow.py
```

أضف الشركات إلى `data/outreach/research_queue.csv`.

### 2. Prepare Batch

```bash
make prepare-100 BATCH_SIZE=10
```

Default = 10 للسلامة. يمكن 25/50/100.

### 3. Validate

```bash
make validate-100
```

يتحقق من:
- source_url
- verification_status ليس placeholder
- عدم وجود تكرار

### 4. Build Queue

```bash
make batch-queue BATCH_SIZE=10
```

يفحص:
- max 3 follow-ups
- cooldown 7 أيام
- حالة ليست contacted/opted_out/lost

### 5. Generate Outreach

```bash
make outreach
```

### 6. Review & Send Manually

راجع المسودات في `outbox/YYYY-MM-DD/` ثم أرسل يدويًا.

## القواعد

- لا scraping عدواني.
- لا بيانات شخصية حساسة.
- opt-out في كل رسالة.
- max 3 متابعات.
- cooldown 7 أيام.
- manual review إلزامي.

## التدرج

- الأسبوع 1-2: 10/يوم
- الأسبوع 3-4: 25/يوم
- الشهر 2: 50/يوم
- الشهر 3+: 100/يوم
