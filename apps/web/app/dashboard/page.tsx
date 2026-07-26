"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import {
  authenticatedFetch,
  clearSession,
  parseApiError,
} from "../../lib/runtime-api";

export default function DashboardEntryPage() {
  const router = useRouter();
  const [message, setMessage] = useState("جاري تحديد مساحة العمل...");

  useEffect(() => {
    let active = true;
    const resolveWorkspace = async () => {
      try {
        const response = await authenticatedFetch("/api/v1/auth/me");
        if (response.status === 401 || response.status === 403) {
          clearSession();
          router.replace("/login");
          return;
        }
        if (!response.ok) throw new Error(await parseApiError(response));
        const profile = await response.json();
        const workspace = String(profile.tenant_id || "").trim();
        if (!workspace) throw new Error("لا توجد مساحة عمل مرتبطة بالحساب");
        router.replace(`/${encodeURIComponent(workspace)}/dashboard`);
      } catch (error: unknown) {
        if (active) {
          setMessage(error instanceof Error ? error.message : "تعذر تحديد مساحة العمل");
        }
      }
    };

    void resolveWorkspace();
    return () => {
      active = false;
    };
  }, [router]);

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4" dir="rtl">
      <div className="bg-white rounded-xl border border-slate-200 p-6 text-center">
        <p className="text-slate-700">{message}</p>
      </div>
    </div>
  );
}
