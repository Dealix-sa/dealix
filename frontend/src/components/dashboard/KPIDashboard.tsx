"use client";

import { useLocale } from "next-intl";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { TrendingUp, TrendingDown, RefreshCw, Download } from "lucide-react";
import { formatCurrency } from "@/lib/utils";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface MrrDataPoint {
  month: string;
  monthAr: string;
  mrr: number;
}

interface PipelineStage {
  stageEn: string;
  stageAr: string;
  count: number;
  value: number;
}

interface ProductTier {
  nameEn: string;
  nameAr: string;
  value: number;
  color: string;
}

interface HealthDimension {
  nameEn: string;
  nameAr: string;
  score: number;
}

interface ActivityEvent {
  id: string;
  titleEn: string;
  titleAr: string;
  kind: string;
  timestampLabel: string;
  timestampLabelAr: string;
}

// ---------------------------------------------------------------------------
// Mock data
// ---------------------------------------------------------------------------

// 12-month MRR series: 18,000 SAR base, ~5% monthly growth
const MRR_BASE = 18000;
const MRR_GROWTH = 0.05;

const MRR_MONTHS_EN = [
  "Jun 25", "Jul 25", "Aug 25", "Sep 25", "Oct 25", "Nov 25",
  "Dec 25", "Jan 26", "Feb 26", "Mar 26", "Apr 26", "May 26",
];
const MRR_MONTHS_AR = [
  "يون 25", "يول 25", "أغس 25", "سبت 25", "أكت 25", "نوف 25",
  "ديس 25", "يان 26", "فبر 26", "مار 26", "أبر 26", "ماي 26",
];

const mrrData: MrrDataPoint[] = MRR_MONTHS_EN.map((month, i) => ({
  month,
  monthAr: MRR_MONTHS_AR[i] ?? month,
  mrr: Math.round(MRR_BASE * Math.pow(1 + MRR_GROWTH, i)),
}));

const currentMrr = mrrData[mrrData.length - 1]?.mrr ?? 0;
const previousMrr = mrrData[mrrData.length - 2]?.mrr ?? 0;
const momGrowthPct =
  previousMrr > 0
    ? (((currentMrr - previousMrr) / previousMrr) * 100)
    : 0;
const currentArr = currentMrr * 12;
const activeClients = 16;
const churnedThisMonth = 1;
const healthScore = 72;

const pipelineStages: PipelineStage[] = [
  { stageEn: "Diagnostic", stageAr: "تشخيص", count: 6, value: 0 },
  { stageEn: "Sprint Active", stageAr: "سبرينت نشط", count: 5, value: 2495 },
  { stageEn: "Proposal", stageAr: "عرض", count: 3, value: 9000 },
  { stageEn: "Retainer", stageAr: "عقد شهري", count: 2, value: 9998 },
];

const productTiers: ProductTier[] = [
  { nameEn: "Free Diagnostic", nameAr: "تشخيص مجاني", value: 6, color: "#94a3b8" },
  { nameEn: "499 SAR Sprint", nameAr: "سبرينت 499 ر.س", value: 5, color: "#60a5fa" },
  { nameEn: "1,500 SAR Data Pack", nameAr: "باقة بيانات 1,500 ر.س", value: 4, color: "#C9A96E" },
  { nameEn: "2,999–4,999 Managed Ops", nameAr: "عمليات مدارة 2,999–4,999", value: 3, color: "#f59e0b" },
  { nameEn: "5K+ Custom AI", nameAr: "ذكاء اصطناعي مخصص +5K", value: 2, color: "#10b981" },
];

const healthDimensions: HealthDimension[] = [
  { nameEn: "Data Readiness", nameAr: "جاهزية البيانات", score: 82 },
  { nameEn: "Onboarding Ops", nameAr: "عمليات الإعداد", score: 68 },
  { nameEn: "Delivery Quality", nameAr: "جودة التسليم", score: 79 },
  { nameEn: "ZATCA Compliance", nameAr: "الامتثال لزاتكا", score: 55 },
  { nameEn: "Client Retention", nameAr: "احتفاظ بالعملاء", score: 76 },
  { nameEn: "Recurring Revenue", nameAr: "إيرادات متكررة", score: 70 },
];

