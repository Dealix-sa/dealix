"use client";

import { useMemo, useState } from "react";
import { useLocale } from "next-intl";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { PrimaryCta } from "@/components/wave3/PrimaryCta";
import { Disclaimer } from "@/components/wave3/Disclaimer";
import { calcRevenueLeakage } from "@/lib/wave3/scoring";
import { routeToHref } from "@/lib/wave3/routes";
import { captureLead, type LeadForm } from "@/lib/wave3/leadCapture";
import { revenueLeakage } from "@/content/wave3/tools/revenueLeakage";

const fmt = (n: number) => new Intl.NumberFormat("en-US").format(Math.round(n));

export function RevenueLeakageCalculator() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const tool = revenueLeakage;

  const [inputs, setInputs] = useState({
    monthlyLeads: 100,
    avgDealValue: 5000,
    closeRatePct: 15,
    followupGapPct: 40,
  });
  const [submitted, setSubmitted] = useState(false);
  const [lead, setLead] = useState<LeadForm>({ name: "", email: "", company: "", consent: false });
  const [leadDone, setLeadDone] = useState(false);
  const [busy, setBusy] = useState(false);

  const result = useMemo(() => calcRevenueLeakage(inputs), [inputs]);
  const rec = tool.recommended[result.band];

  function set<K extends keyof typeof inputs>(key: K, value: number) {
    setInputs((p) => ({ ...p, [key]: Number.isFinite(value) ? value : 0 }));
  }

  async function submitLead(e: React.FormEvent) {
    e.preventDefault();
    if (!lead.name || !lead.email || !lead.consent) return;
    setBusy(true);
    await captureLead("tool_revenue_leakage", lead, { score: result.estimateMid, band: result.band, locale });
    setBusy(false);
    setLeadDone(true);
  }

  const fields: { key: keyof typeof inputs; ar: string; en: string }[] = [
    { key: "monthlyLeads", ar: "عدد الفرص الشهرية", en: "Monthly opportunities" },
    { key: "avgDealValue", ar: "متوسط قيمة الصفقة (ريال)", en: "Average deal value (SAR)" },
    { key: "closeRatePct", ar: "معدل الإغلاق الحالي (%)", en: "Current close rate (%)" },
    { key: "followupGapPct", ar: "نسبة الفرص بلا متابعة موثّقة (%)", en: "Opportunities without documented follow-up (%)" },
  ];

  return (
    <div dir={isAr ? "rtl" : "ltr"} className={isAr ? "text-right" : "text-left"}>
      <h1 className="text-3xl font-bold font-display">{isAr ? tool.titleAr : tool.titleEn}</h1>
      <p className="mt-3 text-muted-foreground leading-relaxed">{isAr ? tool.introAr : tool.introEn}</p>

      <Card className="mt-8 p-6">
        <div className="grid gap-4 sm:grid-cols-2">
          {fields.map((f) => (
            <label key={f.key} className="text-sm">
              <span className="text-muted-foreground">{isAr ? f.ar : f.en}</span>
              <input
                type="number"
                min={0}
                className="mt-1 w-full rounded-lg border border-border bg-background px-3 py-2"
                value={inputs[f.key]}
                onChange={(e) => set(f.key, parseFloat(e.target.value))}
              />
            </label>
          ))}
        </div>
        <Button className="mt-5" size="lg" type="button" onClick={() => setSubmitted(true)}>
          {isAr ? "احسب التقدير" : "Calculate estimate"}
        </Button>
      </Card>

      {submitted && (
        <div className="mt-6 space-y-6">
          <Card className="p-6">
            <p className="text-sm text-muted-foreground">
              {isAr ? "تقدير تعليمي للقيمة الشهرية المعرّضة للخطر" : "Educational estimate of monthly value at risk"}
            </p>
            <p className="text-4xl font-bold font-display text-gold-500">
              {fmt(result.estimateLow)} – {fmt(result.estimateHigh)}
            </p>
            <p className="mt-1 text-sm text-muted-foreground">{isAr ? "ريال / شهرياً (تقديري)" : "SAR / month (estimated)"}</p>

            {result.gaps.length > 0 && (
              <div className="mt-6">
                <p className="font-semibold">{isAr ? "أهم الفجوات" : "Top gaps"}</p>
                <ul className="mt-2 list-disc space-y-1 ps-5 text-sm text-muted-foreground">
                  {result.gaps.map((g, i) => (
                    <li key={i}>{isAr ? g.ar : g.en}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="mt-6">
              <p className="font-semibold">{isAr ? "الطبقة المقترحة" : "Recommended Dealix OS"}</p>
              <p className="mt-1 text-sm text-muted-foreground">{isAr ? rec.osAr : rec.osEn}</p>
            </div>

            <div className="mt-6">
              <PrimaryCta
                locale={locale}
                href={routeToHref(rec.nextStep.route)}
                labelAr={rec.nextStep.labelAr}
                labelEn={rec.nextStep.labelEn}
              />
            </div>

            <Disclaimer locale={locale} variant="educational" />
          </Card>

          {!leadDone ? (
            <Card className="p-6">
              <p className="font-semibold">
                {isAr ? "ابعث لي التقدير وملخص الخطوات" : "Send me my estimate and next steps"}
              </p>
              <form onSubmit={submitLead} className="mt-4 grid gap-3">
                <input
                  className="rounded-lg border border-border bg-background px-3 py-2 text-sm"
                  placeholder={isAr ? "الاسم" : "Name"}
                  value={lead.name}
                  onChange={(e) => setLead({ ...lead, name: e.target.value })}
                  required
                />
                <input
                  type="email"
                  className="rounded-lg border border-border bg-background px-3 py-2 text-sm"
                  placeholder={isAr ? "البريد الإلكتروني" : "Email"}
                  value={lead.email}
                  onChange={(e) => setLead({ ...lead, email: e.target.value })}
                  required
                />
                <label className="flex items-start gap-2 text-xs text-muted-foreground">
                  <input
                    type="checkbox"
                    className="mt-0.5"
                    checked={lead.consent}
                    onChange={(e) => setLead({ ...lead, consent: e.target.checked })}
                    required
                  />
                  <span>
                    {isAr
                      ? "أوافق على التواصل معي يدوياً. لن يُرسَل أي شيء تلقائياً."
                      : "I agree to be contacted manually. Nothing is sent automatically."}
                  </span>
                </label>
                <Button type="submit" disabled={busy || !lead.consent}>
                  {busy ? (isAr ? "جارٍ الإرسال…" : "Sending…") : isAr ? "أرسل" : "Send"}
                </Button>
              </form>
            </Card>
          ) : (
            <Card className="p-6 text-sm text-muted-foreground">
              {isAr ? "تم الاستلام. سنتواصل معك يدوياً." : "Got it. We'll reach out manually."}
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
