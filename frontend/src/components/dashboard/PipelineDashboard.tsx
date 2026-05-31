"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type PipelineStageKey =
  | "lead"
  | "qualified"
  | "diagnostic_sent"
  | "sprint_proposed"
  | "sprint_active"
  | "closed_won"
  | "closed_lost";

interface StageConfig {
  key: PipelineStageKey;
  labelAr: string;
  labelEn: string;
  color: string;
  badgeBg: string;
  badgeText: string;
}

interface StageSummary {
  stage: PipelineStageKey;
  count: number;
  totalValueSar: number;
}

interface Deal {
  id: string;
  companyNameAr: string;
  companyNameEn: string;
  stage: PipelineStageKey;
  valueSar: number;
  probability: number;
  daysInStage: number;
  nextActionAr: string;
  nextActionEn: string;
  hasNextAction: boolean;
}

interface ForecastCard {
  labelAr: string;
  labelEn: string;
  days: number;
  weightedValueSar: number;
  dealCount: number;
}

// ---------------------------------------------------------------------------
// Static configuration
// ---------------------------------------------------------------------------

const STAGE_CONFIGS: StageConfig[] = [
  {
    key: "lead",
    labelAr: "عميل محتمل",
    labelEn: "Lead",
    color: "#94a3b8",
    badgeBg: "bg-slate-100",
    badgeText: "text-slate-700",
  },
  {
    key: "qualified",
    labelAr: "مؤهل",
    labelEn: "Qualified",
    color: "#60a5fa",
    badgeBg: "bg-blue-100",
    badgeText: "text-blue-700",
  },
  {
    key: "diagnostic_sent",
    labelAr: "تشخيص أُرسل",
    labelEn: "Diagnostic Sent",
    color: "#a78bfa",
    badgeBg: "bg-violet-100",
    badgeText: "text-violet-700",
  },
  {
    key: "sprint_proposed",
    labelAr: "Sprint مقترح",
    labelEn: "Sprint Proposed",
    color: "#fb923c",
    badgeBg: "bg-orange-100",
    badgeText: "text-orange-700",
  },
  {
    key: "sprint_active",
    labelAr: "Sprint نشط",
    labelEn: "Sprint Active",
    color: "#facc15",
    badgeBg: "bg-yellow-100",
    badgeText: "text-yellow-800",
  },
  {
    key: "closed_won",
    labelAr: "مُغلق - ربح",
    labelEn: "Closed Won",
    color: "#10b981",
    badgeBg: "bg-emerald-100",
    badgeText: "text-emerald-700",
  },
  {
    key: "closed_lost",
    labelAr: "مُغلق - خسارة",
    labelEn: "Closed Lost",
    color: "#ef4444",
    badgeBg: "bg-red-100",
    badgeText: "text-red-700",
  },
];

// ---------------------------------------------------------------------------
// Hardcoded mock data
// ---------------------------------------------------------------------------

const STAGE_SUMMARIES: StageSummary[] = [
  { stage: "lead", count: 18, totalValueSar: 9_200_000 },
  { stage: "qualified", count: 11, totalValueSar: 7_800_000 },
  { stage: "diagnostic_sent", count: 7, totalValueSar: 5_600_000 },
  { stage: "sprint_proposed", count: 5, totalValueSar: 4_500_000 },
  { stage: "sprint_active", count: 3, totalValueSar: 2_800_000 },
  { stage: "closed_won", count: 8, totalValueSar: 6_400_000 },
  { stage: "closed_lost", count: 4, totalValueSar: 2_100_000 },
];

const TOP_DEALS: Deal[] = [
  {
    id: "D-001",
    companyNameAr: "مجموعة السدير للصناعات",
    companyNameEn: "Al-Sudair Industries Group",
    stage: "sprint_active",
    valueSar: 1_200_000,
    probability: 75,
    daysInStage: 5,
    nextActionAr: "مراجعة Proof Pack مع المؤسس",
    nextActionEn: "Review Proof Pack with founder",
    hasNextAction: true,
  },
  {
    id: "D-002",
    companyNameAr: "شركة التقنية المتطورة",
    companyNameEn: "Advanced Tech Co.",
    stage: "sprint_proposed",
    valueSar: 980_000,
    probability: 55,
    daysInStage: 9,
    nextActionAr: "متابعة قرار الموافقة على الميزانية",
    nextActionEn: "Follow up on budget approval decision",
    hasNextAction: true,
  },
  {
    id: "D-003",
    companyNameAr: "مجموعة المستقبل التجارية",
    companyNameEn: "Al-Mustaqbal Trading Group",
    stage: "diagnostic_sent",
    valueSar: 860_000,
    probability: 40,
    daysInStage: 12,
    nextActionAr: "جدولة مكالمة مراجعة التشخيص",
    nextActionEn: "Schedule diagnostic review call",
    hasNextAction: true,
  },
  {
    id: "D-004",
    companyNameAr: "شركة النخبة للخدمات",
    companyNameEn: "Elite Services Co.",
    stage: "qualified",
    valueSar: 720_000,
    probability: 30,
    daysInStage: 18,
    nextActionAr: "لم تُحدد بعد",
    nextActionEn: "Not yet defined",
    hasNextAction: false,
  },
  {
    id: "D-005",
    companyNameAr: "مجموعة الأمانة اللوجستية",
    companyNameEn: "Al-Amanah Logistics Group",
    stage: "sprint_proposed",
    valueSar: 650_000,
    probability: 60,
    daysInStage: 7,
    nextActionAr: "إرسال العقد للمراجعة القانونية",
    nextActionEn: "Send contract for legal review",
    hasNextAction: true,
  },
];

