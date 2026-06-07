"use client";

import { useState } from "react";
import { SECTORS } from "../lib/offerings";

/**
 * Custom AI request form — approval-first.
 *
 * Submits to the GOVERNED intake endpoint (`/api/v1/leads`) which runs
 * intake → ICP → qualification → booking. It NEVER auto-sends anything
 * externally. If the API base is not configured or the request fails, the
 * form degrades gracefully to a pre-filled mailto so a real request is never
 * lost. No data is scraped; the customer enters their own details.
 */

type Locale = "ar" | "en";
type State = "idle" | "submitting" | "success" | "fallback";

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "";
const CONTACT_EMAIL = "hello@dealix.me";

const BUDGET_BANDS: { value: string; estimate: number; ar: string; en: string }[] = [
  { value: "diagnostic", estimate: 499, ar: "تشخيص / سبرنت (٤٩٩ – ١٥٠٠ ريال)", en: "Diagnostic / Sprint (499 – 1,500 SAR)" },
  { value: "command_sprint", estimate: 7500, ar: "Command Sprint (٧٥٠٠ – ١٥٠٠٠ ريال)", en: "Command Sprint (7,500 – 15,000 SAR)" },
  { value: "monthly", estimate: 2999, ar: "تشغيل شهري (٢٩٩٩ – ٧٥٠٠ ريال/شهر)", en: "Monthly ops (2,999 – 7,500 SAR/mo)" },
  { value: "custom", estimate: 0, ar: "غير محدّد بعد", en: "Not sure yet" },
];

const COPY = {
  ar: {
    name: "الاسم",
    company: "الشركة",
    email: "البريد الإلكتروني",
    phone: "الجوال (اختياري)",
    sector: "القطاع",
    city: "المدينة",
    need: "وش تبي نسوّي؟ اوصف التحدّي أو ما تريد بناءه",
    needPlaceholder: "مثال: عندنا leads كثيرة بدون متابعة منظمة، ونبي نظام يرتّب الأولويات ويكتب المسودات وأنا أوافق وأرسل…",
    budget: "الميزانية التقريبية",
    timeline: "الإطار الزمني",
    timelineOptions: ["في أقرب وقت", "خلال شهر", "خلال ربع السنة", "أستكشف فقط"],
    submit: "أرسل الطلب",
    submitting: "جارٍ الإرسال…",
    successTitle: "وصلنا طلبك ✓",
    successBody:
      "راح نراجعه ونتواصل معك. لا يتم إرسال أو تنفيذ أي شيء خارجي بدون موافقتك — approval-first.",
    fallbackTitle: "خطوة أخيرة",
    fallbackBody: "اضغط الزر لإرسال طلبك عبر البريد مباشرة (جهّزناه لك كاملاً):",
    fallbackBtn: "أرسل عبر البريد",
    required: "هذا الحقل مطلوب",
    selectOne: "اختر…",
    approval: "approval-first · لا إرسال آلي · لا scraping · بياناتك تبقى لك",
  },
  en: {
    name: "Name",
    company: "Company",
    email: "Email",
    phone: "Phone (optional)",
    sector: "Sector",
    city: "City",
    need: "What do you want us to build? Describe the challenge.",
    needPlaceholder: "e.g. We have many leads but no organised follow-up. We want a system that prioritises, drafts the messages, and I approve & send…",
    budget: "Approximate budget",
    timeline: "Timeline",
    timelineOptions: ["As soon as possible", "Within a month", "This quarter", "Just exploring"],
    submit: "Send request",
    submitting: "Sending…",
    successTitle: "Request received ✓",
    successBody:
      "We'll review it and reach out. Nothing is sent or executed externally without your approval — approval-first.",
    fallbackTitle: "One last step",
    fallbackBody: "Tap to send your request by email directly (we pre-filled it for you):",
    fallbackBtn: "Send by email",
    required: "This field is required",
    selectOne: "Select…",
    approval: "approval-first · no auto-send · no scraping · your data stays yours",
  },
};

