# Payment Confirmation Checklist

## الهدف

منع التسليم المجاني وتحويل كل proposal إلى payment أو lost/nurture.

## عند موافقة العميل

نفذ:

```powershell
.\scripts\start_paid_delivery.ps1 -Client "Client Name" -Offer "ai-trust" -Amount "5000"
```

## عند تأكيد الدفع

نفذ:

```powershell
.\scripts\confirm_payment.ps1 -Client "Client Name"
```

## بعد تأكيد الدفع

1. افتح intake.
2. ابدأ delivery tracker.
3. لا تستخدم بيانات حساسة في prompt.
4. أنشئ تقرير AI Trust أو Delivery Accuracy.
5. بعد التسليم أنشئ Proof Pack.
6. بعد Proof Pack أرسل Retainer Offer.

## قاعدة CEO

لا يوجد full delivery قبل payment confirmation إلا إذا قرر سامي ذلك صراحة لسبب استراتيجي.
