"use client";

import { useState } from "react";
import WhatsAppCTA from "@/components/WhatsAppCTA";
import { CONTACT_EMAIL, mailtoLink } from "@/lib/contact";

type FormState = "idle" | "submitting" | "forwarded" | "fallback" | "error";

const BUDGET_OPTIONS = ["أقل من 10 آلاف", "10–25 ألف", "25–75 ألف", "أكثر من 75 ألف"];

// Lead capture form → POST /api/leads. When the backend isn't reachable the
// API answers 202 forwarded:false and we surface direct-contact fallbacks so
// no lead is silently lost.
export default function LeadForm() {
  const [state, setState] = useState<FormState>("idle");
  const [company, setCompany] = useState("");
  const [sector, setSector] = useState("");
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [city, setCity] = useState("");
  const [problem, setProblem] = useState("");
  const [budget, setBudget] = useState("");

  const composedMessage = [
    city && `المدينة: ${city}`,
    problem && `أكبر مشكلة الآن: ${problem}`,
    budget && `الميزانية التقريبية: ${budget}`,
  ]
    .filter(Boolean)
    .join("\n");

  const waSummary = `السلام عليكم،\nاسم الشركة: ${company}\nالقطاع: ${sector}\n${composedMessage}\nأريد أبدأ مع Dealix`;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setState("submitting");
    try {
      const res = await fetch("/api/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          company,
          sector,
          email,
          name,
          message: composedMessage,
          language_pref: "ar",
        }),
      });
      if (!res.ok) {
        setState("error");
        return;
      }
      const data = await res.json();
      setState(data.forwarded ? "forwarded" : "fallback");
    } catch {
      setState("error");
    }
  }

  if (state === "forwarded") {
    return (
      <div className="rounded-3xl border border-emerald-400/30 bg-emerald-400/[0.06] p-8 text-center">
        <p className="text-3xl">✅</p>
        <h3 className="mt-3 text-xl font-black text-emerald-300">استلمنا طلبك</h3>
        <p className="mt-2 text-sm leading-7 text-slate-300">
          نراجع المعلومات ونتواصل معك خلال 24 ساعة.
        </p>
      </div>
    );
  }

  if (state === "fallback") {
    return (
      <div className="rounded-3xl border border-amber-400/30 bg-amber-400/[0.06] p-8 text-center">
        <p className="text-3xl">📩</p>
        <h3 className="mt-3 text-xl font-black text-amber-300">استلمنا طلبك</h3>
        <p className="mt-2 text-sm leading-7 text-slate-300">
          للتأكيد الأسرع، أرسل نفس المعلومات مباشرة:
        </p>
        <div className="mt-5 flex flex-wrap justify-center gap-3">
          <WhatsAppCTA message={waSummary} fallbackSubject="طلب بدء مع Dealix" />
          <a
            href={mailtoLink("طلب بدء مع Dealix", waSummary)}
            className="rounded-2xl border border-white/20 px-6 py-3 text-sm font-bold hover:bg-white/10"
          >
            {CONTACT_EMAIL}
          </a>
        </div>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} dir="rtl" className="space-y-4 text-right">
      <div className="grid gap-4 md:grid-cols-2">
        <label className="block">
          <span className="mb-1 block text-sm font-bold text-slate-300">
            اسم الشركة <span className="text-cyan-400">*</span>
          </span>
          <input
            required
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="w-full rounded-2xl border border-white/15 bg-white/[0.04] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-400/60 focus:outline-none"
            placeholder="شركتك"
          />
        </label>
        <label className="block">
          <span className="mb-1 block text-sm font-bold text-slate-300">
            القطاع <span className="text-cyan-400">*</span>
          </span>
          <input
            required
            value={sector}
            onChange={(e) => setSector(e.target.value)}
            className="w-full rounded-2xl border border-white/15 bg-white/[0.04] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-400/60 focus:outline-none"
            placeholder="عيادات، عقار، لوجستيات..."
          />
        </label>
        <label className="block">
          <span className="mb-1 block text-sm font-bold text-slate-300">
            البريد الإلكتروني <span className="text-cyan-400">*</span>
          </span>
          <input
            required
            type="email"
            dir="ltr"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full rounded-2xl border border-white/15 bg-white/[0.04] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-400/60 focus:outline-none"
            placeholder="you@company.com"
          />
        </label>
        <label className="block">
          <span className="mb-1 block text-sm font-bold text-slate-300">الاسم</span>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full rounded-2xl border border-white/15 bg-white/[0.04] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-400/60 focus:outline-none"
            placeholder="اسمك"
          />
        </label>
        <label className="block">
          <span className="mb-1 block text-sm font-bold text-slate-300">المدينة</span>
          <input
            value={city}
            onChange={(e) => setCity(e.target.value)}
            className="w-full rounded-2xl border border-white/15 bg-white/[0.04] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-400/60 focus:outline-none"
            placeholder="الرياض، جدة..."
          />
        </label>
        <label className="block">
          <span className="mb-1 block text-sm font-bold text-slate-300">
            الميزانية التقريبية
          </span>
          <select
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
            className="w-full rounded-2xl border border-white/15 bg-white/[0.04] px-4 py-3 text-sm text-white focus:border-cyan-400/60 focus:outline-none"
          >
            <option value="" className="bg-[#06111f]">
              اختر (اختياري)
            </option>
            {BUDGET_OPTIONS.map((b) => (
              <option key={b} value={b} className="bg-[#06111f]">
                {b} ريال
              </option>
            ))}
          </select>
        </label>
      </div>
      <label className="block">
        <span className="mb-1 block text-sm font-bold text-slate-300">
          أكبر مشكلة تشغيلية الآن
        </span>
        <textarea
          value={problem}
          onChange={(e) => setProblem(e.target.value)}
          rows={3}
          className="w-full rounded-2xl border border-white/15 bg-white/[0.04] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-400/60 focus:outline-none"
          placeholder="مثال: الاستفسارات تجينا واتساب وتضيع بدون متابعة"
        />
      </label>

      {state === "error" && (
        <p className="rounded-2xl border border-red-400/30 bg-red-400/[0.06] px-4 py-3 text-sm text-red-300">
          حدث خطأ أثناء الإرسال. حاول مرة أخرى أو تواصل معنا مباشرة على {CONTACT_EMAIL}.
        </p>
      )}

      <button
        type="submit"
        disabled={state === "submitting"}
        className="w-full rounded-2xl bg-cyan-400 px-6 py-4 text-lg font-black text-[#06111f] transition-colors hover:bg-cyan-300 disabled:opacity-60"
      >
        {state === "submitting" ? "جارٍ الإرسال..." : "أرسل الطلب"}
      </button>
      <p className="text-center text-xs text-slate-500">
        لا نطلب بيانات مالية حساسة. البيانات تُستخدم فقط للتشخيص المبدئي. PDPL-compliant.
      </p>
    </form>
  );
}
