// from __future__ import annotations
"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type HealthTier = "healthy" | "moderate" | "at_risk" | "critical";
type AlertSeverity = "critical" | "high" | "medium";
type TrendDirection = "up" | "down" | "flat";

interface DimensionScores {
  data_readiness: number;
  onboarding_ops: number;
  delivery_quality: number;
  zatca_compliance: number;
  client_retention: number;
  recurring_revenue: number;
}

interface ClientRecord {
  id: string;
  nameAr: string;
  nameEn: string;
  healthScore: number;
  tier: HealthTier;
  trend: TrendDirection;
  dimensions: DimensionScores;
}

interface Alert {
  id: string;
  clientNameAr: string;
  clientNameEn: string;
  severity: AlertSeverity;
  messageAr: string;
  messageEn: string;
  actionAr: string;
  actionEn: string;
}

// ---------------------------------------------------------------------------
// Mock data — 6 clients with realistic health profiles
// ---------------------------------------------------------------------------

const MOCK_CLIENTS: ClientRecord[] = [
  {
    id: "c1",
    nameAr: "شركة الرياض للتقنية",
    nameEn: "Riyadh Tech Co.",
    healthScore: 88,
    tier: "healthy",
    trend: "up",
    dimensions: {
      data_readiness: 90,
      onboarding_ops: 85,
      delivery_quality: 92,
      zatca_compliance: 88,
      client_retention: 84,
      recurring_revenue: 90,
    },
  },
  {
    id: "c2",
    nameAr: "مجموعة النخبة التجارية",
    nameEn: "Elite Trading Group",
    healthScore: 79,
    tier: "healthy",
    trend: "up",
    dimensions: {
      data_readiness: 82,
      onboarding_ops: 78,
      delivery_quality: 80,
      zatca_compliance: 85,
      client_retention: 72,
      recurring_revenue: 76,
    },
  },
  {
    id: "c3",
    nameAr: "شركة الأفق للخدمات",
    nameEn: "Horizon Services Ltd.",
    healthScore: 66,
    tier: "moderate",
    trend: "flat",
    dimensions: {
      data_readiness: 70,
      onboarding_ops: 65,
      delivery_quality: 68,
      zatca_compliance: 72,
      client_retention: 60,
      recurring_revenue: 60,
    },
  },
  {
    id: "c4",
    nameAr: "مؤسسة سهل للتوزيع",
    nameEn: "Sahl Distribution Est.",
    healthScore: 58,
    tier: "moderate",
    trend: "down",
    dimensions: {
      data_readiness: 55,
      onboarding_ops: 60,
      delivery_quality: 62,
      zatca_compliance: 70,
      client_retention: 50,
      recurring_revenue: 52,
    },
  },
  {
    id: "c5",
    nameAr: "شركة القمة للاستشارات",
    nameEn: "Summit Consulting Co.",
    healthScore: 44,
    tier: "at_risk",
    trend: "down",
    dimensions: {
      data_readiness: 40,
      onboarding_ops: 45,
      delivery_quality: 50,
      zatca_compliance: 55,
      client_retention: 38,
      recurring_revenue: 36,
    },
  },
  {
    id: "c6",
    nameAr: "مؤسسة الفجر للتجزئة",
    nameEn: "Fajr Retail Est.",
    healthScore: 29,
    tier: "critical",
    trend: "down",
    dimensions: {
      data_readiness: 25,
      onboarding_ops: 30,
      delivery_quality: 28,
      zatca_compliance: 35,
      client_retention: 22,
      recurring_revenue: 34,
    },
  },
];

