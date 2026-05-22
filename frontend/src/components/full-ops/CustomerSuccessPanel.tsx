"use client";

import { useLocale, useTranslations } from "next-intl";
import { AlertTriangle, Play, RefreshCw, TrendingUp, Users } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn, formatRelativeTime } from "@/lib/utils";
import type { CsCycleResponse, CsOpportunity } from "./types";

function urgencyVariant(
  urgency?: string,
): "red" | "gold" | "blue" | "outline" {
  if (urgency === "urgent") return "red";
  if (urgency === "high") return "gold";
  if (urgency === "normal") return "blue";
  return "outline";
}

function StatTile({
  label,
  value,
  tone,
}: {
  label: string;
  value: number;
  tone: "rose" | "emerald" | "blue" | "gold" | "muted";
}) {
  const ring =
    tone === "rose"
      ? "border-rose-500/30 bg-rose-500/5 text-rose-300"
      : tone === "emerald"
        ? "border-emerald-500/30 bg-emerald-500/5 text-emerald-300"
        : tone === "blue"
          ? "border-blue-500/30 bg-blue-500/5 text-blue-300"
          : tone === "gold"
            ? "border-gold-500/30 bg-gold-500/5 text-gold-300"
            : "border-border bg-muted/30 text-muted-foreground";
  return (
    <div
      className={cn(
        "rounded-xl border px-3 py-2.5 flex flex-col gap-0.5",
        ring,
      )}
    >
      <span className="text-[10px] uppercase tracking-wider opacity-70">
        {label}
      </span>
      <span className="text-xl font-semibold tabular-nums">{value}</span>
    </div>
  );
}

export function CustomerSuccessPanel({
  cycle,
  loading,
  running,
  onRun,
}: {
  cycle: CsCycleResponse | null;
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
        <div className="h-32 rounded-xl border border-border bg-muted/30 animate-pulse" />
      </div>
    );
  }

  if (!cycle || !cycle.cycle_id) {
    return (
      <div className="text-center py-10">
        <p className="text-sm text-muted-foreground mb-4">
          {t("cs.empty")}
        </p>
        <Button variant="gold" size="sm" onClick={onRun} disabled={running}>
          {running ? (
            <RefreshCw className="w-3.5 h-3.5 me-1.5 animate-spin" />
          ) : (
            <Play className="w-3.5 h-3.5 me-1.5" />
          )}
          {t("cs.runNow")}
        </Button>
      </div>
    );
  }

  const summary = cycle.summary ?? {};
  const opportunities: CsOpportunity[] = cycle.opportunities ?? [];

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-foreground">
            {isAr ? cycle.title_ar : cycle.title_en}
          </p>
          <p className="text-xs text-muted-foreground mt-0.5">
            {cycle.on_date}
            {cycle.generated_at
              ? ` · ${formatRelativeTime(cycle.generated_at, locale)}`
              : ""}{" "}
            · <span className="font-mono">{cycle.cycle_id}</span>
          </p>
        </div>
        <Button variant="gold" size="sm" onClick={onRun} disabled={running}>
          {running ? (
            <RefreshCw className="w-3.5 h-3.5 me-1.5 animate-spin" />
          ) : (
            <Play className="w-3.5 h-3.5 me-1.5" />
          )}
          {t("cs.runNow")}
        </Button>
      </div>

      {/* Summary tiles */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-2">
        <StatTile
          label={t("cs.summary.active")}
          value={summary.active_customers ?? 0}
          tone="muted"
        />
        <StatTile
          label={t("cs.summary.opportunities")}
          value={summary.opportunities_total ?? 0}
          tone="blue"
        />
        <StatTile
          label={t("cs.summary.atRisk")}
          value={summary.at_risk ?? 0}
          tone="rose"
        />
        <StatTile
          label={t("cs.summary.expansion")}
          value={summary.expansion_ready ?? 0}
          tone="emerald"
        />
        <StatTile
          label={t("cs.summary.renewals")}
          value={summary.renewals_due ?? 0}
          tone="gold"
        />
        <StatTile
          label={t("cs.summary.detractors")}
          value={summary.nps_detractors ?? 0}
          tone="rose"
        />
      </div>

      {/* Counters */}
      <div className="flex flex-wrap gap-2 text-[11px] text-muted-foreground">
        <span className="inline-flex items-center gap-1.5">
          <Users className="w-3.5 h-3.5" />
          {t("cs.approvalsCreated", {
            count: cycle.approvals_created ?? 0,
          })}
        </span>
        <span className="inline-flex items-center gap-1.5">
          <TrendingUp className="w-3.5 h-3.5" />
          {t("cs.workItemsCreated", {
            count: cycle.work_items_created ?? 0,
          })}
        </span>
      </div>

      {/* Opportunity list */}
      <div>
        <p className="text-xs font-semibold text-foreground mb-2">
          {t("cs.opportunities")}
        </p>
        {opportunities.length === 0 ? (
          <p className="text-[11px] text-muted-foreground">
            {t("cs.noOpportunities")}
          </p>
        ) : (
          <ul className="space-y-2">
            {opportunities.slice(0, 12).map((opp, idx) => {
              const action = isAr
                ? opp.recommended_action_ar
                : opp.recommended_action_en;
              return (
                <li
                  key={`${opp.customer_id ?? "?"}-${opp.type ?? "?"}-${idx}`}
                  className="rounded-xl border border-border bg-muted/20 px-3 py-2 flex flex-col gap-1"
                >
                  <div className="flex flex-wrap items-center gap-2">
                    <Badge
                      variant={urgencyVariant(opp.urgency)}
                      className="text-[10px] px-1.5 py-0"
                    >
                      {opp.urgency ?? "normal"}
                    </Badge>
                    <span className="text-xs font-semibold text-foreground">
                      {opp.type ?? ""}
                    </span>
                    <span className="text-[11px] font-mono text-muted-foreground">
                      {opp.customer_id ?? ""}
                    </span>
                  </div>
                  {action ? (
                    <p className="text-[12px] text-muted-foreground leading-relaxed">
                      {action}
                    </p>
                  ) : null}
                </li>
              );
            })}
          </ul>
        )}
      </div>

      {/* Hard gates */}
      {cycle.hard_gates && cycle.hard_gates.length > 0 ? (
        <div>
          <p className="text-xs font-semibold text-foreground mb-2">
            {t("cs.hardGates")}
          </p>
          <div className="flex flex-wrap gap-1.5">
            {cycle.hard_gates.map((gate) => (
              <Badge
                key={gate}
                variant="outline"
                className="text-[10px] px-1.5 py-0 font-mono"
              >
                {gate}
              </Badge>
            ))}
          </div>
        </div>
      ) : null}

      {/* Warnings */}
      {cycle.warnings && cycle.warnings.length > 0 ? (
        <div className="rounded-xl border border-amber-500/30 bg-amber-500/5 px-3 py-2">
          <p className="text-xs font-semibold text-amber-300 mb-1 inline-flex items-center gap-1.5">
            <AlertTriangle className="w-3.5 h-3.5" />
            {t("cs.warnings")}
          </p>
          <ul className="text-[11px] text-amber-200/90 list-disc list-inside space-y-0.5">
            {cycle.warnings.slice(0, 5).map((w, idx) => (
              <li key={idx}>{w}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
