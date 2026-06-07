"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const CALENDLY = process.env.NEXT_PUBLIC_CALENDLY_URL || "https://calendly.com/sami-dealix";
const EMAIL_GENERAL = "hello@dealix.me";
const EMAIL_FOUNDER = "founder@dealix.sa";
const EMAIL_DPO = "dpo@dealix.me";

export function ContactPage() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [form, setForm] = useState({ name: "", company: "", email: "", message: "" });
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<"ok" | "fallback" | null>(null);

  function update(field: keyof typeof form, value: string) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (busy) return;
    setBusy(true);
    setResult(null);
    try {
      const res = await fetch(`${API_BASE}/api/v1/public/demo-request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...form, source: "contact-page" }),
      });
      setResult(res.ok ? "ok" : "fallback");
    } catch {
      setResult("fallback");
    } finally {
      setBusy(false);
    }
  }

  const field = "w-full rounded-lg border border-border/60 bg-background px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#C9974B]/40";

  return (
    <PublicGtmShell>
      <div
        className={`mx-auto max-w-4xl px-6 py-12 space-y-12 ${isAr ? "text-right" : "text-left"}`}
        dir={isAr ? "rtl" : "ltr"}
      >
        {/* Hero */}
        <section className="space-y-4">
          <Badge className="bg-[#0A1628] text-[#C9974B] border-0 text-xs">{isAr ? "تواصل" : "Contact"}</Badge>
          <h1 className="text-4xl font-bold leading-tight md:text-5xl">
            {isAr ? "لنتحدّث عن إيراداتك" : "Let's talk about your revenue"}
          </h1>
          <p className="max-w-2xl text-lg text-muted-foreground leading-relaxed">
            {isAr
              ? "احجز مكالمة قصيرة، أو راسلنا، أو ابدأ مباشرة بتشخيص Risk Score مجاني. نرد خلال 48 ساعة عمل."
              : "Book a short call, email us, or start directly with a free Risk Score. We reply within 48 business hours."}
          </p>
        </section>

        {/* Channels */}
        <section className="grid gap-4 sm:grid-cols-3">
          <a href={CALENDLY} target="_blank" rel="noopener noreferrer" className="rounded-xl border border-border/60 bg-card/50 p-5 hover:border-[#C9974B]/40 transition-colors">
            <div className="text-2xl mb-2">📅</div>
            <p className="font-semibold text-sm">{isAr ? "احجز مكالمة" : "Book a call"}</p>
            <p className="text-xs text-muted-foreground mt-1">{isAr ? "30 دقيقة مع المؤسس" : "30 minutes with the founder"}</p>
          </a>
          <a href={`mailto:${EMAIL_GENERAL}`} className="rounded-xl border border-border/60 bg-card/50 p-5 hover:border-[#C9974B]/40 transition-colors">
            <div className="text-2xl mb-2">✉️</div>
            <p className="font-semibold text-sm">{isAr ? "راسلنا" : "Email us"}</p>
            <p className="text-xs text-muted-foreground mt-1 break-all">{EMAIL_GENERAL}</p>
          </a>
          <a href={`mailto:${EMAIL_FOUNDER}`} className="rounded-xl border border-border/60 bg-card/50 p-5 hover:border-[#C9974B]/40 transition-colors">
            <div className="text-2xl mb-2">👤</div>
            <p className="font-semibold text-sm">{isAr ? "المؤسس مباشرة" : "Founder direct"}</p>
            <p className="text-xs text-muted-foreground mt-1 break-all">{EMAIL_FOUNDER}</p>
          </a>
        </section>

        {/* Message form */}
        <section className="rounded-2xl border border-border/60 bg-card/50 p-8">
          <h2 className="text-xl font-bold mb-5">{isAr ? "أرسل رسالة" : "Send a message"}</h2>
          {result === "ok" ? (
            <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-6 text-center">
              <p className="font-semibold text-emerald-600 dark:text-emerald-400">{isAr ? "تم الاستلام ✓" : "Received ✓"}</p>
              <p className="text-sm text-muted-foreground mt-1">{isAr ? "سنرد خلال 48 ساعة عمل." : "We'll reply within 48 business hours."}</p>
            </div>
          ) : (
            <form onSubmit={submit} className="grid gap-4 sm:grid-cols-2">
              <input className={field} placeholder={isAr ? "الاسم" : "Name"} value={form.name} onChange={(e) => update("name", e.target.value)} required />
              <input className={field} placeholder={isAr ? "الشركة" : "Company"} value={form.company} onChange={(e) => update("company", e.target.value)} />
              <input type="email" className={`${field} sm:col-span-2`} placeholder={isAr ? "البريد الإلكتروني" : "Email"} value={form.email} onChange={(e) => update("email", e.target.value)} required />
              <textarea className={`${field} sm:col-span-2 min-h-[110px]`} placeholder={isAr ? "كيف نقدر نساعدك؟" : "How can we help?"} value={form.message} onChange={(e) => update("message", e.target.value)} required />
              <div className="sm:col-span-2 flex flex-col gap-3">
                <Button type="submit" size="lg" disabled={busy} className="bg-[#C9974B] text-[#0A1628] hover:bg-[#b8863a] font-bold w-full sm:w-auto">
                  {busy ? (isAr ? "جارٍ الإرسال…" : "Sending…") : isAr ? "إرسال" : "Send"}
                </Button>
                {result === "fallback" && (
                  <p className="text-sm text-amber-600 dark:text-amber-400">
                    {isAr
                      ? <>تعذّر الإرسال التلقائي. راسلنا على <a className="underline font-medium" href={`mailto:${EMAIL_GENERAL}`}>{EMAIL_GENERAL}</a>.</>
                      : <>Automatic submit failed. Email us at <a className="underline font-medium" href={`mailto:${EMAIL_GENERAL}`}>{EMAIL_GENERAL}</a>.</>}
                  </p>
                )}
              </div>
            </form>
          )}
        </section>

        {/* Data / PDPL */}
        <section className="rounded-xl border border-border/60 bg-muted/20 p-5 text-sm text-muted-foreground">
          <p>
            {isAr
              ? <>لطلبات حماية البيانات (PDPL) — الوصول أو الحذف أو الاعتراض — راسل مسؤول حماية البيانات على <a className="underline" href={`mailto:${EMAIL_DPO}`}>{EMAIL_DPO}</a>. لا نرسل أي تواصل تجاري بدون أساس نظامي وموافقة.</>
              : <>For data-protection (PDPL) requests — access, deletion, or objection — email our Data Protection Officer at <a className="underline" href={`mailto:${EMAIL_DPO}`}>{EMAIL_DPO}</a>. We never send commercial outreach without a lawful basis and consent.</>}
          </p>
        </section>
      </div>
    </PublicGtmShell>
  );
}
