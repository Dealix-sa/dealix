"use client";

import { useLocale, useTranslations } from "next-intl";
import { motion } from "framer-motion";
import { Cpu, Crown, Network } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn, getStatusColor } from "@/lib/utils";
import type { AgentNode, DirectorNode, HierarchyResponse } from "./types";

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
  node: AgentNode;
  isAr: boolean;
  variant: "orchestrator" | "director" | "operator";
}) {
  const role = isAr ? node.role_ar : node.role_en;
  const ring =
    variant === "orchestrator"
      ? "border-gold-500/40 bg-gold-500/5"
      : variant === "director"
        ? "border-blue-500/30 bg-blue-500/5"
        : "border-border bg-card";

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
      {node.capabilities && node.capabilities.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1">
          {node.capabilities.slice(0, 6).map((cap) => (
            <span
              key={cap}
              className="rounded-md bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground"
            >
              {cap}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

function DirectorBranch({
  director,
  isAr,
  index,
}: {
  director: DirectorNode;
  isAr: boolean;
  index: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 + index * 0.06 }}
      className="rounded-2xl border border-border bg-muted/20 p-3"
    >
      <NodeCard node={director} isAr={isAr} variant="director" />
      <div className="mt-3 space-y-2 ps-3 border-s border-dashed border-border">
        {director.operators.length === 0 ? (
          <p className="text-xs text-muted-foreground py-1">
            {isAr ? "لا مشغّلون" : "No operators"}
          </p>
        ) : (
          director.operators.map((op) => (
            <NodeCard key={op.agent_id} node={op} isAr={isAr} variant="operator" />
          ))
        )}
      </div>
    </motion.div>
  );
}

export function AgentPyramid({
  data,
  loading,
}: {
  data: HierarchyResponse | null;
  loading: boolean;
}) {
  const t = useTranslations("fullOps");
  const locale = useLocale();
  const isAr = locale === "ar";

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {Array.from({ length: 3 }).map((_, i) => (
          <div
            key={i}
            className="h-40 rounded-2xl border border-border bg-muted/30 animate-pulse"
          />
        ))}
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-12 text-muted-foreground">
        <Network className="w-8 h-8 mx-auto mb-2 opacity-50" />
        <p className="text-sm">{t("pyramid.empty")}</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Totals */}
      <div className="flex flex-wrap gap-2">
        <Badge variant="gold" className="text-xs">
          <Crown className="w-3 h-3 me-1" />
          {t("pyramid.directors")}: {data.totals.directors}
        </Badge>
        <Badge variant="blue" className="text-xs">
          <Cpu className="w-3 h-3 me-1" />
          {t("pyramid.operators")}: {data.totals.operators}
        </Badge>
        <Badge variant="emerald" className="text-xs">
          {t("pyramid.maxAutonomy")}: L{data.totals.max_autonomy_level}
        </Badge>
      </div>

      {/* Orchestrator */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="mx-auto max-w-md"
      >
        <p className="text-[11px] uppercase tracking-widest text-muted-foreground mb-1 text-center">
          {t("pyramid.orchestrator")}
        </p>
        <NodeCard node={data.orchestrator} isAr={isAr} variant="orchestrator" />
      </motion.div>

      {/* Connector */}
      <div className="flex justify-center">
        <div className="h-4 w-px bg-border" />
      </div>

      {/* Directors + operators */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
        {data.directors.map((d, i) => (
          <DirectorBranch key={d.agent_id} director={d} isAr={isAr} index={i} />
        ))}
      </div>
    </div>
  );
}
