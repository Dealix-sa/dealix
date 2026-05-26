# 🏢 دليل تشغيل منظومة ديلكس المحلية (Operating Manual)

دليل التشغيل اليومي الكامل الموجه لمشغل المنظومة (Sami Assiri) لإدارة حركة السوق وحوكمة مخرجات الذكاء الاصطناعي بنجاح.

---

## 1. الدورة التشغيلية اليومية (Daily Operating Cycle)
كل صباح، يتم تفعيل الآلة التشغيلية عبر الخطوات التالية:

### الخطوة 1: فحص الجاهزية والاستقرار برمجياً:
```powershell
.\scripts\dealix-launch-mode.ps1
```
يتحقق الأمر من وجود السجلات الخمسة واجتياز الفحوصات الأمنية والتراجعية.

### الخطوة 2: استعراض المهام اليومية وقائمة العملاء وتجهيز الملفات:
```powershell
.\scripts\dealix-operator-day.ps1
```
يعرض التقرير اليومي، ويقترح الإجراء المباشر التالي، ويفتح تلقائياً مجلدات العمل لإرسال الرسائل المجهزة يدوياً ومتابعة العملاء.

---

## 2. إدارة مبيعات المخرجات التجارية والتحصيل المالي
* **إطلاق تواصل أولى لعميل جديد:**
  ```powershell
  py -3 scripts/mark_lead.py "اسم العميل" outreach_sent "First outbound message sent"
  ```
* **تلقي رد وتصنيفه ومعرفة الرد الأنسب:**
  ```powershell
  py -3 scripts/triage_reply.py "أهلاً سامي، مهتم ونريد معرفة الأسعار"
  ```
* **حجز جلسة اكتشاف وتجهيز الأسئلة:**
  ```powershell
  py -3 scripts/new_discovery_call.py "اسم العميل"
  ```
* **صياغة مقترح سعر فني تجاري مخصص ومحكوم:**
  ```powershell
  py -3 scripts/proposal_from_lead.py "اسم العميل"
  ```
* **إرسال طلب التحصيل المالي:**
  ```powershell
  powershell -File scripts/start_paid_delivery.ps1 -Client "اسم العميل" -Offer "ai-trust" -Amount "5000"
  ```
* **تأكيد استلام الدفعة وإطلاق التشغيل:**
  ```powershell
  powershell -File scripts/confirm_payment.ps1 -Client "اسم العميل"
  ```
* **تسليم المخرجات وإغلاق الصفقة وصياغة حزمة الإثبات:**
  ```powershell
  powershell -File scripts/complete_delivery.ps1 -Client "اسم العميل" -Offer "ai-trust"
  ```

---

## 3. حماية البيانات والحوكمة النشطة
* **فحص سلامة وجدة أي نصوص تسويقية:**
  ```powershell
  py -3 dealix.py governance-check --text "نص الرسالة المقترحة"
  ```
* **تأمين البيانات والنسخ الاحتياطي قبل أي إجراء تشغيلي واسع:**
  ```powershell
  py -3 scripts/runtime_snapshot.py
  ```
