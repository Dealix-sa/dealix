"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function OnboardingPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [data, setData] = useState({
    sector: "",
    company_size: "",
    phone: "",
    website: "",
  });
  const [loading, setLoading] = useState(false);

  const sectors = [
    "تقنية", "تجارة", "مقاولات", "تصنيع", "خدمات", "صحة", "تعليم", "عقارات", "نقل", "أخرى"
  ];
  const sizes = [
    { value: "1-5", label: "١–٥ موظفين" },
    { value: "6-20", label: "٦–٢٠ موظف" },
    { value: "21-50", label: "٢١–٥٠ موظف" },
    { value: "51-200", label: "٥١–٢٠٠ موظف" },
    { value: "200+", label: "٢٠٠+ موظف" },
  ];

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/v1/onboarding/wizard", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (res.ok) {
        // Get tenant from localStorage or redirect to dashboard
        const tenantId = localStorage.getItem("tenant_id") || "default";
        router.push(`/${tenantId}/dashboard`);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4" dir="rtl">
      <div className="w-full max-w-lg bg-white rounded-2xl shadow-xl p-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-xl font-bold text-slate-900">إعداد Dealix</h1>
          <div className="flex gap-1">
            {[1, 2, 3].map((s) => (
              <div
                key={s}
                className={`w-8 h-2 rounded-full ${
                  s <= step ? "bg-emerald-500" : "bg-slate-200"
                }`}
              />
            ))}
          </div>
        </div>

        {step === 1 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-slate-800">
              ما قطاع شركتك؟
            </h2>
            <div className="grid grid-cols-2 gap-3">
              {sectors.map((sector) => (
                <button
                  key={sector}
                  onClick={() => {
                    setData({ ...data, sector });
                    setStep(2);
                  }}
                  className={`p-4 border-2 rounded-xl text-center transition ${
                    data.sector === sector
                      ? "border-emerald-500 bg-emerald-50 text-emerald-700 font-semibold"
                      : "border-slate-200 hover:border-emerald-300"
                  }`}
                >
                  {sector}
                </button>
              ))}
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-slate-800">
              كم عدد موظفينك؟
            </h2>
            <div className="space-y-3">
              {sizes.map((size) => (
                <button
                  key={size.value}
                  onClick={() => {
                    setData({ ...data, company_size: size.value });
                    setStep(3);
                  }}
                  className={`w-full p-4 border-2 rounded-xl text-right transition ${
                    data.company_size === size.value
                      ? "border-emerald-500 bg-emerald-50 text-emerald-700 font-semibold"
                      : "border-slate-200 hover:border-emerald-300"
                  }`}
                >
                  {size.label}
                </button>
              ))}
            </div>
            <button
              onClick={() => setStep(1)}
              className="text-slate-500 text-sm hover:text-slate-700"
            >
              رجوع
            </button>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-slate-800">
              بيانات التواصل
            </h2>
            <input
              type="tel"
              placeholder="رقم الجوال (اختياري)"
              className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              value={data.phone}
              onChange={(e) => setData({ ...data, phone: e.target.value })}
            />
            <input
              type="url"
              placeholder="موقع الشركة (اختياري)"
              className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              value={data.website}
              onChange={(e) => setData({ ...data, website: e.target.value })}
            />
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="w-full bg-emerald-600 text-white py-3 rounded-lg font-semibold hover:bg-emerald-700 transition disabled:opacity-50"
            >
              {loading ? "جاري الحفظ..." : "إكمال الإعداد ودخول لوحة التحكم"}
            </button>
            <button
              onClick={() => setStep(2)}
              className="w-full text-slate-500 text-sm hover:text-slate-700"
            >
              رجوع
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
