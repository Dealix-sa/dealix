"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type AlertType = "payment" | "health" | "onboarding" | "report";
type AlertStatus = "pending" | "approved" | "dismissed";

interface FounderAlert {
  id: string;
  type: AlertType;
  title_ar: string;
  title_en: string;
  amount_sar?: number;
  customer_name?: string;
  created_at: string;
  status: AlertStatus;
  reviewed_by?: string;
}

type FilterStatus = "all" | AlertStatus;
type FilterType = "all" | AlertType;

// ---------------------------------------------------------------------------
// Alert type config
// ---------------------------------------------------------------------------

const TYPE_CONFIG: Record<AlertType, { label_ar: string; label_en: string; color: string }> = {
  payment: {
    label_ar: "دفع",
    label_en: "Payment",
    color: "bg-emerald-100 text-emerald-800 border-emerald-300",
  },
  health: {
    label_ar: "صحة",
    label_en: "Health",
    color: "bg-blue-100 text-blue-800 border-blue-300",
  },
  onboarding: {
    label_ar: "تأهيل",
    label_en: "Onboarding",
    color: "bg-purple-100 text-purple-800 border-purple-300",
  },
  report: {
    label_ar: "تقرير",
    label_en: "Report",
    color: "bg-amber-100 text-amber-800 border-amber-300",
  },
};

