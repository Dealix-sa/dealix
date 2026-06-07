"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api } from "@/lib/api";

type Status = "idle" | "submitting" | "success" | "error";

interface SuccessPayload {
  calendly_url?: string;
  message?: string;
  lead_id?: string;
}

/**
 * Public lead-capture form. POSTs to /api/v1/public/demo-request (store A —
 * read by the daily lead-prep engine). DRAFT-ONLY: nothing is auto-sent.
 */
export function LeadIntakeForm({ source = "web.lead_form" }: { source?: string }) {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [status, setStatus] = useState<Status>("idle");
  const [result, setResult] = useState<SuccessPayload | null>(null);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    name: "", company: "", email: "", phone: "",
    sector: "", size: "", message: "", consent: false, website: "",
  });

  const set = (k: keyof typeof form, v: string | boolean) =>
    setForm((f) => ({ ...f, [k]: v }));

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    if (!form.name || !form.company || !form.email.includes("@") || !form.phone) {
      setError(isAr ? "الاسم والشركة والبريد والجوال مطلوبة." : "Name, company, email and phone are required.");
      return;
    }
    if (!form.consent) {
      setError(isAr ? "يرجى الموافقة على التواصل." : "Please consent to be contacted.");
      return;
    }
    setStatus("submitting");
    try {
      const { data } = await api.postPublicDemoRequest({ ...form, source });
      setResult(data as SuccessPayload);
      setStatus("success");
    } catch {
      setStatus("error");
      setError(isAr ? "تعذّر الإرسال. حاول مرة أخرى." : "Submission failed. Please try again.");
    }
  }

  if (status === "success") {
    return (
      <div className="rounded-2xl border-2 border-emerald-500/40 bg-emerald-500/5 p-6 text-center" dir={isAr ? "rtl" : "ltr"}>
        <p className="text-lg font-bold">{isAr ? "تم استلام طلبك ✓" : "Request received ✓"}</p>
        <p className="mt-2 text-sm text-muted-foreground">
          {result?.message || (isAr ? "سنتواصل خلال 4 ساعات عمل." : "We'll reach out within 4 business hours.")}
        </p>
        {result?.calendly_url && (
          <Button variant="gold" size="lg" className="mt-4" asChild>
            <a href={result.calendly_url} target="_blank" rel="noopener noreferrer">
              {isAr ? "احجز مكالمة الآن" : "Book a call now"}
            </a>
          </Button>
        )}
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="space-y-4" dir={isAr ? "rtl" : "ltr"}>
      <input type="text" name="website" tabIndex={-1} autoComplete="off" aria-hidden="true"
        value={form.website} onChange={(e) => set("website", e.target.value)}
        style={{ position: "absolute", left: "-9999px", width: 1, height: 1 }} />

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <Label htmlFor="li-name">{isAr ? "الاسم *" : "Name *"}</Label>
          <Input id="li-name" className="mt-1.5" value={form.name}
            onChange={(e) => set("name", e.target.value)} required />
        </div>
        <div>
          <Label htmlFor="li-company">{isAr ? "الشركة *" : "Company *"}</Label>
          <Input id="li-company" className="mt-1.5" value={form.company}
            onChange={(e) => set("company", e.target.value)} required />
        </div>
        <div>
          <Label htmlFor="li-email">{isAr ? "البريد *" : "Email *"}</Label>
          <Input id="li-email" type="email" className="mt-1.5" value={form.email}
            onChange={(e) => set("email", e.target.value)} required />
        </div>
        <div>
          <Label htmlFor="li-phone">{isAr ? "الجوال *" : "Phone *"}</Label>
          <Input id="li-phone" className="mt-1.5" value={form.phone} dir="ltr"
            onChange={(e) => set("phone", e.target.value)} required />
        </div>
        <div>
          <Label htmlFor="li-sector">{isAr ? "القطاع" : "Sector"}</Label>
          <Input id="li-sector" className="mt-1.5" value={form.sector}
            onChange={(e) => set("sector", e.target.value)} />
        </div>
        <div>
          <Label htmlFor="li-size">{isAr ? "حجم الفريق" : "Team size"}</Label>
          <Input id="li-size" className="mt-1.5" value={form.size}
            onChange={(e) => set("size", e.target.value)} />
        </div>
      </div>

      <div>
        <Label htmlFor="li-message">{isAr ? "ما التحدي الأكبر في إيراداتك؟" : "Your biggest revenue challenge?"}</Label>
        <textarea id="li-message" value={form.message} rows={3}
          onChange={(e) => set("message", e.target.value)}
          className="mt-1.5 w-full rounded-md border border-input bg-background px-3 py-2 text-sm leading-relaxed" />
      </div>

      <label className="flex items-start gap-2 text-sm">
        <input type="checkbox" checked={form.consent}
          onChange={(e) => set("consent", e.target.checked)} className="mt-1" />
        <span className="text-muted-foreground">
          {isAr
            ? "أوافق على أن يتواصل معي فريق Dealix (PDPL)."
            : "I consent to be contacted by Dealix (PDPL)."}
        </span>
      </label>

      {error && <p className="text-sm text-red-500">{error}</p>}

      <Button type="submit" variant="gold" size="lg" className="w-full" disabled={status === "submitting"}>
        {status === "submitting"
          ? (isAr ? "جارٍ الإرسال…" : "Submitting…")
          : (isAr ? "ابدأ — احجز تشخيصاً" : "Start — book a diagnostic")}
      </Button>

      <p className="text-xs text-muted-foreground text-center">
        {isAr ? "لا إرسال تلقائي — كل تواصل بموافقتك." : "No auto-send — all contact is approval-first."}
      </p>
    </form>
  );
}
