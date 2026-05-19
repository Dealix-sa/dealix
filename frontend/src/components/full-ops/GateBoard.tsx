"use client";

import { useLocale, useTranslations } from "next-intl";
import { ShieldCheck } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { GateRuleItem } from "./types";

function severityVariant(severity: string): "red" | "gold" | "blue" {
  const s = severity.toLowerCase();
  if (s === "critical" || s === "high") return "red";
  if (s === "medium") return "gold";
  return "blue";
}

function GateChip({ gate, isAr }: { gate: GateRuleItem; isAr: boolean }) {
  const title = isAr ? gate.title_ar : gate.title_en;
  return (
    <div className="rounded-xl border border-border bg-muted/20 p-3">
      <div className="flex items-start justify-between gap-2">
        <p className="text-xs font-semibold text-foreground leading-snug">
          {title}
        </p>
        <Badge
          variant={severityVariant(gate.severity)}
          className="text-[10px] px-1.5 py-0 flex-shrink-0"
        >
          {gate.severity}
        </Badge>
      </div>
      <p className="text-[11px] text-muted-foreground mt-1.5 font-mono">
        {gate.metric} {gate.comparator} {gate.threshold}
      </p>
      <div className="mt-1.5 flex flex-wrap items-center gap-1.5">
        <span className="rounded-md bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground">
          {gate.source}
        </span>
        {gate.window_day !== null && (
          <span className="rounded-md bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground">
            {isAr ? `يوم ${gate.window_day}` : `day ${gate.window_day}`}
          </span>
        )}
        <span className="rounded-md bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground font-mono">
          {gate.gate_id}
        </span>
      </div>
    </div>
  );
}

export function GateBoard({
  gates,
  loading,
}: {
  gates: GateRuleItem[];
  loading: boolean;
}) {
  const t = useTranslations("fullOps");
  const locale = useLocale();
  const isAr = locale === "ar";

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div
            key={i}
            className="h-24 rounded-xl border border-border bg-muted/30 animate-pulse"
          />
        ))}
      </div>
    );
  }

  if (gates.length === 0) {
    return (
      <div className={cn("text-center py-10 text-muted-foreground")}>
        <ShieldCheck className="w-8 h-8 mx-auto mb-2 opacity-50" />
        <p className="text-sm">{t("strategy.gates.empty")}</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <p className="text-xs text-muted-foreground">
        {t("strategy.gates.count", { count: gates.length })}
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
        {gates.map((gate) => (
          <GateChip key={gate.gate_id} gate={gate} isAr={isAr} />
        ))}
      </div>
    </div>
  );
}
