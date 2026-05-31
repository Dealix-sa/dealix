// from __future__ import annotations
"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useState, useMemo } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const DEALIX_MONTHLY_COST = 3498; // 499 sprint + 2999 managed
const DEALIX_ANNUAL_COST = DEALIX_MONTHLY_COST * 12;
const CONV_IMPROVEMENT = 1.25; // +25% relative
const CHURN_IMPROVEMENT = 0.7; // -30% relative

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface CalcInputs {
  monthlyLeads: number;
  conversionRate: number; // percent 0-100
  avgDealSize: number; // SAR
  churnRate: number; // percent 0-100
}

interface CalcOutputs {
  currentMonthlyRevenue: number;
  newConversionRate: number;
  newChurnRate: number;
  newMonthlyRevenue: number;
  monthlyUplift: number;
  annualUplift: number;
  dealixMonthlyCost: number;
  dealixAnnualCost: number;
  netRoiPct: number;
  paybackMonths: number;
}

// ---------------------------------------------------------------------------
// Pure calculation
// ---------------------------------------------------------------------------

function compute(inputs: CalcInputs): CalcOutputs {
  const { monthlyLeads, conversionRate, avgDealSize, churnRate } = inputs;

  const currentConvFraction = conversionRate / 100;
  const currentMonthlyRevenue = monthlyLeads * currentConvFraction * avgDealSize;

  const newConvFraction = currentConvFraction * CONV_IMPROVEMENT;
  const newConversionRate = newConvFraction * 100;
  const newChurnRate = churnRate * CHURN_IMPROVEMENT;

  // Churn reduction adds retained revenue — modelled as an uplift multiplier.
  // Retained MRR uplift = currentMRR * churnRateReduction
  const churnRateReduction = (churnRate - newChurnRate) / 100;
  const conversionUplift = monthlyLeads * (newConvFraction - currentConvFraction) * avgDealSize;
  const retentionUplift = currentMonthlyRevenue * churnRateReduction;
  const newMonthlyRevenue = currentMonthlyRevenue + conversionUplift + retentionUplift;

  const monthlyUplift = newMonthlyRevenue - currentMonthlyRevenue;
  const annualUplift = monthlyUplift * 12;

  const netRoiPct =
    DEALIX_ANNUAL_COST > 0
      ? ((annualUplift - DEALIX_ANNUAL_COST) / DEALIX_ANNUAL_COST) * 100
      : 0;

  const paybackMonths =
    monthlyUplift > DEALIX_MONTHLY_COST
      ? DEALIX_MONTHLY_COST / (monthlyUplift - DEALIX_MONTHLY_COST)
      : Infinity;

  return {
    currentMonthlyRevenue,
    newConversionRate,
    newChurnRate,
    newMonthlyRevenue,
    monthlyUplift,
    annualUplift,
    dealixMonthlyCost: DEALIX_MONTHLY_COST,
    dealixAnnualCost: DEALIX_ANNUAL_COST,
    netRoiPct,
    paybackMonths,
  };
}

// ---------------------------------------------------------------------------
// Formatting helpers
// ---------------------------------------------------------------------------

function formatSar(value: number): string {
  return new Intl.NumberFormat("en-SA", {
    style: "decimal",
    maximumFractionDigits: 0,
  }).format(Math.round(value));
}

function formatPct(value: number, decimals = 1): string {
  return `${value.toFixed(decimals)}%`;
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

interface NumericInputProps {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  onChange: (v: number) => void;
  suffix?: string;
}

function NumericInput({ label, value, min, max, step, onChange, suffix }: NumericInputProps) {
  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <label className="text-sm font-medium">{label}</label>
        <span className="text-sm font-bold text-[var(--dealix-navy)]">
          {formatSar(value)}{suffix ? ` ${suffix}` : ""}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full accent-[var(--dealix-gold)] cursor-pointer"
      />
      <div className="flex justify-between text-xs text-muted-foreground">
        <span>{formatSar(min)}</span>
        <span>{formatSar(max)}</span>
      </div>
    </div>
  );
}

interface MetricRowProps {
  label: string;
  without: string;
  withDealix: string;
  highlight?: boolean;
}

