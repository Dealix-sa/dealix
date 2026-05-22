"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

interface RoiCalculatorProps {
  locale: string;
}

const DEFAULTS = {
  monthlyLeads: 200,
  currentConversionPct: 8,
  avgDealSar: 12000,
  leakagePct: 35, // % of leads with no owner / no evidence / no next action
  recoveryRatePct: 25,
};

const FORMATTER_AR = new Intl.NumberFormat("ar-SA", { maximumFractionDigits: 0 });
const FORMATTER_EN = new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 });

const L = {
  ar: {
    section: "مدخلات الـ funnel",
    monthlyLeads: "Leads شهرياً",
    conversionPct: "معدل التحويل الحالي (%)",
    avgDeal: "متوسط قيمة الصفقة (ريال)",
    leakage: "Leads بلا owner أو دليل (%)",
    recovery: "نسبة الاسترداد بعد Dealix (%)",
    results: "النتائج",
    closedNow: "صفقات مغلقة الآن (شهرياً)",
    closedNowSar: "إيراد محقق الآن (ريال/شهر)",
    atRisk: "Leads معرضة للضياع",
    atRiskSar: "إيراد معرض للضياع (ريال/شهر)",
    recoverable: "قابل للاسترداد بـ Dealix (ريال/شهر)",
    quarterly: "تقدير ربع سنوي",
    payback: "نقطة التعادل لـ Proof Pack (1,500 ر.س)",
    months: "شهر",
    weeks: "أسبوع",
    days: "يوم",
    sameMonth: "نفس الشهر",
    cta: "تشخيص لـ 10 leads بـ 499 ر.س",
    learn: "كيف يعمل Proof Pack",
    disclaimer: "تقديري — ليس وعداً بإيراد. عدّل نسبة الاسترداد حسب نضج فريقك.",
  },
  en: {
    section: "Funnel inputs",
    monthlyLeads: "Leads per month",
    conversionPct: "Current conversion rate (%)",
    avgDeal: "Average deal value (SAR)",
    leakage: "Leads without owner / evidence (%)",
    recovery: "Recovery rate after Dealix (%)",
    results: "Results",
    closedNow: "Deals closed now (monthly)",
    closedNowSar: "Revenue captured now (SAR/mo)",
    atRisk: "Leads at risk",
    atRiskSar: "Revenue at risk (SAR/mo)",
    recoverable: "Recoverable with Dealix (SAR/mo)",
    quarterly: "Quarterly estimate",
    payback: "Proof Pack payback (1,500 SAR)",
    months: "mo",
    weeks: "wk",
    days: "day",
    sameMonth: "same month",
    cta: "10-lead diagnostic — 499 SAR",
    learn: "How Proof Pack works",
    disclaimer: "Estimate — not a revenue promise. Tune the recovery rate to your team maturity.",
  },
} as const;

function paybackLabel(days: number, isAr: boolean, msgs: typeof L.ar) {
  if (days <= 0) return isAr ? "فوري" : "instant";
  if (days <= 30) return `${days} ${msgs.days}`;
  if (days <= 90) {
    const wk = Math.round(days / 7);
    return `${wk} ${msgs.weeks}`;
  }
  const m = Math.round(days / 30);
  if (m <= 1) return msgs.sameMonth;
  return `${m} ${msgs.months}`;
}

