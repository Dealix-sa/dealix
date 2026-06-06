# Outreach Approval Queue

> Source of truth: `data/revenue/outreach_queue.jsonl`. **Nothing is sent
> automatically.** A draft is only sent after the founder marks it `approved`
> and sends it manually. No cold automation, no spam, no fake personalization,
> no guaranteed revenue.

## States
`draft` → `approved` → `sent`  (or `rejected`)

A row may be marked `sent` **only** if it was previously `approved`.

## How to use
1. The sales sub-agent drafts a message per target → status `draft`.
2. Founder reviews each draft here, edits, then sets `approval_status` to
   `approved` or `rejected` in the JSONL.
3. Founder sends the approved message manually (WhatsApp / email).
4. Founder marks it `sent` and logs any reply against the target in
   `data/growth/first_30_targets.csv`.

## First safe message (template)
> السلام عليكم [الاسم]،
> أبني Dealix كنظام تشغيل أعمال بالذكاء الاصطناعي للشركات السعودية. الفكرة ليست
> CRM ولا chatbot. نبدأ من أكثر نقاط التعطل وضوحًا: الفرص، المتابعة، العروض،
> الإثبات، والقرار التنفيذي القادم.
> أفتح 3 تجارب فقط كـ Command Sprint لمدة 7 أيام. المخرج: Revenue Map،
> Proof Register، Executive Command Brief، Next Action Board، Approval Register.
> بدون إرسال تلقائي، وبدون وعود مبالغ فيها، وكل شيء بموافقة بشرية.
> يناسبك أرسل لك Diagnostic مختصر؟

## Current queue
| Company | Person | Evidence | Status | Notes |
|---------|--------|----------|--------|-------|
| [Agency 1 — replace] | — | — | draft | Fill person/role + evidence before approving |

_Run `python scripts/founder_daily_command.py` to see what is due today._
