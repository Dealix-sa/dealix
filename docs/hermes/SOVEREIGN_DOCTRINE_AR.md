# Dealix — العقيدة السيادية (Hermes)

> «Dealix ليس تطبيقًا. Dealix نظامٌ سيادي يحوّل كل ما يدخله إلى قيمة قابلة للقياس.»

هذه الوثيقة الأم: ما القاعدة المركزية؟ ما طبقات النظام؟ ما المنتجات الخارجية الآن؟ ما الذي لا يمر دون موافقتك؟

---

## 1) القاعدة المركزية (سبعة مخرجات لا غيرها)

أي شيء يدخل Dealix يجب أن يخرج بواحد أو أكثر من:

1. **Money** — كاش مباشر أو خط أنابيب (pipeline)
2. **Data** — نتيجة أو معلومة تزيد ذكاء النظام
3. **Asset** — قالب / playbook / تقرير / دراسة حالة
4. **Partner** — قناة توزيع أو تنفيذ
5. **Trust** — تقليل خطر أو زيادة قابلية البيع
6. **Access** — وصول لعميل / قطاع / شبكة
7. **Learning** — درس يُحسّن القرار القادم

أي شيء لا ينتج واحدًا منها = **هدر**.

محل الكود: [`dealix/hermes/__init__.py`](../../dealix/hermes/__init__.py) — `ValueOutput`, `DOCTRINE_RULES_AR`.

---

## 2) الـ Pipeline الإلزامي

```
Signal → Opportunity → Decision → Execution → Trust → Outcome → Asset → Scale
```

كل مرحلة لها schema غير قابل للتجاوز ([`dealix/hermes/core/schemas.py`](../../dealix/hermes/core/schemas.py)).

- **Signal Intake** — `SignalIntake` يقبل أي إشارة من ١٢ مصدر.
- **Opportunity Graph** — يحوّل الإشارات إلى فرص مُسعّرة بـ `expected_value_sar`.
- **Decision Memo** — قبل أي تنفيذ S3+ تُكتب مذكّرة.
- **Execution Plan** — خطوات مرتّبة بمسؤولين وأدوات؛ لا تنفّذ من تلقاء نفسها.
- **Trust Check** — guardrails (overclaim/PII/cold-channel) + MCP risk.
- **Outcome Log** — نتيجة مُحدّدة (won/lost/paid/risk_blocked/learning…)؛ لا إيراد قبل `PAID`.
- **Asset Builder** — كل نتيجة تُراجَع: هل تستحق template/playbook/case study؟
- **Scale/Kill** — كل ٣٠ يومًا: ما الذي نضاعفه وما الذي نُغلقه؟

---

## 3) الطبقة السيادية (Sami-only)

خمسة مستويات:

| المستوى | المعنى | مثال |
| --- | --- | --- |
| S0_AUTONOMOUS | داخلي قابل للتراجع تمامًا | قراءة فرصة، احتساب priority |
| S1_INTERNAL | داخلي مُدقّق، لا مرسل خارجي | صياغة عرض، بناء evidence pack |
| S2_SAMI_APPROVAL | سامي يوافق قبل التنفيذ | تسعير، تعديل عرض، مقترح خارجي |
| S3_SOVEREIGN_MEMO | مذكّرة مكتوبة + توقيع سامي | إرسال رسالة خارجية، توقيع شراكة |
| S4_SOVEREIGN_RESERVED | سامي وحده يبدأها | public API، marketplace، spin-out، استحواذ |

محل الكود: [`dealix/hermes/sovereignty.py`](../../dealix/hermes/sovereignty.py).

> القاعدة: لا يمكن لأي وكيل خفض المستوى تحت الأرضيّة (`SOVEREIGN_FLOOR_ACTIONS`). يرفع الـ Gate تلقائيًا.

---

## 4) الحوكمة: Agent Registry + Tool Registry

كل وكيل له **Agent Card** ([`dealix/hermes/trust/agent_registry.py`](../../dealix/hermes/trust/agent_registry.py)):
- `mission`, `owner`, `allowed_tools`, `forbidden_tools`, `max_sovereignty_level`, `kpis`.
- وكيل بدون KPI = لا يدخل النظام.
- وكيل بدون Card = لا ينفّذ.

كل أداة لها **Tool Card** ([`dealix/hermes/trust/tool_registry.py`](../../dealix/hermes/trust/tool_registry.py)):
- `scope`, `sovereignty_floor`, `risk_score`, `reversible`, `mcp_origin`.
- `send_external_message` أرضيّتها S3.
- `publish_public_api` و`publish_marketplace_listing` أرضيّتهما S4.

الـ **PermissionMatrix** ([`dealix/hermes/trust/permissions.py`](../../dealix/hermes/trust/permissions.py)) ترفض أي زوج (agent, tool) يخالف:
1. Tool في `forbidden_tools` للوكيل.
2. Tool خارج `allowed_tools` (إذا حُدّدت).
3. سقف الوكيل أدنى من أرضيّة الأداة.

---

## 5) الحماية أمام MCP — Tool Poisoning

أبحاث MCP وOWASP LLM Top 10 ترصد *tool poisoning* (تعليمات خبيثة داخل metadata) كأحد أعلى المخاطر:

- [`dealix/hermes/trust/mcp_security.py`](../../dealix/hermes/trust/mcp_security.py): فحص ثابت لتعليمات الحقن، hash مستقر للـ metadata، كشف التغيير الصامت.
- [`dealix/hermes/trust/guardrails.py`](../../dealix/hermes/trust/guardrails.py): overclaim, PII, cold channel.

