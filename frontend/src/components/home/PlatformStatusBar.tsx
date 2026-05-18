"use client";

import { useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { Activity, AlertCircle, CheckCircle2 } from "lucide-react";
import {
  fetchHealthz,
  fetchVersion,
  getApiBase,
  type HealthzPayload,
} from "@/lib/public-api";
import { cn } from "@/lib/utils";

export function PlatformStatusBar() {
  const t = useTranslations("public.status");
  const locale = useLocale();
  const isRTL = locale === "ar";
  const [health, setHealth] = useState<HealthzPayload | null>(null);
  const [versionStatus, setVersionStatus] = useState<"ok" | "missing" | "loading">(
    "loading",
  );
  const [versionLabel, setVersionLabel] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      const [hz, ver] = await Promise.all([fetchHealthz(), fetchVersion()]);
      if (cancelled) return;
      if (hz.ok && hz.data) setHealth(hz.data);
      if (ver.ok && ver.data?.version) {
        setVersionStatus("ok");
        setVersionLabel(ver.data.version as string);
      } else {
        setVersionStatus("missing");
        if (hz.data?.version) {
          setVersionLabel(String(hz.data.version));
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const apiOk = health?.status === "ok";
  const apiBase = getApiBase();

  return (
    <div
      className={cn(
        "border-b border-border/40 px-4 py-1.5 text-[11px]",
        apiOk ? "bg-secondary/10" : "bg-destructive/10",
        isRTL && "text-right",
      )}
      dir={isRTL ? "rtl" : "ltr"}
      role="status"
    >
      <div className="page-container flex flex-wrap items-center justify-center gap-x-4 gap-y-1">
        <span className="inline-flex items-center gap-1.5 text-muted-foreground">
          <Activity className="w-3 h-3 text-primary" aria-hidden />
          <span className="font-mono opacity-80">{apiBase}</span>
        </span>
        <span className="inline-flex items-center gap-1">
          {apiOk ? (
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" aria-hidden />
          ) : (
            <AlertCircle className="w-3.5 h-3.5 text-destructive" aria-hidden />
          )}
          <span className={apiOk ? "text-emerald-600 dark:text-emerald-400" : "text-destructive"}>
            {apiOk ? t("apiLive") : t("apiDown")}
          </span>
        </span>
        {versionLabel && (
          <span className="text-muted-foreground">
            {t("version")}: <strong className="text-foreground">{versionLabel}</strong>
          </span>
        )}
        {versionStatus === "missing" && (
          <span className="text-amber-600 dark:text-amber-400">{t("versionPendingDeploy")}</span>
        )}
      </div>
    </div>
  );
}
