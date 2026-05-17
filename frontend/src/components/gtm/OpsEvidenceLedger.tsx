"use client";

import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";

type EvRow = {
  event_type: string;
  summary: string;
  created_at?: string;
  entity_type?: string;
  entity_id?: string;
};

export function OpsEvidenceLedger() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const adminKey = getAdminApiKey();
  const [items, setItems] = useState<EvRow[]>([]);
  const [err, setErr] = useState("");

  useEffect(() => {
    if (!isOpsConfigured()) {
      setErr(opsMissingKeyMessage(isAr));
      return;
    }
    api
      .getEvidenceLedger(adminKey, 60)
      .then((r) => setItems((r.data as { items?: EvRow[] }).items ?? []))
      .catch(() => setErr(isAr ? "تعذّر تحميل الأدلة." : "Evidence load failed."));
  }, [adminKey, isAr]);

  return (
    <div className="space-y-4" dir={isAr ? "rtl" : "ltr"}>
      <p className="text-sm text-muted-foreground">
        {isAr ? "أحداث الأدلة الأخيرة — مسار التصريف." : "Recent evidence events — GTM trail."}
      </p>
      {err && <p className="text-destructive text-sm">{err}</p>}
      <div className="space-y-2 max-h-[60vh] overflow-auto">
        {items.map((ev, i) => (
          <Card key={`${ev.event_type}-${i}`} className="p-3 text-sm">
            <p className="font-mono text-xs text-primary">{ev.event_type}</p>
            <p className="mt-1">{ev.summary}</p>
            <p className="text-xs text-muted-foreground mt-1">
              {ev.entity_type}:{ev.entity_id} · {ev.created_at}
            </p>
          </Card>
        ))}
      </div>
    </div>
  );
}