const STATUS_CONFIG: Record<AlertStatus, { label_ar: string; label_en: string; color: string }> = {
  pending: { label_ar: "معلّق", label_en: "Pending", color: "bg-orange-100 text-orange-800 border-orange-300" },
  approved: { label_ar: "موافق عليه", label_en: "Approved", color: "bg-green-100 text-green-800 border-green-300" },
  dismissed: { label_ar: "مُتجاهَل", label_en: "Dismissed", color: "bg-slate-100 text-slate-600 border-slate-300" },
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function timeAgo(isoString: string, isAr: boolean): string {
  const now = Date.now();
  const then = new Date(isoString).getTime();
  const diffMs = now - then;
  const diffMin = Math.floor(diffMs / 60_000);
  if (diffMin < 1) return isAr ? "الآن" : "just now";
  if (diffMin < 60) return isAr ? `منذ ${diffMin} د` : `${diffMin}m ago`;
  const diffH = Math.floor(diffMin / 60);
  if (diffH < 24) return isAr ? `منذ ${diffH} س` : `${diffH}h ago`;
  const diffD = Math.floor(diffH / 24);
  return isAr ? `منذ ${diffD} أيام` : `${diffD}d ago`;
}

// ---------------------------------------------------------------------------
// Skeleton
// ---------------------------------------------------------------------------

function AlertSkeleton() {
  return (
    <div className="space-y-3">
      {[1, 2, 3].map((i) => (
        <div key={i} className="h-24 rounded-lg bg-muted animate-pulse" />
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Alert card
// ---------------------------------------------------------------------------

function AlertCard({
  alert,
  isAr,
  onApprove,
  onDismiss,
}: {
  alert: FounderAlert;
  isAr: boolean;
  onApprove: (id: string) => void;
  onDismiss: (id: string) => void;
}) {
  const typeCfg = TYPE_CONFIG[alert.type];
  const statusCfg = STATUS_CONFIG[alert.status];
  const isPending = alert.status === "pending";

  return (
    <Card
      className={`p-4 transition-opacity ${
        alert.status === "dismissed" ? "opacity-60" : ""
      }`}
    >
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div className="flex items-start gap-3 flex-1 min-w-0">
          <div className="flex flex-col gap-1.5">
            <div className="flex items-center gap-2 flex-wrap">
              <Badge variant="outline" className={`text-xs ${typeCfg.color}`}>
                {isAr ? typeCfg.label_ar : typeCfg.label_en}
              </Badge>
              {!isPending && (
                <Badge variant="outline" className={`text-xs ${statusCfg.color}`}>
                  {isAr ? statusCfg.label_ar : statusCfg.label_en}
                </Badge>
              )}
            </div>
            <p className="font-semibold text-sm leading-snug">
              {isAr ? alert.title_ar : alert.title_en}
            </p>
            {alert.customer_name && (
              <p className="text-xs text-muted-foreground">{alert.customer_name}</p>
            )}
            {alert.amount_sar !== undefined && (
              <p className="text-sm font-bold text-[var(--dealix-deep-green)]">
                {alert.amount_sar.toLocaleString("ar-SA")} {isAr ? "ر.س" : "SAR"}
              </p>
            )}
          </div>
        </div>
        <div className="flex flex-col items-end gap-2">
          <span className="text-xs text-muted-foreground whitespace-nowrap">
            {timeAgo(alert.created_at, isAr)}
          </span>
          {isPending && (
            <div className="flex gap-2">
              <Button
                size="sm"
                className="bg-[var(--dealix-deep-green)] hover:bg-[var(--dealix-deep-green)]/90 text-white text-xs h-8"
                onClick={() => onApprove(alert.id)}
              >
                {isAr ? "موافقة وإرسال" : "Approve & Send"}
              </Button>
              <Button
                size="sm"
                variant="outline"
                className="text-xs h-8"
                onClick={() => onDismiss(alert.id)}
              >
                {isAr ? "تجاهل" : "Dismiss"}
              </Button>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
}

// ---------------------------------------------------------------------------
// Summary bar
// ---------------------------------------------------------------------------

function SummaryBar({
  alerts,
  isAr,
}: {
  alerts: FounderAlert[];
  isAr: boolean;
}) {
  const pendingCount = alerts.filter((a) => a.status === "pending").length;
  const approvedToday = alerts.filter((a) => {
    if (a.status !== "approved") return false;
    const d = new Date(a.created_at);
    const today = new Date();
    return d.toDateString() === today.toDateString();
  }).length;
  const dismissedToday = alerts.filter((a) => {
    if (a.status !== "dismissed") return false;
    const d = new Date(a.created_at);
    const today = new Date();
    return d.toDateString() === today.toDateString();
  }).length;

  return (
    <div className="grid grid-cols-3 gap-3 mb-6">
      <Card className="p-3 text-center border-orange-200 bg-orange-50 dark:bg-orange-950/20">
        <p className="text-2xl font-black text-orange-600">{pendingCount}</p>
        <p className="text-xs text-muted-foreground mt-0.5">
          {isAr ? "معلّق" : "Pending"}
        </p>
      </Card>
      <Card className="p-3 text-center border-green-200 bg-green-50 dark:bg-green-950/20">
        <p className="text-2xl font-black text-green-600">{approvedToday}</p>
        <p className="text-xs text-muted-foreground mt-0.5">
          {isAr ? "موافق عليه اليوم" : "Approved today"}
        </p>
      </Card>
      <Card className="p-3 text-center">
        <p className="text-2xl font-black text-muted-foreground">{dismissedToday}</p>
        <p className="text-xs text-muted-foreground mt-0.5">
          {isAr ? "مُتجاهَل اليوم" : "Dismissed today"}
        </p>
      </Card>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function FounderAlertCenter() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const adminKey = getAdminApiKey();

  const [alerts, setAlerts] = useState<FounderAlert[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [filterStatus, setFilterStatus] = useState<FilterStatus>("all");
  const [filterType, setFilterType] = useState<FilterType>("all");

  const fetchAlerts = useCallback(async () => {
    if (!isOpsConfigured()) {
      setError(opsMissingKeyMessage(isAr));
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE}/api/v1/founder/alerts`, {
        headers: { "X-Admin-API-Key": adminKey },
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = (await res.json()) as { alerts?: FounderAlert[] };
      setAlerts(data.alerts ?? []);
    } catch {
      setError(
        isAr
          ? "تعذّر تحميل التنبيهات — تحقق من مفتاح API."
          : "Could not load alerts — check your API key.",
      );
    } finally {
      setLoading(false);
    }
  }, [adminKey, isAr]);

  useEffect(() => {
    void fetchAlerts();
  }, [fetchAlerts]);

  const handleApprove = useCallback(
    async (id: string) => {
      try {
        await fetch(`${API_BASE}/api/v1/founder/alerts/${encodeURIComponent(id)}/approve`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Admin-API-Key": adminKey,
          },
        });
        setAlerts((prev) =>
          prev.map((a) => (a.id === id ? { ...a, status: "approved" as AlertStatus } : a)),
        );
      } catch {
        setError(isAr ? "فشل الإرسال." : "Approval failed.");
      }
    },
    [adminKey, isAr],
  );

  const handleDismiss = useCallback(
    async (id: string) => {
      try {
        await fetch(`${API_BASE}/api/v1/founder/alerts/${encodeURIComponent(id)}/dismiss`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Admin-API-Key": adminKey,
          },
        });
        setAlerts((prev) =>
          prev.map((a) => (a.id === id ? { ...a, status: "dismissed" as AlertStatus } : a)),
        );
      } catch {
        setError(isAr ? "فشل التجاهل." : "Dismiss failed.");
      }
    },
    [adminKey, isAr],
  );

  const filtered = alerts.filter((a) => {
    if (filterStatus !== "all" && a.status !== filterStatus) return false;
    if (filterType !== "all" && a.type !== filterType) return false;
    return true;
  });

  const filterStatusOptions: { value: FilterStatus; label_ar: string; label_en: string }[] = [
    { value: "all", label_ar: "الكل", label_en: "All" },
    { value: "pending", label_ar: "معلّق", label_en: "Pending" },
    { value: "approved", label_ar: "موافق عليه", label_en: "Approved" },
    { value: "dismissed", label_ar: "مُتجاهَل", label_en: "Dismissed" },
  ];

  const filterTypeOptions: { value: FilterType; label_ar: string; label_en: string }[] = [
    { value: "all", label_ar: "كل الأنواع", label_en: "All types" },
    { value: "payment", label_ar: "دفع", label_en: "Payment" },
    { value: "health", label_ar: "صحة", label_en: "Health" },
    { value: "onboarding", label_ar: "تأهيل", label_en: "Onboarding" },
    { value: "report", label_ar: "تقرير", label_en: "Report" },
  ];

  return (
    <div className="space-y-4" dir={isAr ? "rtl" : "ltr"}>
      <div>
        <h1 className="text-xl font-bold text-[var(--dealix-deep-green)]">
          {isAr ? "مركز تنبيهات المؤسس" : "Founder Alert Center"}
        </h1>
        <p className="text-xs text-muted-foreground mt-1">
          {isAr
            ? "لن يُرسَل أي شيء دون موافقة صريحة — APPROVAL_FIRST"
            : "Nothing is sent without explicit approval — APPROVAL_FIRST"}
        </p>
      </div>

      {error && (
        <div className="rounded-md border border-destructive/40 bg-destructive/5 px-4 py-3 text-sm text-destructive">
          {error}
        </div>
      )}

      <SummaryBar alerts={alerts} isAr={isAr} />

      {/* Filters */}
      <div className="flex flex-wrap gap-3 items-center">
        <div className="flex gap-1.5 flex-wrap">
          {filterStatusOptions.map((o) => (
            <button
              key={o.value}
              onClick={() => setFilterStatus(o.value)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-colors ${
                filterStatus === o.value
                  ? "bg-[var(--dealix-deep-green)] text-white border-[var(--dealix-deep-green)]"
                  : "border-border hover:border-[var(--dealix-deep-green)]/40"
              }`}
            >
              {isAr ? o.label_ar : o.label_en}
            </button>
          ))}
        </div>
        <div className="w-px h-4 bg-border hidden sm:block" />
        <div className="flex gap-1.5 flex-wrap">
          {filterTypeOptions.map((o) => (
            <button
              key={o.value}
              onClick={() => setFilterType(o.value)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-colors ${
                filterType === o.value
                  ? "bg-[var(--dealix-gold)]/20 border-[var(--dealix-gold)] text-[var(--dealix-gold)]"
                  : "border-border hover:border-[var(--dealix-gold)]/40"
              }`}
            >
              {isAr ? o.label_ar : o.label_en}
            </button>
          ))}
        </div>
        <Button
          variant="outline"
          size="sm"
          className="ms-auto text-xs"
          onClick={() => void fetchAlerts()}
          disabled={loading}
        >
          {loading ? (isAr ? "جاري التحميل..." : "Loading...") : (isAr ? "تحديث" : "Refresh")}
        </Button>
      </div>

      {/* Alert list */}
      {loading ? (
        <AlertSkeleton />
      ) : filtered.length === 0 ? (
        <Card className="p-10 text-center">
          <p className="text-lg font-semibold text-muted-foreground">
            {isAr ? "لا توجد تنبيهات" : "No alerts"}
          </p>
          <p className="text-sm text-muted-foreground mt-1">
            {isAr
              ? "جميع التنبيهات تمت مراجعتها أو لا توجد تنبيهات جديدة."
              : "All alerts have been reviewed or there are no new alerts."}
          </p>
        </Card>
      ) : (
        <div className="space-y-3">
          {filtered.map((alert) => (
            <AlertCard
              key={alert.id}
              alert={alert}
              isAr={isAr}
              onApprove={(id) => void handleApprove(id)}
              onDismiss={(id) => void handleDismiss(id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