const MOCK_ALERTS: Alert[] = [
  {
    id: "a1",
    clientNameAr: "مؤسسة الفجر للتجزئة",
    clientNameEn: "Fajr Retail Est.",
    severity: "critical",
    messageAr: "تراجع حاد في جميع الأبعاد الستة — خطر فقدان العميل قريب",
    messageEn: "Sharp decline across all 6 dimensions — churn risk imminent",
    actionAr: "جدول مكالمة طارئة وقدم خطة إنقاذ خلال ٤٨ ساعة",
    actionEn: "Schedule emergency call and deliver rescue plan within 48 hours",
  },
  {
    id: "a2",
    clientNameAr: "شركة القمة للاستشارات",
    clientNameEn: "Summit Consulting Co.",
    severity: "high",
    messageAr: "الإيرادات المتكررة انخفضت ٢٣٪ خلال ٦٠ يوماً الماضية",
    messageEn: "Recurring revenue declined 23% over the past 60 days",
    actionAr: "راجع شروط العقد وقدم عرضاً للتجديد المبكر",
    actionEn: "Review contract terms and present an early renewal offer",
  },
  {
    id: "a3",
    clientNameAr: "مؤسسة سهل للتوزيع",
    clientNameEn: "Sahl Distribution Est.",
    severity: "high",
    messageAr: "درجة الاحتفاظ بالعميل انخفضت إلى ما دون حد الخطر",
    messageEn: "Client retention score dropped below risk threshold",
    actionAr: "فعّل برنامج إعادة التفاعل وأرسل تقرير قيمة مخصص",
    actionEn: "Activate re-engagement program and send a tailored value report",
  },
];

// ---------------------------------------------------------------------------
// Constants — dimension labels
// ---------------------------------------------------------------------------

interface DimensionMeta {
  key: keyof DimensionScores;
  labelAr: string;
  labelEn: string;
}

const DIMENSIONS: DimensionMeta[] = [
  { key: "data_readiness", labelAr: "جاهزية البيانات", labelEn: "Data Readiness" },
  { key: "onboarding_ops", labelAr: "عمليات الإعداد", labelEn: "Onboarding Ops" },
  { key: "delivery_quality", labelAr: "جودة التسليم", labelEn: "Delivery Quality" },
  { key: "zatca_compliance", labelAr: "امتثال ZATCA", labelEn: "ZATCA Compliance" },
  { key: "client_retention", labelAr: "الاحتفاظ بالعميل", labelEn: "Client Retention" },
  { key: "recurring_revenue", labelAr: "الإيراد المتكرر", labelEn: "Recurring Revenue" },
];

// ---------------------------------------------------------------------------
// Pure helpers
// ---------------------------------------------------------------------------

function tierFromScore(score: number): HealthTier {
  if (score >= 75) return "healthy";
  if (score >= 55) return "moderate";
  if (score >= 35) return "at_risk";
  return "critical";
}

function tierColors(tier: HealthTier): {
  bg: string;
  text: string;
  bar: string;
  border: string;
} {
  const map: Record<HealthTier, { bg: string; text: string; bar: string; border: string }> = {
    healthy: {
      bg: "bg-emerald-100 dark:bg-emerald-950/40",
      text: "text-emerald-700 dark:text-emerald-300",
      bar: "bg-emerald-500",
      border: "border-emerald-300 dark:border-emerald-700",
    },
    moderate: {
      bg: "bg-yellow-100 dark:bg-yellow-950/40",
      text: "text-yellow-700 dark:text-yellow-300",
      bar: "bg-yellow-500",
      border: "border-yellow-300 dark:border-yellow-700",
    },
    at_risk: {
      bg: "bg-orange-100 dark:bg-orange-950/40",
      text: "text-orange-700 dark:text-orange-300",
      bar: "bg-orange-500",
      border: "border-orange-300 dark:border-orange-700",
    },
    critical: {
      bg: "bg-red-100 dark:bg-red-950/40",
      text: "text-red-700 dark:text-red-300",
      bar: "bg-red-500",
      border: "border-red-300 dark:border-red-700",
    },
  };
  return map[tier];
}

