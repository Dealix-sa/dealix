"use client";

import { useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

// ---------------------------------------------------------------------------
// Options (bilingual)
// ---------------------------------------------------------------------------

const REQUEST_TYPES = [
  { id: "custom_ai", ar: "نظام ذكاء اصطناعي مخصّص", en: "Custom AI build", icon: "🧩" },
  { id: "managed_ops", ar: "تشغيل إيراد مُدار (شهري)", en: "Managed Revenue Ops (monthly)", icon: "⚙️" },
  { id: "diagnostic", ar: "تشخيص مجاني / Sprint", en: "Free diagnostic / Sprint", icon: "🔍" },
  { id: "partnership", ar: "شراكة / وكالة", en: "Partnership / Agency", icon: "🤝" },
  { id: "other", ar: "شيء آخر", en: "Something else", icon: "💬" },
];

const SECTORS = [
  { id: "real_estate", ar: "العقار والمقاولات", en: "Real Estate & Construction" },
  { id: "technology", ar: "التقنية و SaaS", en: "Technology & SaaS" },
  { id: "professional_services", ar: "الخدمات المهنية", en: "Professional Services" },
  { id: "b2b_services", ar: "خدمات B2B", en: "B2B Services" },
  { id: "finance", ar: "المالية والمحاسبة", en: "Finance & Accounting" },
  { id: "hospitality", ar: "الضيافة والفعاليات", en: "Hospitality & Events" },
  { id: "retail", ar: "التجزئة والتجارة", en: "Retail & Commerce" },
  { id: "healthcare", ar: "الصحة والرعاية", en: "Healthcare" },
  { id: "other", ar: "قطاع آخر", en: "Other sector" },
];

const BUDGETS = [
  { id: "under_5k", ar: "أقل من ٥٬٠٠٠ ر.س", en: "Under 5,000 SAR" },
  { id: "5k_15k", ar: "٥٬٠٠٠ – ١٥٬٠٠٠ ر.س", en: "5,000 – 15,000 SAR" },
  { id: "15k_25k", ar: "١٥٬٠٠٠ – ٢٥٬٠٠٠ ر.س", en: "15,000 – 25,000 SAR" },
  { id: "over_25k", ar: "أكثر من ٢٥٬٠٠٠ ر.س", en: "Over 25,000 SAR" },
  { id: "not_sure", ar: "غير متأكد بعد", en: "Not sure yet" },
];

const VALUE_POINTS = [
  {
    ar: "تشخيص مجاني أولاً — ترى القيمة قبل أن تدفع",
    en: "Free diagnostic first — see value before you pay",
  },
  {
    ar: "Proof Pack موثّق بالأدلة (L0–L5)، لا وعود",
    en: "Evidence-backed Proof Pack (L0–L5), not promises",
  },
  {
    ar: "موافقتك مطلوبة قبل أي إرسال أو إجراء خارجي",
    en: "Your approval is required before any external send or action",
  },
  {
    ar: "عربي/إنجليزي · PDPL أصلاً · توقيت الرياض",
    en: "Arabic/English · PDPL-native · Riyadh time",
  },
];

const inputClass =
  "mt-1.5 w-full rounded-lg border border-input bg-background px-3.5 py-2.5 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring transition-shadow";

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export function ContactForm() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const dir = isAr ? "rtl" : "ltr";

  const [form, setForm] = useState({
    request_type: "custom_ai",
    name: "",
    company: "",
    email: "",
    phone: "",
    sector: "",
    budget: "",
    message: "",
    consent: false,
    website: "", // honeypot — must stay empty
  });
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [bookingUrl, setBookingUrl] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  function update<K extends keyof typeof form>(k: K, v: (typeof form)[K]) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.name || !form.company || !form.email.includes("@") || !form.phone) {
      setStatus(isAr ? "يرجى تعبئة الاسم والشركة والبريد والجوال." : "Please fill name, company, email and phone.");
      return;
    }
    if (!form.consent) {
      setStatus(isAr ? "الموافقة مطلوبة للمتابعة." : "Consent is required to continue.");
      return;
    }

    const rt = REQUEST_TYPES.find((r) => r.id === form.request_type);
    const rtLabel = rt ? (isAr ? rt.ar : rt.en) : form.request_type;
    const budget = BUDGETS.find((b) => b.id === form.budget);
    const budgetLabel = budget ? (isAr ? budget.ar : budget.en) : "";

    const composedMessage = [
      `[${rtLabel}]`,
      budgetLabel ? `${isAr ? "الميزانية" : "Budget"}: ${budgetLabel}` : "",
      "",
      form.message,
    ]
      .filter(Boolean)
      .join("\n");

    setBusy(true);
    setStatus("");
    const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    try {
      const res = await fetch(`${base}/api/v1/public/demo-request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: form.name,
          company: form.company,
          email: form.email,
          phone: form.phone,
          sector: form.sector,
          message: composedMessage,
          consent: form.consent,
          website: form.website,
          source: "website.contact",
          ref: form.request_type,
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || "failed");
      setSubmitted(true);
      setSuccessMsg(
        data.message ||
          (isAr ? "تم استلام طلبك — سنتواصل خلال 4 ساعات عمل." : "Request received — we'll be in touch within 4 business hours."),
      );
      if (data.calendly_url) setBookingUrl(data.calendly_url);
    } catch {
      setStatus(
        isAr
          ? "تعذّر الإرسال الآن. تحقّق من الاتصال وحاول مجدداً بعد لحظات."
          : "Couldn't submit right now. Check your connection and try again shortly.",
      );
    } finally {
      setBusy(false);
    }
  }

  // -------------------------------------------------------------------------
  // Success state
  // -------------------------------------------------------------------------
  if (submitted) {
    return (
      <div dir={dir} className={`mx-auto max-w-2xl ${isAr ? "text-right" : "text-left"}`}>
        <div className="rounded-2xl border border-emerald-500/30 bg-emerald-50/60 dark:bg-emerald-950/20 p-8 text-center">
          <div className="text-5xl mb-4">✅</div>
          <h2 className="text-2xl font-bold mb-2">{isAr ? "وصلنا طلبك" : "We got your request"}</h2>
          <p className="text-muted-foreground leading-relaxed mb-6">{successMsg}</p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
            {bookingUrl && (
              <Button asChild size="lg" className="w-full sm:w-auto bg-gold-500 text-navy-500 hover:bg-gold-400 font-bold">
                <a href={bookingUrl} target="_blank" rel="noopener noreferrer">
                  {isAr ? "احجز مكالمة الآن" : "Book a call now"}
                </a>
              </Button>
            )}
            <Button asChild size="lg" variant="outline" className="w-full sm:w-auto">
              <Link href={`/${locale}`}>{isAr ? "العودة للرئيسية" : "Back to home"}</Link>
            </Button>
          </div>
          <p className="mt-6 text-xs text-muted-foreground">
            {isAr
              ? "القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value"
              : "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"}
          </p>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------------------------
  // Form
  // -------------------------------------------------------------------------
  return (
    <div dir={dir} className={isAr ? "text-right" : "text-left"}>
      {/* Hero */}
      <header className="rounded-2xl bg-gradient-to-br from-[#001F3F] to-[#0a2040] text-white p-8 md:p-10 mb-8">
        <Badge className="mb-4 bg-gold-500/20 text-gold-300 border-gold-500/30">
          {isAr ? "تحدّث معنا — Dealix" : "Talk to us — Dealix"}
        </Badge>
        <h1 className="text-3xl md:text-4xl font-bold leading-tight">
          {isAr ? "عندك فكرة أو تحدّي؟ خلّنا نبنيه معك" : "Got a goal or a challenge? Let's build it with you"}
        </h1>
        <p className="mt-4 text-white/70 max-w-2xl leading-relaxed">
          {isAr
            ? "اطلب نظام ذكاء اصطناعي مخصّصاً، أو تشغيل إيراد مُدار، أو ابدأ بتشخيص مجاني. صف ما تريد إنجازه وسنرجع لك بخطة واضحة وأدلة — لا وعود فارغة."
            : "Request a custom AI build, managed revenue ops, or start with a free diagnostic. Tell us what you want to achieve and we'll come back with a clear, evidence-based plan — no empty promises."}
        </p>
      </header>

      <div className="grid gap-8 lg:grid-cols-5">
        {/* Value column */}
        <aside className="lg:col-span-2 space-y-5">
          <div className="rounded-2xl border border-border/60 bg-card/50 p-6">
            <h2 className="font-bold text-lg mb-4">{isAr ? "ماذا تتوقّع؟" : "What to expect"}</h2>
            <ul className="space-y-3">
              {VALUE_POINTS.map((p) => (
                <li key={p.en} className="flex items-start gap-2.5 text-sm">
                  <span className="text-emerald-500 mt-0.5 flex-shrink-0">✓</span>
                  <span className="text-muted-foreground leading-relaxed">{isAr ? p.ar : p.en}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className="rounded-2xl border border-gold-500/25 bg-gold-500/5 p-6">
            <h3 className="font-semibold mb-2 text-sm">{isAr ? "سلّم الخدمات" : "The service ladder"}</h3>
            <ol className="space-y-1.5 text-sm text-muted-foreground">
              <li>0 — {isAr ? "تشخيص مجاني" : "Free diagnostic"}</li>
              <li>1 — {isAr ? "Sprint استخباراتي · ٤٩٩ ر.س" : "Intelligence Sprint · 499 SAR"}</li>
              <li>2 — {isAr ? "حزمة بيانات-لإيراد · ١٬٥٠٠ ر.س" : "Data-to-Revenue Pack · 1,500 SAR"}</li>
              <li>3 — {isAr ? "تشغيل إيراد مُدار · ٢٬٩٩٩+ ر.س/شهر" : "Managed Revenue Ops · 2,999+ SAR/mo"}</li>
              <li>4 — {isAr ? "نظام AI مخصّص · ٥٬٠٠٠–٢٥٬٠٠٠ ر.س" : "Custom AI build · 5,000–25,000 SAR"}</li>
            </ol>
          </div>
        </aside>

        {/* Form column */}
        <form onSubmit={submit} className="lg:col-span-3 rounded-2xl border border-border/60 bg-card/50 p-6 md:p-8 space-y-5">
          {/* Request type */}
          <div>
            <label className="text-sm font-medium">{isAr ? "نوع الطلب *" : "Request type *"}</label>
            <div className="mt-2 grid sm:grid-cols-2 gap-2">
              {REQUEST_TYPES.map((t) => (
                <label
                  key={t.id}
                  className={`flex items-center gap-2.5 rounded-lg border p-3 cursor-pointer transition-colors text-sm ${
                    form.request_type === t.id ? "border-gold-500 bg-gold-500/5" : "border-border/50 hover:bg-muted/20"
                  }`}
                >
                  <input
                    type="radio"
                    name="request_type"
                    value={t.id}
                    checked={form.request_type === t.id}
                    onChange={() => update("request_type", t.id)}
                    className="accent-gold-500"
                  />
                  <span>{t.icon}</span>
                  <span className="font-medium">{isAr ? t.ar : t.en}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label htmlFor="name" className="text-sm font-medium">{isAr ? "الاسم *" : "Name *"}</label>
              <input id="name" required value={form.name} onChange={(e) => update("name", e.target.value)} className={inputClass} />
            </div>
            <div>
              <label htmlFor="company" className="text-sm font-medium">{isAr ? "الشركة *" : "Company *"}</label>
              <input id="company" required value={form.company} onChange={(e) => update("company", e.target.value)} className={inputClass} />
            </div>
            <div>
              <label htmlFor="email" className="text-sm font-medium">{isAr ? "البريد الإلكتروني *" : "Email *"}</label>
              <input id="email" type="email" required value={form.email} onChange={(e) => update("email", e.target.value)} className={inputClass} />
            </div>
            <div>
              <label htmlFor="phone" className="text-sm font-medium">{isAr ? "الجوال *" : "Phone *"}</label>
              <input id="phone" type="tel" required dir="ltr" placeholder="+9665XXXXXXXX" value={form.phone} onChange={(e) => update("phone", e.target.value)} className={`${inputClass} ${isAr ? "text-right" : ""}`} />
            </div>
            <div>
              <label htmlFor="sector" className="text-sm font-medium">{isAr ? "القطاع" : "Sector"}</label>
              <select id="sector" value={form.sector} onChange={(e) => update("sector", e.target.value)} className={inputClass}>
                <option value="">{isAr ? "اختر القطاع" : "Select sector"}</option>
                {SECTORS.map((s) => (
                  <option key={s.id} value={s.id}>{isAr ? s.ar : s.en}</option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="budget" className="text-sm font-medium">{isAr ? "الميزانية التقديرية" : "Estimated budget"}</label>
              <select id="budget" value={form.budget} onChange={(e) => update("budget", e.target.value)} className={inputClass}>
                <option value="">{isAr ? "اختياري" : "Optional"}</option>
                {BUDGETS.map((b) => (
                  <option key={b.id} value={b.id}>{isAr ? b.ar : b.en}</option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label htmlFor="message" className="text-sm font-medium">
              {isAr ? "صف ما تريد إنجازه" : "Describe what you want to achieve"}
            </label>
            <textarea
              id="message"
              rows={5}
              value={form.message}
              onChange={(e) => update("message", e.target.value)}
              className={inputClass}
              placeholder={
                isAr
                  ? "مثال: عندنا CRM مليان لكن المتابعة ضعيفة، نبي نظام يرتّب الفرص ويجهّز مسودات تواصل قبل الموافقة..."
                  : "e.g. Our CRM is full but follow-up is weak; we want a system that prioritizes opportunities and drafts outreach for approval..."
              }
            />
          </div>

          {/* Honeypot (visually hidden) */}
          <input
            type="text"
            tabIndex={-1}
            autoComplete="off"
            aria-hidden="true"
            value={form.website}
            onChange={(e) => update("website", e.target.value)}
            className="absolute -left-[9999px] h-0 w-0 opacity-0"
          />

          <label className="flex items-start gap-2.5 text-sm cursor-pointer">
            <input type="checkbox" checked={form.consent} onChange={(e) => update("consent", e.target.checked)} className="mt-0.5 accent-gold-500" />
            <span className="text-muted-foreground leading-relaxed">
              {isAr
                ? "أوافق على مراجعة طلبي والتواصل معي للمتابعة. لا تسويق بارد آلي — كل تواصل بموافقة. (PDPL)"
                : "I consent to my request being reviewed and to follow-up contact. No automated cold outreach — every contact is consented. (PDPL)"}
            </span>
          </label>

          <Button type="submit" disabled={busy} size="lg" className="w-full bg-gold-500 text-navy-500 hover:bg-gold-400 font-bold">
            {busy ? (isAr ? "جاري الإرسال..." : "Submitting...") : isAr ? "أرسل الطلب" : "Send request"}
          </Button>

          {status && <p className="text-sm text-destructive">{status}</p>}

          <p className="text-xs text-muted-foreground text-center pt-1">
            {isAr
              ? "القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value"
              : "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة"}
          </p>
        </form>
      </div>
    </div>
  );
}
