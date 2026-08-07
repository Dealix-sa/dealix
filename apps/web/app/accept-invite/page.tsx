"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import {
  apiUrl,
  parseApiError,
  persistSession,
  type DealixSessionTokens,
} from "../../lib/runtime-api";

function decodeInviteEmail(token: string): string {
  const payloadPart = token.split(".")[1];
  if (!payloadPart) return "";

  try {
    const normalized = payloadPart.replace(/-/g, "+").replace(/_/g, "/");
    const padded = normalized.padEnd(Math.ceil(normalized.length / 4) * 4, "=");
    const payload = JSON.parse(atob(padded));
    return typeof payload?.sub === "string" ? payload.sub.trim().toLowerCase() : "";
  } catch {
    return "";
  }
}

export default function AcceptInvitePage() {
  const router = useRouter();
  const [token, setToken] = useState("");
  const [form, setForm] = useState({ name: "", password: "", confirmPassword: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const inviteToken = new URLSearchParams(window.location.search).get("token")?.trim() || "";
    setToken(inviteToken);
    if (!inviteToken) {
      setError("رابط الدعوة غير مكتمل أو لا يحتوي رمزًا صالحًا.");
      return;
    }

    // Keep the single-use token in memory only; remove it from browser history
    // before the user submits the form or follows another link.
    window.history.replaceState({}, document.title, "/accept-invite");
  }, []);

  const handleAccept = async (event: React.FormEvent) => {
    event.preventDefault();
    setError("");

    if (!token) {
      setError("افتح رابط الدعوة الأصلي مرة أخرى.");
      return;
    }
    if (form.password !== form.confirmPassword) {
      setError("كلمتا المرور غير متطابقتين.");
      return;
    }

    const email = decodeInviteEmail(token);
    if (!email) {
      setError("رمز الدعوة غير صالح.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(apiUrl("/api/v1/auth/invite/accept"), {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          token,
          name: form.name.trim(),
          password: form.password,
        }),
        cache: "no-store",
      });

      if (!response.ok) throw new Error(await parseApiError(response));

      const tokens: DealixSessionTokens = await response.json();
      if (!tokens.access_token || !tokens.refresh_token) {
        throw new Error("تم قبول الدعوة لكن تعذر إنشاء جلسة الدخول.");
      }

      persistSession(tokens, { email });
      router.replace("/dashboard");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "تعذر قبول الدعوة");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4" dir="rtl">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl">
        <h1 className="mb-2 text-center text-3xl font-bold text-slate-900">قبول دعوة Dealix</h1>
        <p className="mb-8 text-center text-slate-500">
          أنشئ بيانات دخولك للانضمام إلى مساحة العمل المدعوة.
        </p>

        <form onSubmit={handleAccept} className="space-y-4">
          <input
            type="text"
            placeholder="الاسم الكامل"
            required
            minLength={2}
            autoComplete="name"
            className="w-full rounded-lg border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            value={form.name}
            onChange={(event) => setForm({ ...form, name: event.target.value })}
          />
          <input
            type="password"
            placeholder="كلمة المرور الجديدة"
            required
            minLength={8}
            autoComplete="new-password"
            className="w-full rounded-lg border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            value={form.password}
            onChange={(event) => setForm({ ...form, password: event.target.value })}
          />
          <input
            type="password"
            placeholder="تأكيد كلمة المرور"
            required
            minLength={8}
            autoComplete="new-password"
            className="w-full rounded-lg border border-slate-200 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            value={form.confirmPassword}
            onChange={(event) => setForm({ ...form, confirmPassword: event.target.value })}
          />

          {error && (
            <p className="text-sm text-red-600" role="alert">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading || !token}
            className="w-full rounded-lg bg-emerald-600 py-3 font-semibold text-white transition hover:bg-emerald-700 disabled:opacity-50"
          >
            {loading ? "جاري قبول الدعوة..." : "قبول الدعوة والدخول"}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-slate-500">
          لديك حساب بالفعل؟{" "}
          <a href="/login" className="font-semibold text-emerald-600 hover:text-emerald-700">
            تسجيل الدخول
          </a>
        </div>
      </div>
    </div>
  );
}