function tierLabelBilingual(tier: HealthTier): { ar: string; en: string } {
  const map: Record<HealthTier, { ar: string; en: string }> = {
    healthy: { ar: "صحي", en: "Healthy" },
    moderate: { ar: "متوسط", en: "Moderate" },
    at_risk: { ar: "في خطر", en: "At Risk" },
    critical: { ar: "حرج", en: "Critical" },
  };
  return map[tier];
}

function alertSeverityConfig(sev: AlertSeverity): {
  bg: string;
  text: string;
  label: string;
} {
  const map: Record<AlertSeverity, { bg: string; text: string; label: string }> = {
    critical: { bg: "bg-red-100 dark:bg-red-950/40", text: "text-red-700 dark:text-red-300", label: "Critical" },
    high: { bg: "bg-orange-100 dark:bg-orange-950/40", text: "text-orange-700 dark:text-orange-300", label: "High" },
    medium: { bg: "bg-yellow-100 dark:bg-yellow-950/40", text: "text-yellow-700 dark:text-yellow-300", label: "Medium" },
  };
  return map[sev];
}

function trendSymbol(trend: TrendDirection): string {
  if (trend === "up") return "▲";
  if (trend === "down") return "▼";
  return "—";
}

function trendColor(trend: TrendDirection): string {
  if (trend === "up") return "text-emerald-600";
  if (trend === "down") return "text-red-500";
  return "text-muted-foreground";
}

// ---------------------------------------------------------------------------
// SVG Radar chart — pure CSS/SVG, no recharts
// ---------------------------------------------------------------------------

interface RadarChartProps {
  scores: DimensionScores;
  size?: number;
}

function RadarChart({ scores, size = 200 }: RadarChartProps) {
  const center = size / 2;
  const maxRadius = center * 0.75;
  const n = DIMENSIONS.length;

  // Generate polygon points for a given radius fraction
  function getPoint(index: number, fraction: number): [number, number] {
    // Start at top (-90 deg offset so first dimension is at the top)
    const angle = (2 * Math.PI * index) / n - Math.PI / 2;
    const r = maxRadius * fraction;
    return [center + r * Math.cos(angle), center + r * Math.sin(angle)];
  }

  function pointsString(fraction: number): string {
    return DIMENSIONS.map((_, i) => getPoint(i, fraction).join(",")).join(" ");
  }

  const scorePoints = DIMENSIONS.map((d, i) => {
    const fraction = scores[d.key] / 100;
    return getPoint(i, fraction).join(",");
  }).join(" ");

  // Grid levels
  const gridLevels = [0.25, 0.5, 0.75, 1.0];

  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      aria-label="Radar chart of 6 health dimensions"
    >
      {/* Grid polygons */}
      {gridLevels.map((level) => (
        <polygon
          key={level}
          points={pointsString(level)}
          fill="none"
          stroke="currentColor"
          strokeOpacity={0.12}
          strokeWidth={1}
        />
      ))}

      {/* Spokes */}
      {DIMENSIONS.map((_, i) => {
        const [x, y] = getPoint(i, 1);
        return (
          <line
            key={i}
            x1={center}
            y1={center}
            x2={x}
            y2={y}
            stroke="currentColor"
            strokeOpacity={0.15}
            strokeWidth={1}
          />
        );
      })}

      {/* Data polygon */}
      <polygon
        points={scorePoints}
        fill="#001F3F"
        fillOpacity={0.25}
        stroke="#001F3F"
        strokeWidth={2}
        strokeLinejoin="round"
      />

      {/* Data dots */}
      {DIMENSIONS.map((d, i) => {
        const [x, y] = getPoint(i, scores[d.key] / 100);
        return (
          <circle
            key={d.key}
            cx={x}
            cy={y}
            r={3.5}
            fill="#001F3F"
          />
        );
      })}

      {/* Labels */}
      {DIMENSIONS.map((d, i) => {
        const [x, y] = getPoint(i, 1.18);
        return (
          <text
            key={d.key}
            x={x}
            y={y}
            textAnchor="middle"
            dominantBaseline="middle"
            fontSize={7.5}
            fill="currentColor"
            fillOpacity={0.7}
          >
            {d.labelEn}
          </text>
        );
      })}
    </svg>
  );
}

