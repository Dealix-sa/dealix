"use client";

import { useLocale, useTranslations } from "next-intl";
import { motion } from "framer-motion";
import { AlertOctagon, Ban, ShieldAlert } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import type { BilingualText, CommandCenterResponse, QueueBlock } from "./types";

function QueuePanel({
  titleKey,
  block,
  isAr,
}: {
  titleKey: string;
  block: QueueBlock;
  isAr: boolean;
}) {
  const t = useTranslations("fullOps");
  return (
    <div className="rounded-xl border border-border bg-muted/20 p-3">
      <div className="flex items-center justify-between mb-2">
        <p className="text-xs font-semibold text-foreground">
          {t(`commandCenter.queues.${titleKey}` as "commandCenter.queues.growth")}
        </p>
        <Badge variant="outline" className="text-[10px]">
          {block.count}
        </Badge>
      </div>
      {block.top_3.length === 0 ? (
        <p className="text-[11px] text-muted-foreground">
          {t("commandCenter.queueEmpty")}
        </p>
      ) : (
        <ul className="space-y-1">
          {block.top_3.map((row, i) => (
            <li
              key={i}
              className="flex items-start gap-1.5 text-[11px] text-muted-foreground"
            >
              <span className="mt-1.5 w-1 h-1 rounded-full bg-blue-400 flex-shrink-0" />
              <span className="truncate">{isAr ? row.ar : row.en}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export function CommandCenter({
  data,
  loading,
}: {
  data: CommandCenterResponse | null;
  loading: boolean;
}) {
  const t = useTranslations("fullOps");
  const locale = useLocale();
  const isAr = locale === "ar";

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <div
            key={i}
            className="h-28 rounded-xl border border-border bg-muted/30 animate-pulse"
          />
        ))}
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-10 text-muted-foreground">
        <p className="text-sm">{t("commandCenter.empty")}</p>
      </div>
    );
  }

  const decisions: BilingualText[] = data.today_top_3_decisions ?? [];
  const queues: { key: string; block: QueueBlock }[] = [
    { key: "growth", block: data.growth_queue },
    { key: "sales", block: data.sales_queue },
    { key: "support", block: data.support_queue },
    { key: "cs", block: data.cs_queue },
    { key: "delivery", block: data.delivery_queue },
  ];

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold text-foreground">
          {isAr ? data.title_ar : data.title_en}
        </p>
      </div>

      {/* Top 3 decisions */}
      <div>
        <p className="text-xs font-semibold text-foreground mb-2">
          {t("commandCenter.topDecisions")}
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
          {decisions.length === 0 ? (
            <p className="text-[11px] text-muted-foreground">
              {t("commandCenter.noDecisions")}
            </p>
          ) : (
            decisions.map((d, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.06 }}
                className="rounded-xl border border-gold-500/25 bg-gold-500/5 p-3"
              >
                <span className="inline-flex w-5 h-5 items-center justify-center rounded-md bg-gold-500/15 text-[11px] font-bold text-gold-400 mb-1.5">
                  {i + 1}
                </span>
                <p className="text-xs text-foreground leading-snug">
                  {isAr ? d.ar : d.en}
                </p>
              </motion.div>
            ))
          )}
        </div>
      </div>

      {/* Queues per OS */}
      <div>
        <p className="text-xs font-semibold text-foreground mb-2">
          {t("commandCenter.queuesTitle")}
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
          {queues.map((q) => (
            <QueuePanel
              key={q.key}
              titleKey={q.key}
              block={q.block}
              isAr={isAr}
            />
          ))}
        </div>
      </div>

      {/* Executive summary + compliance + blocked */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
        <div className="rounded-xl border border-border bg-muted/20 p-3">
          <p className="text-xs font-semibold text-foreground mb-2">
            {t("commandCenter.executiveSummary")}
          </p>
          <p className="text-2xl font-bold text-foreground tabular-nums">
            {data.executive_summary.total_items}
          </p>
          <p className="text-[11px] text-muted-foreground">
            {t("commandCenter.totalItems")}
          </p>
          <div className="mt-2 flex flex-wrap gap-1">
            {Object.entries(data.executive_summary.by_priority).map(
              ([prio, n]) => (
                <span
                  key={prio}
                  className="rounded-md bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground"
                >
                  {prio}: {n}
                </span>
              ),
            )}
          </div>
        </div>

        <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-3">
          <p className="flex items-center gap-1.5 text-xs font-semibold text-red-400 mb-2">
            <AlertOctagon className="w-3.5 h-3.5" />
            {t("commandCenter.complianceAlerts")}
          </p>
          <div className="flex gap-3">
            <div>
              <p className="text-xl font-bold text-red-400 tabular-nums">
                {data.compliance_alerts.count}
              </p>
              <p className="text-[10px] text-muted-foreground">
                {t("commandCenter.alerts")}
              </p>
            </div>
            <div>
              <p className="text-xl font-bold text-red-400 tabular-nums">
                {data.compliance_alerts.escalated}
              </p>
              <p className="text-[10px] text-muted-foreground">
                {t("commandCenter.escalated")}
              </p>
            </div>
          </div>
          <ul className="mt-2 space-y-1">
            {data.compliance_alerts.top_3.map((row, i) => (
              <li
                key={i}
                className="text-[11px] text-red-400/90 truncate"
              >
                {isAr ? row.ar : row.en}
              </li>
            ))}
          </ul>
        </div>

        <div className="rounded-xl border border-amber-500/20 bg-amber-500/5 p-3">
          <p className="flex items-center gap-1.5 text-xs font-semibold text-amber-400 mb-2">
            <Ban className="w-3.5 h-3.5" />
            {t("commandCenter.blockedActions")}
          </p>
          <p className="text-xl font-bold text-amber-400 tabular-nums">
            {data.blocked_actions.count}
          </p>
          <ul className="mt-2 space-y-1">
            {data.blocked_actions.first_3.map((row, i) => (
              <li
                key={i}
                className="text-[11px] text-amber-400/90 truncate"
              >
                {isAr ? row.ar : row.en}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Hard gates */}
      {data.hard_gates.length > 0 && (
        <div className="rounded-xl border border-border bg-muted/20 p-3">
          <p className="flex items-center gap-1.5 text-xs font-semibold text-foreground mb-2">
            <ShieldAlert className="w-3.5 h-3.5 text-red-400" />
            {t("commandCenter.hardGates")}
          </p>
          <div className="flex flex-wrap gap-1.5">
            {data.hard_gates.map((gate) => (
              <span
                key={gate}
                className="rounded-md bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground"
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
