"use client";

import { useEffect, useState } from "react";
import { useTranslations, useLocale } from "next-intl";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

const stageColors: Record<string, string> = {
  lead: "#94a3b8",
  qualified: "#60a5fa",
  proposal: "#C9A96E",
  negotiation: "#f59e0b",
  closed_won: "#10b981",
  closed_lost: "#ef4444",
};

// `/revenue-pipeline/summary` -> pipeline_summary aggregate counts.
interface PipelineSummary {
  total_leads: number;
  commitments: number;
  paid: number;
  total_revenue_sar: number;
}

interface PipelineBar {
  stage: string;
  count: number;
  value: number;
  key: string;
}

// Map the aggregate pipeline summary onto the chart's stage bars.
function summaryToBars(s: PipelineSummary, isAr: boolean): PipelineBar[] {
  const openLeads = Math.max((s.total_leads ?? 0) - (s.commitments ?? 0), 0);
  const openCommitments = Math.max((s.commitments ?? 0) - (s.paid ?? 0), 0);
  return [
    {
      key: "lead",
      stage: isAr ? "عميل محتمل" : "Lead",
      count: openLeads,
      value: 0,
    },
    {
      key: "proposal",
      stage: isAr ? "التزام" : "Commitment",
      count: openCommitments,
      value: 0,
    },
    {
      key: "closed_won",
      stage: isAr ? "مدفوع" : "Paid",
      count: s.paid ?? 0,
      value: s.total_revenue_sar ?? 0,
    },
  ];
}

export function DealPipelineChart() {
  const t = useTranslations("dashboard");
  const locale = useLocale();
  const isAr = locale === "ar";

  const [data, setData] = useState<PipelineBar[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const res = await api.getPipeline();
        if (cancelled) return;
        const body = res.data as { pipeline_summary?: PipelineSummary } | undefined;
        const summary = body?.pipeline_summary;
        if (summary) {
          setData(summaryToBars(summary, isAr));
          setError(null);
        }
      } catch {
        if (!cancelled) {
          setError(isAr ? "تعذر تحميل خط الأنابيب" : "Could not load pipeline");
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
    <Card>
      <CardHeader>
        <CardTitle className="text-base font-semibold">{t("dealPipeline")}</CardTitle>
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
          <BarChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 5 }} barSize={32}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
            <XAxis
              dataKey="stage"
              tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              contentStyle={{
                background: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "12px",
                fontSize: 12,
              }}
              cursor={{ fill: "hsl(var(--muted))" }}
            />
            <Bar dataKey="count" radius={[6, 6, 0, 0]}>
              {data.map((entry) => (
                <Cell key={entry.key} fill={stageColors[entry.key] ?? "#C9A96E"} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
        )}
      </CardContent>
    </Card>
  );
}