// ---------------------------------------------------------------------------
// Portfolio-average radar
// ---------------------------------------------------------------------------

function portfolioAvgScores(): DimensionScores {
  const keys = DIMENSIONS.map((d) => d.key);
  const result = {} as DimensionScores;
  for (const k of keys) {
    const avg =
      MOCK_CLIENTS.reduce((acc, c) => acc + c.dimensions[k], 0) /
      MOCK_CLIENTS.length;
    result[k] = Math.round(avg);
  }
  return result;
}

// ---------------------------------------------------------------------------
// Stat card
// ---------------------------------------------------------------------------

interface StatCardProps {
  titleAr: string;
  titleEn: string;
  value: string | number;
  subtitleAr?: string;
  subtitleEn?: string;
  accentClass?: string;
  isAr: boolean;
}

function StatCard({
  titleAr,
  titleEn,
  value,
  subtitleAr,
  subtitleEn,
  accentClass = "text-[var(--dealix-navy)]",
  isAr,
}: StatCardProps) {
  return (
    <Card className="p-5">
      <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
        {isAr ? titleAr : titleEn}
      </p>
      <p className={`text-4xl font-black tabular-nums mt-2 ${accentClass}`}>
        {value}
      </p>
      {(subtitleAr || subtitleEn) && (
        <p className="text-xs text-muted-foreground mt-1">
          {isAr ? subtitleAr : subtitleEn}
        </p>
      )}
    </Card>
  );
}

// ---------------------------------------------------------------------------
// Client row
// ---------------------------------------------------------------------------

interface ClientRowProps {
  client: ClientRecord;
  isAr: boolean;
  isSelected: boolean;
  onSelect: () => void;
}

