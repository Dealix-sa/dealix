# No Fake Claims Policy

سياسة منع الادعاءات المضلِّلة والمضمونة

## الغرض

منع نشر أي ادعاءات مضمونة أو مزيّفة أو مضلِّلة في المحتوى
الصادر عن المنصة، سواء في التواصل الخارجي أو المحتوى العام أو
دراسات الحالة أو صفحات الهبوط.

## القاعدة الأساسية

> **لا ادعاء بنتيجة مضمونة.** لا نضمن مبيعات، عائد استثمار، أرباح،
> نتائج محددة، أو أرقاماً مخترعة. كل ادعاء برقم يجب أن يستند إلى
> دليل موثّق في Proof Ledger.

## الادعاءات الممنوعة

### 1. الادعاءات المضمونة

- "نتائج مضمونة"
- "عائد مضمون"
- "نضمن لك مبيعات"
- "نضمن لكم"
- "نضمن النتائج"
- "مضمون"
- "100% guaranteed"
- "risk-free"
- "promise 10x"
- "guaranteed ROI"

**التنفيذ**: `auto_client_acquisition/governance_os/draft_gate.py`
يفحص هذه الأنماط عبر `audit_draft_text()`.

### 2. الإثبات المزيّف

- شهادات مختلقة
- أرقام مخترعة
- إحصاءات بدون مصدر
- "fake proof"، "fake testimonial"

### 3. موضوعات مضلِّلة

- `Re:` أو `Fwd:` في إيميل بارد لمحاكاة رد سابق.

### 4. إشارات غير مصرّح بها

- استخدام اسم أو شعار عميل دون إذن موثّق.
- ادعاء شراكة غير موجودة.

## التطبيق التقني

### فحص المسودة (Draft Gate)

```python
from auto_client_acquisition.governance_os.draft_gate import audit_draft_text

issues = audit_draft_text(draft_text)
# أي issue يبدأ بـ "forbidden_claim:" → BLOCK
```

### فحص سلامة الادعاء

```python
from auto_client_acquisition.governance_os.claim_safety import audit_claim_safety

result = audit_claim_safety(text)
if result.suggested_decision == GovernanceDecision.BLOCK:
    # منع النشر
```

### فحص صفحات الهبوط

`tests/test_landing_forbidden_claims.py` يفحص صفحات الهبوط ضد
الادعاءات الممنوعة.

## الاختبارات ذات الصلة

- `tests/test_no_fake_claims.py`
- `tests/test_no_guaranteed_claims.py`
- `tests/test_v7_no_guaranteed_claims.py`
- `tests/test_v7_no_fake_proof.py`
- `tests/test_landing_forbidden_claims.py`
- `tests/test_commercial_claim_safety.py`
- `tests/test_outbound_safety_gates.py`

## الإجراء عند الكشف

1. **حظر النشر/الإرسال** فوراً.
2. **إعادة المسودة** للمراجعة مع توضيح الادعاء الممنوع.
3. **تسجيل** في سجل المراجعة.
4. إذا تكرر من نفس المصدر، **تصعيد** للمؤسس.

## المصادقة

- **المسؤول**: فريق الامتثال + المراجِعون
- **المراجعة**: ربع سنوي أو عند إضافة نمط ادعاء جديد
- **المراجع**: `AI_USAGE_POLICY_AR.md`،
  `auto_client_acquisition/governance_os/draft_gate.py`