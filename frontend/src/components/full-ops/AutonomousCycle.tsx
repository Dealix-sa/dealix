"use client";

import { useLocale, useTranslations } from "next-intl";
import { motion } from "framer-motion";
import { Play, RefreshCw, ShieldAlert } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { formatRelativeTime } from "@/lib/utils";
import type { CycleResponse } from "./types";

interface StageView {
  key: string;
  count: number;
}

function buildStages(cycle: CycleResponse): StageView[] {
  return [
    { key: "intake", count: cycle.stages.intake.count },
    { key: "enriched", count: cycle.stages.enriched.count },
    { key: "scored", count: cycle.stages.scored.count },
    { key: "qualified", count: cycle.stages.qualified.count },
    { key: "drafts", count: cycle.stages.drafts.count },
    { key: "proof", count: cycle.stages.proof_events.count },
  ];
}

export function AutonomousCycle({
  cycle,
  loading,
  running,
  onRun,
}: {
  cycle: CycleResponse | null;
  loading: boolean;
  running: boolean;
  onRun: () => void;
}) {
  const t = useTranslations("fullOps");
  const locale = useLocale();
  const isAr = locale === "ar";

  if (loading) {
    return (
      <div className="space-y-3">
        <div className="h-8 w-48 rounded bg-muted/40 animate-pulse" />
        <div className="grid grid-cols-3 md:grid-cols-6 gap-2">
          {Array.from({ length: 6 }).map((_, i) => (
            <div
              key={i}
              className="h-20 rounded-xl border border-border bg-muted/30 animate-pulse"
            />
          ))}
        </div>
      </div>
    );
  }

  if (!cycle) {
    return (
      <div className="text-center py-10">
        <p className="text-sm text-muted-foreground mb-4">
          {t("cycle.empty")}
        </p>
        <Button variant="gold" size="sm" onClick={onRun} disabled={running}>
          {running ? (
            <RefreshCw className="w-3.5 h-3.5 me-1.5 animate-spin" />
          ) : (
            <Play className="w-3.5 h-3.5 me-1.5" />
          )}
          {t("cycle.runNow")}
        </Button>
      </div>
    );
  }

  const stages = buildStages(cycle);
  const maxCount = Math.max(1, ...stages.map((s) => s.count));
  const q = cycle.stages.qualified;

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-foreground">
            {isAr ? cycle.title_ar : cycle.title_en}
          </p>
          <p className="text-xs text-muted-foreground mt-0.5">
            {cycle.on_date} ·{" "}
            {formatRelativeTime(cycle.generated_at, locale)} ·{" "}
            <span className="font-mono">{cycle.cycle_id}</span>
          </p>
        </div>
        <Button variant="gold" size="sm" onClick={onRun} disabled={running}>
          {running ? (
            <RefreshCw className="w-3.5 h-3.5 me-1.5 animate-spin" />
          ) : (
            <Play className="w-3.5 h-3.5 me-1.5" />
          )}
          {t("cycle.runNow")}
        </Button>
      </div>

      {/* Stage funnel */}
      <div className="grid grid-cols-3 md:grid-cols-6 gap-2">
        {stages.map((stage, i) => (
          <motion.div
            key={stage.key}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className="rounded-xl border border-border bg-muted/20 p-3"
          >
            <p className="text-2xl font-bold text-foreground tabular-nums">
              {stage.count}
            </p>
            <p className="text-[11px] text-muted-foreground mt-0.5">
              {t(`cycle.stages.${stage.key}` as "cycle.stages.intake")}
            </p>
            <Progress
              value={(stage.count / maxCount) * 100}
              className="mt-2 h-1"
            />
          </motion.div>
        ))}
      </div>

      {/* Qualified breakdown */}
      <div className="flex flex-wrap gap-2">
        <Badge variant="emerald" className="text-xs">
          {t("cycle.accept")}: {q.accept}
        </Badge>
        <Badge variant="gold" className="text-xs">
          {t("cycle.diagnostic")}: {q.diagnostic}
        </Badge>
        <Badge variant="red" className="text-xs">
          {t("cycle.reject")}: {q.reject}
        </Badge>
        <Badge variant="outline" className="text-xs">
          {t("cycle.approvalsPending")}: {cycle.approvals_pending.count}
        </Badge>
      </div>

      {/* Next actions */}
      {cycle.next_actions.length > 0 && (
        <div>
          <p className="text-xs font-semibold text-foreground mb-2">
            {t("cycle.nextActions")}
          </p>
          <ul className="space-y-1.5">
            {cycle.next_actions.map((action, i) => (
              <li
                key={i}
                className="flex items-start gap-2 text-xs text-muted-foreground"
              >
                <span className="mt-1.5 w-1 h-1 rounded-full bg-gold-400 flex-shrink-0" />
                <span>{isAr ? action.ar : action.en}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Hard gates */}
      {cycle.hard_gates.length > 0 && (
        <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-3">
          <p className="flex items-center gap-1.5 text-xs font-semibold text-red-400 mb-2">
            <ShieldAlert className="w-3.5 h-3.5" />
            {t("cycle.hardGates")}
          </p>
          <div className="flex flex-wrap gap-1.5">
            {cycle.hard_gates.map((gate) => (
              <span
                key={gate}
                className="rounded-md bg-red-500/10 px-1.5 py-0.5 text-[10px] text-red-400"
              >
                {gate}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
