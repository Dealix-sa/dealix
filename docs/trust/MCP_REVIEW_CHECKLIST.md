# Dealix — MCP Server Review Checklist — قائمة مراجعة خوادم MCP

> 25-item checklist applied before any MCP server is connected to a Dealix agent. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## العربية

### الغرض
كل خادم MCP يُربط بمنصّة Dealix يجب أن يجتاز هذه القائمة قبل التشغيل. لا يُعتمد خادم بدون توقيع المُراجِع وتاريخ المراجعة.

### المراجعة (25 بندًا)

**الهوية والملكية**
1. اسم الخادم ومالكه البشري موثّقان.
2. المستودع المصدري معروف وموثّق الإصدار.
3. مفتاح التوقيع الرقمي مُتحقَّق منه.

**النطاق والقدرات**
4. قائمة الأدوات (tools) المُعلَنة كاملة.
5. كل أداة موصوفة بـ inputs/outputs دون غموض.
6. لا أداة تنفّذ shell أو eval ديناميكي.
7. لا أداة تكتب إلى نظام ملفات خارج sandbox.

**البيانات**
8. مصادر البيانات التي يصل إليها الخادم محصورة ومُعلَنة.
9. لا يُرسل بيانات لطرف ثالث دون موافقة.
10. لا يُسجّل PII في السجلات الافتراضية.
11. سياسة الاحتفاظ مُعلَنة وتطابق [DATA_BOUNDARIES_SAMPLE.md](DATA_BOUNDARIES_SAMPLE.md).

**الأمن**
12. مصادقة الخادم تستخدم مفاتيح ذات أعمار قصيرة.
13. النقل بـ TLS فقط.
14. لا حقن (injection) ممكن في معاملات الأدوات.
15. سرّيات (secrets) العميل لا تظهر في الردود.

**الحوكمة**
16. الخادم مُسجَّل في [AGENT_REGISTRY_SAMPLE.md](AGENT_REGISTRY_SAMPLE.md) كأداة، لا كوكيل مستقل.
17. كل أداة لها خانة في [TOOL_PERMISSION_MATRIX_SAMPLE.md](TOOL_PERMISSION_MATRIX_SAMPLE.md).
18. الإجراءات الحساسة محدّدة كـ `approval_required` بشكل افتراضي.

**التدقيق**
19. كل استدعاء يُسجَّل في AI Run Ledger.
20. context_hash مُحتسَب لكل تشغيل.
21. لا قدرة على «الاختفاء» — كل خطأ مُسجَّل.

**الاستجابة للحوادث**
22. آلية وقف فوري (kill-switch) موثّقة.
23. قناة إبلاغ عن ثغرات مُعلَنة.
24. خطّة rollback إلى إصدار سابق متاحة.

**التوقيع**
25. المراجِع المُسمّى ووقت المراجعة مكتوبان أدناه.

### نموذج توقيع
- اسم الخادم: `{{ mcp_server_name }}`
- إصدار: `{{ version }}`
- المراجِع: `{{ reviewer }}`
- تاريخ: `{{ date }}`
- النتيجة: `pass | conditional | fail`
- ملاحظات: `{{ notes }}`

---

## English

### Purpose
Every MCP server connected to Dealix must pass this 25-item review before going live. No server is approved without reviewer signature and date.

### The 25 Items

**Identity and Ownership**
1. Server name and named human owner documented.
2. Source repository known and version-pinned.
3. Digital signing key verified.

**Scope and Capabilities**
4. Full list of declared tools is complete.
5. Each tool has unambiguous inputs/outputs.
6. No tool performs shell or dynamic eval.
7. No tool writes outside the sandbox filesystem.

**Data**
8. Server data sources are scoped and declared.
9. No third-party data transmission without consent.
10. No PII in default logs.
11. Retention policy declared and matches [DATA_BOUNDARIES_SAMPLE.md](DATA_BOUNDARIES_SAMPLE.md).

**Security**
12. Server authentication uses short-lived keys.
13. Transport TLS only.
14. No injection possible in tool parameters.
15. Customer secrets do not appear in responses.

**Governance**
16. Server registered in [AGENT_REGISTRY_SAMPLE.md](AGENT_REGISTRY_SAMPLE.md) as a tool, not an autonomous agent.
17. Every tool has a row in [TOOL_PERMISSION_MATRIX_SAMPLE.md](TOOL_PERMISSION_MATRIX_SAMPLE.md).
18. Sensitive operations default to `approval_required`.

**Audit**
19. Every call logged in AI Run Ledger.
20. context_hash computed per run.
21. No silent failure — every error logged.

**Incident Response**
22. Kill-switch mechanism documented.
23. Vulnerability disclosure channel published.
24. Rollback to previous version available.

**Signature**
25. Named reviewer and review date recorded below.

### Signature Block
- Server name: `{{ mcp_server_name }}`
- Version: `{{ version }}`
- Reviewer: `{{ reviewer }}`
- Date: `{{ date }}`
- Result: `pass | conditional | fail`
- Notes: `{{ notes }}`

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
