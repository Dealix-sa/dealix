"use client";

import { useLocale } from "next-intl";
import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const SECTORS = [
  { id: "real_estate", ar: "العقار والتطوير", en: "Real Estate & Development" },
  { id: "contracting", ar: "المقاولات وإدارة المشاريع", en: "Contracting & Project Mgmt" },
  { id: "facilities", ar: "إدارة المرافق والصيانة", en: "Facilities & Maintenance" },
  { id: "professional_services", ar: "خدمات احترافية B2B", en: "Professional B2B Services" },
  { id: "technology", ar: "تقنية / SaaS", en: "Technology / SaaS" },
  { id: "hospitality", ar: "ضيافة وفعاليات", en: "Hospitality & Events" },
  { id: "other", ar: "أخرى", en: "Other" },
];

const SIZES = [
  { id: "1-10", label: "1–10" },
  { id: "11-50", label: "11–50" },
  { id: "51-200", label: "51–200" },
  { id: "200+", label: "200+" },
];

export function ContactForm({
  defaultEmail = "",
  defaultPlan = "",
}: {
  defaultEmail?: string;
  defaultPlan?: string;
}) {
  const locale = useLocale();
  const isAr = locale === "ar";

  const planNote =
    defaultPlan === "growth"
      ? isAr
        ? "مهتم بخطة النمو (2,999 ر.س/شهر)"
        : "Interested in the Growth plan (2,999 SAR/mo)"
      : "";

  const [form, setForm] = useState({
    name: "",
    company: "",
    email: defaultEmail,
    phone: "",
    sector: "",
    size: "",
    message: planNote,
    consent: false,
    website: "", // honeypot
  });
  const [busy, setBusy] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [status, setStatus] = useState("");
  const [calendly, setCalendly] = useState("");

  function set<K extends keyof typeof form>(k: K, v: (typeof form)[K]) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.consent) {
      setStatus(isAr ? "الموافقة مطلوبة للمتابعة." : "Consent is required to continue.");
      return;
    }
    setBusy(true);
    setStatus("");
    try {
      const res = await fetch("/api/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...form, source: "contact_page" }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok || data.ok === false) {
        throw new Error(data.detail || "failed");
      }
      setCalendly(data.calendly_url || "");
      setSubmitted(true);
    } catch (err) {
      const detail = err instanceof Error ? err.message : "failed";
      setStatus(
        detail === "missing_required_fields"
          ? isAr
            ? "يرجى تعبئة الاسم والشركة والبريد والجوال."
            : "Please fill name, company, email and phone."
          : isAr
            ? "تعذّر الإرسال — تحقق من الاتصال وحاول مجدداً."
            : "Couldn't submit — check your connection and try again.",
      );
    } finally {
      setBusy(false);
    }
  }

  if (submitted) {
    return (
      <Card className="p-8 text-center border-emerald-500/30 bg-emerald-50/50 dark:bg-emerald-950/20 max-w-lg mx-auto">
        <div className="text-4xl mb-3">✅</div>
        <h3 className="text-xl font-bold text-emerald-700 dark:text-emerald-300">
          {isAr ? "تم استلام طلبك!" : "Your request was received!"}
        </h3>
        <p className="text-muted-foreground mt-2 text-sm">
          {isAr
            ? "سنتواصل معك خلال ساعات العمل. للرد الأسرع احجز مكالمة الآن."
            : "We'll be in touch within business hours. For the fastest response, book a call now."}
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          {calendly && (
            <Button asChild variant="gold">
              <a href={calendly} target="_blank" rel="noopener noreferrer">
                {isAr ? "احجز مكالمة" : "Book a call"}
              </a>
            </Button>
          )}
          <Button asChild variant="outline">
            <Link href={`/${locale}/proof-pack`}>
              {isAr ? "شاهد عيّنة Proof Pack" : "View a Proof Pack sample"}
            </Link>
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <form onSubmit={submit} className="max-w-lg mx-auto space-y-5" dir={isAr ? "rtl" : "ltr"}>
      {/* honeypot */}
      <input
        type="text"
        tabIndex={-1}
        autoComplete="off"
        aria-hidden
        value={form.website}
        onChange={(e) => set("website", e.target.value)}
        className="hidden"
      />

      <div className="grid sm:grid-cols-2 gap-4">
        <div>
          <Label htmlFor="name" className="text-sm font-medium">
            {isAr ? "الاسم الكامل *" : "Full name *"}
          </Label>
          <Input id="name" required value={form.name} onChange={(e) => set("name", e.target.value)} className="mt-1" />
        </div>
        <div>
          <Label htmlFor="company" className="text-sm font-medium">
            {isAr ? "اسم الشركة *" : "Company name *"}
          </Label>
          <Input id="company" required value={form.company} onChange={(e) => set("company", e.target.value)} className="mt-1" />
        </div>
      </div>

      <div className="grid sm:grid-cols-2 gap-4">
        <div>
          <Label htmlFor="email" className="text-sm font-medium">
            {isAr ? "البريد الإلكتروني *" : "Work email *"}
          </Label>
          <Input id="email" type="email" required value={form.email} onChange={(e) => set("email", e.target.value)} className="mt-1" />
        </div>
        <div>
          <Label htmlFor="phone" className="text-sm font-medium">
            {isAr ? "رقم الجوال *" : "Phone *"}
          </Label>
          <Input id="phone" type="tel" required placeholder="+9665…" value={form.phone} onChange={(e) => set("phone", e.target.value)} className="mt-1" />
        </div>
      </div>

      <div className="grid sm:grid-cols-2 gap-4">
        <div>
          <Label htmlFor="sector" className="text-sm font-medium">
            {isAr ? "القطاع" : "Sector"}
          </Label>
          <select
            id="sector"
            value={form.sector}
            onChange={(e) => set("sector", e.target.value)}
            className="mt-1 w-full h-10 rounded-md border border-input bg-background px-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">{isAr ? "اختر القطاع" : "Select sector"}</option>
            {SECTORS.map((s) => (
              <option key={s.id} value={s.id}>
                {isAr ? s.ar : s.en}
              </option>
            ))}
          </select>
        </div>
        <div>
          <Label htmlFor="size" className="text-sm font-medium">
            {isAr ? "حجم الفريق" : "Team size"}
          </Label>
          <select
            id="size"
            value={form.size}
            onChange={(e) => set("size", e.target.value)}
            className="mt-1 w-full h-10 rounded-md border border-input bg-background px-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">{isAr ? "اختر الحجم" : "Select size"}</option>
            {SIZES.map((s) => (
              <option key={s.id} value={s.id}>
                {s.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div>
        <Label htmlFor="message" className="text-sm font-medium">
          {isAr ? "كيف نقدر نساعدك؟" : "How can we help?"}
        </Label>
        <textarea
          id="message"
          rows={4}
          value={form.message}
          onChange={(e) => set("message", e.target.value)}
          className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          placeholder={
            isAr
              ? "مثال: نريد تشخيصاً لتسرّب الإيراد في قسم المبيعات…"
              : "e.g. We'd like a diagnostic on revenue leakage in our sales team…"
          }
        />
      </div>

      <label className="flex items-start gap-2 text-sm cursor-pointer">
        <input
          type="checkbox"
          checked={form.consent}
          onChange={(e) => set("consent", e.target.checked)}
          className="mt-0.5 accent-primary"
        />
        <span className="text-muted-foreground">
          {isAr
            ? "أوافق على التواصل معي بخصوص هذا الطلب. بياناتي تُعالَج وفق PDPL ولا يوجد إرسال آلي."
            : "I consent to be contacted about this request. My data is processed under PDPL with no automated outreach."}
        </span>
      </label>

      <Button type="submit" disabled={busy} size="lg" variant="gold" className="w-full">
        {busy ? (isAr ? "جارٍ الإرسال…" : "Submitting…") : isAr ? "أرسل الطلب" : "Send request"}
      </Button>

      {status && <p className="text-sm text-destructive text-center">{status}</p>}

      <p className="text-xs text-muted-foreground text-center">
        {isAr ? (
          <>
            تفضّل مكالمة مباشرة؟{" "}
            <a href="https://calendly.com/sami-assiri11/dealix-demo" target="_blank" rel="noopener noreferrer" className="underline">
              احجز عبر Calendly
            </a>
          </>
        ) : (
          <>
            Prefer a direct call?{" "}
            <a href="https://calendly.com/sami-assiri11/dealix-demo" target="_blank" rel="noopener noreferrer" className="underline">
              Book via Calendly
            </a>
          </>
        )}
      </p>

      <div className="flex flex-wrap justify-center gap-2 pt-2">
        {(isAr
          ? ["لا تسويق بارد آلي", "موافقة قبل كل خطوة", "PDPL", "سجل تدقيق كامل"]
          : ["No cold outreach", "Approval before every step", "PDPL", "Full audit log"]
        ).map((b) => (
          <Badge key={b} variant="secondary" className="text-xs">
            {b}
          </Badge>
        ))}
      </div>
    </form>
  );
}
