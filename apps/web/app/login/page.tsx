"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const TOKEN_KEY = "dealix_access_token";
const REFRESH_KEY = "dealix_refresh_token";
const USER_KEY = "dealix_user";

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

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const payload: Record<string, string> = {
        email: form.email,
        password: form.password,
      };
      if (form.tenant_slug) payload.tenant_slug = form.tenant_slug;
      if (mfaRequired && form.totp_code) payload.totp_code = form.totp_code;

      const res = await fetch("/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Login failed");
      }

      if (data.mfa_required) {
        setMfaRequired(true);
        setError("أدخل رمز المصادقة الثنائية (TOTP)");
        setLoading(false);
        return;
      }

      if (typeof window !== "undefined") {
        localStorage.setItem(TOKEN_KEY, JSON.stringify(data.access_token));
        localStorage.setItem(REFRESH_KEY, JSON.stringify(data.refresh_token));
        localStorage.setItem(
          USER_KEY,
          JSON.stringify({ email: form.email, tenant_slug: form.tenant_slug }),
        );
      }

      const dest = form.tenant_slug ? `/${form.tenant_slug}/dashboard` : "/dashboard";
      router.push(dest);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Login failed";
      setError(message);
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
          ادخل إلى نظام Dealix
        </p>

        <form onSubmit={handleLogin} className="space-y-4">
          <input
            type="email"
            placeholder="البريد الإلكتروني"
            required
            className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
          <input
            type="password"
            placeholder="كلمة المرور"
            required
            className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
          <input
            type="text"
            placeholder="معرّف المؤسسة (اختياري)"
            className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
            value={form.tenant_slug}
            onChange={(e) => setForm({ ...form, tenant_slug: e.target.value })}
          />
          {mfaRequired && (
            <input
              type="text"
              inputMode="numeric"
              placeholder="رمز TOTP (6 أرقام)"
              required
              className="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              value={form.totp_code}
              onChange={(e) => setForm({ ...form, totp_code: e.target.value })}
            />
          )}
          {error && <p className="text-red-500 text-sm">{error}</p>}
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
            أنشئ حسابك
          </a>
        </div>
      </div>
    </div>
  );
}