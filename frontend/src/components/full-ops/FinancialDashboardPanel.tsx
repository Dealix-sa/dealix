"use client";

import { useLocale, useTranslations } from "next-intl";
import {
  AlertTriangle,
  Coins,
  Play,
  RefreshCw,
  ShieldAlert,
  TrendingDown,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn, formatRelativeTime } from "@/lib/utils";
import type { FinancialCycleResponse } from "./types";

function severityVariant(
  severity?: string,
): "red" | "gold" | "blue" | "outline" {
  if (severity === "critical") return "red";
  if (severity === "high") return "red";
  if (severity === "medium") return "gold";
  if (severity === "low") return "blue";
  return "outline";
}

function fmtNumber(n: number | undefined, locale: string): string {
  if (n === undefined || n === null || Number.isNaN(n)) return "—";
  try {
    return new Intl.NumberFormat(locale, { maximumFractionDigits: 1 }).format(n);
  } catch {
    return String(n);
  }
}

function MetricTile({
  label,
  value,
  suffix,
  tone,
}: {
  label: string;
  value: string;
  suffix?: string;
  tone: "emerald" | "rose" | "blue" | "gold" | "muted";
}) {
  const ring =
    tone === "emerald"
      ? "border-emerald-500/30 bg-emerald-500/5 text-emerald-300"
      : tone === "rose"
        ? "border-rose-500/30 bg-rose-500/5 text-rose-300"
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
      <span className="text-xl font-semibold tabular-nums">
        {value}
        {suffix ? (
          <span className="ms-1 text-[11px] font-normal opacity-70">
            {suffix}
          </span>
        ) : null}
      </span>
    </div>
  );
}

