"use client";

import { useLocale } from "next-intl";
import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

export function ContactForm() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [form, setForm] = useState({
    name: "",
    company: "",
    email: "",
    phone: "",
    sector: "",
    message: "",
    consent: false,
    website: "", // honeypot
    source: "contact_page",
  });
  const [status, setStatus] = useState("");
  const [calendly, setCalendly] = useState("");
  const [busy, setBusy] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.name || !form.company || !form.email || !form.phone) {
      setStatus(isAr ? "الحقول الأساسية مطلوبة." : "Required fields are missing.");
      return;
    }
    if (!form.consent) {
      setStatus(isAr ? "الموافقة مطلوبة." : "Consent is required.");
      return;
    }
    setBusy(true);
    setStatus("");
    try {
      const res = await api.postPublicDemoRequest(form);
      const data = res.data as { calendly_url?: string; message?: string };
      setCalendly(data.calendly_url || "");
      setSubmitted(true);
      setStatus(
        data.message ||
          (isAr
            ? "تم استلام طلبك — سنتواصل خلال ساعات العمل."
            : "We received your request — we'll be in touch within business hours."),
      );
    } catch {
      setStatus(
        isAr
          ? "تعذّر الإرسال — تحقّق من الاتصال وحاول مجدداً."
          : "Submit failed — check your connection and try again.",
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className={`space-y-12 ${isAr ? "text-right" : "text-left"}`} dir={isAr ? "rtl" : "ltr"}>
      {/* Hero */}
      <header className="rounded-2xl bg-gradient-to-br from-[#001F3F] to-[#0a2040] text-white p-8">
        <Badge className="mb-4 bg-amber-500/20 text-amber-300 border-amber-500/30">
          {isAr ? "تواصل — Dealix" : "Contact — Dealix"}
        </Badge>
        <h1 className="text-4xl font-bold leading-tight">
          {isAr ? "احجز تشخيصك المجاني أو تواصل معنا" : "Book your free diagnostic or reach us"}
        </h1>
        <p className="mt-4 text-white/70 max-w-xl leading-relaxed">
          {isAr
            ? "رد بشري خلال ساعات العمل — لا رسائل آلية. أخبرنا بوضعك ونرجع لك بأفضل خطوة تالية."
            : "A human reply within business hours — no automated messages. Tell us your situation and we'll suggest the best next step."}
        </p>
      </header>

      <div className="grid gap-8 lg:grid-cols-[1.3fr_1fr]">
        {/* Form */}
        <section>
          {submitted ? (
            <Card className="p-8 text-center border-emerald-500/30 bg-emerald-50/50 dark:bg-emerald-950/20">
              <div className="text-4xl mb-3">✅</div>
              <h3 className="text-xl font-bold text-emerald-700 dark:text-emerald-300">
                {isAr ? "تم الاستلام!" : "Received!"}
              </h3>
              <p className="text-muted-foreground mt-2">{status}</p>
              <div className="mt-6 flex flex-wrap justify-center gap-3">
                {calendly && (
                  <Button asChild>
                    <a href={calendly} target="_blank" rel="noopener noreferrer">
                      {isAr ? "احجز موعداً الآن" : "Book a time now"}
                    </a>
                  </Button>
                )}
                <Button asChild variant="outline">
                  <Link href={`/${locale}/services`}>
                    {isAr ? "تصفّح الخدمات" : "Browse services"}
                  </Link>
                </Button>
              </div>
            </Card>
          ) : (
            <form onSubmit={submit} className="space-y-5">
              {/* honeypot */}
              <input
                type="text"
                tabIndex={-1}
                autoComplete="off"
                value={form.website}
                onChange={(e) => setForm((f) => ({ ...f, website: e.target.value }))}
                className="hidden"
                aria-hidden="true"
              />
              {([
                ["name", isAr ? "الاسم الكامل *" : "Full Name *", "text", true],
                ["company", isAr ? "اسم الشركة *" : "Company Name *", "text", true],
                ["email", isAr ? "البريد الإلكتروني *" : "Email Address *", "email", true],
                ["phone", isAr ? "رقم الجوال *" : "Phone *", "tel", true],
                ["sector", isAr ? "القطاع (اختياري)" : "Sector (optional)", "text", false],
              ] as const).map(([k, label, type, required]) => (
                <div key={k}>
                  <Label htmlFor={k} className="text-sm font-medium">{label}</Label>
                  <Input
                    id={k}
                    type={type}
                    required={required}
                    value={form[k as keyof typeof form] as string}
                    onChange={(e) => setForm((f) => ({ ...f, [k]: e.target.value }))}
                    className="mt-1"
                  />
                </div>
              ))}

              <div>
                <Label htmlFor="message" className="text-sm font-medium">
                  {isAr ? "كيف نقدر نساعدك؟ (اختياري)" : "How can we help? (optional)"}
                </Label>
                <textarea
                  id="message"
                  rows={4}
                  value={form.message}
                  onChange={(e) => setForm((f) => ({ ...f, message: e.target.value }))}
                  className="mt-1 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  placeholder={
                    isAr
                      ? "مثال: نخسر leads على واتساب بسبب تأخّر الرد..."
                      : "e.g. We lose WhatsApp leads due to slow replies..."
                  }
                />
              </div>

              <label className="flex items-start gap-2 text-sm cursor-pointer">
                <input
                  type="checkbox"
                  checked={form.consent}
                  onChange={(e) => setForm((f) => ({ ...f, consent: e.target.checked }))}
                  className="mt-0.5 accent-primary"
                />
                <span>
                  {isAr
                    ? "أوافق على التواصل معي للمتابعة. لا outreach بارد آلي."
                    : "I consent to follow-up contact. No automated cold outreach."}
                </span>
              </label>

              <Button type="submit" disabled={busy} size="lg" className="w-full">
                {busy
                  ? isAr
                    ? "جاري الإرسال..."
                    : "Submitting..."
                  : isAr
                    ? "أرسل واحجز التشخيص"
                    : "Send & book diagnostic"}
              </Button>

              {status && !submitted && <p className="text-sm text-destructive">{status}</p>}
            </form>
          )}
        </section>

        {/* Side info */}
        <aside className="space-y-4">
          <Card className="p-5">
            <h3 className="font-semibold mb-3">{isAr ? "ماذا تتوقّع" : "What to expect"}</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              {(isAr
                ? [
                    "رد بشري خلال ساعات العمل",
                    "تشخيص مجاني مختصر لوضعك",
                    "توصية بأفضل خطوة تالية بلا ضغط",
                    "كل تواصل بموافقتك — بلا أتمتة",
                  ]
                : [
                    "Human reply within business hours",
                    "A short free diagnostic of your situation",
                    "A no-pressure best-next-step recommendation",
                    "All contact with your consent — no automation",
                  ]
              ).map((item) => (
                <li key={item} className="flex items-start gap-2">
                  <span className="text-emerald-500 mt-0.5 flex-shrink-0">✓</span>
                  {item}
                </li>
              ))}
            </ul>
          </Card>
          <Card className="p-5">
            <h3 className="font-semibold mb-2">{isAr ? "تبي تبني شيء مخصّص؟" : "Want something custom?"}</h3>
            <p className="text-sm text-muted-foreground mb-3">
              {isAr
                ? "إذا عندك مشروع محدّد، صف لنا النطاق ونرجع لك بخطة وتقدير."
                : "If you have a specific project, describe the scope and we'll return a plan and estimate."}
            </p>
            <Button asChild variant="outline" size="sm">
              <Link href={`/${locale}/custom`}>{isAr ? "اطلب بناءً مخصّصاً" : "Request a custom build"}</Link>
            </Button>
          </Card>
        </aside>
      </div>
    </div>
  );
}
