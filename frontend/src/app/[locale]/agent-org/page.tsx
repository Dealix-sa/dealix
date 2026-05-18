"use client";

import { useCallback, useEffect, useState } from "react";
import { useTranslations, useLocale } from "next-intl";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";

type Role = {
  id: string;
  name_ar: string;
  name_en: string;
  tier: number;
  tier_label: string;
  mission_ar: string;
  mission_en: string;
  autonomy_label: string;
  produces_external: boolean;
};

type Director = Role & { directs: Role[] };
type OrgChart = {
  chief: Role & { directs: Director[] };
  headcount: number;
  tiers: { chief: number; directors: number; operators: number };
};

type WorkItem = {
  id: string;
  agent_name_en: string;
  kind: string;
  title_ar: string;
  title_en: string;
  summary: string;
  external: boolean;
  status: string;
};

type CycleReport = {
  cycle_id: string;
  run_date: string;
  agents_run: number;
  items_total: number;
  items_pending_approval: number;
  items_internal: number;
  escalations: string[];
  founder_brief_ar: string;
  founder_brief_en: string;
  work_items: WorkItem[];
};

export default function AgentOrgPage() {
  const t = useTranslations("agentOrg");
  const locale = useLocale();
  const isAr = locale === "ar";

  const [chart, setChart] = useState<OrgChart | null>(null);
  const [report, setReport] = useState<CycleReport | null>(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getAgentOrgChart()
      .then((res) => setChart(res.data as OrgChart))
      .catch(() => setError("chart"));
  }, []);

  const runCycle = useCallback(async () => {
    setRunning(true);
    setError(null);
    try {
      const res = await api.runAgentOrgDailyCycle();
      setReport(res.data as CycleReport);
    } catch {
      setError("cycle");
    } finally {
      setRunning(false);
    }
  }, []);

  const name = (r: Role) => (isAr ? r.name_ar : r.name_en);
  const mission = (r: Role) => (isAr ? r.mission_ar : r.mission_en);

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <p className="text-xs text-muted-foreground mb-6 rounded-lg border border-border bg-muted/20 px-3 py-2">
        {t("hint")}
      </p>

      <div className="flex flex-wrap items-center gap-4 mb-8">
        <Button onClick={() => void runCycle()} disabled={running}>
          {running ? t("running") : t("runCycle")}
        </Button>
        {chart && (
          <span className="text-sm text-muted-foreground">
            {chart.headcount} {t("headcount")} · {chart.tiers.directors}{" "}
            {t("director")} · {chart.tiers.operators} {t("operator")}
          </span>
        )}
      </div>

      {report && (
        <section className="mb-10 space-y-4">
          <div className="rounded-xl border border-border bg-card/40 p-5">
            <h3 className="text-sm font-semibold mb-2">{t("founderBrief")}</h3>
            <p className="text-sm leading-relaxed">
              {isAr ? report.founder_brief_ar : report.founder_brief_en}
            </p>
          </div>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            <Stat label={t("headcount")} value={report.agents_run} />
            <Stat
              label={t("pendingApproval")}
              value={report.items_pending_approval}
              accent
            />
            <Stat label={t("internalDone")} value={report.items_internal} />
            <Stat label={t("escalations")} value={report.escalations.length} />
          </div>
          {report.escalations.length > 0 && (
            <ul className="space-y-1">
              {report.escalations.map((e) => (
                <li
                  key={e}
                  className="text-xs rounded-lg border border-amber-500/40 bg-amber-500/10 px-3 py-2"
                >
                  {e}
                </li>
              ))}
            </ul>
          )}
          <div>
            <h3 className="text-sm font-semibold mb-3">{t("workItems")}</h3>
            <ul className="space-y-2">
              {report.work_items.map((w) => (
                <li
                  key={w.id}
                  className="rounded-lg border border-border bg-card/30 px-4 py-3"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <p className="text-sm font-medium">
                        {isAr ? w.title_ar : w.title_en}
                      </p>
                      <p className="text-xs text-muted-foreground mt-0.5">
                        {w.agent_name_en} · {w.summary}
                      </p>
                    </div>
                    <span
                      className={
                        "shrink-0 rounded-full px-2 py-0.5 text-[10px] font-medium " +
                        (w.external
                          ? "bg-amber-500/15 text-amber-600 dark:text-amber-400"
                          : "bg-emerald-500/15 text-emerald-600 dark:text-emerald-400")
                      }
                    >
                      {w.external ? t("external") : t("internal")}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}

      {chart && (
        <section className="space-y-6">
          <RoleCard role={chart.chief} name={name(chart.chief)} mission={mission(chart.chief)} />
          <div className="grid gap-6 lg:grid-cols-2">
            {chart.chief.directs.map((d) => (
              <div
                key={d.id}
                className="rounded-xl border border-border bg-card/30 p-4"
              >
                <RoleCard role={d} name={name(d)} mission={mission(d)} />
                <ul className="mt-3 space-y-2 border-t border-border pt-3">
                  {d.directs.map((op) => (
                    <li key={op.id} className="text-sm">
                      <span className="font-medium">{name(op)}</span>
                      <span className="text-muted-foreground"> — {mission(op)}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>
      )}

      {error && (
        <p className="mt-4 text-sm text-destructive">
          {error === "chart"
            ? "Could not load the org chart."
            : "Could not run the daily cycle."}
        </p>
      )}
    </AppLayout>
  );
}

function Stat({
  label,
  value,
  accent,
}: {
  label: string;
  value: number;
  accent?: boolean;
}) {
  return (
    <div className="rounded-xl border border-border bg-card/40 p-4">
      <p
        className={
          "text-2xl font-bold " + (accent ? "text-amber-600 dark:text-amber-400" : "")
        }
      >
        {value}
      </p>
      <p className="text-xs text-muted-foreground mt-1">{label}</p>
    </div>
  );
}

function RoleCard({
  role,
  name,
  mission,
}: {
  role: Role;
  name: string;
  mission: string;
}) {
  return (
    <div>
      <div className="flex items-center gap-2">
        <h3 className="text-base font-semibold">{name}</h3>
        <span className="rounded-full bg-muted px-2 py-0.5 text-[10px] uppercase tracking-wide text-muted-foreground">
          {role.tier_label}
        </span>
        <span className="rounded-full bg-muted px-2 py-0.5 text-[10px] text-muted-foreground">
          {role.autonomy_label}
        </span>
      </div>
      <p className="text-sm text-muted-foreground mt-1">{mission}</p>
    </div>
  );
}