function ClientRow({ client, isAr, isSelected, onSelect }: ClientRowProps) {
  const colors = tierColors(client.tier);
  const tierLabel = tierLabelBilingual(client.tier);

  return (
    <tr
      onClick={onSelect}
      className={`cursor-pointer transition-colors hover:bg-muted/50 ${
        isSelected ? "bg-muted/70" : ""
      }`}
    >
      {/* Name */}
      <td className="py-3 px-4 border-b border-border/40">
        <div>
          <p className="text-sm font-semibold">
            {isAr ? client.nameAr : client.nameEn}
          </p>
          <p className="text-xs text-muted-foreground">
            {isAr ? client.nameEn : client.nameAr}
          </p>
        </div>
      </td>

      {/* Score bar */}
      <td className="py-3 px-4 border-b border-border/40 min-w-[120px]">
        <div className="space-y-1">
          <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
            <div
              className={`h-full rounded-full ${colors.bar}`}
              style={{ width: `${client.healthScore}%` }}
            />
          </div>
          <p className="text-xs font-bold tabular-nums">{client.healthScore}</p>
        </div>
      </td>

      {/* Tier badge */}
      <td className="py-3 px-4 border-b border-border/40">
        <span
          className={`inline-block text-xs font-semibold px-2 py-0.5 rounded-full ${colors.bg} ${colors.text}`}
        >
          {isAr ? tierLabel.ar : tierLabel.en}
        </span>
      </td>

      {/* Dimension scores — small bars */}
      {DIMENSIONS.map((dim) => {
        const s = client.dimensions[dim.key];
        const dimTier = tierFromScore(s);
        const dimColors = tierColors(dimTier);
        return (
          <td key={dim.key} className="py-3 px-2 border-b border-border/40">
            <div className="flex flex-col items-center gap-0.5">
              <div className="h-1.5 w-10 rounded-full bg-muted overflow-hidden">
                <div
                  className={`h-full rounded-full ${dimColors.bar}`}
                  style={{ width: `${s}%` }}
                />
              </div>
              <span className="text-[10px] tabular-nums text-muted-foreground">{s}</span>
            </div>
          </td>
        );
      })}

      {/* Trend */}
      <td className="py-3 px-4 border-b border-border/40">
        <span className={`text-base font-bold ${trendColor(client.trend)}`}>
          {trendSymbol(client.trend)}
        </span>
      </td>
    </tr>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export default function HealthIntelligenceDashboard() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [selectedClientId, setSelectedClientId] = useState<string | null>(null);

  const totalClients = MOCK_CLIENTS.length;
  const avgScore = Math.round(
    MOCK_CLIENTS.reduce((acc, c) => acc + c.healthScore, 0) / totalClients
  );
  const atRiskCount = MOCK_CLIENTS.filter(
    (c) => c.tier === "at_risk" || c.tier === "critical"
  ).length;

  const avgTier = tierFromScore(avgScore);
  const avgTierColors = tierColors(avgTier);

  const portfolioRadar = portfolioAvgScores();

  const sorted = [...MOCK_CLIENTS].sort((a, b) => b.healthScore - a.healthScore);
  const top3 = sorted.slice(0, 3);
  const medalLabels = ["1", "2", "3"];

  const selectedClient = MOCK_CLIENTS.find((c) => c.id === selectedClientId);

  return (
    <div className="min-h-screen bg-background" dir={isAr ? "rtl" : "ltr"}>
      <div className="max-w-7xl mx-auto px-4 py-10 space-y-8">

        {/* Page header */}
        <header className={isAr ? "text-right" : "text-left"}>
          <div className="flex gap-2 mb-2 flex-wrap">
            <span className="badge-ai text-xs font-semibold px-2.5 py-1 rounded-full">
              {isAr ? "عرض المؤسس" : "Founder View"}
            </span>
            <Badge variant="outline" className="text-xs">
              {isAr ? "محاكاة — بيانات تجريبية" : "Demo — Mock Data"}
            </Badge>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-[var(--dealix-navy)] dark:text-foreground">
            {isAr ? "لوحة الذكاء الصحي للمحفظة" : "Health Intelligence Dashboard"}
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            {isAr
              ? "نظرة شاملة على صحة العملاء عبر ٦ أبعاد — تحديث مستمر"
              : "Full portfolio health overview across 6 dimensions — continuous monitoring"}
          </p>
        </header>

        {/* Stat cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <StatCard
            titleAr="إجمالي العملاء"
            titleEn="Total Clients"
            value={totalClients}
            isAr={isAr}
          />
          <StatCard
            titleAr="متوسط درجة الصحة"
            titleEn="Avg Health Score"
            value={avgScore}
            subtitleAr={isAr ? avgTier === "healthy" ? "صحي" : avgTier === "moderate" ? "متوسط" : "في خطر" : undefined}
            subtitleEn={!isAr ? avgTier : undefined}
            accentClass={avgTierColors.text}
            isAr={isAr}
          />
          <StatCard
            titleAr="عملاء في خطر"
            titleEn="At-Risk Clients"
            value={atRiskCount}
            subtitleAr="يتطلبون تدخلاً استباقياً"
            subtitleEn="Require proactive intervention"
            accentClass={atRiskCount > 0 ? "text-red-600" : "text-emerald-600"}
            isAr={isAr}
          />
        </div>

        {/* Radar + leaderboard row */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          {/* Portfolio radar */}
          <Card className="p-5 flex flex-col gap-4">
            <div>
              <p className="font-semibold text-sm">
                {isAr ? "متوسط المحفظة — الأبعاد الستة" : "Portfolio Average — 6 Dimensions"}
              </p>
              <p className="text-xs text-muted-foreground mt-0.5">
                {isAr
                  ? "يعرض متوسط أداء المحفظة الكاملة — انقر على عميل لتفصيل درجاته"
                  : "Shows full portfolio average — click a client row for their breakdown"}
              </p>
            </div>
            <div className="flex flex-col items-center gap-4">
              <RadarChart
                scores={selectedClient ? selectedClient.dimensions : portfolioRadar}
                size={220}
              />
              {selectedClient && (
                <p className="text-xs text-muted-foreground">
                  {isAr
                    ? `يعرض: ${selectedClient.nameAr}`
                    : `Showing: ${selectedClient.nameEn}`}
                </p>
              )}
              {!selectedClient && (
                <p className="text-xs text-muted-foreground">
                  {isAr ? "متوسط المحفظة" : "Portfolio average"}
                </p>
              )}
              {/* Dimension legend */}
              <div className="grid grid-cols-2 gap-x-4 gap-y-1 w-full text-xs">
                {DIMENSIONS.map((d) => {
                  const score = selectedClient
                    ? selectedClient.dimensions[d.key]
                    : portfolioRadar[d.key];
                  const t = tierFromScore(score);
                  const tc = tierColors(t);
                  return (
                    <div key={d.key} className="flex items-center justify-between gap-2">
                      <span className="text-muted-foreground truncate">
                        {isAr ? d.labelAr : d.labelEn}
                      </span>
                      <span className={`font-bold tabular-nums ${tc.text}`}>{score}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          </Card>

          {/* Leaderboard */}
          <Card className="p-5 flex flex-col gap-4">
            <p className="font-semibold text-sm">
              {isAr ? "أفضل ٣ عملاء أداءً" : "Top 3 Performers"}
            </p>
            <div className="space-y-3">
              {top3.map((client, i) => {
                const colors = tierColors(client.tier);
                return (
                  <div
                    key={client.id}
                    className={`flex items-center gap-3 p-3 rounded-xl border ${colors.border} ${colors.bg}`}
                  >
                    <span className="text-xl font-black w-6 text-center shrink-0 text-[var(--dealix-gold)]">
                      {medalLabels[i]}
                    </span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-semibold truncate">
                        {isAr ? client.nameAr : client.nameEn}
                      </p>
                      <p className="text-xs text-muted-foreground truncate">
                        {isAr ? client.nameEn : client.nameAr}
                      </p>
                    </div>
                    <div className="text-end shrink-0">
                      <p className={`text-xl font-black tabular-nums ${colors.text}`}>
                        {client.healthScore}
                      </p>
                      <p className={`text-[10px] font-semibold ${trendColor(client.trend)}`}>
                        {trendSymbol(client.trend)}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
            {/* Tier legend */}
            <div className="mt-auto pt-2 border-t border-border/40">
              <p className="text-xs text-muted-foreground mb-2">
                {isAr ? "دليل الألوان" : "Color guide"}
              </p>
              <div className="flex flex-wrap gap-2 text-xs">
                {(["healthy", "moderate", "at_risk", "critical"] as HealthTier[]).map((t) => {
                  const c = tierColors(t);
                  const l = tierLabelBilingual(t);
                  return (
                    <span
                      key={t}
                      className={`px-2 py-0.5 rounded-full font-medium ${c.bg} ${c.text}`}
                    >
                      {isAr ? l.ar : l.en} (
                      {t === "healthy"
                        ? "75+"
                        : t === "moderate"
                        ? "55-74"
                        : t === "at_risk"
                        ? "35-54"
                        : "<35"}
                      )
                    </span>
                  );
                })}
              </div>
            </div>
          </Card>
        </div>

        {/* Client health table */}
        <Card className="overflow-hidden">
          <div className="p-4 border-b border-border/40 flex items-center justify-between">
            <p className="font-semibold text-sm">
              {isAr ? "جدول صحة العملاء" : "Client Health Table"}
            </p>
            <p className="text-xs text-muted-foreground">
              {isAr ? "انقر على صف للتفاصيل في الرسم" : "Click a row to see radar breakdown"}
            </p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-muted/30">
                  <th className={`py-2 px-4 font-medium text-muted-foreground text-xs text-${isAr ? "right" : "left"}`}>
                    {isAr ? "العميل" : "Client"}
                  </th>
                  <th className="py-2 px-4 font-medium text-muted-foreground text-xs text-center">
                    {isAr ? "الدرجة" : "Score"}
                  </th>
                  <th className="py-2 px-4 font-medium text-muted-foreground text-xs text-center">
                    {isAr ? "المستوى" : "Tier"}
                  </th>
                  {DIMENSIONS.map((d) => (
                    <th
                      key={d.key}
                      className="py-2 px-2 font-medium text-muted-foreground text-[10px] text-center"
                    >
                      {isAr ? d.labelAr.split(" ")[0] : d.labelEn.split(" ")[0]}
                    </th>
                  ))}
                  <th className="py-2 px-4 font-medium text-muted-foreground text-xs text-center">
                    {isAr ? "الاتجاه" : "Trend"}
                  </th>
                </tr>
              </thead>
              <tbody>
                {MOCK_CLIENTS.map((client) => (
                  <ClientRow
                    key={client.id}
                    client={client}
                    isAr={isAr}
                    isSelected={selectedClientId === client.id}
                    onSelect={() =>
                      setSelectedClientId(
                        selectedClientId === client.id ? null : client.id
                      )
                    }
                  />
                ))}
              </tbody>
            </table>
          </div>
        </Card>

        {/* Alerts section */}
        <div>
          <h2 className="text-base font-semibold mb-3">
            {isAr ? "التنبيهات النشطة" : "Active Alerts"}
          </h2>
          <div className="space-y-3">
            {MOCK_ALERTS.map((alert) => {
              const sevConfig = alertSeverityConfig(alert.severity);
              return (
                <Card
                  key={alert.id}
                  className={`p-4 border ${
                    alert.severity === "critical"
                      ? "border-red-300 dark:border-red-700"
                      : alert.severity === "high"
                      ? "border-orange-300 dark:border-orange-700"
                      : "border-yellow-300 dark:border-yellow-700"
                  } ${sevConfig.bg}`}
                >
                  <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                    <div className="space-y-1 flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span
                          className={`text-xs font-bold uppercase px-2 py-0.5 rounded-full ${sevConfig.bg} ${sevConfig.text} border ${
                            alert.severity === "critical"
                              ? "border-red-300 dark:border-red-700"
                              : alert.severity === "high"
                              ? "border-orange-300 dark:border-orange-700"
                              : "border-yellow-300 dark:border-yellow-700"
                          }`}
                        >
                          {sevConfig.label}
                        </span>
                        <span className="text-sm font-semibold">
                          {isAr ? alert.clientNameAr : alert.clientNameEn}
                        </span>
                      </div>
                      <p className={`text-sm ${sevConfig.text}`}>
                        {isAr ? alert.messageAr : alert.messageEn}
                      </p>
                    </div>
                    <div className={`shrink-0 sm:max-w-xs ${isAr ? "sm:text-right" : "sm:text-left"}`}>
                      <p className="text-xs text-muted-foreground font-medium uppercase tracking-wide mb-0.5">
                        {isAr ? "الإجراء الموصى به" : "Recommended Action"}
                      </p>
                      <p className="text-xs font-semibold">
                        {isAr ? alert.actionAr : alert.actionEn}
                      </p>
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>

        {/* Footer note */}
        <p className="text-xs text-muted-foreground border border-border/40 rounded-lg p-3 bg-muted/20">
          {isAr
            ? "* جميع البيانات المعروضة تجريبية للتوضيح. في الإنتاج، تُستدعى من قاعدة البيانات وتتحدث تلقائياً."
            : "* All data shown is mock/demo for illustration. In production, data is fetched from the database and updated automatically."}
        </p>
      </div>
    </div>
  );
}
