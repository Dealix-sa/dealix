"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { api } from "@/lib/api";
import { AgentPyramid } from "./AgentPyramid";
import { AutonomousCycle } from "./AutonomousCycle";
import { ApprovalQueue } from "./ApprovalQueue";
import { CommandCenter } from "./CommandCenter";
import { StrategyBoard } from "./StrategyBoard";
import { StrategicCyclePanel } from "./StrategicCyclePanel";
import { DecisionLedger } from "./DecisionLedger";
import { GateBoard } from "./GateBoard";
import { CustomerSuccessPanel } from "./CustomerSuccessPanel";
import { FinancialDashboardPanel } from "./FinancialDashboardPanel";
import { BoardMemoViewer } from "./BoardMemoViewer";
import type {
  ApprovalCardItem,
  ApprovalsPendingResponse,
  CommandCenterResponse,
  CsCycleResponse,
  CycleResponse,
  FinancialCycleResponse,
  GateRuleItem,
  HierarchyResponse,
  StrategicCycleResponse,
  StrategicGatesResponse,
  StrategicTierResponse,
} from "./types";

function unwrap<T>(payload: unknown): T {
  // Backend responses may be wrapped in a { data: ... } envelope.
  if (
    payload &&
    typeof payload === "object" &&
    "data" in (payload as Record<string, unknown>)
  ) {
    return (payload as { data: T }).data;
  }
  return payload as T;
}

