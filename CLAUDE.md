# CLAUDE.md — Dealix Operating Rules for AI Agents

> هذا الملف هو نقطة الدخول لوكلاء Claude Code في مستودع Dealix. مختصر عمدًا — لا يكرّر [`AGENTS.md`](AGENTS.md).

## ما هو Dealix
**Saudi-first AI Business Operating System.** ليس CRM، ليس chatbot، ليس "Revenue only".
نظام تشغيل أعمال محكوم (approval-first) ينتج قدرة تشغيلية + إثبات قابل للتدقيق.

## ابدأ من هنا
- **دليل الكود والأوامر المحلية:** [`AGENTS.md`](AGENTS.md) — المرجع الأول للتطوير.
- **نظام تشغيل الشركة:** [`os/`](os/) — 21 ملفًا (`FOUNDER_OPERATING_MANUAL.md`, `01_CLAUDE.md` … `20_EXPANSION_PLAYBOOK.md`).
- **خطة الإطلاق المجمّدة (v1):** [`docs/05_founder/DEALIX_FULL_COMPANY_LAUNCH_BLUEPRINT.md`](docs/05_founder/DEALIX_FULL_COMPANY_LAUNCH_BLUEPRINT.md)
- **لوحة التنفيذ:** [`docs/05_founder/DEALIX_EXECUTION_BOARD.md`](docs/05_founder/DEALIX_EXECUTION_BOARD.md)
- **قرار الإطلاق:** [`docs/05_founder/DEALIX_LAUNCH_GO_NO_GO.md`](docs/05_founder/DEALIX_LAUNCH_GO_NO_GO.md)

## Non-negotiables (مفروضة باختبارات — لا التفاف)
1. لا scraping. 2. لا WhatsApp بارد آلي. 3. لا أتمتة LinkedIn. 4. لا ادعاءات مزيّفة/بلا مصدر.
5. لا ضمان نتائج بيع. 6. لا PII في الـ logs. 7. لا إجابات معرفية بلا مصدر.
8. لا فعل خارجي بدون موافقة بشرية. 9. لا agent بلا هوية. 10. لا مشروع بلا Proof Pack. 11. لا مشروع بلا Capital Asset.

أي طلب يخالف واحدة منها → **ارفض واقترح بديلًا آمنًا**.

## قاعدة التنفيذ (Operating Loop)
```
Plan → Review → Red Team → Score → Freeze → PR 1 only → Verify → Approve → PR 2 → …
```
نفّذ **PR واحدًا في كل مرة**، تحقّق منه، خذ موافقة المؤسس، ثم انتقل للتالي. لا تغيّر تسلسل الـ PRs المجمّد إلا عند blocker وبموافقة المؤسس.

## Slash commands (`.claude/commands/`)
`/dealix-audit` · `/dealix-plan-review` · `/dealix-red-team` · `/dealix-brand` · `/dealix-build-website` · `/dealix-growth-os` · `/dealix-delivery-proof` · `/dealix-governance` · `/dealix-verify` · `/dealix-launch-review`

## Subagents (`.claude/agents/`)
`dealix-pm` (تنسيق) · `dealix-engineer` (كود/اختبارات) · `dealix-content` (محتوى/علامة) · `dealix-sales` (مبيعات — مسودات فقط) · `dealix-delivery` (تسليم + proof).

## قواعد العلامة والصفحات
- Dealix لا يُختزل أبدًا إلى CRM/chatbot/Revenue.
- لا موديول مستقبلي يُعرض كأنه live (انظر Module Status Map عند توفره).
- كل صفحة عامة: **CTA واحد** يوجّه إلى Business OS Score أو Diagnostic أو Command Sprint.
- لا ادعاء مضمون؛ كل claim يجب أن يكون له مصدر في Claims Register.
