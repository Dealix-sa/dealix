"use client";

import { useState, useEffect, useCallback } from "react";
import { useTranslations, useLocale } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import { Filter } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn, formatRelativeTime, getStatusColor } from "@/lib/utils";
import { api } from "@/lib/api";
import type { AgentActivity, AgentType, AgentStatus } from "@/types";

const POLL_INTERVAL_MS = 15000;

interface RosterAgent {
  agent_id: string;
  name: string;
  autonomy_level: number;
  capability_tags: string[];
  registered: boolean;
  status: string;
}

interface AgentPyramid {
  tier_1_chief: RosterAgent[];
  tier_2_operator: RosterAgent[];
  tier_3_tool: RosterAgent[];
  total_agents: number;
  max_autonomy_level: number;
  l5_forbidden: boolean;
}

// Map a capability tag to one of the 5 visual agent types the feed renders.
function capabilityToAgentType(tags: string[]): AgentType {
  const joined = tags.join(",");
  if (joined.includes("compliance")) return "compliance";
  if (joined.includes("growth")) return "outreach";
  if (joined.includes("sales") || joined.includes("executive")) return "scoring";
  if (
    joined.includes("self_improvement") ||
    joined.includes("delivery") ||
    joined.includes("customer_success")
  )
    return "intelligence";
  return "orchestrator";
}

// Roster status -> the AgentStatus the feed badges understand.
function rosterStatusToActivityStatus(status: string): AgentStatus {
  const s = status.toLowerCase();
  if (s === "active" || s === "running") return "running";
  if (s === "retired" || s === "failed" || s === "blocked") return "failed";
  if (s === "approved" || s === "completed") return "completed";
  return "pending";
}

// Convert the live Full-Ops agent pyramid into feed rows.
function pyramidToActivities(p: AgentPyramid, isAr: boolean): AgentActivity[] {
  const tiers: Array<{ agents: RosterAgent[]; tierAr: string; tierEn: string }> = [
    { agents: p.tier_1_chief ?? [], tierAr: "قائد", tierEn: "Chief" },
    { agents: p.tier_2_operator ?? [], tierAr: "مشغّل", tierEn: "Operator" },
    { agents: p.tier_3_tool ?? [], tierAr: "أداة", tierEn: "Tool" },
  ];
  const rows: AgentActivity[] = [];
  for (const { agents, tierAr, tierEn } of tiers) {
    for (const a of agents) {
      const tags = a.capability_tags ?? [];
      rows.push({
        id: a.agent_id,
        agentType: capabilityToAgentType(tags),
        action: isAr
          ? `وكيل ${tierAr} «${a.name}» — مستوى استقلالية L${a.autonomy_level}`
          : `${tierEn} agent "${a.name}" — autonomy L${a.autonomy_level}`,
        target: tags.length > 0 ? tags.join(", ") : isAr ? "بدون وسوم قدرات" : "no capability tags",
        status: rosterStatusToActivityStatus(a.status),
        timestamp: new Date().toISOString(),
        requiresApproval: a.autonomy_level >= 4,
      });
    }
  }
  return rows;
}

const agentIcons: Record<AgentType, string> = {
  outreach: "📤",
  scoring: "📊",
  compliance: "🛡️",
  intelligence: "🔍",
  orchestrator: "⚙️",
};

const agentColors: Record<AgentType, string> = {
  outreach: "bg-blue-500/10 text-blue-400",
  scoring: "bg-gold-500/10 text-gold-400",
  compliance: "bg-purple-500/10 text-purple-400",
  intelligence: "bg-emerald-500/10 text-emerald-400",
  orchestrator: "bg-orange-500/10 text-orange-400",
};

interface ActivityItemProps {
  activity: AgentActivity;
  index: number;
}

function ActivityItem({ activity, index }: ActivityItemProps) {
  const t = useTranslations("agents");
  const locale = useLocale();
  const isAr = locale === "ar";

  return (
    <motion.div
      initial={{ opacity: 0, x: isAr ? 20 : -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.05 }}
      className="flex items-start gap-4 p-4 rounded-xl hover:bg-muted/30 transition-colors border border-transparent hover:border-border/50 group"
    >
      {/* Agent icon */}
      <div className={cn("w-10 h-10 rounded-xl flex items-center justify-center text-lg flex-shrink-0", agentColors[activity.agentType])}>
        {agentIcons[activity.agentType]}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <span className={cn("text-xs font-semibold px-2 py-0.5 rounded-full", agentColors[activity.agentType])}>
            {t(`agentTypes.${activity.agentType}` as "agentTypes.outreach")}
          </span>
          {activity.requiresApproval && (
            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-gold-500/10 text-gold-400 border border-gold-500/20 font-medium">
              {isAr ? "يتطلب موافقة" : "Needs Approval"}
            </span>
          )}
        </div>
        <p className="text-sm text-foreground mb-1">{activity.action}</p>
        <p className="text-xs text-muted-foreground">
          {isAr ? "الهدف:" : "Target:"} {activity.target}
        </p>
        {activity.duration && (
          <p className="text-[10px] text-muted-foreground/60 mt-1">
            {isAr ? "المدة:" : "Duration:"} {(activity.duration / 1000).toFixed(1)}s
          </p>
        )}
      </div>

      {/* Status & time */}
      <div className="flex flex-col items-end gap-1.5 flex-shrink-0">
        <Badge
          variant="outline"
          className={cn("text-[10px] px-2 py-0.5 h-5", getStatusColor(activity.status))}
        >
          {t(`status.${activity.status}` as "status.running")}
        </Badge>
        <span className="text-[10px] text-muted-foreground">
          {formatRelativeTime(activity.timestamp, locale)}
        </span>
      </div>
    </motion.div>
  );
}