export function FullOpsConsole() {
  const t = useTranslations("fullOps");
  const locale = useLocale();
  const isAr = locale === "ar";

  const [hierarchy, setHierarchy] = useState<HierarchyResponse | null>(null);
  const [cycle, setCycle] = useState<CycleResponse | null>(null);
  const [commandCenter, setCommandCenter] =
    useState<CommandCenterResponse | null>(null);
  const [approvals, setApprovals] = useState<ApprovalCardItem[]>([]);

  const [strategicTier, setStrategicTier] =
    useState<StrategicTierResponse | null>(null);
  const [strategicCycle, setStrategicCycle] =
    useState<StrategicCycleResponse | null>(null);
  const [strategicGates, setStrategicGates] = useState<GateRuleItem[]>([]);

  const [loadingHierarchy, setLoadingHierarchy] = useState(true);
  const [loadingCycle, setLoadingCycle] = useState(true);
  const [loadingCommandCenter, setLoadingCommandCenter] = useState(true);
  const [loadingApprovals, setLoadingApprovals] = useState(true);
  const [running, setRunning] = useState(false);

  const [loadingStrategicTier, setLoadingStrategicTier] = useState(true);
  const [loadingStrategicCycle, setLoadingStrategicCycle] = useState(true);
  const [loadingStrategicGates, setLoadingStrategicGates] = useState(true);
  const [runningStrategic, setRunningStrategic] = useState(false);

  const [csCycle, setCsCycle] = useState<CsCycleResponse | null>(null);
  const [loadingCs, setLoadingCs] = useState(true);
  const [runningCs, setRunningCs] = useState(false);

  const [financialCycle, setFinancialCycle] =
    useState<FinancialCycleResponse | null>(null);
  const [loadingFinancial, setLoadingFinancial] = useState(true);
  const [runningFinancial, setRunningFinancial] = useState(false);

  const loadHierarchy = useCallback(async () => {
    setLoadingHierarchy(true);
    try {
      const res = await api.getFullOpsHierarchy();
      setHierarchy(unwrap<HierarchyResponse>(res.data));
    } catch {
      setHierarchy(null);
    } finally {
      setLoadingHierarchy(false);
    }
  }, []);

  const loadCycle = useCallback(async () => {
    setLoadingCycle(true);
    try {
      const res = await api.getFullOpsLatestCycle();
      const data = unwrap<CycleResponse | null>(res.data);
      setCycle(data && data.cycle_id ? data : null);
    } catch {
      setCycle(null);
    } finally {
      setLoadingCycle(false);
    }
  }, []);

  const loadCommandCenter = useCallback(async () => {
    setLoadingCommandCenter(true);
    try {
      const res = await api.getFullOpsCommandCenter();
      setCommandCenter(unwrap<CommandCenterResponse>(res.data));
    } catch {
      setCommandCenter(null);
    } finally {
      setLoadingCommandCenter(false);
    }
  }, []);

  const loadApprovals = useCallback(async () => {
    setLoadingApprovals(true);
    try {
      const res = await api.getApprovalsPending();
      const data = unwrap<ApprovalsPendingResponse>(res.data);
      const rows = data.cards ?? data.pending ?? [];
      setApprovals(Array.isArray(rows) ? rows : []);
    } catch {
      setApprovals([]);
    } finally {
      setLoadingApprovals(false);
    }
  }, []);

  const loadStrategicTier = useCallback(async () => {
    setLoadingStrategicTier(true);
    try {
      const res = await api.getStrategicTier();
      setStrategicTier(unwrap<StrategicTierResponse>(res.data));
    } catch {
      setStrategicTier(null);
    } finally {
      setLoadingStrategicTier(false);
    }
  }, []);

  const loadStrategicCycle = useCallback(async () => {
    setLoadingStrategicCycle(true);
    try {
      const res = await api.getStrategicLatest();
      const data = unwrap<StrategicCycleResponse | null>(res.data);
      setStrategicCycle(data && data.cycle_id ? data : null);
    } catch {
      setStrategicCycle(null);
    } finally {
      setLoadingStrategicCycle(false);
    }
  }, []);

  const loadStrategicGates = useCallback(async () => {
    setLoadingStrategicGates(true);
    try {
      const res = await api.getStrategicGates();
      const data = unwrap<StrategicGatesResponse>(res.data);
      setStrategicGates(Array.isArray(data?.gates) ? data.gates : []);
    } catch {
      setStrategicGates([]);
    } finally {
      setLoadingStrategicGates(false);
    }
  }, []);

  const loadCs = useCallback(async () => {
    setLoadingCs(true);
    try {
      const res = await api.getCustomerSuccessLatest();
      const data = unwrap<CsCycleResponse | null>(res.data);
      setCsCycle(data && data.cycle_id ? data : null);
    } catch {
      setCsCycle(null);
    } finally {
      setLoadingCs(false);
    }
  }, []);

  const loadFinancial = useCallback(async () => {
    setLoadingFinancial(true);
    try {
      const res = await api.getFinancialLatest();
      const data = unwrap<FinancialCycleResponse | null>(res.data);
      setFinancialCycle(data && !data.empty ? data : null);
    } catch {
      setFinancialCycle(null);
    } finally {
      setLoadingFinancial(false);
    }
  }, []);

  const loadAll = useCallback(() => {
    void loadStrategicTier();
    void loadStrategicCycle();
    void loadStrategicGates();
    void loadCs();
    void loadFinancial();
    void loadHierarchy();
    void loadCycle();
    void loadCommandCenter();
    void loadApprovals();
  }, [
    loadStrategicTier,
    loadStrategicCycle,
    loadStrategicGates,
    loadCs,
    loadFinancial,
    loadHierarchy,
    loadCycle,
    loadCommandCenter,
    loadApprovals,
  ]);

  useEffect(() => {
    loadAll();
  }, [loadAll]);

  const handleRunCycle = useCallback(async () => {
    setRunning(true);
    try {
      const res = await api.postFullOpsRunCycle();
      const data = unwrap<CycleResponse | null>(res.data);
      if (data && data.cycle_id) {
        setCycle(data);
      } else {
        await loadCycle();
      }
      toast.success(isAr ? "اكتملت دورة العمليات" : "Cycle completed");
      void loadApprovals();
      void loadCommandCenter();
    } catch {
      toast.error(isAr ? "فشل تشغيل الدورة" : "Cycle run failed");
    } finally {
      setRunning(false);
    }
  }, [isAr, loadCycle, loadApprovals, loadCommandCenter]);

  const handleRunCsCycle = useCallback(async () => {
    setRunningCs(true);
    try {
      const res = await api.postCustomerSuccessRunCycle();
      const data = unwrap<CsCycleResponse | null>(res.data);
      if (data && data.cycle_id) {
        setCsCycle(data);
      } else {
        await loadCs();
      }
      toast.success(isAr ? "اكتملت دورة نجاح العملاء" : "CS cycle completed");
      void loadApprovals();
    } catch {
      toast.error(
        isAr ? "فشل تشغيل دورة نجاح العملاء" : "CS cycle run failed",
      );
    } finally {
      setRunningCs(false);
    }
  }, [isAr, loadCs, loadApprovals]);

  const handleRunFinancialCycle = useCallback(async () => {
    setRunningFinancial(true);
    try {
      const res = await api.postFinancialRunCycle({ cadence: "weekly" });
      const data = unwrap<FinancialCycleResponse | null>(res.data);
      if (data && !data.empty) {
        setFinancialCycle(data);
      } else {
        await loadFinancial();
      }
      toast.success(isAr ? "اكتملت الدورة المالية" : "Financial cycle completed");
      void loadApprovals();
    } catch {
      toast.error(
        isAr ? "فشل تشغيل الدورة المالية" : "Financial cycle run failed",
      );
    } finally {
      setRunningFinancial(false);
    }
  }, [isAr, loadFinancial, loadApprovals]);

  const handleRunStrategicCycle = useCallback(async () => {
    setRunningStrategic(true);
    try {
      const res = await api.postStrategicRunCycle();
      const data = unwrap<StrategicCycleResponse | null>(res.data);
      if (data && data.cycle_id) {
        setStrategicCycle(data);
      } else {
        await loadStrategicCycle();
      }
      toast.success(
        isAr ? "اكتملت الدورة الاستراتيجية" : "Strategic cycle completed",
      );
      void loadApprovals();
    } catch {
      toast.error(
        isAr ? "فشل تشغيل الدورة الاستراتيجية" : "Strategic cycle run failed",
      );
    } finally {
      setRunningStrategic(false);
    }
  }, [isAr, loadStrategicCycle, loadApprovals]);

  const anyLoading =
    loadingHierarchy ||
    loadingCycle ||
    loadingCommandCenter ||
    loadingApprovals ||
    loadingStrategicTier ||
    loadingStrategicCycle ||
    loadingStrategicGates ||
    loadingCs ||
    loadingFinancial;

  return (
    <div className="space-y-6">
      <div className="flex justify-end">
        <Button
          variant="outline"
          size="sm"
          onClick={loadAll}
          disabled={anyLoading}
        >
          <RefreshCw
            className={cn("w-4 h-4 me-1.5", anyLoading && "animate-spin")}
          />
          {isAr ? "تحديث" : "Refresh"}
        </Button>
      </div>

      {/* Strategic Autonomy Layer - the CEO loop sits above Full Ops */}
      <div className="rounded-2xl border border-gold-500/20 bg-gold-500/[0.03] p-1">
        <p className="px-3 pt-2 pb-1 text-[11px] uppercase tracking-widest text-gold-400">
          {t("strategy.layerLabel")}
        </p>
        <div className="space-y-6 p-1">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base font-semibold">
                {t("strategy.sections.board")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <StrategyBoard
                data={strategicTier}
                loading={loadingStrategicTier}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base font-semibold">
                {t("strategy.sections.cycle")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <StrategicCyclePanel
                cycle={strategicCycle}
                loading={loadingStrategicCycle}
                running={runningStrategic}
                onRun={handleRunStrategicCycle}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base font-semibold">
                {t("strategy.sections.ledger")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DecisionLedger />
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base font-semibold">
                {t("strategy.sections.gates")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <GateBoard
                gates={strategicGates}
                loading={loadingStrategicGates}
              />
            </CardContent>
          </Card>
        </div>
      </div>

      {/* CS + Financial Autonomy — between Strategy and Full Ops */}
      <div className="rounded-2xl border border-blue-500/20 bg-blue-500/[0.03] p-1">
        <p className="px-3 pt-2 pb-1 text-[11px] uppercase tracking-widest text-blue-400">
          {t("cs.layerLabel")}
        </p>
        <div className="space-y-6 p-1">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base font-semibold">
                {t("cs.sectionTitle")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <CustomerSuccessPanel
                cycle={csCycle}
                loading={loadingCs}
                running={runningCs}
                onRun={handleRunCsCycle}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base font-semibold">
                {t("financial.sectionTitle")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <FinancialDashboardPanel
                cycle={financialCycle}
                loading={loadingFinancial}
                running={runningFinancial}
                onRun={handleRunFinancialCycle}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base font-semibold">
                {t("memo.sectionTitle")}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <BoardMemoViewer />
            </CardContent>
          </Card>
        </div>
      </div>

      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base font-semibold">
            {t("sections.pyramid")}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <AgentPyramid data={hierarchy} loading={loadingHierarchy} />
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base font-semibold">
            {t("sections.cycle")}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <AutonomousCycle
            cycle={cycle}
            loading={loadingCycle}
            running={running}
            onRun={handleRunCycle}
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-base font-semibold">
              {t("sections.queue")}
            </CardTitle>
            <span className="text-[11px] text-muted-foreground">
              {t("queue.humanTouchpoint")}
            </span>
          </div>
        </CardHeader>
        <CardContent>
          <ApprovalQueue
            items={approvals}
            loading={loadingApprovals}
            onChanged={loadApprovals}
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base font-semibold">
            {t("sections.commandCenter")}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <CommandCenter
            data={commandCenter}
            loading={loadingCommandCenter}
          />
        </CardContent>
      </Card>
    </div>
  );
}
