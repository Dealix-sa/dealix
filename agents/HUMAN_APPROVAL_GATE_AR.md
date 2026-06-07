# Human Approval Gate

## متى يجب التوقف للموافقة؟
- قبل أي رسالة خارجية.
- قبل إنشاء invoice أو عرض سعر رسمي.
- قبل تغيير stage إلى Won/Lost.
- قبل إدخال بيانات شخصية في demo أو case study.
- قبل تنفيذ integration يمس بيانات العميل.

## صيغة الموافقة
كل output حساس يجب أن يحتوي:
- Risk level: low/medium/high
- Source data used
- Recommended action
- Human decision: approved/rejected/needs edit
- Approver name/date

## سياسة الافتراض الآمن
إذا شك الوكيل، يصنف العمل `needs_human_review`.