const activityFeed: ActivityEvent[] = [
  {
    id: "1",
    titleEn: "Sprint completed for Client A",
    titleAr: "اكتمل سبرينت لعميل أ",
    kind: "sprint",
    timestampLabel: "2 hours ago",
    timestampLabelAr: "منذ ساعتين",
  },
  {
    id: "2",
    titleEn: "Health score updated to 72",
    titleAr: "تم تحديث درجة الصحة إلى 72",
    kind: "health",
    timestampLabel: "5 hours ago",
    timestampLabelAr: "منذ 5 ساعات",
  },
  {
    id: "3",
    titleEn: "Founder alert approved",
    titleAr: "تمت الموافقة على تنبيه المؤسس",
    kind: "alert",
    timestampLabel: "1 day ago",
    timestampLabelAr: "منذ يوم",
  },
  {
    id: "4",
    titleEn: "New diagnostic started for Client B",
    titleAr: "بدأ تشخيص جديد لعميل ب",
    kind: "diagnostic",
    timestampLabel: "2 days ago",
    timestampLabelAr: "منذ يومين",
  },
  {
    id: "5",
    titleEn: "Proof pack delivered to Client C",
    titleAr: "تم تسليم حزمة الإثبات لعميل ج",
    kind: "proof",
    timestampLabel: "3 days ago",
    timestampLabelAr: "منذ 3 أيام",
  },
];

const LAST_UPDATED_EN = "May 31, 2026";
const LAST_UPDATED_AR = "31 مايو 2026";

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

interface TooltipPayloadEntry {
  name: string;
  value: number;
  color: string;
}

interface CustomTooltipProps {
  active?: boolean;
  payload?: TooltipPayloadEntry[];
  label?: string;
}

function ChartTooltip({ active, payload, label }: CustomTooltipProps) {
  if (!active || !payload || payload.length === 0) return null;
  return (
    <div className="bg-card border border-border rounded-xl p-3 shadow-xl text-sm">
      {label && <p className="font-semibold text-foreground mb-2">{label}</p>}
      {payload.map((entry, i) => (
        <p key={i} style={{ color: entry.color }} className="flex items-center gap-2">
          <span
            className="w-2 h-2 rounded-full inline-block"
            style={{ background: entry.color }}
          />
          {entry.name}: {typeof entry.value === "number" && entry.value > 1000
            ? formatCurrency(entry.value)
            : entry.value}
        </p>
      ))}
    </div>
  );
}

interface PieTooltipPayload {
  name: string;
  value: number;
}

interface PieLabelTooltipProps {
  active?: boolean;
  payload?: PieTooltipPayload[];
}

function PieTooltip({ active, payload }: PieLabelTooltipProps) {
  if (!active || !payload || payload.length === 0) return null;
  const entry = payload[0];
  if (!entry) return null;
  return (
    <div className="bg-card border border-border rounded-xl p-3 shadow-xl text-sm">
      <p className="text-foreground font-semibold">{entry.name}</p>
      <p className="text-muted-foreground">{entry.value} clients</p>
    </div>
  );
}

function healthTierLabel(score: number, isAr: boolean): string {
  if (score >= 80) return isAr ? "ممتاز" : "Healthy";
  if (score >= 60) return isAr ? "متوسط" : "Moderate";
  return isAr ? "في خطر" : "At Risk";
}

function healthTierVariant(score: number): "default" | "secondary" | "destructive" | "outline" {
  if (score >= 80) return "default";
  if (score >= 60) return "secondary";
  return "destructive";
}

