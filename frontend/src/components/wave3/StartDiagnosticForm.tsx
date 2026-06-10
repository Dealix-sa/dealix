"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Disclaimer } from "@/components/wave3/Disclaimer";
import { captureLead, type LeadForm } from "@/lib/wave3/leadCapture";

export function StartDiagnosticForm() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [form, setForm] = useState<LeadForm & { note: string }>({
    name: "",
    email: "",
    company: "",
    consent: false,
    note: "",
  });
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.name || !form.email || !form.consent) return;
    setBusy(true);
    await captureLead("start_diagnostic", form, { locale });
    setBusy(false);
    setDone(true);
  }

  return (
    <div dir={isAr ? "rtl" : "ltr"} className={isAr ? "text-right" : "text-left"}>
      <h1 className="text-3xl font-bold font-display md:text-4xl">
        {isAr ? "ابدأ التشخيص" : "Start your diagnostic"}
      </h1>
      <p className="mt-3 text-muted-foreground leading-relaxed">
        {isAr
          ? "أرسل تشخيصاً مختصراً وسنتواصل معك يدوياً لنرى هل يناسبك Command Sprint. لا إرسال تلقائي."
          : "Submit a short diagnostic and we'll reach out manually to see if a Command Sprint fits. No automated sending."}
      </p>

      {!done ? (
        <Card className="mt-8 p-6">
          <form onSubmit={submit} className="grid gap-3">
            <input
              className="rounded-lg border border-border bg-background px-3 py-2 text-sm"
              placeholder={isAr ? "الاسم" : "Name"}
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              required
            />
            <input
              type="email"
              className="rounded-lg border border-border bg-background px-3 py-2 text-sm"
              placeholder={isAr ? "البريد الإلكتروني" : "Email"}
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              required
            />
            <input
              className="rounded-lg border border-border bg-background px-3 py-2 text-sm"
              placeholder={isAr ? "الشركة" : "Company"}
              value={form.company}
              onChange={(e) => setForm({ ...form, company: e.target.value })}
            />
            <textarea
              className="min-h-24 rounded-lg border border-border bg-background px-3 py-2 text-sm"
              placeholder={isAr ? "أين تشعر أن فرصك تتعطل؟" : "Where do your opportunities stall?"}
              value={form.note}
              onChange={(e) => setForm({ ...form, note: e.target.value })}
            />
            <label className="flex items-start gap-2 text-xs text-muted-foreground">
              <input
                type="checkbox"
                className="mt-0.5"
                checked={form.consent}
                onChange={(e) => setForm({ ...form, consent: e.target.checked })}
                required
              />
              <span>
                {isAr
                  ? "أوافق على التواصل معي يدوياً بخصوص هذا الطلب."
                  : "I agree to be contacted manually about this request."}
              </span>
            </label>
            <Button type="submit" size="lg" disabled={busy || !form.consent}>
              {busy ? (isAr ? "جارٍ الإرسال…" : "Submitting…") : isAr ? "أرسل التشخيص" : "Submit Diagnostic"}
            </Button>
          </form>
          <Disclaimer locale={locale} />
        </Card>
      ) : (
        <Card className="mt-8 p-6 text-sm text-muted-foreground">
          {isAr
            ? "تم استلام طلبك. سنتواصل معك يدوياً قريباً — بدون أي إرسال تلقائي."
            : "Your request was received. We'll reach out manually soon — with no automated sending."}
        </Card>
      )}
    </div>
  );
}
