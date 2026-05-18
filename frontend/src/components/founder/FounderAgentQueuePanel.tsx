"use client";

import { useCallback, useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const ADMIN_KEY = process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || "";

type Task = {
  id: string;
  agent?: string;
  priority?: string;
  title_ar?: string;
  status?: string;
  approval_required?: boolean;
};

type QueuePayload = {
  date?: string;
  verdict?: string;
  stats?: { total?: number; pending?: number; done?: number };
  tasks?: Task[];
};

function headers(): HeadersInit {
  const h: HeadersInit = { "Content-Type": "application/json" };
  if (ADMIN_KEY) h["X-Admin-API-Key"] = ADMIN_KEY;
  return h;
}

export function FounderAgentQueuePanel() {
  const [data, setData] = useState<QueuePayload | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    if (!ADMIN_KEY) {
      setError("Set NEXT_PUBLIC_DEALIX_ADMIN_API_KEY in .env.local");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/v1/founder/agent-queue`, { headers: headers() });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setData(await res.json());
    } catch (e) {
      setError(e instanceof Error ? e.message : "load_failed");
    } finally {
      setLoading(false);
    }
  }, []);

  const seed = async () => {
    if (!ADMIN_KEY) return;
    setLoading(true);
    try {
      await fetch(`${API_BASE}/api/v1/founder/agent-queue/seed-today`, {
        method: "POST",
        headers: headers(),
      });
      await load();
    } finally {
      setLoading(false);
    }
  };

  const markDone = async (taskId: string) => {
    await fetch(`${API_BASE}/api/v1/founder/agent-queue/tasks/${taskId}`, {
      method: "PATCH",
      headers: headers(),
      body: JSON.stringify({ status: "done" }),
    });
    await load();
  };

  useEffect(() => {
    void load();
  }, [load]);

  const tasks = data?.tasks ?? [];

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between gap-2">
        <CardTitle className="text-lg">أسطول الوكلاء — مهام اليوم</CardTitle>
        <div className="flex gap-2">
          <Button type="button" variant="outline" size="sm" disabled={loading} onClick={() => void seed()}>
            حدّث اليوم
          </Button>
          <Button type="button" variant="ghost" size="sm" disabled={loading} onClick={() => void load()}>
            تحديث
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {error && <p className="text-sm text-destructive">{error}</p>}
        {data?.date && (
          <p className="text-sm text-muted-foreground">
            {data.date} · {data.verdict} · pending {data.stats?.pending ?? 0}/{data.stats?.total ?? 0}
          </p>
        )}
        <ul className="space-y-2">
          {tasks.map((t) => (
            <li
              key={t.id}
              className="flex flex-wrap items-center justify-between gap-2 rounded-md border p-2 text-sm"
            >
              <div>
                <Badge variant="outline" className="me-2">
                  {t.agent}
                </Badge>
                <span>{t.title_ar}</span>
                {t.approval_required && (
                  <Badge className="ms-2" variant="secondary">
                    موافقة
                  </Badge>
                )}
              </div>
              <div className="flex items-center gap-2">
                <Badge>{t.status}</Badge>
                {t.status !== "done" && (
                  <Button type="button" size="sm" variant="secondary" onClick={() => void markDone(t.id)}>
                    تم
                  </Button>
                )}
              </div>
            </li>
          ))}
        </ul>
        {!tasks.length && !error && <p className="text-sm text-muted-foreground">لا مهام — اضغط حدّث اليوم</p>}
      </CardContent>
    </Card>
  );
}