function MetricRow({ label, without, withDealix, highlight = false }: MetricRowProps) {
  return (
    <tr className={highlight ? "bg-[var(--dealix-gold)]/10" : undefined}>
      <td className="py-3 px-4 text-sm text-muted-foreground border-b border-border/40">{label}</td>
      <td className="py-3 px-4 text-sm text-center border-b border-border/40">{without}</td>
      <td
        className={`py-3 px-4 text-sm text-center font-semibold border-b border-border/40 ${
          highlight
            ? "text-[var(--dealix-gold)] text-base"
            : "text-[var(--dealix-navy)]"
        }`}
      >
        {withDealix}
      </td>
    </tr>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export function ROICalculator() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [inputs, setInputs] = useState<CalcInputs>({
    monthlyLeads: 50,
    conversionRate: 8,
    avgDealSize: 8000,
    churnRate: 5,
  });

  const results = useMemo(() => compute(inputs), [inputs]);

  const set = <K extends keyof CalcInputs>(key: K, value: number) =>
    setInputs((prev) => ({ ...prev, [key]: value }));

  const t = {
    title: isAr ? "حاسبة العائد على الاستثمار" : "ROI Estimator",
    subtitle: isAr
      ? "تقدير تأثير Dealix على إيراداتك — أرقام تقديرية مبنية على متوسطات السوق"
      : "Estimate Dealix's impact on your revenue — figures are projections based on market averages",
    inputsHeader: isAr ? "المعطيات" : "Your Inputs",
    monthlyLeads: isAr ? "عدد العملاء المحتملين شهرياً" : "Monthly Leads",
    convRate: isAr ? "معدل التحويل الحالي" : "Current Conversion Rate",
    dealSize: isAr ? "متوسط حجم الصفقة (ر.س)" : "Average Deal Size (SAR)",
    churnRate: isAr ? "معدل التراجع الشهري الحالي" : "Current Monthly Churn Rate",
    comparisonHeader: isAr ? "المقارنة" : "Comparison",
    withoutDealix: isAr ? "بدون Dealix" : "Without Dealix",
    withDealix: isAr ? "مع Dealix" : "With Dealix",
    rowConv: isAr ? "معدل التحويل (تقديري)" : "Conversion Rate (estimated)",
    rowChurn: isAr ? "معدل التراجع (تقديري)" : "Churn Rate (estimated)",
    rowMonthlyRev: isAr ? "الإيراد الشهري (ر.س)" : "Monthly Revenue (SAR)",
    rowMonthlyUplift: isAr ? "فائض شهري (ر.س)" : "Monthly Uplift (SAR)",
    rowDealixCost: isAr ? "تكلفة Dealix / شهر (ر.س)" : "Dealix Cost / Month (SAR)",
    rowAnnualUplift: isAr ? "الفائض السنوي المتوقع (ر.س)" : "Projected Annual Uplift (SAR)",
    rowNetRoi: isAr ? "صافي العائد على الاستثمار (تقديري)" : "Net ROI % (estimated)",
    rowPayback: isAr ? "فترة الاسترداد (تقديرية)" : "Payback Period (estimated)",
    annualUpliftLabel: isAr ? "الفائض السنوي التقديري" : "Projected Annual Uplift",
    months: isAr ? "شهر" : "mo",
    disclaimer: isAr
      ? "توقعات مبنية على متوسطات السوق السعودي — النتائج الفعلية تتفاوت"
      : "Projections based on Saudi market averages — actual results vary",
    ctaLabel: isAr
      ? "احصل على حسابك الدقيق — Sprint مجاني أول 7 أيام"
      : "Get Your Precise Estimate — First 7-Day Sprint Free",
    projectionNote: isAr ? "تقديري" : "est.",
  };

  const paybackDisplay =
    results.paybackMonths === Infinity
      ? isAr
        ? "أكثر من 12 شهر"
        : "> 12 months"
      : results.paybackMonths < 1
      ? isAr
        ? "أقل من شهر"
        : "< 1 month"
      : `${results.paybackMonths.toFixed(1)} ${t.months}`;

  return (
    <div
      className="max-w-3xl mx-auto space-y-6"
      dir={isAr ? "rtl" : "ltr"}
    >
      {/* Header */}
      <div className={isAr ? "text-right" : "text-left"}>
        <h2 className="text-2xl font-bold text-[var(--dealix-navy)]">{t.title}</h2>
        <p className="mt-1 text-sm text-muted-foreground">{t.subtitle}</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Inputs */}
        <Card className="p-5 space-y-5">
          <h3 className="font-semibold text-[var(--dealix-navy)] border-b border-border/40 pb-2">
            {t.inputsHeader}
          </h3>

          <NumericInput
            label={t.monthlyLeads}
            value={inputs.monthlyLeads}
            min={5}
            max={500}
            step={5}
            onChange={(v) => set("monthlyLeads", v)}
          />

          <NumericInput
            label={t.convRate}
            value={inputs.conversionRate}
            min={1}
            max={50}
            step={0.5}
            onChange={(v) => set("conversionRate", v)}
            suffix="%"
          />

          <NumericInput
            label={t.dealSize}
            value={inputs.avgDealSize}
            min={1000}
            max={100000}
            step={500}
            onChange={(v) => set("avgDealSize", v)}
            suffix="SAR"
          />

          <NumericInput
            label={t.churnRate}
            value={inputs.churnRate}
            min={1}
            max={30}
            step={0.5}
            onChange={(v) => set("churnRate", v)}
            suffix="%"
          />
        </Card>

        {/* Annual uplift highlight */}
        <div className="flex flex-col gap-4">
          <Card className="p-5 border-[var(--dealix-gold)] bg-[var(--dealix-gold)]/5 flex flex-col items-center justify-center text-center gap-2 flex-1">
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--dealix-gold)]">
              {t.annualUpliftLabel}
            </p>
            <p className="text-4xl font-black text-[var(--dealix-gold)] tabular-nums">
              {formatSar(results.annualUplift)} SAR
            </p>
            <p className="text-xs text-muted-foreground">
              {isAr ? "تقدير — راجع التنويه أدناه" : "estimate — see disclaimer below"}
            </p>
          </Card>

          <Card className="p-5 space-y-3">
            <div className="flex justify-between items-center text-sm">
              <span className="text-muted-foreground">
                {isAr ? `صافي عائد (${t.projectionNote})` : `Net ROI (${t.projectionNote})`}
              </span>
              <span
                className={`font-bold ${
                  results.netRoiPct >= 0
                    ? "text-[var(--dealix-success)]"
                    : "text-[var(--dealix-error)]"
                }`}
              >
                {formatPct(results.netRoiPct, 0)}
              </span>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-muted-foreground">
                {isAr ? `فترة الاسترداد (${t.projectionNote})` : `Payback (${t.projectionNote})`}
              </span>
              <span className="font-bold text-[var(--dealix-navy)]">{paybackDisplay}</span>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-muted-foreground">
                {isAr ? "تكلفة Dealix / شهر" : "Dealix Cost / Month"}
              </span>
              <span className="font-medium">{formatSar(DEALIX_MONTHLY_COST)} SAR</span>
            </div>
          </Card>
        </div>
      </div>

      {/* Comparison table */}
      <Card className="overflow-hidden">
        <div className="p-4 border-b border-border/40">
          <h3 className="font-semibold text-[var(--dealix-navy)]">{t.comparisonHeader}</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr>
                <th className="py-3 px-4 text-sm font-medium text-muted-foreground text-start bg-muted/30">
                  {isAr ? "المقياس" : "Metric"}
                </th>
                <th className="py-3 px-4 text-sm font-medium text-center bg-muted/30">
                  {t.withoutDealix}
                </th>
                <th className="py-3 px-4 text-sm font-medium text-center bg-[var(--dealix-gold)]/10 text-[var(--dealix-gold)]">
                  {t.withDealix}
                </th>
              </tr>
            </thead>
            <tbody>
              <MetricRow
                label={t.rowConv}
                without={formatPct(inputs.conversionRate)}
                withDealix={`${formatPct(results.newConversionRate)} (+25% ${t.projectionNote})`}
              />
              <MetricRow
                label={t.rowChurn}
                without={formatPct(inputs.churnRate)}
                withDealix={`${formatPct(results.newChurnRate)} (-30% ${t.projectionNote})`}
              />
              <MetricRow
                label={t.rowMonthlyRev}
                without={`${formatSar(results.currentMonthlyRevenue)} SAR`}
                withDealix={`${formatSar(results.newMonthlyRevenue)} SAR`}
              />
              <MetricRow
                label={t.rowMonthlyUplift}
                without="—"
                withDealix={`+${formatSar(results.monthlyUplift)} SAR`}
              />
              <MetricRow
                label={t.rowDealixCost}
                without="—"
                withDealix={`${formatSar(DEALIX_MONTHLY_COST)} SAR`}
              />
              <MetricRow
                label={t.rowAnnualUplift}
                without="—"
                withDealix={`${formatSar(results.annualUplift)} SAR`}
                highlight
              />
              <MetricRow
                label={t.rowNetRoi}
                without="—"
                withDealix={formatPct(results.netRoiPct, 0)}
              />
              <MetricRow
                label={t.rowPayback}
                without="—"
                withDealix={paybackDisplay}
              />
            </tbody>
          </table>
        </div>
      </Card>

      {/* Disclaimer */}
      <p className="text-xs text-muted-foreground border border-border/40 rounded-lg p-3 bg-muted/20">
        <strong>{isAr ? "تنويه: " : "Disclaimer: "}</strong>
        {t.disclaimer}
      </p>

      {/* CTA */}
      <Button
        asChild
        className="w-full bg-[var(--dealix-navy)] hover:bg-[var(--dealix-navy-hover)] text-white font-semibold py-3 text-base"
        size="lg"
      >
        <Link href={`/${locale}/dealix-diagnostic`}>{t.ctaLabel}</Link>
      </Button>
    </div>
  );
}
