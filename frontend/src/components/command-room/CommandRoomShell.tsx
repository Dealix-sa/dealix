"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Progress } from "@/components/ui/progress";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";
import {
  Activity,
  AlertCircle,
  Briefcase,
  CheckCircle2,
  Clock,
  Mail,
  Megaphone,
  RefreshCw,
  ShieldAlert,
  Target,
  TrendingUp,
} from "lucide-react";

type TargetRow = {
  company?: string;
  channel?: string;
  next_action?: string;
  priority?: string;
  status?: string;
};

type ApprovalRow = {
  id?: string;
  title?: string;
  channel?: string;
  requested_by?: string;
};

type EvidenceRow = {
  event_type?: string;
  summary?: string;
  created_at?: string;
};

type SupportTicket = {
  id?: string;
  title?: string;
  status?: string;
  priority?: string;
};

type GmailDraft = {
  to_email?: string;
  subject?: string;
  company?: string;
};

type HealthPayload = {
  overall_status?: "healthy" | "degraded" | "unhealthy";
  kpis?: { key: string; value: number | null; computed: boolean }[];
};

type CockpitPayload = {
  cockpit_verdict?: string;
  cockpit_summary_ar?: string;
  next_actions_ar?: string[];
  automation_readiness?: Record<string, number>;
};

