"use client";

import { useState, useEffect, useCallback } from "react";
import { useLocale } from "next-intl";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

interface AgentRow {
  agent_id: string;
  name: string;
  tier: number;
  autonomy_level: number;
  registered: boolean;
  status: string;
}

interface StageResult {
  stage: string;
  stage_index: number;
  action_type: string;
  auto_executed: boolean;
  worker_agent: string;
  director_agent: string;
  approval_ticket_id: string | null;
  metrics: Record<string, unknown>;
}

interface RunView {
  run_id: string;
  customer_id: string;
  state: string;
  current_step: string | null;
}

interface ApprovalRow {
  ticket_id: string;
  action_type: string;
  state: string;
  description: string;
}

const TIER_LABEL: Record<number, [string, string]> = {
  0: ["المنسّق", "Conductor"],
  1: ["المدراء", "Directors"],
  2: ["العمّال المتخصّصون", "Specialist Workers"],
};

export function FullOpsConsole() {
  const isAr = useLocale() === "ar";
  const tr = (ar: string, en: string) => (isAr ? ar : en);

  const [agents, setAgents] = useState<AgentRow[]>([]);
  const [customerId, setCustomerId] = useState("");
  const [requestText, setRequestText] = useState("");
  const [run, setRun] = useState<RunView | null>(null);
  const [results, setResults] = useState<StageResult[]>([]);
  const [approvals, setApprovals] = useState<ApprovalRow[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getFullOpsAgents()
      .then((res) => setAgents((res.data?.agents as AgentRow[]) ?? []))
      .catch(() => setError(tr("تعذّر تحميل الأجينتس", "Could not load agents")));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const startRun = useCallback(async () => {
    if (!customerId.trim()) {
      setError(tr("أدخل معرّف العميل", "Enter a customer id"));
      return;
    }
    setBusy(true);
    setError(null);
    try {
      const created = await api.createFullOpsRun(customerId.trim(), {
        company_name: customerId.trim(),
        source: "full_ops_console",
        request_text: requestText.trim(),
      });
      const runId = created.data?.run?.run_id as string;
      const ran = await api.runAllFullOpsStages(runId);
      setRun(ran.data?.run as RunView);
      setResults((ran.data?.results as StageResult[]) ?? []);
      const appr = await api.getFullOpsRunApprovals(runId);
      setApprovals((appr.data?.pending_approvals as ApprovalRow[]) ?? []);
    } catch {
      setError(tr("فشل تشغيل الدورة", "The run failed"));
    } finally {
      setBusy(false);
    }
  }, [customerId, requestText, isAr]);

  const gatedCount = results.filter((r) => !r.auto_executed).length;
  const autoCount = results.length - gatedCount;

  return (
    <div className="space-y-6">
      {/* Start strip */}
      <Card>
        <CardHeader>
          <CardTitle>{tr("ابدأ دورة تشغيل", "Start a run")}</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap items-center gap-3">
          <Input
            placeholder={tr("معرّف العميل", "Customer id")}
            value={customerId}
            onChange={(e) => setCustomerId(e.target.value)}
            className="w-48"
          />
          <Input
            placeholder={tr("وصف الطلب (اختياري)", "Request text (optional)")}
            value={requestText}
            onChange={(e) => setRequestText(e.target.value)}
            className="flex-1 min-w-[220px]"
          />
          <Button variant="gold" onClick={startRun} disabled={busy}>
            {busy
              ? tr("جارٍ التشغيل…", "Running…")
              : tr("شغّل الدورة كاملة", "Start & run all")}
          </Button>
        </CardContent>
      </Card>

      {error && (
        <p className="text-sm text-red-400" role="alert">
          {error}
        </p>
      )}

      {/* Daily distribution summary */}
      {run && (
        <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
          <SummaryTile label={tr("الحالة", "State")} value={run.state} />
          <SummaryTile
            label={tr("مراحل مُنفّذة ذاتياً", "Auto-executed")}
            value={String(autoCount)}
          />
          <SummaryTile
            label={tr("بانتظار الموافقة", "Approval-gated")}
            value={String(gatedCount)}
          />
          <SummaryTile
            label={tr("إجمالي المراحل", "Stages run")}
            value={String(results.length)}
          />
        </div>
      )}

      {/* Pipeline board */}
      {results.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>{tr("لوحة المراحل (12)", "Pipeline board (12 stages)")}</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {results.map((r) => (
              <div
                key={r.stage}
                className="rounded-xl border border-border/60 p-3 space-y-2"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-semibold">
                    {r.stage_index}. {r.stage}
                  </span>
                  <Badge variant={r.auto_executed ? "emerald" : "gold"}>
                    {r.auto_executed
                      ? tr("ذاتي", "auto")
                      : tr("موافقة", "approval")}
                  </Badge>
                </div>
                <p className="text-xs text-muted-foreground">
                  {r.worker_agent} · {r.action_type}
                </p>
                <div className="flex flex-wrap gap-1">
                  {metricChips(r.metrics)}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Approval inbox */}
      {run && (
        <Card>
          <CardHeader>
            <CardTitle>
              {tr("صندوق الموافقات", "Approval inbox")} ({approvals.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {approvals.length === 0 && (
              <p className="text-sm text-muted-foreground">
                {tr("لا موافقات معلّقة", "No pending approvals")}
              </p>
            )}
            {approvals.map((a) => (
              <div
                key={a.ticket_id}
                className="flex items-center justify-between rounded-lg border border-border/60 p-3"
              >
                <div>
                  <p className="text-sm font-medium">{a.action_type}</p>
                  <p className="text-xs text-muted-foreground">{a.description}</p>
                </div>
                <Badge variant="gold">{a.state}</Badge>
              </div>
            ))}
            <p className="pt-1 text-xs text-muted-foreground">
              {tr(
                "الإرسال الخارجي يتطلّب موافقة المؤسس — لا إرسال تلقائي.",
                "External sends require founder approval — no auto-send.",
              )}
            </p>
          </CardContent>
        </Card>
      )}

      {/* Agent pyramid */}
      <Card>
        <CardHeader>
          <CardTitle>
            {tr("هرم الأجينتس", "Agent pyramid")} ({agents.length})
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {[0, 1, 2].map((tier) => {
            const rows = agents.filter((a) => a.tier === tier);
            if (rows.length === 0) return null;
            const [labelAr, labelEn] = TIER_LABEL[tier];
            return (
              <div key={tier} className="space-y-2">
                <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                  {tr(labelAr, labelEn)}
                </p>
                <div className="flex flex-wrap gap-2">
                  {rows.map((a) => (
                    <Badge
                      key={a.agent_id}
                      variant={a.registered ? "blue" : "outline"}
                    >
                      {a.name} · L{a.autonomy_level}
                    </Badge>
                  ))}
                </div>
              </div>
            );
          })}
        </CardContent>
      </Card>
    </div>
  );
}

function SummaryTile({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-border/60 p-4">
      <p className="text-xs text-muted-foreground">{label}</p>
      <p className="mt-1 text-lg font-bold">{value}</p>
    </div>
  );
}

function metricChips(metrics: Record<string, unknown>) {
  return Object.entries(metrics)
    .filter(([, v]) => ["string", "number", "boolean"].includes(typeof v))
    .slice(0, 4)
    .map(([k, v]) => (
      <span
        key={k}
        className="rounded bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground"
      >
        {k}: {String(v)}
      </span>
    ));
}
