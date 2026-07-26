"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import {
  apiUrl,
  parseApiError,
  persistSession,
  type DealixSessionTokens,
} from "../../lib/runtime-api";

interface SelfServePlan {
  slug: string;
  name_ar: string;
  name_en: string;
  price_sar_monthly: number;
  price_sar_yearly: number | null;
  max_users: number;
  max_leads_per_month: number;
  features: Record<string, boolean>;
}

interface SignupResult {
  tenant_id: string;
  tenant_slug: string;
  user_id: string;
  subscription_id: string;
  plan_slug: string;
}

export default function SignupPage() {
  const router = useRouter();
  const [step, setStep] = useState<"form" | "plan" | "success">("form");
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    company_name: "",
  });
  const [plans, setPlans] = useState<SelfServePlan[]>([]);
  const [selectedPlan, setSelectedPlan] = useState("free");
  const [loadingPlans, setLoadingPlans] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [createdTenant, setCreatedTenant] = useState("");

  useEffect(() => {
    let active = true;
    const loadPlans = async () => {
      try {
        const response = await fetch(apiUrl("/api/v1/onboarding/plans"), {
          headers: { Accept: "application/json" },
          cache: "no-store",
        });
        if (!response.ok) throw new Error(await parseApiError(response));
        const payload = await response.json();
        const availablePlans = Array.isArray(payload.plans) ? payload.plans : [];
        if (!active) return;
        setPlans(availablePlans);
        if (availablePlans.length > 0) {
          setSelectedPlan(
            availablePlans.some((plan: SelfServePlan) => plan.slug === "free")
              ? "free"
              : availablePlans[0].slug,
          );
        }
      } catch (err: unknown) {
        if (!active) return;
        setError(err instanceof Error ? err.message : "تعذر تحميل الخطط");
      } finally {
        if (active) setLoadingPlans(false);
      }
    };
    void loadPlans();
    return () => {
      active = false;
    };
  }, []);

  const selected = useMemo(
    () => plans.find((plan) => plan.slug === selectedPlan),
    [plans, selectedPlan],
  );

  const handleFormSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (!form.name || !form.email || !form.password || !form.company_name) {
      setError("جميع الحقول مطلوبة");
      return;
    }
    if (form.password.length < 8) {
      setError("كلمة المرور يجب ألا تقل عن 8 أحرف");
      return;
    }
    if (plans.length === 0) {
      setError("لا توجد خطط تسجيل ذاتي متاحة حاليًا");
      return;
    }
    setError("");
    setStep("plan");
  };

  const handleSignup = async () => {
    if (!selected) {
      setError("اختر خطة متاحة");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const signupResponse = await fetch(apiUrl("/api/v1/onboarding/signup"), {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          ...form,
          plan_slug: selected.slug,
          billing_cycle: "monthly",
        }),
      });
      if (!signupResponse.ok) {
        throw new Error(await parseApiError(signupResponse));
      }
      const signup: SignupResult = await signupResponse.json();

      // Establish the canonical JWT session immediately after account creation.
      const loginResponse = await fetch(apiUrl("/api/v1/auth/login"), {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          email: form.email,
          password: form.password,
          tenant_slug: signup.tenant_slug,
        }),
      });
      if (!loginResponse.ok) {
        throw new Error(await parseApiError(loginResponse));
      }
      const tokens: DealixSessionTokens = await loginResponse.json();
      persistSession(tokens, {
        email: form.email.trim().toLowerCase(),
        tenant_slug: signup.tenant_slug,
      });

      setCreatedTenant(signup.tenant_slug);
      setStep("success");
      window.setTimeout(() => {
        router.replace(`/${encodeURIComponent(signup.tenant_slug)}/dashboard`);
      }, 1200);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "تعذر إنشاء الحساب");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4" dir="rtl">
      <div className="w-full max-w-lg bg-white rounded-2xl shadow-xl p-8">
        {step === "form" && (
          <>
            <h1 className="text-3xl font-bold text-slate-900 mb-2 text-center">
              ابدأ مع Dealix
            </h1>
            <p className="text-slate-500 text-center mb-8">
              نظام تشغيل ذكي للشركات السعودية — يعمل فوق أدواتك الحالية
            </p>
            <form onSubmit={handleFormSubmit} className="space-y-4">
              <input
                type="text"
                placeholder="الاسم الكامل"
                required
                autoComplete="name"
                className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                value={form.name}
                onChange={(event) => setForm({ ...form, name: event.target.value })}
              />
              <input
                type="email"
                placeholder="البريد الإلكتروني"
                required
                autoComplete="email"
                className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                value={form.email}
                onChange={(event) => setForm({ ...form, email: event.target.value })}
              />
              <input
                type="password"
                placeholder="كلمة المرور — 8 أحرف على الأقل"
                required
                minLength={8}
                autoComplete="new-password"
                className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                value={form.password}
                onChange={(event) => setForm({ ...form, password: event.target.value })}
              />
              <input
                type="text"
                placeholder="اسم الشركة"
                required
                autoComplete="organization"
                className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
                value={form.company_name}
                onChange={(event) => setForm({ ...form, company_name: event.target.value })}
              />
              {error && <p className="text-red-600 text-sm" role="alert">{error}</p>}
              <button
                type="submit"
                disabled={loadingPlans || plans.length === 0}
                className="w-full bg-emerald-600 text-white py-3 rounded-lg font-semibold hover:bg-emerald-700 transition disabled:opacity-50"
              >
                {loadingPlans ? "جاري تحميل الخطط..." : "التالي — اختيار الخطة"}
              </button>
            </form>
          </>
        )}

        {step === "plan" && (
          <>
            <h2 className="text-2xl font-bold text-slate-900 mb-2 text-center">
              اختر خطتك
            </h2>
            <p className="text-sm text-slate-500 text-center mb-6">
              الأسعار والحدود أدناه محمّلة مباشرة من نظام الاشتراكات.
            </p>
            <div className="space-y-3 mb-6">
              {plans.map((plan) => (
                <button
                  type="button"
                  key={plan.slug}
                  onClick={() => setSelectedPlan(plan.slug)}
                  className={`w-full text-right p-4 border-2 rounded-xl cursor-pointer transition ${
                    selectedPlan === plan.slug
                      ? "border-emerald-500 bg-emerald-50"
                      : "border-slate-200 hover:border-emerald-300"
                  }`}
                >
                  <div className="flex justify-between items-center gap-4">
                    <div>
                      <p className="font-bold text-slate-900">
                        {plan.name_ar} <span className="text-xs font-normal text-slate-400">{plan.name_en}</span>
                      </p>
                      <p className="text-sm text-slate-500">
                        حتى {plan.max_users} مستخدم · {plan.max_leads_per_month.toLocaleString("ar-SA")} عميل محتمل شهريًا
                      </p>
                    </div>
                    <div className="text-left shrink-0">
                      <p className="text-xl font-bold text-emerald-600">
                        {plan.price_sar_monthly.toLocaleString("ar-SA")} ر.س
                      </p>
                      <p className="text-xs text-slate-400">/شهر</p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
            {error && <p className="text-red-600 text-sm mb-4" role="alert">{error}</p>}
            <button
              type="button"
              onClick={() => void handleSignup()}
              disabled={loading || !selected}
              className="w-full bg-emerald-600 text-white py-3 rounded-lg font-semibold hover:bg-emerald-700 transition disabled:opacity-50"
            >
              {loading ? "جاري إنشاء مساحة العمل..." : "إنشاء الحساب ومساحة العمل"}
            </button>
            <button
              type="button"
              onClick={() => setStep("form")}
              disabled={loading}
              className="w-full mt-3 text-slate-500 text-sm hover:text-slate-700"
            >
              رجوع
            </button>
          </>
        )}

        {step === "success" && (
          <div className="text-center py-8">
            <div className="text-5xl mb-4" aria-hidden="true">✓</div>
            <h2 className="text-2xl font-bold text-slate-900 mb-2">
              تم إنشاء مساحة العمل بنجاح
            </h2>
            <p className="text-slate-500">
              تم تسجيل الدخول، وجارٍ فتح لوحة {createdTenant || "الشركة"}...
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
