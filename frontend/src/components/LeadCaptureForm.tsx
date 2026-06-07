"use client";

import { useState } from "react";

export default function LeadCaptureForm() {
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);

  async function submit(formData: FormData) {
    setLoading(true);
    const payload = Object.fromEntries(formData.entries());
    const res = await fetch("/api/leads", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    setLoading(false);
    setSent(res.ok);
  }

  if (sent) {
    return <div className="rounded-2xl border p-6">تم استلام الطلب. سنراجع الحالة ونجهز تشخيصًا أوليًا.</div>;
  }

  return (
    <form action={submit} className="grid gap-4 rounded-3xl border p-6 bg-white/5">
      <input name="company" placeholder="اسم الشركة" required className="rounded-xl p-3 text-black" />
      <input name="name" placeholder="اسم المسؤول" className="rounded-xl p-3 text-black" />
      <input name="email" placeholder="البريد الإلكتروني" className="rounded-xl p-3 text-black" />
      <input name="phone" placeholder="رقم التواصل" className="rounded-xl p-3 text-black" />
      <input name="sector" placeholder="القطاع" className="rounded-xl p-3 text-black" />
      <textarea name="pain" placeholder="ما المشكلة التشغيلية أو البيعية التي تريد حلها؟" required className="rounded-xl p-3 text-black min-h-28" />
      <select name="budget" className="rounded-xl p-3 text-black">
        <option value="">نطاق الميزانية</option>
        <option value="pilot">Pilot / تجربة</option>
        <option value="retainer">Retainer شهري</option>
        <option value="enterprise">Enterprise / مخصص</option>
      </select>
      <button disabled={loading} className="rounded-xl bg-white text-black p-3 font-bold">
        {loading ? "جارٍ الإرسال..." : "اطلب تشخيص Dealix"}
      </button>
    </form>
  );
}
