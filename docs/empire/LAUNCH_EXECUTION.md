# Launch Execution — تنفيذ التدشين

This document is the bridge between strategy and the running system. It does
not restate the 90-day model ([`COMMERCIAL_GATES.md`](COMMERCIAL_GATES.md)) or
the seven rungs ([`OFFER_LADDER.md`](OFFER_LADDER.md)) — it turns them into a
concrete 14-day launch sequence run on the tools that now exist in the repo.

## English

### The system you launch on

| Capability | How it runs | Doctrine |
|---|---|---|
| Daily targeting + draft generation | `scripts/daily_operate.sh` / `daily-revenue-machine.yml` cron | draft-only, approval-gated |
| Social content | `POST /api/v1/automation/social/draft` | draft-and-queue, never auto-posted |
| Approval queue (durable) | Command Center → Approvals, `/api/v1/approvals/*` | survives restarts; one-click approve |
| Warm-list outreach | `scripts/warm_list_outreach.py` → markdown drafts | founder sends manually |
| Proposal → artifact | `POST /api/v1/sales/proposal` → shareable HTML | a draft; delivery is approval-gated |
| Revenue pipeline (durable) | `/api/v1/revenue-pipeline/*` | evidence-gated stage advance |
| Morning brief | `GET /api/v1/founder/daily-brief` + email digest | read-only |
| Payments | `POST /api/v1/checkout` → Moyasar | `invoice_created ≠ revenue` |

### The 14-day launch sequence

Every day runs the **Commercial Proof Loop** from `COMMERCIAL_GATES.md`:
10 approved touches → 5 follow-ups → 1 partner talk → 1 demo → 1 small paid
pilot → Proof Pack in 48h → insight → referral/sprint/retainer.

**Day 0 — pre-flight.** Set production secrets (see founder list below).
Run `alembic upgrade head`. Smoke `daily_operate.sh` against staging.
Confirm `DEALIX_MOYASAR_MODE=test` and run a `pilot_1sar` checkout end to end.

**Days 1–3 — warm-list activation.** Run `warm_list_outreach.py` on the
founder's real warm list. Review every draft in the Command Center, approve,
and send manually. Target: 10 approved touches/day. Offer rung 2 — the
**499 SAR Sprint** (`pilot_managed`) — and the free Mini Diagnostic.

**Days 4–7 — first diagnostics + proposals.** For each reply, run the free
diagnostic, then `POST /api/v1/sales/proposal` and hand the HTML artifact to
the prospect. Log each as a pipeline lead; advance only on real evidence.
Cut scope, never price.

**Days 8–14 — first paid pilot.** Push one warm prospect to a paid
`pilot_managed` (499 SAR) or `data_pack` (1,500 SAR) checkout. On payment
confirmation, advance the pipeline to `payment_received` with evidence, and
deliver the 14-section Proof Pack within 48 hours.

### Gate to exit launch

Launch is "done" when **Day-30 gate** of `COMMERCIAL_GATES.md` is met: one
paid pilot, one Proof Pack, one partner loop, three insights, one winning
message, one best ICP. Everything else waits.

### Founder action list (non-code, runs in parallel)

1. **Moyasar KYC** — commercial registration + IBAN → enables real payouts.
   Until then the system runs in `test` mode (`pilot_1sar`).
2. **Third-party credentials** — Meta business verification (WhatsApp),
   PostHog, UptimeRobot, HubSpot/Calendly tokens. Code is wired and waiting.
3. **Legal / PDPL** — DPO registration, DPA signature, SDAIA portal; a lawyer
   reviews the privacy/terms pages before the first paid deal.
4. **Production secrets** — `DATABASE_URL`, `APP_SECRET_KEY`, `MOYASAR_*`,
   `GMAIL_REFRESH_TOKEN`, an LLM key, `REDIS_URL`, `SENTRY_DSN` in Railway.
5. **Engineering drills** — run the k6 load test, rollback drill, and backup
   restore on staging (scripts exist; ~2 hours).
