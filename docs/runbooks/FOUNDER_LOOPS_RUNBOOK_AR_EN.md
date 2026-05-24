# Founder Runbook — Autonomous Distribution Loops
# كتاب تشغيل المؤسس — حلقات التصريف الذاتي

> **Owner:** dealix-pm
> **Branch:** `claude/vibrant-lovelace-KwZio`

---

## كيف تعمل الحلقات / How the loops work

كل حلقة هي دالة pure-compute في `auto_client_acquisition.autonomous_distribution.loops`. تستدعيها سكربتات cron وتكتب تقاريرها في `data/autonomous_loops/`.

Each loop is a pure-compute function in `auto_client_acquisition.autonomous_distribution.loops`. Cron scripts invoke them and write reports to `data/autonomous_loops/`.

---

## Daily Morning Loop — 6:00 AM AST

```bash
python scripts/run_autonomous_distribution_loop.py morning
```

**يُنتج / Produces:** `data/autonomous_loops/YYYY-MM-DD_morning.md`

**ماذا أفعل / What you do:**
1. اقرأ digest العربي + الإنجليزي.
2. اطّلع على high_priority_actions.
3. ادخل `approval_center` لاعتماد أي drafts.
4. ابدأ يومك بناءً على الـ priorities.

---

## Daily Evening Loop — 8:00 PM AST

```bash
python scripts/run_autonomous_distribution_loop.py evening
```

**يُنتج / Produces:** `data/autonomous_loops/YYYY-MM-DD_evening.md`

**ماذا أفعل / What you do:**
1. راجع KPIs (revenue, pipeline, friction).
2. إذا high_severity_frictions > 0، حلّها قبل النوم.
3. تأكد من tomorrow_top_4 وعدّلها إذا لزم.

---

## Weekly Loop — Sunday 6:00 PM AST

```bash
python scripts/run_autonomous_distribution_loop.py weekly
```

**يُنتج / Produces:** `data/autonomous_loops/YYYY-MM-DD_weekly.md`

**ماذا أفعل / What you do:**
1. راجع week_over_week_pct.
2. تأكد من retainers_eligible وارسل عروض retainer.
3. سجّل capital_assets_added في الـ ledger.
4. خطّط للأسبوع القادم بناء على next_week_focus.

---

## Monthly Loop — Day 1 of month

```bash
python scripts/run_autonomous_distribution_loop.py monthly --days-since-launch 30
```

**يُنتج / Produces:** `data/autonomous_loops/YYYY-MM-DD_monthly.md`

**ماذا أفعل / What you do:**
1. تأكد من milestone_verdict (ahead / on_track / behind).
2. اقرأ decisions_for_founder.
3. إذا behind بعد يوم 60، **أوقف بناء عروض جديدة** وركّز على المبيعات.
4. إذا ahead في compounding phase، فعّل Wave 3 (Enterprise Trust).

---

## Decision Rules — قواعد القرار

| Signal | Action |
|---|---|
| `governance_decision == BLOCK` | اقرأ الـ rationale، لا تتجاوز البوابة. |
| `milestone_verdict == "behind"` بعد يوم 60 | أوقف بناء عروض، ركّز sales motion. |
| `milestone_verdict == "ahead"` في compounding | اقترح Wave 3. |
| `doctrine_violations > 0` | افتح friction event، حلّ خلال 24h. |
| `retainers_eligible > 0` | أرسل retainer proposal خلال 48h. |

---

## Cron schedule (مقترح / Suggested)

```cron
# Daily morning brief — 6am AST (= 3am UTC)
0 3 * * * cd /app && python scripts/run_autonomous_distribution_loop.py morning

# Daily evening brief — 8pm AST (= 5pm UTC)
0 17 * * * cd /app && python scripts/run_autonomous_distribution_loop.py evening

# Weekly Sunday 6pm AST (= 3pm UTC Sunday)
0 15 * * 0 cd /app && python scripts/run_autonomous_distribution_loop.py weekly

# Monthly day-1 9am AST (= 6am UTC)
0 6 1 * * cd /app && python scripts/run_autonomous_distribution_loop.py monthly --days-since-launch $(./scripts/days_since_launch.sh)
```

---

## Approval gates — متى تتدخل

| Gate | When | How |
|---|---|---|
| Outreach send | كل مسودة email/whatsapp/linkedin | عبر `approval_center` UI |
| Moyasar live charge | كل دفعة حقيقية | flip `MOYASAR_MODE=live` في Railway env |
| Proof Pack publish | قبل نشر للعميل | راجع draft، وافق في approval_center |
| Capital asset register | بعد كل دفعة | راجع asset_type، وافق |
| Retainer offer | بعد adoption_band=B | راجع، وافق |

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