export function CommandRoomShell() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = useTranslations("commandRoom");
  const adminKey = getAdminApiKey();
  const configured = isOpsConfigured();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [lastRefresh, setLastRefresh] = useState<Date | null>(null);

  const [cockpit, setCockpit] = useState<CockpitPayload | null>(null);
  const [health, setHealth] = useState<HealthPayload | null>(null);
  const [warRoom, setWarRoom] = useState<TargetRow[]>([]);
  const [pipeline, setPipeline] = useState<Record<string, number>>({});
  const [approvals, setApprovals] = useState<ApprovalRow[]>([]);
  const [evidence, setEvidence] = useState<EvidenceRow[]>([]);
  const [gmailDrafts, setGmailDrafts] = useState<GmailDraft[]>([]);
  const [marketing, setMarketing] = useState<{ title_ar?: string; body_ar?: string } | null>(null);
  const [support, setSupport] = useState<SupportTicket[]>([]);

  const load = useCallback(async () => {
    if (!configured) {
      setError(opsMissingKeyMessage(isAr));
      return;
    }
    setLoading(true);
    setError("");
    try {
      const [
        cockpitRes,
        healthRes,
        warRoomRes,
        pipelineRes,
        approvalsRes,
        evidenceRes,
        gmailRes,
        marketingRes,
        supportRes,
      ] = await Promise.all([
        api.getFounderCockpit(adminKey, 10, "morning"),
        api.getFullOpsHealth(adminKey),
        api.getWarRoomTodayPack(adminKey),
        api.getSalesPipelineAutopilot(adminKey),
        api.getApprovalsPending(),
        api.getEvidenceLedger(adminKey, 10),
        api.getGmailDraftsToday(),
        api.getMarketingSocialToday(adminKey),
        api.getSupportTicketsAutopilot(adminKey, 10),
      ]);

      setCockpit(cockpitRes.data as CockpitPayload);
      setHealth(healthRes.data as HealthPayload);
      setWarRoom(
        ((warRoomRes.data as { targets?: { items?: TargetRow[] } })?.targets?.items) ?? [],
      );
      setPipeline(
        ((pipelineRes.data as { stages?: Record<string, number> })?.stages) ?? {},
      );
      setApprovals(
        ((approvalsRes.data as { approvals?: ApprovalRow[] })?.approvals) ?? [],
      );
      setEvidence(
        ((evidenceRes.data as { items?: EvidenceRow[] })?.items) ?? [],
      );
      setGmailDrafts(
        ((gmailRes.data as { drafts?: GmailDraft[] })?.drafts) ?? [],
      );
      setMarketing(
        (marketingRes.data as { title_ar?: string; body_ar?: string }) ?? null,
      );
      setSupport(
        ((supportRes.data as { items?: SupportTicket[] })?.items) ?? [],
      );
      setLastRefresh(new Date());
    } catch {
      setError(isAr ? t("error") : "Command room load failed.");
    } finally {
      setLoading(false);
    }
  }, [adminKey, configured, isAr, t]);

  useEffect(() => {
    load();
  }, [load]);

  const runMorning = async () => {
    if (!configured) return;
    setLoading(true);
    try {
      await api.postFounderCockpitRunMorning(adminKey, { run_optional_scripts: true });
      setTimeout(() => load(), 5000);
    } catch {
      setError(isAr ? t("error") : "Morning command failed.");
      setLoading(false);
    }
  };

  if (!configured) {
    return (
      <div className="p-6">
        <div className="rounded-lg border border-amber-500/30 bg-amber-500/10 p-4 text-amber-700 dark:text-amber-300">
          {opsMissingKeyMessage(isAr)}
        </div>
      </div>
    );
  }

  const readinessEntries = Object.entries(cockpit?.automation_readiness ?? {});
  const readinessAvg =
    readinessEntries.length > 0
      ? Math.round(
          readinessEntries.reduce((sum, [, v]) => sum + (Number(v) || 0), 0) /
            readinessEntries.length,
        )
      : 0;

  return (
    <div className="space-y-6 p-4 md:p-6" dir={isAr ? "rtl" : "ltr"}>
      <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">{t("title")}</h1>
          <p className="text-muted-foreground text-sm">{t("subtitle")}</p>
        </div>
        <div className="flex items-center gap-2">
          {lastRefresh && (
            <span className="text-xs text-muted-foreground">
              {isAr ? "آخر تحديث" : "Last refresh"}: {lastRefresh.toLocaleTimeString(locale)}
            </span>
          )}
          <Button variant="outline" size="sm" onClick={load} disabled={loading}>
            <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
          </Button>
          <Button size="sm" onClick={runMorning} disabled={loading}>
            {t("runMorning")}
          </Button>
        </div>
      </div>

      {error && (
        <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-4 text-red-700 dark:text-red-300">
          {error}
        </div>
      )}

      {/* Top decision row */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="md:col-span-2 border-l-4 border-l-gold-500">
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-base">
              <Target className="h-5 w-5 text-gold-500" />
              {t("todayDecision")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-lg font-semibold">
              {cockpit?.cockpit_verdict ?? (isAr ? "جاري التحميل..." : "Loading...")}
            </p>
            {cockpit?.cockpit_summary_ar && (
              <p className="mt-1 text-sm text-muted-foreground">{cockpit.cockpit_summary_ar}</p>
            )}
            {cockpit?.next_actions_ar && cockpit.next_actions_ar.length > 0 && (
              <ul className="mt-3 space-y-1">
                {cockpit.next_actions_ar.slice(0, 4).map((action, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <CheckCircle2 className="mt-0.5 h-4 w-4 text-emerald-500" />
                    <span>{action}</span>
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-base">
              <Activity className="h-5 w-5 text-blue-500" />
              {t("systemHealth")}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center gap-2">
              {health?.overall_status === "healthy" ? (
                <CheckCircle2 className="h-5 w-5 text-emerald-500" />
              ) : (
                <AlertCircle className="h-5 w-5 text-amber-500" />
              )}
              <span className="font-medium uppercase">{health?.overall_status ?? "—"}</span>
            </div>
            {readinessEntries.length > 0 && (
              <>
                <div className="flex items-center justify-between text-sm">
                  <span>{isAr ? "جاهزية الأتمتة" : "Automation readiness"}</span>
                  <span>{readinessAvg}%</span>
                </div>
                <Progress value={readinessAvg} className="h-2" />
              </>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Main grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-base">
              <Briefcase className="h-4 w-4" />
              {t("warRoom")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {warRoom.length === 0 ? (
              <p className="text-sm text-muted-foreground">{isAr ? "لا أهداف اليوم" : "No targets today"}</p>
            ) : (
              <ul className="space-y-2">
                {warRoom.slice(0, 6).map((t, i) => (
                  <li key={i} className="rounded-md bg-muted/50 p-2 text-sm">
                    <div className="flex items-center justify-between">
                      <span className="font-medium">{t.company}</span>
                      <Badge variant="outline">{t.priority}</Badge>
                    </div>
                    <div className="mt-1 text-xs text-muted-foreground">{t.next_action}</div>
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-base">
              <TrendingUp className="h-4 w-4" />
              {t("pipeline")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {Object.keys(pipeline).length === 0 ? (
              <p className="text-sm text-muted-foreground">{isAr ? "لا بيانات" : "No data"}</p>
            ) : (
              <div className="space-y-2">
                {Object.entries(pipeline).map(([stage, count]) => (
                  <div key={stage} className="flex items-center justify-between text-sm">
                    <span className="capitalize">{stage.replace(/_/g, " ")}</span>
                    <span className="font-semibold">{count}</span>
                  </div>
                ))}
                <Separator />
                <div className="flex items-center justify-between font-semibold">
                  <span>{isAr ? "المجموع" : "Total"}</span>
                  <span>{Object.values(pipeline).reduce((a, b) => a + (Number(b) || 0), 0)}</span>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-base">
              <Clock className="h-4 w-4" />
              {t("approvals")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {approvals.length === 0 ? (
              <p className="text-sm text-muted-foreground">{isAr ? "لا موافقات معلقة" : "No pending approvals"}</p>
            ) : (
              <ul className="space-y-2">
                {approvals.slice(0, 5).map((a, i) => (
                  <li key={i} className="text-sm">
                    <div className="font-medium">{a.title ?? a.id}</div>
                    <div className="text-xs text-muted-foreground">{a.channel}</div>
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-base">
              <CheckCircle2 className="h-4 w-4" />
              {t("evidence")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {evidence.length === 0 ? (
              <p className="text-sm text-muted-foreground">{isAr ? "لا أدلة مسجلة" : "No evidence yet"}</p>
            ) : (
              <ul className="space-y-2">
                {evidence.slice(0, 5).map((e, i) => (
                  <li key={i} className="text-sm">
                    <Badge variant="secondary" className="mb-1">{e.event_type}</Badge>
                    <div className="text-xs text-muted-foreground line-clamp-2">{e.summary}</div>
                  </li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-base">
              <Mail className="h-4 w-4" />
              {t("gmailDrafts")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {gmailDrafts.length === 0 ? (
              <p className="text-sm text-muted-foreground">{isAr ? "لا drafts اليوم" : "No drafts today"}</p>
            ) : (
              <>
                <div className="mb-2 text-sm font-semibold">
                  {gmailDrafts.length} {isAr ? "مسودة" : "drafts"}
                </div>
                <ul className="space-y-2">
                  {gmailDrafts.slice(0, 4).map((d, i) => (
                    <li key={i} className="text-sm">
                      <div className="font-medium">{d.company ?? d.to_email}</div>
                      <div className="text-xs text-muted-foreground line-clamp-1">{d.subject}</div>
                    </li>
                  ))}
                </ul>
              </>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-base">
              <Megaphone className="h-4 w-4" />
              {t("marketing")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {marketing?.title_ar ? (
              <>
                <div className="font-medium">{marketing.title_ar}</div>
                <p className="mt-1 text-xs text-muted-foreground line-clamp-4">
                  {marketing.body_ar}
                </p>
              </>
            ) : (
              <p className="text-sm text-muted-foreground">{isAr ? "لا محتوى اليوم" : "No content today"}</p>
            )}
          </CardContent>
        </Card>

        <Card className="md:col-span-2 lg:col-span-3">
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-base">
              <ShieldAlert className="h-4 w-4" />
              {t("support")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {support.length === 0 ? (
              <p className="text-sm text-muted-foreground">{isAr ? "لا تذاكر مفتوحة" : "No open tickets"}</p>
            ) : (
              <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
                {support.slice(0, 8).map((s, i) => (
                  <div key={i} className="rounded-md bg-muted/50 p-2 text-sm">
                    <div className="font-medium">{s.title ?? s.id}</div>
                    <div className="flex items-center gap-2 mt-1 text-xs text-muted-foreground">
                      <span>{s.status}</span>
                      <span>·</span>
                      <span>{s.priority}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
