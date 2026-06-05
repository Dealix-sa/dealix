# Revenue OS — Opportunity and follow-up system — نظام الإيراد

## Purpose — الغرض

Revenue OS manages the path from a qualified target to a paying engagement. It tracks open opportunities, plans follow-up, drafts offers, and records objections so the team learns from every conversation. AI analyzes opportunity context and recommends next touches and drafts offer language; deterministic workflows schedule follow-up and maintain the log; the human approves every offer and every message before it leaves. The system produces the Revenue Map — a single view of where each opportunity sits, what was promised, what the next move is, and what blocks it. It does not promise sales numbers, does not send anything on the customer's behalf without approval, and treats objections as recorded evidence, not anecdotes.

نظام الإيراد يدير المسار من هدف مؤهَّل إلى ارتباط مدفوع. يتتبّع الفرص المفتوحة، ويخطّط المتابعة، ويصيغ العروض، ويسجّل الاعتراضات ليتعلّم الفريق من كل محادثة. يحلّل الذكاء الاصطناعي سياق الفرصة ويوصي باللمسات التالية ويصيغ لغة العرض؛ وتجدول المسارات الحتمية المتابعة وتحفظ السجل؛ ويعتمد الإنسان كل عرض وكل رسالة قبل إرسالها. ينتج النظام خريطة الإيراد — عرضاً واحداً لموقع كل فرصة، وما وُعد به، والخطوة التالية، وما يعيقها. لا يَعِد بأرقام مبيعات، ولا يرسل شيئاً نيابة عن العميل بلا اعتماد، ويعامل الاعتراضات كدليل مسجّل لا كحكايات.

## Status — الحالة

Revenue OS | BETA | Revenue Map; opportunity + objection logs

نظام الإيراد | BETA | خريطة الإيراد؛ سجلّا الفرص والاعتراضات

## Inputs — المدخلات

- Targeting shortlist and company intelligence from Market Intelligence OS — قائمة الاستهداف واستخبارات الشركة من نظام استخبارات السوق
- Proof Register entries to support offers from Proof OS — مدخلات سجل الإثبات لدعم العروض من نظام الإثبات
- Pricing inputs from Finance OS — مدخلات التسعير من النظام المالي

## Outputs — المخرجات

- Revenue Map: stage, promise, next move, blocker per opportunity — خريطة الإيراد: المرحلة، الوعد، الخطوة التالية، العائق لكل فرصة
- Drafted offers pending approval — عروض مصاغة بانتظار الاعتماد
- Objection log feeding Proof OS and Command OS — سجل الاعتراضات يغذّي نظام الإثبات ونظام القيادة

## Guardrails — الضوابط

- No guaranteed sales outcomes (5): offers state estimated value, never promised revenue — لا ضمان لنتائج البيع
- No external action without approval (8): every message is human-approved — لا إجراء خارجي بلا اعتماد
- No fake or un-sourced claims (4): offer claims trace to the Proof Register — لا ادعاءات مزيّفة أو بلا مصدر
- No PII in logs (6): opportunities use anonymized labels — لا بيانات شخصية في السجلات

## Cross-links — روابط

- [`../00_platform_truth/MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md)
- [`MARKET_INTELLIGENCE_OS.md`](./MARKET_INTELLIGENCE_OS.md) · [`PROOF_OS.md`](./PROOF_OS.md) · [`FINANCE_OS.md`](./FINANCE_OS.md) · [`COMMAND_OS.md`](./COMMAND_OS.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
