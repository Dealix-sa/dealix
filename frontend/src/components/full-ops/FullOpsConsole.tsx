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
import type {
  ApprovalCardItem,
  ApprovalsPendingResponse,
  CommandCenterResponse,
  CycleResponse,
  HierarchyResponse,
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

  const [loadingHierarchy, setLoadingHierarchy] = useState(true);
  const [loadingCycle, setLoadingCycle] = useState(true);
  const [loadingCommandCenter, setLoadingCommandCenter] = useState(true);
  const [loadingApprovals, setLoadingApprovals] = useState(true);
  const [running, setRunning] = useState(false);

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

  const loadAll = useCallback(() => {
    void loadHierarchy();
    void loadCycle();
    void loadCommandCenter();
    void loadApprovals();
  }, [loadHierarchy, loadCycle, loadCommandCenter, loadApprovals]);

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

  const anyLoading =
    loadingHierarchy ||
    loadingCycle ||
    loadingCommandCenter ||
    loadingApprovals;

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
