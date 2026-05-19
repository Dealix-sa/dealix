"use client";

import { useEffect, useState } from "react";
import { useTranslations, useLocale } from "next-intl";
import { motion } from "framer-motion";
import { TrendingUp } from "lucide-react";
import { cn, formatCurrency } from "@/lib/utils";
import { api } from "@/lib/api";
import type { DealStage } from "@/types";

const STAGES: { key: DealStage; color: string; dotColor: string }[] = [
  { key: "lead", color: "border-t-slate-400", dotColor: "bg-slate-400" },
  { key: "qualified", color: "border-t-blue-400", dotColor: "bg-blue-400" },
  { key: "proposal", color: "border-t-gold-400", dotColor: "bg-gold-400" },
  { key: "negotiation", color: "border-t-amber-400", dotColor: "bg-amber-400" },
  { key: "closed_won", color: "border-t-emerald-400", dotColor: "bg-emerald-400" },
];

// Backend `/revenue-pipeline/summary` returns aggregate counts only
// (pipeline_summary.total_leads / commitments / paid / total_revenue_sar),
// not per-deal rows. The board maps those aggregates onto its stage columns.
interface PipelineSummary {
  total_leads: number;
  commitments: number;
  paid: number;
  total_revenue_sar: number;
}

interface StageColumn {
  count: number;
  value: number;
}

// Map the aggregate pipeline summary onto the 5 visible stage columns.
function summaryToColumns(s: PipelineSummary): Record<DealStage, StageColumn> {
  const totalRevenue = s.total_revenue_sar ?? 0;
  const openLeads = Math.max((s.total_leads ?? 0) - (s.commitments ?? 0), 0);
  const openCommitments = Math.max((s.commitments ?? 0) - (s.paid ?? 0), 0);
  return {
    lead: { count: openLeads, value: 0 },
    qualified: { count: 0, value: 0 },
    proposal: { count: openCommitments, value: 0 },
    negotiation: { count: 0, value: 0 },
    closed_won: { count: s.paid ?? 0, value: totalRevenue },
    closed_lost: { count: 0, value: 0 },
  };
}

export function KanbanBoard() {
  const t = useTranslations();
  const locale = useLocale();
  const isAr = locale === "ar";

  const [columns, setColumns] = useState<Record<DealStage, StageColumn> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const res = await api.getPipeline();
        if (cancelled) return;
        const data = res.data as { pipeline_summary?: PipelineSummary } | undefined;
        const summary = data?.pipeline_summary;
        if (summary) {
          setColumns(summaryToColumns(summary));
          setError(null);
        }
      } catch {
        if (!cancelled) {
          setError(
            isAr ? "تعذر تحميل خط الأنابيب من الخادم" : "Could not load pipeline from API",
          );
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

  if (loading) {
    return (
      <p className="p-4 text-sm text-muted-foreground">
        {isAr ? "جاري التحميل…" : "Loading…"}
      </p>
    );
  }

  if (error) {
    return <p className="p-4 text-sm text-destructive">{error}</p>;
  }

  return (
    <div className="flex gap-4 overflow-x-auto pb-4 -mx-1 px-1">
      {STAGES.map((stageConfig, colIdx) => {
        const stageName = t(`pipeline.stages.${stageConfig.key === "closed_won" ? "closed" : stageConfig.key}` as "pipeline.stages.lead");
        const col = columns?.[stageConfig.key] ?? { count: 0, value: 0 };

        return (
          <motion.div
            key={stageConfig.key}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: colIdx * 0.07 }}
            className="flex-shrink-0 w-72"
          >
            {/* Column header */}
            <div className={cn("bg-card border border-border border-t-2 rounded-xl p-4 mb-3", stageConfig.color)}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className={cn("w-2 h-2 rounded-full", stageConfig.dotColor)} />
                  <h3 className="text-sm font-semibold text-foreground">{stageName}</h3>
                </div>
                <span className="text-xs bg-muted text-muted-foreground rounded-full px-2 py-0.5 font-medium">
                  {col.count}
                </span>
              </div>
              {col.value > 0 && (
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <TrendingUp className="w-3 h-3" />
                  <span>{formatCurrency(col.value)}</span>
                </div>
              )}
            </div>

            {/* Aggregate count — the pipeline API exposes counts, not per-deal rows */}
            <div className="rounded-xl border border-dashed border-border p-6 text-center">
              <p className="text-3xl font-bold tabular-nums text-foreground">{col.count}</p>
              <p className="text-xs text-muted-foreground mt-1">
                {isAr ? "في هذه المرحلة" : "in this stage"}
              </p>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