export function RoiCalculator({ locale }: RoiCalculatorProps) {
  const isAr = locale === "ar";
  const msgs = isAr ? L.ar : L.en;
  const fmt = isAr ? FORMATTER_AR : FORMATTER_EN;
  const [monthlyLeads, setMonthlyLeads] = useState(DEFAULTS.monthlyLeads);
  const [convPct, setConvPct] = useState(DEFAULTS.currentConversionPct);
  const [avgDeal, setAvgDeal] = useState(DEFAULTS.avgDealSar);
  const [leakage, setLeakage] = useState(DEFAULTS.leakagePct);
  const [recovery, setRecovery] = useState(DEFAULTS.recoveryRatePct);

  const computed = useMemo(() => {
    const closedNow = monthlyLeads * (convPct / 100);
    const closedNowSar = closedNow * avgDeal;
    const leakedLeads = monthlyLeads * (leakage / 100);
    // Each leaked lead has the SAME conversion potential as the average lead.
    // Revenue at risk = leaked leads × conv rate × avg deal value.
    const atRiskSar = leakedLeads * (convPct / 100) * avgDeal;
    const recoverableSar = atRiskSar * (recovery / 100);
    const quarterlyRecoverableSar = recoverableSar * 3;
    const paybackDays = recoverableSar > 0
      ? Math.ceil((1500 / recoverableSar) * 30)
      : Infinity;
    return {
      closedNow: Math.round(closedNow),
      closedNowSar: Math.round(closedNowSar),
      leakedLeads: Math.round(leakedLeads),
      atRiskSar: Math.round(atRiskSar),
      recoverableSar: Math.round(recoverableSar),
      quarterlyRecoverableSar: Math.round(quarterlyRecoverableSar),
      paybackDays,
    };
  }, [monthlyLeads, convPct, avgDeal, leakage, recovery]);

  return (
    <div className="mt-10 grid gap-8 lg:grid-cols-[1fr_1fr]">
      {/* Inputs */}
      <section className="space-y-5 rounded-lg border border-border/60 bg-card/30 p-6">
        <h2 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
          {msgs.section}
        </h2>
        <NumberField label={msgs.monthlyLeads} value={monthlyLeads} onChange={setMonthlyLeads} min={1} step={10} />
        <RangeField label={msgs.conversionPct} value={convPct} onChange={setConvPct} min={0.5} max={40} step={0.5} format={(v) => `${v}%`} />
        <NumberField label={msgs.avgDeal} value={avgDeal} onChange={setAvgDeal} min={500} step={500} />
        <RangeField label={msgs.leakage} value={leakage} onChange={setLeakage} min={0} max={90} step={1} format={(v) => `${v}%`} />
        <RangeField label={msgs.recovery} value={recovery} onChange={setRecovery} min={0} max={80} step={1} format={(v) => `${v}%`} />
      </section>

      {/* Results */}
      <section className="space-y-4 rounded-lg border border-primary/40 bg-primary/5 p-6">
        <h2 className="text-sm font-semibold uppercase tracking-wider text-primary">
          {msgs.results}
        </h2>
        <ResultRow label={msgs.closedNow} value={fmt.format(computed.closedNow)} />
        <ResultRow label={msgs.closedNowSar} value={`${fmt.format(computed.closedNowSar)} ${isAr ? "ر.س" : "SAR"}`} />
        <hr className="border-border/60" />
        <ResultRow label={msgs.atRisk} value={fmt.format(computed.leakedLeads)} accent />
        <ResultRow label={msgs.atRiskSar} value={`${fmt.format(computed.atRiskSar)} ${isAr ? "ر.س" : "SAR"}`} accent />
        <hr className="border-border/60" />
        <ResultRow label={msgs.recoverable} value={`${fmt.format(computed.recoverableSar)} ${isAr ? "ر.س" : "SAR"}`} bold />
        <ResultRow label={msgs.quarterly} value={`${fmt.format(computed.quarterlyRecoverableSar)} ${isAr ? "ر.س" : "SAR"}`} bold />
        <ResultRow label={msgs.payback} value={paybackLabel(computed.paybackDays, isAr, msgs)} bold />

        <p className="pt-3 text-xs text-muted-foreground leading-relaxed">{msgs.disclaimer}</p>

        <div className="flex flex-wrap gap-3 pt-2">
          <Link
            href={`/${locale}/billing?sku=pilot_managed`}
            className="inline-flex items-center justify-center rounded-md bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground transition hover:bg-primary/90"
          >
            {msgs.cta}
          </Link>
          <Link
            href={`/${locale}/proof-pack`}
            className="inline-flex items-center justify-center rounded-md border border-border/80 px-5 py-2.5 text-sm font-medium hover:bg-card/60"
          >
            {msgs.learn} →
          </Link>
        </div>
      </section>
    </div>
  );
}

interface NumberFieldProps {
  label: string;
  value: number;
  onChange: (v: number) => void;
  min?: number;
  step?: number;
}

function NumberField({ label, value, onChange, min, step }: NumberFieldProps) {
  return (
    <label className="block">
      <span className="text-sm font-medium">{label}</span>
      <input
        type="number"
        value={value}
        min={min}
        step={step}
        onChange={(e) => onChange(Number(e.target.value) || 0)}
        className="mt-2 w-full rounded-md border border-border bg-card/40 px-3 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
      />
    </label>
  );
}

interface RangeFieldProps {
  label: string;
  value: number;
  onChange: (v: number) => void;
  min: number;
  max: number;
  step: number;
  format?: (v: number) => string;
}

function RangeField({ label, value, onChange, min, max, step, format }: RangeFieldProps) {
  return (
    <label className="block">
      <div className="flex items-center justify-between text-sm font-medium">
        <span>{label}</span>
        <span className="font-mono text-xs text-muted-foreground">{format ? format(value) : value}</span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="mt-2 w-full accent-primary"
      />
    </label>
  );
}

interface ResultRowProps {
  label: string;
  value: string;
  accent?: boolean;
  bold?: boolean;
}

function ResultRow({ label, value, accent, bold }: ResultRowProps) {
  return (
    <div className="flex items-baseline justify-between gap-4">
      <span className={`text-sm ${accent ? "text-destructive" : "text-muted-foreground"}`}>{label}</span>
      <span className={`font-mono ${bold ? "text-xl font-semibold" : "text-base"} ${accent ? "text-destructive" : ""}`}>
        {value}
      </span>
    </div>
  );
}