// Stats card — derives counts from the live activity rows.
function AgentStats({ activities }: { activities: AgentActivity[] }) {
  const locale = useLocale();
  const isAr = locale === "ar";

  const count = (s: AgentStatus) => activities.filter((a) => a.status === s).length;

  const stats = [
    { label: isAr ? "يعمل" : "Running", value: count("running"), color: "text-blue-400", bg: "bg-blue-400/10" },
    { label: isAr ? "مكتمل" : "Completed", value: count("completed"), color: "text-emerald-400", bg: "bg-emerald-400/10" },
    { label: isAr ? "قيد الانتظار" : "Pending", value: count("pending"), color: "text-gold-400", bg: "bg-gold-400/10" },
    { label: isAr ? "فشل" : "Failed", value: count("failed"), color: "text-red-400", bg: "bg-red-400/10" },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
      {stats.map((stat, i) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.07 }}
          className={cn("rounded-xl p-4 border border-border", stat.bg)}
        >
          <p className={cn("text-2xl font-bold tabular-nums", stat.color)}>{stat.value}</p>
          <p className="text-xs text-muted-foreground mt-1">{stat.label}</p>
        </motion.div>
      ))}
    </div>
  );
}

export function ActivityFeed() {
  const t = useTranslations("agents");
  const locale = useLocale();
  const isAr = locale === "ar";
  const [activities, setActivities] = useState<AgentActivity[]>([]);
  const [isLive, setIsLive] = useState(true);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      const res = await api.getAgentActivity();
      const data = res.data as { pyramid?: AgentPyramid } | undefined;
      const pyramid = data?.pyramid;
      if (pyramid) {
        setActivities(pyramidToActivities(pyramid, isAr));
        setError(null);
      }
    } catch {
      setError(isAr ? "تعذر تحميل نشاط الوكلاء من الخادم" : "Could not load agent activity from API");
    } finally {
      setLoading(false);
    }
  }, [isAr]);

  useEffect(() => {
    void load();
  }, [load]);

  // Poll the live agent pyramid while in Live mode.
  useEffect(() => {
    if (!isLive) return;
    const interval = setInterval(() => {
      void load();
    }, POLL_INTERVAL_MS);
    return () => clearInterval(interval);
  }, [isLive, load]);

  return (
    <div>
      <AgentStats activities={activities} />
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-base font-semibold">{t("title")}</CardTitle>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setIsLive(!isLive)}
                className={cn(
                  "flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full border transition-colors",
                  isLive
                    ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                    : "bg-muted text-muted-foreground border-border"
                )}
              >
                <span className={cn("w-1.5 h-1.5 rounded-full", isLive ? "bg-emerald-400 animate-pulse" : "bg-muted-foreground")} />
                {isLive ? (isAr ? "مباشر" : "Live") : (isAr ? "متوقف" : "Paused")}
              </button>
              <Button variant="outline" size="sm">
                <Filter className="w-3.5 h-3.5 me-1.5" />
                {isAr ? "تصفية" : "Filter"}
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <ScrollArea className="h-[calc(100vh-20rem)]">
            <div className="p-2">
              {loading ? (
                <p className="p-4 text-sm text-muted-foreground">
                  {isAr ? "جاري التحميل…" : "Loading…"}
                </p>
              ) : error ? (
                <p className="p-4 text-sm text-destructive">{error}</p>
              ) : activities.length === 0 ? (
                <p className="p-4 text-sm text-muted-foreground">
                  {isAr ? "لا يوجد نشاط وكلاء" : "No agent activity"}
                </p>
              ) : (
                <AnimatePresence>
                  {activities.map((activity, i) => (
                    <ActivityItem key={activity.id} activity={activity} index={i} />
                  ))}
                </AnimatePresence>
              )}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}