function dimensionBarColor(score: number): string {
  if (score >= 80) return "bg-emerald-500";
  if (score >= 60) return "bg-amber-500";
  return "bg-red-500";
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export function KPIDashboard() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const mrrChartData = mrrData.map((d) => ({
    month: isAr ? d.monthAr : d.month,
    [isAr ? "الإيرادات الشهرية" : "MRR"]: d.mrr,
  }));

  const mrrKey = isAr ? "الإيرادات الشهرية" : "MRR";

  const pipelineChartData = pipelineStages.map((s) => ({
    stage: isAr ? s.stageAr : s.stageEn,
    [isAr ? "العدد" : "Count"]: s.count,
    value: s.value,
  }));

  const countKey = isAr ? "العدد" : "Count";

  const pieData = productTiers.map((t) => ({
    name: isAr ? t.nameAr : t.nameEn,
    value: t.value,
    color: t.color,
  }));

  return (
    <div className="space-y-6">
      {/* Refresh indicator */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <RefreshCw className="w-3 h-3" />
          <span>
            {isAr
              ? `آخر تحديث: ${LAST_UPDATED_AR}`
              : `Last updated: ${LAST_UPDATED_EN}`}
          </span>
        </div>
        <Button variant="outline" size="sm" className="gap-2">
          <Download className="w-4 h-4" />
          {isAr ? "تصدير التقرير" : "Export Report"}
        </Button>
      </div>

      {/* Section 1: KPI Hero Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* MRR */}
        <Card>
          <CardContent className="pt-6">
            <p className="text-xs text-muted-foreground font-medium mb-1">
              {isAr ? "الإيرادات الشهرية المتكررة" : "MRR"}
            </p>
            <p className="text-2xl font-bold tabular-nums">
              {formatCurrency(currentMrr)}
            </p>
            <div className="flex items-center gap-1 mt-2">
              {momGrowthPct >= 0 ? (
                <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
              ) : (
                <TrendingDown className="w-3.5 h-3.5 text-red-400" />
              )}
              <span
                className={`text-xs font-semibold ${
                  momGrowthPct >= 0 ? "text-emerald-400" : "text-red-400"
                }`}
              >
                {momGrowthPct >= 0 ? "+" : ""}
                {momGrowthPct.toFixed(1)}%{" "}
                {isAr ? "شهريًا" : "MoM"}
              </span>
            </div>
          </CardContent>
        </Card>

        {/* ARR */}
        <Card>
          <CardContent className="pt-6">
            <p className="text-xs text-muted-foreground font-medium mb-1">
              {isAr ? "الإيرادات السنوية المتوقعة" : "ARR (Projected)"}
            </p>
            <p className="text-2xl font-bold tabular-nums">
              {formatCurrency(currentArr)}
            </p>
            <p className="text-xs text-muted-foreground mt-2">
              {isAr ? "بناءً على الإيرادات الشهرية الحالية" : "Based on current MRR"}
            </p>
          </CardContent>
        </Card>

        {/* Active Clients */}
        <Card>
          <CardContent className="pt-6">
            <p className="text-xs text-muted-foreground font-medium mb-1">
              {isAr ? "العملاء النشطون" : "Active Clients"}
            </p>
            <p className="text-2xl font-bold tabular-nums">{activeClients}</p>
            <div className="flex items-center gap-1 mt-2">
              <TrendingDown className="w-3.5 h-3.5 text-red-400" />
              <span className="text-xs text-red-400 font-semibold">
                {churnedThisMonth}{" "}
                {isAr ? "تراجع هذا الشهر" : "churned this month"}
              </span>
            </div>
          </CardContent>
        </Card>

        {/* Health Score */}
        <Card>
          <CardContent className="pt-6">
            <p className="text-xs text-muted-foreground font-medium mb-1">
              {isAr ? "درجة الصحة" : "Health Score"}
            </p>
            <div className="flex items-center gap-2">
              <p className="text-2xl font-bold tabular-nums">{healthScore}</p>
              <Badge variant={healthTierVariant(healthScore)}>
                {healthTierLabel(healthScore, isAr)}
              </Badge>
            </div>
            <Progress value={healthScore} className="mt-3 h-1.5" />
          </CardContent>
        </Card>
      </div>

      {/* Section 2: MRR Trend Chart */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base font-semibold">
            {isAr ? "اتجاه الإيرادات الشهرية (12 شهرًا)" : "MRR Trend (12 months)"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart
              data={mrrChartData}
              margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="hsl(var(--border))"
                vertical={false}
              />
              <XAxis
                dataKey="month"
                tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
                axisLine={false}
                tickLine={false}
                tickFormatter={(v: number) => `${(v / 1000).toFixed(0)}K`}
                width={48}
              />
              <Tooltip content={<ChartTooltip />} />
              <Legend
                wrapperStyle={{
                  fontSize: 12,
                  color: "hsl(var(--muted-foreground))",
                }}
              />
              <Line
                type="monotone"
                dataKey={mrrKey}
                stroke="#C9A96E"
                strokeWidth={2.5}
                dot={false}
                activeDot={{ r: 5, fill: "#C9A96E" }}
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Section 3 + 4: Pipeline Funnel & Product Ladder side by side */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Pipeline Funnel */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base font-semibold">
              {isAr ? "مسار المبيعات" : "Pipeline Funnel"}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart
                layout="vertical"
                data={pipelineChartData}
                margin={{ top: 0, right: 20, left: 8, bottom: 0 }}
                barSize={20}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="hsl(var(--border))"
                  horizontal={false}
                />
                <XAxis
                  type="number"
                  tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  type="category"
                  dataKey="stage"
                  tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
                  axisLine={false}
                  tickLine={false}
                  width={90}
                />
                <Tooltip content={<ChartTooltip />} />
                <Bar
                  dataKey={countKey}
                  radius={[0, 6, 6, 0]}
                  fill="#C9A96E"
                />
              </BarChart>
            </ResponsiveContainer>
            {/* SAR values legend */}
            <div className="mt-3 space-y-1">
              {pipelineStages.map((s) => (
                <div
                  key={s.stageEn}
                  className="flex items-center justify-between text-xs text-muted-foreground"
                >
                  <span>{isAr ? s.stageAr : s.stageEn}</span>
                  <span className="tabular-nums font-medium text-foreground">
                    {s.value > 0 ? formatCurrency(s.value) : "—"}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Product Ladder Distribution */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base font-semibold">
              {isAr ? "توزيع مستويات المنتج" : "Product Ladder Distribution"}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col items-center gap-4">
              <ResponsiveContainer width="100%" height={180}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={80}
                    paddingAngle={3}
                    dataKey="value"
                  >
                    {pieData.map((entry, i) => (
                      <Cell key={i} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip content={<PieTooltip />} />
                </PieChart>
              </ResponsiveContainer>
              <div className="w-full space-y-1.5">
                {productTiers.map((t) => (
                  <div
                    key={t.nameEn}
                    className="flex items-center gap-2 text-xs"
                  >
                    <span
                      className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                      style={{ background: t.color }}
                    />
                    <span className="flex-1 text-muted-foreground truncate">
                      {isAr ? t.nameAr : t.nameEn}
                    </span>
                    <span className="font-medium tabular-nums text-foreground">
                      {t.value}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Section 5: Health Score Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base font-semibold">
            {isAr ? "تفاصيل درجة الصحة" : "Health Score Breakdown"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {healthDimensions.map((dim) => (
              <div key={dim.nameEn} className="space-y-1.5">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-foreground font-medium">
                    {isAr ? dim.nameAr : dim.nameEn}
                  </span>
                  <span className="tabular-nums text-muted-foreground">
                    {dim.score}%
                  </span>
                </div>
                <div className="h-2 w-full rounded-full bg-muted overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all ${dimensionBarColor(dim.score)}`}
                    style={{ width: `${dim.score}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Section 6: Weekly Activity Feed */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base font-semibold">
            {isAr ? "سجل النشاط الأسبوعي" : "Weekly Activity Feed"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {activityFeed.map((event) => (
              <div
                key={event.id}
                className="flex items-start gap-3 p-3 rounded-xl hover:bg-muted/50 transition-colors"
              >
                <div className="w-8 h-8 rounded-xl bg-muted flex items-center justify-center text-sm flex-shrink-0 font-bold text-muted-foreground">
                  {event.kind === "sprint"
                    ? "S"
                    : event.kind === "health"
                    ? "H"
                    : event.kind === "alert"
                    ? "A"
                    : event.kind === "diagnostic"
                    ? "D"
                    : "P"}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-foreground truncate">
                    {isAr ? event.titleAr : event.titleEn}
                  </p>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    {isAr ? event.timestampLabelAr : event.timestampLabel}
                  </p>
                </div>
                <Badge variant="outline" className="text-[10px] h-5 px-1.5 flex-shrink-0">
                  {isAr
                    ? event.kind === "sprint"
                      ? "سبرينت"
                      : event.kind === "health"
                      ? "صحة"
                      : event.kind === "alert"
                      ? "تنبيه"
                      : event.kind === "diagnostic"
                      ? "تشخيص"
                      : "إثبات"
                    : event.kind}
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
