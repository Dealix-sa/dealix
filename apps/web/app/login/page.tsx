"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import {
  apiUrl,
  parseApiError,
  persistSession,
  type DealixSessionTokens,
} from "../../lib/runtime-api";

export default function LoginPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    email: "",
    password: "",
    tenant_slug: "",
    totp_code: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [mfaRequired, setMfaRequired] = useState(false);

  const handleLogin = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const payload: Record<string, string> = {
        email: form.email.trim().toLowerCase(),
        password: form.password,
      };
      if (form.tenant_slug.trim()) payload.tenant_slug = form.tenant_slug.trim();
      if (mfaRequired && form.totp_code.trim()) payload.totp_code = form.totp_code.trim();

      const response = await fetch(apiUrl("/api/v1/auth/login"), {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(await parseApiError(response));
      }
      const data: DealixSessionTokens & { mfa_required?: boolean } = await response.json();

      if (data.mfa_required) {
        setMfaRequired(true);
        setError("أدخل رمز المصادقة الثنائية (TOTP)");
        return;
      }

      persistSession(data, {
        email: form.email.trim().toLowerCase(),
        tenant_slug: form.tenant_slug.trim() || undefined,
      });

      const destination = form.tenant_slug.trim()
        ? `/${encodeURIComponent(form.tenant_slug.trim())}/dashboard`
        : "/dashboard";
      router.replace(destination);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "تعذر تسجيل الدخول");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4" dir="rtl">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2 text-center">
          تسجيل الدخول
        </h1>
        <p className="text-slate-500 text-center mb-8">
          ادخل إلى نظام تشغيل شركتك في Dealix
        </p>

        <form onSubmit={handleLogin} className="space-y-4">
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
            placeholder="كلمة المرور"
            required
            autoComplete="current-password"
            className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
            value={form.password}
            onChange={(event) => setForm({ ...form, password: event.target.value })}
          />
          <input
            type="text"
            placeholder="معرّف المؤسسة (اختياري)"
            autoComplete="organization"
            className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
            value={form.tenant_slug}
            onChange={(event) => setForm({ ...form, tenant_slug: event.target.value })}
          />
          {mfaRequired && (
            <input
              type="text"
              inputMode="numeric"
              placeholder="رمز TOTP (6 أرقام)"
              required
              autoComplete="one-time-code"
              className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              value={form.totp_code}
              onChange={(event) => setForm({ ...form, totp_code: event.target.value })}
            />
          )}
          {error && <p className="text-red-600 text-sm" role="alert">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-emerald-600 text-white py-3 rounded-lg font-semibold hover:bg-emerald-700 transition disabled:opacity-50"
          >
            {loading ? "جاري الدخول..." : "تسجيل الدخول"}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-slate-500">
          ليس لديك حساب؟{" "}
          <a href="/signup" className="text-emerald-600 hover:text-emerald-700 font-semibold">
            أنشئ مساحة عمل
          </a>
        </div>
      </div>
    </div>
  );
}
