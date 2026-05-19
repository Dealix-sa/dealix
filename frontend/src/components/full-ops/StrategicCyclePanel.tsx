"use client";

import { useLocale, useTranslations } from "next-intl";
import { motion } from "framer-motion";
import {
  AlertTriangle,
  Check,
  GitBranch,
  Play,
  RefreshCw,
  ShieldAlert,
  X,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn, formatRelativeTime } from "@/lib/utils";
import { decisionTypeVariant, statusVariant } from "./DecisionLedger";
import type { StrategicCycleResponse } from "./types";

export function StrategicCyclePanel({
  cycle,
  loading,
  running,
  onRun,
}: {
  cycle: StrategicCycleResponse | null;
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
        <div className="h-8 w-56 rounded bg-muted/40 animate-pulse" />
        <div className="h-40 rounded-xl border border-border bg-muted/30 animate-pulse" />
      </div>
    );
  }

  if (!cycle) {
    return (
      <div className="text-center py-10">
        <p className="text-sm text-muted-foreground mb-4">
          {t("strategy.cycle.empty")}
        </p>
        <Button variant="gold" size="sm" onClick={onRun} disabled={running}>
          {running ? (
            <RefreshCw className="w-3.5 h-3.5 me-1.5 animate-spin" />
          ) : (
            <Play className="w-3.5 h-3.5 me-1.5" />
          )}
          {t("strategy.cycle.runNow")}
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-foreground">
            {isAr ? cycle.title_ar : cycle.title_en}
          </p>
          <p className="text-xs text-muted-foreground mt-0.5">
            {cycle.on_date} · {cycle.cadence} ·{" "}
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
          {t("strategy.cycle.runNow")}
        </Button>
      </div>

      {/* Gate evaluations */}
      <div>
        <p className="text-xs font-semibold text-foreground mb-2">
          {t("strategy.cycle.gateEvaluations")}
        </p>
        {cycle.gate_evaluations.length === 0 ? (
          <p className="text-[11px] text-muted-foreground">
            {t("strategy.cycle.noGates")}
          </p>
        ) : (
          <div className="overflow-x-auto rounded-xl border border-border">
            <table className="w-full text-xs">
              <thead>
                <tr className="border-b border-border bg-muted/30 text-muted-foreground">
                  <th className="px-3 py-2 text-start font-semibold">
                    {t("strategy.cycle.col.gate")}
                  </th>
                  <th className="px-3 py-2 text-start font-semibold">
                    {t("strategy.cycle.col.result")}
                  </th>
                  <th className="px-3 py-2 text-end font-semibold">
                    {t("strategy.cycle.col.observed")}
                  </th>
                  <th className="px-3 py-2 text-start font-semibold">
                    {t("strategy.cycle.col.decisionType")}
                  </th>
                  <th className="px-3 py-2 text-start font-semibold">
                    {t("strategy.cycle.col.note")}
                  </th>
                </tr>
              </thead>
              <tbody>
                {cycle.gate_evaluations.map((g) => (
                  <tr
                    key={g.gate_id}
                    className="border-b border-border last:border-0 hover:bg-muted/20"
                  >
                    <td className="px-3 py-2 text-foreground">
                      {isAr ? g.title_ar : g.title_en}
                    </td>
                    <td className="px-3 py-2">
                      <Badge
                        variant={g.passed ? "emerald" : "red"}
                        className="text-[10px] px-1.5 py-0"
                      >
                        {g.passed ? (
                          <Check className="w-3 h-3 me-0.5" />
                        ) : (
                          <X className="w-3 h-3 me-0.5" />
                        )}
                        {g.passed
                          ? t("strategy.cycle.pass")
                          : t("strategy.cycle.fail")}
                      </Badge>
                    </td>
                    <td className="px-3 py-2 text-end tabular-nums text-foreground">
                      {g.observed_value}
                    </td>
                    <td className="px-3 py-2">
                      {g.decision_type ? (
                        <Badge
                          variant={decisionTypeVariant(g.decision_type)}
                          className="text-[10px] px-1.5 py-0"
                        >
                          {g.decision_type}
                        </Badge>
                      ) : (
                        <span className="text-muted-foreground">—</span>
                      )}
                    </td>
                    <td className="px-3 py-2 text-muted-foreground max-w-xs truncate">
                      {isAr ? g.note_ar : g.note_en}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Decisions */}
      <div>
        <p className="text-xs font-semibold text-foreground mb-2">
          {t("strategy.cycle.decisions")}
        </p>
        {cycle.decisions.length === 0 ? (
          <p className="text-[11px] text-muted-foreground">
            {t("strategy.cycle.noDecisions")}
          </p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {cycle.decisions.map((d, i) => (
              <motion.div
                key={d.decision_id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="rounded-xl border border-border bg-muted/20 p-3"
              >
                <div className="flex items-start justify-between gap-2">
                  <Badge
                    variant={decisionTypeVariant(d.decision_type)}
                    className="text-[10px] px-1.5 py-0"
                  >
                    {d.decision_type}
                  </Badge>
                  <Badge
                    variant={statusVariant(d.status)}
                    className="text-[10px] px-1.5 py-0"
                  >
                    {t(
                      `strategy.ledger.status.${d.status}` as "strategy.ledger.status.recommended",
                    )}
                  </Badge>
                </div>
                <p className="text-xs font-semibold text-foreground mt-2">
                  {d.target}
                </p>
                <p className="text-[11px] text-muted-foreground mt-0.5 leading-snug">
                  {isAr ? d.rationale_ar : d.rationale_en}
                </p>
                <div className="mt-1.5 flex flex-wrap items-center gap-1.5">
                  <span className="rounded-md bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground tabular-nums">
                    {t("strategy.ledger.col.score")}: {d.score}
                  </span>
                  <span className="rounded-md bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground">
                    {d.decision_band}
                  </span>
                  {d.irreversible && (
                    <span className="rounded-md bg-red-500/10 px-1.5 py-0.5 text-[10px] text-red-400">
                      {t("strategy.ledger.irreversible")}
                    </span>
                  )}
                  {d.requires_approval && (
                    <span className="rounded-md bg-gold-500/10 px-1.5 py-0.5 text-[10px] text-gold-400">
                      {t("strategy.ledger.requiresApproval")}
                    </span>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* Summary badges */}
      <div className="flex flex-wrap gap-2">
        <Badge variant="outline" className="text-xs">
          {t("strategy.cycle.approvalsPending")}: {cycle.approvals_pending.count}
        </Badge>
        <Badge variant="outline" className="text-xs">
          {t("strategy.cycle.delegatedCount")}: {cycle.delegated_cycles.length}
        </Badge>
      </div>

      {/* Delegated cycles */}
      {cycle.delegated_cycles.length > 0 && (
        <div>
          <p className="flex items-center gap-1.5 text-xs font-semibold text-foreground mb-2">
            <GitBranch className="w-3.5 h-3.5" />
            {t("strategy.cycle.delegatedCycles")}
          </p>
          <ul className="space-y-1.5">
            {cycle.delegated_cycles.map((dc) => (
              <li
                key={dc.cycle_id}
                className="flex items-start gap-2 text-xs text-muted-foreground"
              >
                <span className="mt-1.5 w-1 h-1 rounded-full bg-blue-400 flex-shrink-0" />
                <span>
                  <span className="font-mono text-foreground">
                    {dc.cycle_id}
                  </span>{" "}
                  · {dc.summary}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Next actions */}
      {cycle.next_actions.length > 0 && (
        <div>
          <p className="text-xs font-semibold text-foreground mb-2">
            {t("strategy.cycle.nextActions")}
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

      {/* Warnings */}
      {cycle.warnings.length > 0 && (
        <div className="rounded-xl border border-amber-500/20 bg-amber-500/5 p-3">
          <p className="flex items-center gap-1.5 text-xs font-semibold text-amber-400 mb-2">
            <AlertTriangle className="w-3.5 h-3.5" />
            {t("strategy.cycle.warnings")}
          </p>
          <ul className="space-y-1">
            {cycle.warnings.map((w, i) => (
              <li key={i} className="text-[11px] text-amber-400/90">
                {w}
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
            {t("strategy.cycle.hardGates")}
          </p>
          <div className={cn("flex flex-wrap gap-1.5")}>
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