---

## 6) المحركات (Engines)

| Engine | محل الكود | ما يخرج منه |
| --- | --- | --- |
| Money | `dealix/hermes/money/` | Cash Scout, Pricing, Proposal, Follow-up, Dashboard |
| Product | `dealix/hermes/products/` | Offer Library, Scale/Kill |
| Partner | `dealix/hermes/partners/` | Scout, Fit Score |
| Intelligence | `dealix/hermes/intelligence/` | Market Radar |
| Training | `dealix/hermes/training/` | Workshop Builder + Library |
| Customer | `dealix/hermes/customer/` | Health Score, Value Report |
| Venture | `dealix/hermes/ventures/` | Vertical Launcher |

---

## 7) العروض الخارجية الآن (Offer Library)

تظهر للسوق ٦ عروض فقط — البقية داخلية حتى يقرّر سامي إخراجها:

1. **Revenue Hunter Pilot** — 999–4,999 ر.س / ١٤ يوم.
2. **AI Trust Kit** — 5,000–25,000 ر.س / ١٤ يوم.
3. **Agency White-label Kit** — 1,000–10,000 ر.س — S3 memo إجباري.
4. **Founder OS Setup** — 2,000–8,000 ر.س / ٧ أيام.
5. **Market Radar Report** — 4,000–15,000 ر.س / ١٠ أيام.
6. **Executive PMO Lite** — 2,999–4,999 ر.س / شهر.

محل الكود: [`dealix/hermes/products/offer_library.py`](../../dealix/hermes/products/offer_library.py).

---

## 8) الـ Sovereign Console (الواجهة)

`GET /api/v1/hermes/console` (admin-gated) يُعيد:

```text
command.fastest_cash_action       — أسرع كاش هذا الأسبوع
command.top_strategic_opportunity — أعلى فرصة استراتيجية
command.sovereign_approval_required — قائمة موافقات تنتظرك
command.scale / command.kill      — ماذا نضاعف، وماذا نُغلق
money.{pipeline_value_sar, cash_collected_sar, fastest_cash[]}
trust.{agents_registered, tools_registered, audit_chain_valid, approvals_pending}
doctrine_rules_ar                 — القواعد الـ ٧ المرئية يوميًا
```

محل الكود: [`dealix/hermes/console.py`](../../dealix/hermes/console.py) و[`api/routers/hermes_console.py`](../../api/routers/hermes_console.py).

---

## 9) APIs المُتاحة الآن (admin-gated)

| Endpoint | الغرض |
| --- | --- |
| `GET  /api/v1/hermes/console` | لقطة Sovereign Console |
| `POST /api/v1/hermes/signals` | تسجيل إشارة جديدة |
| `GET  /api/v1/hermes/signals` | قائمة الإشارات |
| `POST /api/v1/hermes/opportunities` | تحويل إشارة(ات) إلى فرصة مُسعّرة |
| `GET  /api/v1/hermes/opportunities/top` | أعلى N فرصة بـ expected_value |
| `GET  /api/v1/hermes/money/dashboard` | Money Dashboard |
| `GET  /api/v1/hermes/offers` | Offer Library (الفعّالة) |
| `POST /api/v1/hermes/sovereignty/propose` | اقتراح عمل عبر Gate |
| `POST /api/v1/hermes/sovereignty/approvals/{id}/decide` | قرار موافقة سيادي |
| `GET  /api/v1/hermes/sovereignty/approvals/pending` | الموافقات المعلّقة |
| `GET  /api/v1/hermes/trust/agents` | Agent Registry |
| `GET  /api/v1/hermes/trust/tools` | Tool Registry |
| `POST /api/v1/hermes/trust/permissions/check` | فحص (agent, tool) |
| `GET  /api/v1/hermes/trust/audit` | ذيل audit log مع تحقّق السلسلة |
| `POST /api/v1/hermes/trust/mcp/score` | تقييم metadata لأداة MCP |

---

## 10) القواعد الحاكمة (مرئية يوميًا في الـ Console)

- كل ما يدخل Dealix يجب أن يخرج بأحد المخرجات السبعة أو يُصنّف هدراً.
- لا Agent يعمل خارج Agent Registry وTool Permissions وSovereignty Gate.
- لا execution خارجي بدون Trust Check.
- لا قرار حساس بدون مذكّرة (Decision Memo) وموافقة سامي عند المستوى المطلوب.
- لا outcome بدون asset review.
- لا public API ولا Marketplace ولا White-label بدون موافقة سيادية صريحة (S4).
- لا أرقام إيراد قبل invoice_paid، ولا upsell قبل Proof.

---

## ١١) خارطة الطريق التنفيذية

| الموجة | المسلّمات |
| --- | --- |
| **W1 (هذه)** | Sovereignty Gate + Signal Intake + Opportunity + Outcome + Asset + Console API |
| **W2** | Money Dashboard مكتمل + Revenue Hunter Pilot operationalised + Proposal Factory في UI |
| **W3** | Agent Registry + Tool Registry تُخزّن في Postgres + Approval queue على Redis |
| **W4** | Product Factory في الواجهة + Partner Scout مع pipeline + Market Radar بمصادر علنية |

> القرار التالي مفتوح لك يا سامي: أي موجة نُسرّعها؟ (الافتراض: W2 → كاش هذا الأسبوع.)
