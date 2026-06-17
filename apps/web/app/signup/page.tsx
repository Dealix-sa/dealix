"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function SignupPage() {
  const router = useRouter();
  const [step, setStep] = useState<"form" | "plan" | "success">("form");
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    company_name: "",
  });
  const [selectedPlan, setSelectedPlan] = useState("starter");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.name || !form.email || !form.password || !form.company_name) {
      setError("All fields are required");
      return;
    }
    setError("");
    setStep("plan");
  };

  const handleSignup = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/v1/onboarding/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          plan_slug: selectedPlan,
          billing_cycle: "monthly",
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Signup failed");
      }
      setStep("success");
      setTimeout(() => {
        router.push(`/${data.tenant_id}/dashboard`);
      }, 2000);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const plans = [
    { id: "free", name: "مجاني", nameEn: "Free", price: "0", desc: "CRM فقط — للتجربة" },
    { id: "starter", name: "بداية", nameEn: "Starter", price: "199", desc: "CRM + Projects + Support" },
    { id: "growth", name: "نمو", nameEn: "Growth", price: "599", desc: "كل الوحدات ما عدا Enterprise" },
    { id: "scale", name: "توسع", nameEn: "Scale", price: "1,499", desc: "كل شي + API + Reports" },
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4" dir="rtl">
      <div className="w-full max-w-lg bg-white rounded-2xl shadow-xl p-8">
        {step === "form" && (
          <>
            <h1 className="text-3xl font-bold text-slate-900 mb-2 text-center">
              ابدأ مع Dealix
            </h1>
            <p className="text-slate-500 text-center mb-8">
              نظام التشغيل الرقمي للشركة السعودية
            </p>
            <form onSubmit={handleFormSubmit} className="space-y-4">
              <input
                type="text"
                placeholder="الاسم الكامل"
                className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
              />
              <input
                type="email"
                placeholder="البريد الإلكتروني"
                className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
              />
              <input
                type="password"
                placeholder="كلمة المرور"
                className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
              />
              <input
                type="text"
                placeholder="اسم الشركة"
                className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                value={form.company_name}
                onChange={(e) => setForm({ ...form, company_name: e.target.value })}
              />
              {error && <p className="text-red-500 text-sm">{error}</p>}
              <button
                type="submit"
                className="w-full bg-emerald-600 text-white py-3 rounded-lg font-semibold hover:bg-emerald-700 transition"
              >
                التالي — اختيار الخطة
              </button>
            </form>
          </>
        )}

        {step === "plan" && (
          <>
            <h2 className="text-2xl font-bold text-slate-900 mb-6 text-center">
              اختر خطتك
            </h2>
            <div className="space-y-3 mb-6">
              {plans.map((plan) => (
                <div
                  key={plan.id}
                  onClick={() => setSelectedPlan(plan.id)}
                  className={`p-4 border-2 rounded-xl cursor-pointer transition ${
                    selectedPlan === plan.id
                      ? "border-emerald-500 bg-emerald-50"
                      : "border-slate-200 hover:border-emerald-300"
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <p className="font-bold text-slate-900">{plan.name}</p>
                      <p className="text-sm text-slate-500">{plan.desc}</p>
                    </div>
                    <div className="text-left">
                      <p className="text-xl font-bold text-emerald-600">
                        {plan.price} ر.س
                      </p>
                      <p className="text-xs text-slate-400">/شهر</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
            <button
              onClick={handleSignup}
              disabled={loading}
              className="w-full bg-emerald-600 text-white py-3 rounded-lg font-semibold hover:bg-emerald-700 transition disabled:opacity-50"
            >
              {loading ? "جاري إنشاء الحساب..." : "إنشاء الحساب وبدء التجربة المجانية"}
            </button>
            <button
              onClick={() => setStep("form")}
              className="w-full mt-3 text-slate-500 text-sm hover:text-slate-700"
            >
              رجوع
            </button>
          </>
        )}

        {step === "success" && (
          <div className="text-center py-8">
            <div className="text-6xl mb-4">🎉</div>
            <h2 className="text-2xl font-bold text-slate-900 mb-2">
              تم إنشاء حسابك بنجاح!
            </h2>
            <p className="text-slate-500">
              جاري التوجيه إلى لوحة التحكم...
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
