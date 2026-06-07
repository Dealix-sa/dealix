"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

type Status = "idle" | "submitting" | "success" | "error";

interface SuccessPayload {
  calendly_url?: string;
  message?: string;
  lead_id?: string;
}

const BUDGETS = [
  { value: "<5000", ar: "أقل من 5,000 ر.س", en: "Under 5,000 SAR" },
  { value: "5000-25000", ar: "5,000 – 25,000 ر.س", en: "5,000 – 25,000 SAR" },
  { value: "25000-100000", ar: "25,000 – 100,000 ر.س", en: "25,000 – 100,000 SAR" },
  { value: ">100000", ar: "أكثر من 100,000 ر.س", en: "Over 100,000 SAR" },
  { value: "not_sure", ar: "غير محدد بعد", en: "Not sure yet" },
];

const TIMELINES = [
  { value: "asap", ar: "في أقرب وقت", en: "ASAP" },
  { value: "30d", ar: "خلال 30 يوماً", en: "Within 30 days" },
  { value: "90d", ar: "خلال 90 يوماً", en: "Within 90 days" },
  { value: "exploring", ar: "أستكشف فقط", en: "Just exploring" },
];

export function CustomSolutionForm() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [status, setStatus] = useState<Status>("idle");
  const [result, setResult] = useState<SuccessPayload | null>(null);
  const [error, setError] = useState<string>("");

  const [form, setForm] = useState({
    name: "",
    company: "",
    email: "",
    phone: "",
    sector: "",
    what_to_build: "",
    budget_range: "",
    timeline: "",
    consent: false,
    website: "", // honeypot — must stay empty
  });

  const set = (k: keyof typeof form, v: string | boolean) =>
    setForm((f) => ({ ...f, [k]: v }));

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    if (!form.name || !form.company || !form.email.includes("@")) {
      setError(isAr ? "الاسم والشركة والبريد مطلوبة." : "Name, company and a valid email are required.");
      return;
    }
    if (!form.what_to_build.trim()) {
      setError(isAr ? "صف ما تريد أن نبنيه." : "Describe what you want us to build.");
      return;
    }
    if (!form.consent) {
      setError(isAr ? "يرجى الموافقة على التواصل." : "Please consent to be contacted.");
      return;
    }
    setStatus("submitting");
    try {
      const { data } = await api.postPublicCustomRequest({ ...form, source: "web.custom_form" });
      setResult(data as SuccessPayload);
      setStatus("success");
    } catch {
      setStatus("error");
      setError(isAr ? "تعذّر الإرسال. حاول مرة أخرى." : "Submission failed. Please try again.");
    }
  }

  if (status === "success") {
    return (
      <Card className="border-2 border-gold-500/40">
        <CardHeader>
          <Badge variant="gold" className="w-fit mb-2">{isAr ? "تم الاستلام" : "Received"}</Badge>
          <CardTitle className="text-2xl">
            {isAr ? "وصلنا طلبك المخصّص ✓" : "Your custom request is in ✓"}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground leading-relaxed">
            {result?.message ||
              (isAr
                ? "سنراجع المتطلبات ونتواصل خلال 4 ساعات عمل."
                : "We'll review the requirements and reply within 4 business hours.")}
          </p>
          {result?.calendly_url && (
            <Button variant="gold" size="lg" asChild>
              <a href={result.calendly_url} target="_blank" rel="noopener noreferrer">
                {isAr ? "احجز مكالمة الآن" : "Book a call now"}
              </a>
            </Button>
          )}
          <p className="text-xs text-muted-foreground">
            {isAr
              ? "ملاحظة: لا نرسل أي شيء نيابةً عنك. كل تواصل بموافقتك المسبقة."
              : "Note: we never send anything on your behalf. All outreach is pre-approved by you."}
          </p>
        </CardContent>
      </Card>
    );
  }

  const inputCls = "mt-1.5";

  return (
    <Card className="border-2 border-border/60" dir={isAr ? "rtl" : "ltr"}>
      <CardHeader>
        <Badge variant="gold" className="w-fit mb-2 text-xs uppercase tracking-wide">
          {isAr ? "حل مخصّص" : "Custom Solution"}
        </Badge>
        <CardTitle className="text-2xl">
          {isAr ? "اطلب حلاً مخصّصاً" : "Request a Custom Solution"}
        </CardTitle>
        <p className="text-sm text-muted-foreground mt-1">
          {isAr
            ? "صف بالتفصيل ما تريد أن يبنيه Dealix لعملك — AI، أتمتة، تكامل، أو لوحة قيادة. نراجع ونرد بمقترح."
            : "Describe what you want Dealix to build — AI, automation, integration, or a command center. We review and reply with a proposal."}
        </p>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-4">
          {/* Honeypot — visually hidden, bots fill it */}
          <input
            type="text"
            name="website"
            tabIndex={-1}
            autoComplete="off"
            aria-hidden="true"
            value={form.website}
            onChange={(e) => set("website", e.target.value)}
            style={{ position: "absolute", left: "-9999px", width: 1, height: 1 }}
          />

          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <Label htmlFor="cs-name">{isAr ? "الاسم *" : "Name *"}</Label>
              <Input id="cs-name" className={inputCls} value={form.name}
                onChange={(e) => set("name", e.target.value)} required />
            </div>
            <div>
              <Label htmlFor="cs-company">{isAr ? "الشركة *" : "Company *"}</Label>
              <Input id="cs-company" className={inputCls} value={form.company}
                onChange={(e) => set("company", e.target.value)} required />
            </div>
            <div>
              <Label htmlFor="cs-email">{isAr ? "البريد الإلكتروني *" : "Email *"}</Label>
              <Input id="cs-email" type="email" className={inputCls} value={form.email}
                onChange={(e) => set("email", e.target.value)} required />
            </div>
            <div>
              <Label htmlFor="cs-phone">{isAr ? "الجوال" : "Phone"}</Label>
              <Input id="cs-phone" className={inputCls} value={form.phone}
                onChange={(e) => set("phone", e.target.value)} dir="ltr" />
            </div>
            <div>
              <Label htmlFor="cs-sector">{isAr ? "القطاع" : "Sector"}</Label>
              <Input id="cs-sector" className={inputCls} value={form.sector}
                onChange={(e) => set("sector", e.target.value)}
                placeholder={isAr ? "مثال: عقار، فنتك، SaaS" : "e.g. real-estate, fintech, SaaS"} />
            </div>
            <div>
              <Label htmlFor="cs-budget">{isAr ? "الميزانية التقديرية" : "Estimated budget"}</Label>
              <select id="cs-budget" value={form.budget_range}
                onChange={(e) => set("budget_range", e.target.value)}
                className="mt-1.5 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
                <option value="">{isAr ? "اختر…" : "Select…"}</option>
                {BUDGETS.map((b) => (
                  <option key={b.value} value={b.value}>{isAr ? b.ar : b.en}</option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <Label htmlFor="cs-timeline">{isAr ? "الإطار الزمني" : "Timeline"}</Label>
            <select id="cs-timeline" value={form.timeline}
              onChange={(e) => set("timeline", e.target.value)}
              className="mt-1.5 w-full rounded-md border border-input bg-background px-3 py-2 text-sm">
              <option value="">{isAr ? "اختر…" : "Select…"}</option>
              {TIMELINES.map((t) => (
                <option key={t.value} value={t.value}>{isAr ? t.ar : t.en}</option>
              ))}
            </select>
          </div>

          <div>
            <Label htmlFor="cs-build">{isAr ? "ما الذي تريد أن نبنيه؟ *" : "What do you want us to build? *"}</Label>
            <textarea id="cs-build" value={form.what_to_build}
              onChange={(e) => set("what_to_build", e.target.value)}
              required rows={5}
              className="mt-1.5 w-full rounded-md border border-input bg-background px-3 py-2 text-sm leading-relaxed"
              placeholder={isAr
                ? "مثال: مساعد AI بالعربي يرد على leads خلال 45 ثانية، يؤهّل، ويحجز ديمو فوق CRM الحالي."
                : "e.g. an Arabic AI assistant that replies to leads in 45s, qualifies, and books demos on top of our CRM."} />
          </div>

          <label className="flex items-start gap-2 text-sm">
            <input type="checkbox" checked={form.consent}
              onChange={(e) => set("consent", e.target.checked)} className="mt-1" />
            <span className="text-muted-foreground">
              {isAr
                ? "أوافق على أن يتواصل معي فريق Dealix بخصوص طلبي (PDPL)."
                : "I consent to be contacted by Dealix about my request (PDPL)."}
            </span>
          </label>

          {error && <p className="text-sm text-red-500">{error}</p>}

          <Button type="submit" variant="gold" size="lg" className="w-full"
            disabled={status === "submitting"}>
            {status === "submitting"
              ? (isAr ? "جارٍ الإرسال…" : "Submitting…")
              : (isAr ? "أرسل الطلب" : "Send request")}
          </Button>

          <p className="text-xs text-muted-foreground text-center">
            {isAr
              ? "لا إرسال تلقائي ولا رسائل باردة — كل تواصل بموافقتك."
              : "No auto-send, no cold outreach — all contact is approval-first."}
          </p>
        </form>
      </CardContent>
    </Card>
  );
}
