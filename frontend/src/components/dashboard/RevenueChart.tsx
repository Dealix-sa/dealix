"use client";

import { useEffect, useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { useTranslations, useLocale } from "next-intl";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency } from "@/lib/utils";
import { api } from "@/lib/api";
import type { RevenueDataPoint } from "@/types";

// `/dashboard/metrics` returns a single point-in-time snapshot, not a
// monthly series. Backend deals: { revenue_sar_paid, paid } feeds the
// current-period bar; pipeline (commitments) feeds the target line.
interface DashboardMetrics {
  deals?: { total?: number; paid?: number; revenue_sar_paid?: number };
}

interface PipelineSummary {
  total_revenue_sar?: number;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-card border border-border rounded-xl p-3 shadow-xl text-sm">
        <p className="font-semibold text-foreground mb-2">{label}</p>
        {payload.map((entry: { name: string; value: number; color: string }, i: number) => (
          <p key={i} style={{ color: entry.color }} className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full inline-block" style={{ background: entry.color }} />
            {entry.name}: {formatCurrency(entry.value)}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export function RevenueChart() {
  const t = useTranslations("dashboard");
  const locale = useLocale();
  const isAr = locale === "ar";

  const [data, setData] = useState<RevenueDataPoint[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const [metricsRes, pipelineRes] = await Promise.all([
          api.getDashboardMetrics(),
          api.getPipeline(),
        ]);
        if (cancelled) return;
        const metrics = (metricsRes.data?.data ?? metricsRes.data) as
          | DashboardMetrics
          | undefined;
        const pipeline = (pipelineRes.data as { pipeline_summary?: PipelineSummary } | undefined)
          ?.pipeline_summary;

        const revenue = metrics?.deals?.revenue_sar_paid ?? 0;
        const deals = metrics?.deals?.paid ?? 0;
        const target = pipeline?.total_revenue_sar ?? revenue;

        setData([
          {
            month: isAr ? "حتى تاريخه" : "To date",
            revenue,
            target,
            deals,
          },
        ]);
        setError(null);
      } catch {
        if (!cancelled) {
          setError(isAr ? "تعذر تحميل بيانات الإيرادات" : "Could not load revenue data");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [isAr]);

  return (
    <Card className="col-span-2">
      <CardHeader>
        <CardTitle className="text-base font-semibold">{t("revenueChart")}</CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? (
          <p className="text-sm text-muted-foreground py-24 text-center">
            {isAr ? "جاري التحميل…" : "Loading…"}
          </p>
        ) : error ? (
          <p className="text-sm text-destructive py-24 text-center">{error}</p>
        ) : (
        <ResponsiveContainer width="100%" height={280}>
          <AreaChart data={data} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
            <defs>
              <linearGradient id="revenueGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#C9A96E" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#C9A96E" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="targetGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
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
              tickFormatter={(v) => `${(v / 1000000).toFixed(1)}M`}
              width={50}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              wrapperStyle={{ fontSize: 12, color: "hsl(var(--muted-foreground))" }}
            />
            <Area
              type="monotone"
              dataKey="revenue"
              name={locale === "ar" ? "الإيرادات" : "Revenue"}
              stroke="#C9A96E"
              strokeWidth={2.5}
              fill="url(#revenueGrad)"
              dot={false}
              activeDot={{ r: 5, fill: "#C9A96E" }}
            />
            <Area
              type="monotone"
              dataKey="target"
              name={locale === "ar" ? "الهدف" : "Target"}
              stroke="#10b981"
              strokeWidth={2}
              fill="url(#targetGrad)"
              strokeDasharray="5 3"
              dot={false}
              activeDot={{ r: 4, fill: "#10b981" }}
            />
          </AreaChart>
        </ResponsiveContainer>
        )}
      </CardContent>
    </Card>
  );
}