const FORECAST_CARDS: ForecastCard[] = [
  {
    labelAr: "التوقعات — 30 يوماً",
    labelEn: "30-Day Forecast",
    days: 30,
    weightedValueSar: 2_340_000,
    dealCount: 4,
  },
  {
    labelAr: "التوقعات — 60 يوماً",
    labelEn: "60-Day Forecast",
    days: 60,
    weightedValueSar: 4_870_000,
    dealCount: 9,
  },
  {
    labelAr: "التوقعات — 90 يوماً",
    labelEn: "90-Day Forecast",
    days: 90,
    weightedValueSar: 7_650_000,
    dealCount: 15,
  },
];

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function formatSar(value: number, locale: string): string {
  const formatted = new Intl.NumberFormat(locale === "ar" ? "ar-SA" : "en-SA", {
    style: "currency",
    currency: "SAR",
    maximumFractionDigits: 0,
  }).format(value);
  return formatted;
}

function getStageMeta(key: PipelineStageKey): StageConfig {
  return STAGE_CONFIGS.find((s) => s.key === key) ?? STAGE_CONFIGS[0];
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function StageBadge({ stageKey, locale }: { stageKey: PipelineStageKey; locale: string }) {
  const meta = getStageMeta(stageKey);
  return (
    <span
      className={cn(
        "inline-block rounded-full px-2 py-0.5 text-xs font-medium",
        meta.badgeBg,
        meta.badgeText,
      )}
    >
      {locale === "ar" ? meta.labelAr : meta.labelEn}
    </span>
  );
}

function PipelineKanbanStrip({ locale }: { locale: string }) {
  const isAr = locale === "ar";
  return (
    <div className="grid grid-cols-7 gap-2">
      {STAGE_CONFIGS.map((stage) => {
        const summary = STAGE_SUMMARIES.find((s) => s.stage === stage.key);
        const count = summary?.count ?? 0;
        const value = summary?.totalValueSar ?? 0;
        return (
          <div
            key={stage.key}
            className="flex flex-col items-center rounded-xl border border-gray-100 bg-white p-3 shadow-sm"
          >
            <div
              className="mb-2 h-1.5 w-full rounded-full"
              style={{ backgroundColor: stage.color }}
            />
            <span className="mb-1 text-center text-xs font-semibold leading-tight text-gray-700">
              {isAr ? stage.labelAr : stage.labelEn}
            </span>
            <span
              className="mb-1 flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold text-white"
              style={{ backgroundColor: stage.color }}
            >
              {count}
            </span>
            <span className="text-center text-xs text-gray-500">
              {isAr
                ? `${(value / 1_000_000).toFixed(1)} م`
                : `${(value / 1_000_000).toFixed(1)}M`}
            </span>
          </div>
        );
      })}
    </div>
  );
}

function TopDealsTable({ locale }: { locale: string }) {
  const isAr = locale === "ar";
  return (
    <div className="overflow-x-auto rounded-xl border border-gray-100 bg-white shadow-sm">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-100 bg-gray-50 text-xs font-semibold uppercase tracking-wide text-gray-500">
            <th className={cn("px-4 py-3", isAr ? "text-right" : "text-left")}>
              {isAr ? "الشركة" : "Company"}
            </th>
            <th className={cn("px-4 py-3", isAr ? "text-right" : "text-left")}>
              {isAr ? "المرحلة" : "Stage"}
            </th>
            <th className={cn("px-4 py-3 text-right")}>
              {isAr ? "القيمة" : "Value (SAR)"}
            </th>
            <th className="px-4 py-3 text-center">
              {isAr ? "الاحتمالية" : "Probability"}
            </th>
            <th className="px-4 py-3 text-center">
              {isAr ? "أيام في المرحلة" : "Days in Stage"}
            </th>
            <th className={cn("px-4 py-3", isAr ? "text-right" : "text-left")}>
              {isAr ? "الخطوة التالية" : "Next Action"}
            </th>
            <th className="px-4 py-3 text-center">
              {isAr ? "إجراء" : "Action"}
            </th>
          </tr>
        </thead>
        <tbody>
          {TOP_DEALS.map((deal, idx) => (
            <tr
              key={deal.id}
              className={cn(
                "border-b border-gray-50 transition-colors hover:bg-gray-50",
                idx % 2 === 0 ? "bg-white" : "bg-gray-50/40",
              )}
            >
              <td className={cn("px-4 py-3 font-medium text-gray-900", isAr ? "text-right" : "text-left")}>
                <div>{isAr ? deal.companyNameAr : deal.companyNameEn}</div>
                <div className="text-xs font-normal text-gray-400">{deal.id}</div>
              </td>
              <td className={cn("px-4 py-3", isAr ? "text-right" : "text-left")}>
                <StageBadge stageKey={deal.stage} locale={locale} />
              </td>
              <td className="px-4 py-3 text-right font-semibold text-gray-800">
                {formatSar(deal.valueSar, locale)}
              </td>
              <td className="px-4 py-3 text-center">
                <div className="flex items-center justify-center gap-2">
                  <div className="h-1.5 w-16 rounded-full bg-gray-200">
                    <div
                      className={cn(
                        "h-1.5 rounded-full",
                        deal.probability >= 70
                          ? "bg-emerald-500"
                          : deal.probability >= 45
                          ? "bg-amber-400"
                          : "bg-slate-400",
                      )}
                      style={{ width: `${deal.probability}%` }}
                    />
                  </div>
                  <span className="w-8 text-xs text-gray-500">{deal.probability}%</span>
                </div>
              </td>
              <td className="px-4 py-3 text-center">
                <span
                  className={cn(
                    "inline-block rounded-full px-2 py-0.5 text-xs font-medium",
                    deal.daysInStage > 14
                      ? "bg-red-100 text-red-600"
                      : deal.daysInStage > 7
                      ? "bg-amber-100 text-amber-700"
                      : "bg-green-100 text-green-700",
                  )}
                >
                  {deal.daysInStage}
                </span>
              </td>
              <td
                className={cn(
                  "px-4 py-3 text-xs",
                  isAr ? "text-right" : "text-left",
                  deal.hasNextAction ? "text-gray-700" : "text-red-400 font-medium",
                )}
              >
                {isAr ? deal.nextActionAr : deal.nextActionEn}
              </td>
              <td className="px-4 py-3 text-center">
                <button
                  type="button"
                  className="rounded-md border border-gray-200 bg-white px-3 py-1 text-xs font-medium text-gray-600 shadow-sm transition-colors hover:border-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1"
                >
                  {isAr ? "تقدّم" : "Advance"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ForecastStrip({ locale }: { locale: string }) {
  const isAr = locale === "ar";
  return (
    <div className="grid grid-cols-3 gap-4">
      {FORECAST_CARDS.map((card) => (
        <div
          key={card.days}
          className="rounded-xl border border-blue-100 bg-gradient-to-br from-blue-50 to-white p-4 shadow-sm"
        >
          <div className="mb-1 text-xs font-semibold uppercase tracking-wide text-blue-500">
            {isAr ? card.labelAr : card.labelEn}
          </div>
          <div className="mb-1 text-2xl font-bold text-gray-900">
            {isAr
              ? `${(card.weightedValueSar / 1_000_000).toFixed(2)} م.ر`
              : `SAR ${(card.weightedValueSar / 1_000_000).toFixed(2)}M`}
          </div>
          <div className="text-xs text-gray-500">
            {isAr
              ? `${card.dealCount} صفقة مرجّحة`
              : `${card.dealCount} weighted deals`}
          </div>
        </div>
      ))}
    </div>
  );
}

function PipelineHealthIndicator({ locale }: { locale: string }) {
  const isAr = locale === "ar";

  const dealsWithNextAction = TOP_DEALS.filter((d) => d.hasNextAction).length;
  const stalledDeals = TOP_DEALS.filter((d) => d.daysInStage > 14);
  const healthPct = Math.round((dealsWithNextAction / TOP_DEALS.length) * 100);

  return (
    <div className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
      <div className="mb-3 flex items-center justify-between">
        <span className="text-sm font-semibold text-gray-800">
          {isAr ? "صحة خط الأنابيب" : "Pipeline Health"}
        </span>
        <span
          className={cn(
            "rounded-full px-2 py-0.5 text-xs font-semibold",
            healthPct >= 70
              ? "bg-emerald-100 text-emerald-700"
              : healthPct >= 45
              ? "bg-amber-100 text-amber-700"
              : "bg-red-100 text-red-700",
          )}
        >
          {healthPct}%
        </span>
      </div>

      <div className="mb-3">
        <div className="mb-1 flex justify-between text-xs text-gray-500">
          <span>
            {isAr
              ? "الصفقات ذات خطوة تالية محددة"
              : "Deals with next action defined"}
          </span>
          <span>
            {dealsWithNextAction}/{TOP_DEALS.length}
          </span>
        </div>
        <div className="h-2 w-full rounded-full bg-gray-100">
          <div
            className={cn(
              "h-2 rounded-full transition-all",
              healthPct >= 70
                ? "bg-emerald-500"
                : healthPct >= 45
                ? "bg-amber-400"
                : "bg-red-500",
            )}
            style={{ width: `${healthPct}%` }}
          />
        </div>
      </div>

      {stalledDeals.length > 0 && (
        <div className="rounded-lg border border-amber-200 bg-amber-50 p-3">
          <div className="flex items-start gap-2">
            <div className="mt-0.5 h-2 w-2 flex-shrink-0 rounded-full bg-amber-500" />
            <div>
              <div className="text-xs font-semibold text-amber-700">
                {isAr
                  ? `${stalledDeals.length} صفقة متوقفة (أكثر من 14 يوماً)`
                  : `${stalledDeals.length} stalled deal${stalledDeals.length > 1 ? "s" : ""} (14+ days)`}
              </div>
              <div className="mt-1 text-xs text-amber-600">
                {stalledDeals
                  .map((d) => (isAr ? d.companyNameAr : d.companyNameEn))
                  .join(isAr ? "، " : ", ")}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export default function PipelineDashboard() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const totalPipelineValue = STAGE_SUMMARIES.filter(
    (s) => s.stage !== "closed_lost",
  ).reduce((sum, s) => sum + s.totalValueSar, 0);

  const openDeals = STAGE_SUMMARIES.filter(
    (s) => s.stage !== "closed_won" && s.stage !== "closed_lost",
  ).reduce((sum, s) => sum + s.count, 0);

  return (
    <div
      className={cn(
        "min-h-screen bg-gray-50 p-6",
        isAr ? "text-right" : "text-left",
      )}
      dir={isAr ? "rtl" : "ltr"}
    >
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          {isAr ? "خط أنابيب المبيعات" : "Sales Pipeline"}
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          {isAr
            ? "لوحة متابعة الصفقات النشطة والتوقعات التجارية — 7 مراحل"
            : "Active deal tracking and commercial forecasting — 7 stages"}
        </p>
      </div>

      {/* Top-level KPIs */}
      <div className="mb-6 grid grid-cols-3 gap-4">
        <div className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide text-gray-400">
            {isAr ? "إجمالي خط الأنابيب" : "Total Pipeline Value"}
          </div>
          <div className="mt-1 text-2xl font-bold text-gray-900">
            {isAr
              ? `${(totalPipelineValue / 1_000_000).toFixed(1)} م.ر`
              : `SAR ${(totalPipelineValue / 1_000_000).toFixed(1)}M`}
          </div>
        </div>
        <div className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide text-gray-400">
            {isAr ? "الصفقات المفتوحة" : "Open Deals"}
          </div>
          <div className="mt-1 text-2xl font-bold text-gray-900">{openDeals}</div>
        </div>
        <div className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
          <div className="text-xs font-semibold uppercase tracking-wide text-gray-400">
            {isAr ? "الصفقات المغلقة (ربح)" : "Closed Won (this period)"}
          </div>
          <div className="mt-1 text-2xl font-bold text-emerald-600">
            {STAGE_SUMMARIES.find((s) => s.stage === "closed_won")?.count ?? 0}
          </div>
        </div>
      </div>

      {/* Kanban stage summary */}
      <section className="mb-6">
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-gray-500">
          {isAr ? "توزيع المراحل" : "Stage Distribution"}
        </h2>
        <PipelineKanbanStrip locale={locale} />
      </section>

      {/* 30/60/90 day forecast */}
      <section className="mb-6">
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-gray-500">
          {isAr ? "التوقعات المرجّحة" : "Weighted Forecast"}
        </h2>
        <ForecastStrip locale={locale} />
      </section>

      {/* Pipeline health */}
      <section className="mb-6">
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-gray-500">
          {isAr ? "مؤشر صحة خط الأنابيب" : "Pipeline Health Indicator"}
        </h2>
        <PipelineHealthIndicator locale={locale} />
      </section>

      {/* Top 5 deals */}
      <section className="mb-6">
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-gray-500">
          {isAr ? "أبرز 5 صفقات" : "Top 5 Deals"}
        </h2>
        <TopDealsTable locale={locale} />
      </section>

      {/* Disclaimer note */}
      <p className="mt-2 text-xs text-gray-400">
        {isAr
          ? "البيانات المعروضة تجريبية. جميع الإجراءات تتطلب مراجعة المؤسس قبل التنفيذ."
          : "Data shown is illustrative. All actions require founder review before execution."}
      </p>
    </div>
  );
}
