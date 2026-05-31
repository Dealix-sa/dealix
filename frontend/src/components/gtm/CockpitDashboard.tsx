"use client";

import { useEffect, useState } from "react";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";

type Panel = {
  title_ar: string;
  title_en: string;
  primary: string;
  secondary?: string;
  estimate?: boolean;
};

type CockpitData = {
  revenue_today?: { count?: number; sar?: number; is_estimate?: boolean };
  mrr_current?: { active_subscriptions?: number; mrr_sar?: number };
  pending_approvals?: { count?: number };
  friction_top_7d?: Array<{ signal?: string; count?: number }>;
  agent_runs_24h?: { events_24h?: number };
  subscription_summary?: { due_count?: number; due_mrr_sar?: number };
  next_action_today?: { action_ar?: string; action_en?: string };
  red_lines?: Array<{
    code: string;
    severity: string;
    title_ar: string;
    title_en: string;
    suggested_action_ar: string;
    suggested_action_en: string;
  }>;
  generated_at?: string;
};

export function CockpitDashboard({ isAr }: { isAr: boolean }) {
  const [data, setData] = useState<CockpitData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      if (!isOpsConfigured()) {
        setError(opsMissingKeyMessage(isAr));
        setLoading(false);
        return;
      }
      try {
        const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const res = await fetch(`${base}/api/v1/founder/dashboard/cockpit`, {
          headers: { "X-API-Key": getAdminApiKey() },
          cache: "no-store",
        });
        if (!res.ok) {
          setError(
            isAr
              ? `فشل تحميل البيانات (${res.status})`
              : `Failed to load (${res.status})`,
          );
        } else {
          setData(await res.json());
        }
      } catch (e) {
        setError(isAr ? "خطأ في الاتصال" : "Connection error");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [isAr]);

  if (loading) {
    return (
      <p className="text-sm text-muted-foreground">
        {isAr ? "جاري التحميل..." : "Loading..."}
      </p>
    );
  }

  if (error) {
    return (
      <div className="rounded border border-amber-300 bg-amber-50 p-4 text-sm">
        <strong>{isAr ? "تنبيه: " : "Notice: "}</strong>
        {error}
      </div>
    );
  }

  if (!data) return null;

  const panels: Panel[] = [
    {
      title_ar: "إيرادات اليوم",
      title_en: "Revenue today",
      primary: `${data.revenue_today?.sar ?? 0} SAR`,
      secondary: `${data.revenue_today?.count ?? 0} ${isAr ? "معاملة" : "txns"}`,
      estimate: data.revenue_today?.is_estimate,
    },
    {
      title_ar: "MRR الحالي",
      title_en: "Current MRR",
      primary: `${data.mrr_current?.mrr_sar ?? 0} SAR`,
      secondary: `${data.mrr_current?.active_subscriptions ?? 0} ${isAr ? "اشتراك نشط" : "active subs"}`,
      estimate: true,
    },
    {
      title_ar: "موافقات معلّقة",
      title_en: "Pending approvals",
      primary: String(data.pending_approvals?.count ?? 0),
    },
    {
      title_ar: "إشارات friction (٧ أيام)",
      title_en: "Friction signals (7d)",
      primary: String(data.friction_top_7d?.length ?? 0),
      secondary: data.friction_top_7d?.[0]?.signal || "—",
    },
    {
      title_ar: "نشاط الأسطول (٢٤س)",
      title_en: "Fleet activity (24h)",
      primary: String(data.agent_runs_24h?.events_24h ?? 0),
      estimate: true,
    },
    {
      title_ar: "تجديدات مستحقة",
      title_en: "Renewals due",
      primary: `${data.subscription_summary?.due_count ?? 0}`,
      secondary: `${data.subscription_summary?.due_mrr_sar ?? 0} SAR`,
    },
    {
      title_ar: "الإجراء التالي",
      title_en: "Next action",
      primary: isAr
        ? data.next_action_today?.action_ar || "—"
        : data.next_action_today?.action_en || "—",
    },
  ];

  return (
    <div className="space-y-6">
      {data.red_lines && data.red_lines.length > 0 && (
        <div className="rounded border border-red-300 bg-red-50 p-4">
          <h2 className="mb-2 text-sm font-semibold text-red-900">
            {isAr ? "خطوط حمراء" : "Red lines"}
          </h2>
          <ul className="space-y-1 text-sm text-red-800">
            {data.red_lines.map((alert) => (
              <li key={alert.code}>
                <strong>{isAr ? alert.title_ar : alert.title_en}</strong> ·{" "}
                {isAr ? alert.suggested_action_ar : alert.suggested_action_en}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {panels.map((p, i) => (
          <article
            key={i}
            className="rounded-lg border bg-card p-4 shadow-sm"
            data-test={`cockpit-panel-${i}`}
          >
            <p className="text-xs uppercase tracking-wide text-muted-foreground">
              {isAr ? p.title_ar : p.title_en}
            </p>
            <p className="mt-2 text-2xl font-semibold">{p.primary}</p>
            {p.secondary && (
              <p className="mt-1 text-xs text-muted-foreground">{p.secondary}</p>
            )}
            {p.estimate && (
              <p className="mt-2 text-[10px] uppercase text-amber-600">
                {isAr ? "تقدير" : "estimate"}
              </p>
            )}
          </article>
        ))}
      </div>

      <p className="text-[10px] text-muted-foreground">
        {isAr ? "تم التحديث: " : "Updated: "}
        {data.generated_at}
      </p>
    </div>
  );
}