export default function CustomRequestForm({ locale = "ar" }: { locale?: Locale }) {
  const t = COPY[locale];
  const rtl = locale === "ar";
  const [state, setState] = useState<State>("idle");
  const [mailto, setMailto] = useState<string>("");

  function buildSummary(form: HTMLFormElement): {
    payload: Record<string, unknown>;
    mailtoHref: string;
  } {
    const data = new FormData(form);
    const get = (k: string) => String(data.get(k) ?? "").trim();
    const band = BUDGET_BANDS.find((b) => b.value === get("budget"));
    const message = [
      `[Custom AI request — dealix.me/${locale === "ar" ? "ar/" : ""}custom]`,
      `Need: ${get("need")}`,
      `Budget band: ${band ? band.en : get("budget")}`,
      `Timeline: ${get("timeline")}`,
    ].join("\n");

    const payload = {
      company: get("company"),
      name: get("name"),
      email: get("email"),
      phone: get("phone"),
      sector: get("sector"),
      region: get("city") || "Saudi Arabia",
      budget: band?.estimate ?? 0,
      message,
      source: "web.custom",
    };

    const subject = `Custom AI request — ${get("company") || get("name")}`;
    const body = [
      `Name: ${get("name")}`,
      `Company: ${get("company")}`,
      `Email: ${get("email")}`,
      `Phone: ${get("phone")}`,
      `Sector: ${get("sector")}  City: ${get("city")}`,
      ``,
      message,
    ].join("\n");
    const mailtoHref = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(
      subject,
    )}&body=${encodeURIComponent(body)}`;

    return { payload, mailtoHref };
  }

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const { payload, mailtoHref } = buildSummary(form);
    setMailto(mailtoHref);

    // No backend configured → go straight to the email fallback.
    if (!API_BASE) {
      setState("fallback");
      return;
    }

    setState("submitting");
    try {
      const res = await fetch(`${API_BASE}/api/v1/leads`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      setState(res.ok ? "success" : "fallback");
    } catch {
      setState("fallback");
    }
  }

  if (state === "success" || state === "fallback") {
    const done = state === "success";
    return (
      <div
        dir={rtl ? "rtl" : "ltr"}
        className="rounded-3xl border border-emerald-400/30 bg-emerald-400/5 p-8 text-center"
      >
        <p className="text-2xl font-black text-emerald-300">
          {done ? t.successTitle : t.fallbackTitle}
        </p>
        <p className="mx-auto mt-3 max-w-md text-sm leading-7 text-slate-300">
          {done ? t.successBody : t.fallbackBody}
        </p>
        {!done && (
          <a
            href={mailto}
            className="mt-6 inline-block rounded-2xl bg-emerald-400 px-8 py-3 font-black text-[#06111f] hover:bg-emerald-300"
          >
            {t.fallbackBtn}
          </a>
        )}
      </div>
    );
  }

  const field =
    "w-full rounded-xl border border-white/10 bg-white/[0.04] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-300/50 focus:outline-none";
  const label = "mb-1.5 block text-xs font-semibold text-slate-300";

  return (
    <form
      dir={rtl ? "rtl" : "ltr"}
      onSubmit={handleSubmit}
      className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 md:p-8"
      noValidate
    >
      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label className={label} htmlFor="name">{t.name}</label>
          <input id="name" name="name" required className={field} autoComplete="name" />
        </div>
        <div>
          <label className={label} htmlFor="company">{t.company}</label>
          <input id="company" name="company" required className={field} autoComplete="organization" />
        </div>
        <div>
          <label className={label} htmlFor="email">{t.email}</label>
          <input id="email" name="email" type="email" required className={field} autoComplete="email" />
        </div>
        <div>
          <label className={label} htmlFor="phone">{t.phone}</label>
          <input id="phone" name="phone" inputMode="tel" className={field} autoComplete="tel" />
        </div>
        <div>
          <label className={label} htmlFor="sector">{t.sector}</label>
          <select id="sector" name="sector" required defaultValue="" className={field}>
            <option value="" disabled>{t.selectOne}</option>
            {SECTORS.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
        <div>
          <label className={label} htmlFor="city">{t.city}</label>
          <input id="city" name="city" className={field} autoComplete="address-level2" />
        </div>
      </div>

      <div className="mt-4">
        <label className={label} htmlFor="need">{t.need}</label>
        <textarea
          id="need"
          name="need"
          required
          rows={4}
          placeholder={t.needPlaceholder}
          className={field}
        />
      </div>

      <div className="mt-4 grid gap-4 sm:grid-cols-2">
        <div>
          <label className={label} htmlFor="budget">{t.budget}</label>
          <select id="budget" name="budget" required defaultValue="" className={field}>
            <option value="" disabled>{t.selectOne}</option>
            {BUDGET_BANDS.map((b) => (
              <option key={b.value} value={b.value}>{rtl ? b.ar : b.en}</option>
            ))}
          </select>
        </div>
        <div>
          <label className={label} htmlFor="timeline">{t.timeline}</label>
          <select id="timeline" name="timeline" required defaultValue="" className={field}>
            <option value="" disabled>{t.selectOne}</option>
            {t.timelineOptions.map((o) => (
              <option key={o} value={o}>{o}</option>
            ))}
          </select>
        </div>
      </div>

      <button
        type="submit"
        disabled={state === "submitting"}
        className="mt-6 w-full rounded-2xl bg-cyan-400 px-6 py-4 text-lg font-black text-[#06111f] hover:bg-cyan-300 disabled:opacity-60"
      >
        {state === "submitting" ? t.submitting : t.submit}
      </button>

      <p className="mt-4 text-center text-xs text-slate-500">{t.approval}</p>
    </form>
  );
}
