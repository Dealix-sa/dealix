"use client";

import { useCallback, useEffect, useState } from "react";
import { useTranslations, useLocale } from "next-intl";
import { RefreshCw } from "lucide-react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

interface PortalSection {
  title_ar?: string;
  title_en?: string;
  [key: string]: unknown;
}

interface PortalData {
  customer_handle: string;
  company_name: string | null;
  language_default: string;
  sections: Record<string, PortalSection>;
  promise_ar: string;
  promise_en: string;
}

export default function CustomerPortalPage() {
  const t = useTranslations("customerPortal");
  const locale = useLocale();
  const isAr = locale === "ar";
  const [handle, setHandle] = useState("Slot-A");
  const [data, setData] = useState<PortalData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getCustomerPortal(handle.trim() || "Slot-A");
      setData(res.data as PortalData);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "load_failed";
      setError(msg);
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [handle]);

  useEffect(() => {
    void load();
    // Initial load only — manual reload via the Load button afterwards.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const promise = data ? (isAr ? data.promise_ar : data.promise_en) : null;

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <div className="flex flex-wrap gap-3 items-end mb-6">
        <div className="flex flex-col gap-1">
          <label className="text-xs text-muted-foreground">{t("handleLabel")}</label>
          <Input
            value={handle}
            onChange={(e) => setHandle(e.target.value)}
            className="w-64"
          />
        </div>
        <Button onClick={() => void load()} disabled={loading}>
          <RefreshCw className={loading ? "w-4 h-4 me-1 animate-spin" : "w-4 h-4 me-1"} />
          {t("load")}
        </Button>
      </div>

      {loading && (
        <p className="text-sm text-muted-foreground">
          {isAr ? "جاري التحميل…" : "Loading…"}
        </p>
      )}

      {!loading && error && (
        <div className="rounded-xl border border-destructive/40 bg-destructive/10 p-4">
          <p className="text-sm font-medium text-destructive">
            {isAr ? "تعذّر تحميل بوابة العميل" : "Could not load the customer portal"}
          </p>
          <p className="text-xs text-muted-foreground mt-1">{error}</p>
          <Button
            variant="outline"
            size="sm"
            className="mt-3"
            onClick={() => void load()}
          >
            {isAr ? "إعادة المحاولة" : "Retry"}
          </Button>
        </div>
      )}

      {!loading && !error && data && (
        <div className="space-y-4">
          {promise && (
            <div className="rounded-xl border border-border p-4 bg-muted/20">
              <h3 className="text-sm font-semibold mb-2">{t("promiseTitle")}</h3>
              <p className="text-sm leading-relaxed">{promise}</p>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(data.sections).map(([key, section]) => (
              <div
                key={key}
                className="rounded-xl border border-border p-4 bg-card"
              >
                <h3 className="text-sm font-semibold mb-2">
                  {(isAr ? section.title_ar : section.title_en) || key}
                </h3>
                <pre className="text-xs text-muted-foreground bg-muted/40 rounded-lg p-3 overflow-auto max-h-56">
                  {JSON.stringify(section, null, 2)}
                </pre>
              </div>
            ))}
          </div>
        </div>
      )}
    </AppLayout>
  );
}
