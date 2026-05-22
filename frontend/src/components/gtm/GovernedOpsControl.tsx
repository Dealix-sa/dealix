"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";

type SchedulerStatus = {
  running?: boolean;
  hour_ksa?: number;
  next_run_utc?: string | null;
  last_run_at?: string | null;
  last_verdict?: string | null;
};

type GovEvent = {
  event_type?: string;
  occurred_at?: string;
  actor?: string;
  payload?: Record<string, unknown>;
};

/**
 * Founder control surface for the governed Full Ops loop (M11):
 * scheduler status + kill switch, run-day-now, and the governance log.
 */
export function GovernedOpsControl() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = useTranslations("ops.governed");
  const ts = useTranslations("ops.governed.scheduler");
  const tl = useTranslations("ops.governed.log");
  const [scheduler, setScheduler] = useState<SchedulerStatus | null>(null);
  const [events, setEvents] = useState<GovEvent[]>([]);
  const [blockedCount, setBlockedCount] = useState<number>(0);
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    if (!isOpsConfigured()) {
      setErr(opsMissingKeyMessage(isAr));
      setLoading(false);
      return;
    }
    const key = getAdminApiKey();
    setLoading(true);
    setErr("");
    try {
      const [schedRes, logRes, blockedRes] = await Promise.all([
        api.getSchedulerStatus(key),
        api.getGovernanceLog(key, 20),
        api.getGovernanceBlocked(key, 100),
      ]);
      setScheduler(schedRes.data as SchedulerStatus);
      setEvents(((logRes.data as { events?: GovEvent[] })?.events) ?? []);
      setBlockedCount(((blockedRes.data as { count?: number })?.count) ?? 0);
    } catch {
      setErr(t("loadFailed"));
    } finally {
      setLoading(false);
    }
  }, [isAr, t]);

  useEffect(() => {
    void load();
  }, [load]);

  const act = useCallback(
    async (fn: () => Promise<unknown>) => {
      setBusy(true);
      setErr("");
      try {
        await fn();
        await load();
      } catch {
        setErr(t("actionFailed"));
      } finally {
        setBusy(false);
      }
    },
    [t, load],
  );

  const running = scheduler?.running === true;

  return (
    <Card className="p-4 space-y-4">
      <div className="flex items-center justify-between gap-2">
        <h3 className="text-sm font-semibold">{t("title")}</h3>
        <Button variant="ghost" size="sm" onClick={() => void load()} disabled={loading}>
          {t("refresh")}
        </Button>
      </div>

      {err && <p className="text-xs text-destructive">{err}</p>}
      {loading && (
        <p className="text-xs text-muted-foreground">{t("loading")}</p>
      )}

      {!loading && !err && (
        <>
          {/* Scheduler + kill switch */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-xs">
              <span
                className={`px-2 py-0.5 rounded border ${
                  running
                    ? "border-emerald-500/40 text-emerald-700 dark:text-emerald-400"
                    : "border-muted text-muted-foreground"
                }`}
              >
                {running ? ts("running") : ts("stopped")}
              </span>
              {scheduler?.next_run_utc && (
                <span className="text-muted-foreground">
                  {ts("nextRun")}: {scheduler.next_run_utc}
                </span>
              )}
            </div>
            {scheduler?.last_verdict && (
              <p className="text-xs text-muted-foreground">
                {ts("lastDay")}:{" "}
                <span className="font-mono">{scheduler.last_verdict}</span>
                {scheduler.last_run_at ? ` · ${scheduler.last_run_at}` : ""}
              </p>
            )}
            <div className="flex flex-wrap gap-2">
              <Button
                size="sm"
                variant="outline"
                disabled={busy || running}
                onClick={() => void act(() => api.postSchedulerStart(getAdminApiKey()))}
              >
                {ts("start")}
              </Button>
              <Button
                size="sm"
                variant="destructive"
                disabled={busy || !running}
                onClick={() => void act(() => api.postSchedulerStop(getAdminApiKey()))}
              >
                {ts("stopKill")}
              </Button>
              <Button
                size="sm"
                variant="outline"
                disabled={busy}
                onClick={() => void act(() => api.postGovernedDayRun(getAdminApiKey()))}
              >
                {ts("runNow")}
              </Button>
            </div>
          </div>

          {/* Governance log */}
          <div>
            <p className="text-xs text-muted-foreground mb-1">
              {tl("title")}
              {blockedCount > 0 && (
                <span className="text-destructive">
                  {" "}
                  · {blockedCount} {tl("blockedSuffix")}
                </span>
              )}
            </p>
            {events.length === 0 ? (
              <p className="text-xs text-muted-foreground">{tl("empty")}</p>
            ) : (
              <ul className="space-y-1" role="list">
                {events.slice(0, 12).map((ev, i) => (
                  <li
                    key={`${ev.event_type ?? "ev"}-${i}`}
                    className="text-xs border rounded px-2 py-1"
                  >
                    <span className="font-mono">{ev.event_type ?? "—"}</span>
                    {ev.actor ? (
                      <span className="text-muted-foreground"> · {ev.actor}</span>
                    ) : null}
                    {ev.occurred_at ? (
                      <span className="text-muted-foreground"> · {ev.occurred_at}</span>
                    ) : null}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </>
      )}
    </Card>
  );
}