6. **Known follow-up** — the frontend auth flow (`useAuth` login/register)
   expects a `{user, tokens}` response shape; the backend `/auth/login` and
   `/auth/register` return a flat `TokenResponse`. Reconcile the contract
   (transform in `useAuth`, or add a `user` block server-side) before opening
   public sign-up — needs a running frontend to verify.
7. **Daily** — review the approval queue in the Command Center each morning
   (~15 minutes).

---

## العربية

### النظام الذي تُدشّن عليه

التشغيل اليومي يمرّ كله بطابور موافقة بضغطة — لا إرسال ولا نشر تلقائي:
الاستهداف وتوليد المسوّدات (`daily_operate.sh`)، محتوى السوشل
(`/automation/social/draft`)، طابور الموافقات الدائم (مركز القيادة)، القائمة
الدافئة (`warm_list_outreach.py`)، العرض → أداة HTML قابلة للمشاركة
(`/sales/proposal`)، خط الإيراد الدائم (`/revenue-pipeline/*`)، الموجز الصباحي
(`/founder/daily-brief`)، والدفع عبر Moyasar (`/checkout`).

### تسلسل التدشين — 14 يوماً

كل يوم يُشغّل **حلقة الإثبات التجاري** من `COMMERCIAL_GATES.md`: 10 لمسات
معتمَدة ← 5 متابعات ← محادثة شريك ← demo ← أول pilot مدفوع صغير ← Proof Pack
خلال 48 ساعة ← رؤية ← إحالة أو sprint أو retainer.

- **يوم 0 — ما قبل الإقلاع.** ضبط أسرار الإنتاج، `alembic upgrade head`،
  smoke لـ`daily_operate.sh` على staging، و checkout تجريبي بـ`pilot_1sar`.
- **أيام 1–3 — تفعيل القائمة الدافئة.** تشغيل `warm_list_outreach.py`، مراجعة
  كل مسوّدة من مركز القيادة واعتمادها وإرسالها يدوياً — 10 لمسات/يوم. العرض:
  Sprint بـ499 ريال + التشخيص المجاني.
- **أيام 4–7 — أول تشخيصات وعروض.** لكل ردّ: تشخيص مجاني ثم `/sales/proposal`
  وتسليم أداة الـHTML. تسجيل كل واحد كـlead في خط الإيراد؛ التقدّم بالأدلّة فقط.
  قلّص النطاق لا السعر.
- **أيام 8–14 — أول صفقة مدفوعة.** دفع عميل دافئ واحد إلى checkout مدفوع
  (`pilot_managed` 499 أو `data_pack` 1,500). عند تأكيد الدفع: تقديم خط
  الإيراد إلى `payment_received` بالأدلّة، وتسليم Proof Pack خلال 48 ساعة.

### بوابة الخروج من التدشين

ينتهي التدشين عند تحقّق **بوابة اليوم 30** في `COMMERCIAL_GATES.md`: pilot
مدفوع واحد، Proof Pack واحد، حلقة شريك، 3 رؤى، رسالة رابحة، أفضل ICP.

### قائمة مهام المؤسس (غير برمجية — بالتوازي)

1. **Moyasar KYC** — السجل التجاري + الآيبان ← يفتح استلام الفلوس فعلياً؛
   حتى ذلك النظام يعمل بوضع `test`.
2. **اعتمادات الطرف الثالث** — Meta، PostHog، UptimeRobot، HubSpot/Calendly.
3. **قانوني/PDPL** — DPO، DPA، بوابة SDAIA، ومراجعة محامٍ قبل أول صفقة مدفوعة.
4. **أسرار الإنتاج** في Railway.
5. **تمارين هندسية** — k6، rollback، backup restore على staging.
6. **متابعة معروفة** — تدشين auth في الفرونت إند يتوقّع شكل `{user, tokens}`
   بينما الباك إند يُرجع `TokenResponse` مسطّحاً؛ يجب مواءمة العقد قبل فتح
   التسجيل العام.
7. **يومياً** — مراجعة طابور الموافقات (~15 دقيقة).
