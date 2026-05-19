"use client";

import { useLocale, useTranslations } from "next-intl";
import { motion } from "framer-motion";
import { ArrowDown, Crown, Network, Users } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn, getStatusColor } from "@/lib/utils";
import type { StrategicAgentNode, StrategicTierResponse } from "./types";

function autonomyVariant(level: number): "emerald" | "blue" | "gold" {
  if (level >= 3) return "emerald";
  if (level === 2) return "blue";
  return "gold";
}

function AutonomyBadge({ level }: { level: number }) {
  return (
    <Badge variant={autonomyVariant(level)} className="text-[10px] px-1.5 py-0">
      {`L${level}`}
    </Badge>
  );
}

function StatusPill({ status }: { status: string }) {
  return (
    <Badge
      variant="outline"
      className={cn("text-[10px] px-1.5 py-0", getStatusColor(status))}
    >
      {status}
    </Badge>
  );
}

function NodeCard({
  node,
  isAr,
  variant,
}: {
  node: StrategicAgentNode;
  isAr: boolean;
  variant: "ceo" | "director";
}) {
  const role = isAr ? node.role_ar : node.role_en;
  const ring =
    variant === "ceo"
      ? "border-gold-500/40 bg-gold-500/5"
      : "border-blue-500/30 bg-blue-500/5";

  return (
    <div className={cn("rounded-xl border p-3", ring)}>
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <p className="text-sm font-semibold text-foreground truncate">
            {node.name}
          </p>
          <p className="text-xs text-muted-foreground truncate">{role}</p>
        </div>
        <div className="flex flex-col items-end gap-1 flex-shrink-0">
          <AutonomyBadge level={node.autonomy_level} />
          <StatusPill status={node.status} />
        </div>
      </div>
    </div>
  );
}

export function StrategyBoard({
  data,
  loading,
}: {
  data: StrategicTierResponse | null;
  loading: boolean;
}) {
  const t = useTranslations("fullOps");
  const locale = useLocale();
  const isAr = locale === "ar";

  if (loading) {
    return (
      <div className="space-y-3">
        <div className="h-20 rounded-2xl border border-border bg-muted/30 animate-pulse mx-auto max-w-md" />
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <div
              key={i}
              className="h-24 rounded-2xl border border-border bg-muted/30 animate-pulse"
            />
          ))}
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-12 text-muted-foreground">
        <Network className="w-8 h-8 mx-auto mb-2 opacity-50" />
        <p className="text-sm">{t("strategy.board.empty")}</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Totals */}
      <div className="flex flex-wrap gap-2">
        <Badge variant="gold" className="text-xs">
          <Crown className="w-3 h-3 me-1" />
          {t("strategy.board.ceoTier")}
        </Badge>
        <Badge variant="blue" className="text-xs">
          <Users className="w-3 h-3 me-1" />
          {t("strategy.board.directors")}: {data.totals.board_directors}
        </Badge>
        <Badge variant="emerald" className="text-xs">
          {t("strategy.board.maxAutonomy")}: L{data.totals.max_autonomy_level}
        </Badge>
      </div>

      {/* CEO */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="mx-auto max-w-md"
      >
        <p className="text-[11px] uppercase tracking-widest text-muted-foreground mb-1 text-center">
          {t("strategy.board.ceo")}
        </p>
        <NodeCard node={data.ceo} isAr={isAr} variant="ceo" />
      </motion.div>

      {/* Connector */}
      <div className="flex justify-center">
        <div className="h-4 w-px bg-border" />
      </div>

      {/* Board directors */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3">
        {data.board_directors.map((d, i) => (
          <motion.div
            key={d.agent_id}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 + i * 0.06 }}
          >
            <NodeCard node={d} isAr={isAr} variant="director" />
          </motion.div>
        ))}
      </div>

      {/* Delegation to operational pyramid */}
      <div className="flex flex-col items-center pt-1">
        <ArrowDown className="w-4 h-4 text-gold-400" />
        <div className="rounded-xl border border-gold-500/25 bg-gold-500/5 px-3 py-2 mt-1 text-center">
          <p className="text-[11px] text-muted-foreground">
            {t("strategy.board.delegatesTo")}
          </p>
          <p className="text-xs font-mono font-semibold text-gold-400 mt-0.5">
            {data.delegates_to_operational}
          </p>
        </div>
      </div>
    </div>
  );
}
