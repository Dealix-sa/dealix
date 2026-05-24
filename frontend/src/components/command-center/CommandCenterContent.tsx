"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

export function CommandCenterContent() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [data, setData] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    api.getCommandCenter().then((r) => setData(r.data as Record<string, unknown>));
  }, []);

  const decisions = (data?.today_top_3_decisions as string[]) || [];
  const actions = (data?.next_best_actions as string[]) || [];
  const gates = (data?.hard_gates || {}) as Record<string, boolean>;

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>{isAr ? "قرارات اليوم" : "Today's decisions"}</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="list-disc ps-5 text-sm space-y-2">
            {decisions.length ? (
              decisions.map((d) => <li key={d}>{d}</li>)
            ) : (
              <li className="text-muted-foreground">
                {isAr ? "لا قرارات بعد — شغّل الحلقة اليومية" : "No decisions yet — run daily loop"}
              </li>
            )}
          </ul>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>{isAr ? "أفضل إجراءات تالية" : "Next best actions"}</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="list-disc ps-5 text-sm space-y-2">
            {actions.map((a) => (
              <li key={a}>{a}</li>
            ))}
          </ul>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>{isAr ? "بوابات الأمان" : "Safety gates"}</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-2">
          {Object.entries(gates).map(([k, v]) => (
            <Badge key={k} variant={v ? "default" : "destructive"}>
              {k}
            </Badge>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