export function FinancialDashboardPanel({
  cycle,
  loading,
  running,
  onRun,
}: {
  cycle: FinancialCycleResponse | null;
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

  if (!cycle || cycle.empty) {
    return (
      <div className="text-center py-10">
        <p className="text-sm text-muted-foreground mb-4">
          {t("financial.empty")}
        </p>
        <Button variant="gold" size="sm" onClick={onRun} disabled={running}>
          {running ? (
            <RefreshCw className="w-3.5 h-3.5 me-1.5 animate-spin" />
          ) : (
            <Play className="w-3.5 h-3.5 me-1.5" />
          )}
          {t("financial.runNow")}
        </Button>
      </div>
    );
  }

  const m = cycle.metrics ?? {};
  const anomalies = cycle.anomalies ?? [];
  const violations = cycle.threshold_violations ?? [];
  const pendingCount = cycle.approvals_pending?.count ?? 0;

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-foreground">
            {isAr ? cycle.title_ar : cycle.title_en}
          </p>
          <p className="text-xs text-muted-foreground mt-0.5">
            {cycle.period_end} · {cycle.cadence}
            {cycle.generated_at
              ? ` · ${formatRelativeTime(cycle.generated_at, locale)}`
              : ""}
            {cycle.cycle_id ? (
              <>
                {" "}
                · <span className="font-mono">{cycle.cycle_id}</span>
              </>
            ) : null}
          </p>
        </div>
        <Button variant="gold" size="sm" onClick={onRun} disabled={running}>
          {running ? (
            <RefreshCw className="w-3.5 h-3.5 me-1.5 animate-spin" />
          ) : (
            <Play className="w-3.5 h-3.5 me-1.5" />
          )}
          {t("financial.runNow")}
        </Button>
      </div>

      {/* Metric tiles */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
        <MetricTile
          label={t("financial.metrics.mrr")}
          value={fmtNumber(m.mrr_sar, locale)}
          suffix="SAR"
          tone="emerald"
        />
        <MetricTile
          label={t("financial.metrics.arr")}
          value={fmtNumber(m.arr_sar, locale)}
          suffix="SAR"
          tone="emerald"
        />
        <MetricTile
          label={t("financial.metrics.nrr")}
          value={fmtNumber(m.nrr_pct, locale)}
          suffix="%"
          tone="blue"
        />
        <MetricTile
          label={t("financial.metrics.churn")}
          value={fmtNumber(m.churn_pct_monthly, locale)}
          suffix="%"
          tone="rose"
        />
        <MetricTile
          label={t("financial.metrics.runway")}
          value={fmtNumber(m.runway_months, locale)}
          suffix={t("financial.metrics.monthsUnit")}
          tone="gold"
        />
        <MetricTile
          label={t("financial.metrics.margin")}
          value={fmtNumber(m.gross_margin_pct, locale)}
          suffix="%"
          tone="emerald"
        />
        <MetricTile
          label={t("financial.metrics.ltv")}
          value={fmtNumber(m.ltv_sar, locale)}
          suffix="SAR"
          tone="blue"
        />
        <MetricTile
          label={t("financial.metrics.cacPayback")}
          value={fmtNumber(m.cac_payback_months, locale)}
          suffix={t("financial.metrics.monthsUnit")}
          tone="muted"
        />
      </div>

      {/* Pending approvals */}
      <div className="flex flex-wrap gap-2 text-[11px] text-muted-foreground">
        <span className="inline-flex items-center gap-1.5">
          <ShieldAlert className="w-3.5 h-3.5" />
          {t("financial.approvalsPending", { count: pendingCount })}
        </span>
        <span className="inline-flex items-center gap-1.5">
          <Coins className="w-3.5 h-3.5" />
          {t("financial.anomalyCount", { count: anomalies.length })}
        </span>
        <span className="inline-flex items-center gap-1.5">
          <TrendingDown className="w-3.5 h-3.5" />
          {t("financial.violationCount", { count: violations.length })}
        </span>
      </div>

      {/* Threshold violations */}
      {violations.length > 0 ? (
        <div>
          <p className="text-xs font-semibold text-foreground mb-2">
            {t("financial.violationsTitle")}
          </p>
          <ul className="space-y-2">
            {violations.slice(0, 12).map((v, idx) => {
              const rule = v.rule ?? {};
              const title = isAr ? rule.title_ar : rule.title_en;
              return (
                <li
                  key={`${rule.rule_id ?? "rule"}-${idx}`}
                  className="rounded-xl border border-border bg-muted/20 px-3 py-2 flex flex-col gap-1"
                >
                  <div className="flex flex-wrap items-center gap-2">
                    <Badge
                      variant={severityVariant(rule.severity)}
                      className="text-[10px] px-1.5 py-0"
                    >
                      {rule.severity ?? "low"}
                    </Badge>
                    <span className="text-xs font-semibold text-foreground">
                      {title ?? rule.rule_id}
                    </span>
                    <span className="text-[11px] font-mono text-muted-foreground">
                      {rule.metric} {rule.comparator}{" "}
                      {fmtNumber(rule.threshold, locale)}
                    </span>
                  </div>
                  <p className="text-[12px] text-muted-foreground">
                    {t("financial.observed")}{" "}
                    <span className="font-mono">
                      {fmtNumber(v.observed_value, locale)}
                    </span>
                    {" · "}
                    {t("financial.action")}{" "}
                    <span className="font-mono">
                      {v.action_on_violation ?? rule.action_on_violation ?? ""}
                    </span>
                  </p>
                </li>
              );
            })}
          </ul>
        </div>
      ) : null}

      {/* Anomalies */}
      {anomalies.length > 0 ? (
        <div>
          <p className="text-xs font-semibold text-foreground mb-2">
            {t("financial.anomaliesTitle")}
          </p>
          <ul className="space-y-2">
            {anomalies.slice(0, 8).map((a, idx) => {
              const title = isAr ? a.title_ar : a.title_en;
              return (
                <li
                  key={`${a.kind ?? "anomaly"}-${idx}`}
                  className="rounded-xl border border-border bg-muted/20 px-3 py-2 flex flex-col gap-1"
                >
                  <div className="flex flex-wrap items-center gap-2">
                    <Badge
                      variant={severityVariant(a.severity)}
                      className="text-[10px] px-1.5 py-0"
                    >
                      {a.severity ?? "low"}
                    </Badge>
                    <span className="text-xs font-semibold text-foreground">
                      {title ?? a.kind ?? ""}
                    </span>
                  </div>
                  <p className="text-[11px] font-mono text-muted-foreground">
                    obs={fmtNumber(a.observed, locale)} · exp=
                    {fmtNumber(a.expected, locale)}
                    {typeof a.delta_pct === "number"
                      ? ` · Δ=${fmtNumber(a.delta_pct, locale)}%`
                      : ""}
                  </p>
                </li>
              );
            })}
          </ul>
        </div>
      ) : null}

      {/* Hard gates */}
      {cycle.hard_gates && cycle.hard_gates.length > 0 ? (
        <div>
          <p className="text-xs font-semibold text-foreground mb-2">
            {t("financial.hardGates")}
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
            {t("financial.warnings")}
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
