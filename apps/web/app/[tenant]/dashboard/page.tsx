"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

import {
  authenticatedFetch,
  clearSession,
  parseApiError,
} from "../../../lib/runtime-api";

interface KPICard {
  label: string;
  label_ar: string;
  value: string | number;
  icon: string;
}

interface DashboardAction {
  id: string;
  label: string;
  label_ar?: string;
  href: string;
}

interface DashboardNotification {
  type: string;
  title: string;
  title_ar?: string;
  action?: {
    label: string;
    label_ar?: string;
    href: string;
  };
}

interface DashboardActivity {
  title: string;
  title_ar?: string;
  timestamp?: string | null;
}

interface DashboardData {
  tenant_name: string;
  plan_name: string;
  subscription_status: string;
  kpi_cards: KPICard[];
  quick_actions: DashboardAction[];
  recent_activity: DashboardActivity[];
  notifications: DashboardNotification[];
}

export default function DashboardPage() {
  const params = useParams();
  const router = useRouter();
  const tenant = String(params.tenant || "workspace");
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    const loadDashboard = async () => {
      try {
        const response = await authenticatedFetch("/api/v1/customer/dashboard/");
        if (response.status === 401 || response.status === 403) {
          clearSession();
          router.replace("/login");
          return;
        }
        if (!response.ok) throw new Error(await parseApiError(response));
        const payload: DashboardData = await response.json();
        if (active) setData(payload);
      } catch (err: unknown) {
        if (active) {
          setError(err instanceof Error ? err.message : "تعذر تحميل لوحة الشركة");
        }
      } finally {
        if (active) setLoading(false);
      }
    };

    void loadDashboard();
    return () => {
      active = false;
    };
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center" dir="rtl">
        <div className="text-emerald-600 text-xl font-semibold">جاري تحميل لوحة الشركة...</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4" dir="rtl">
        <div className="max-w-md bg-white rounded-xl border border-red-100 p-6 text-center">
          <p className="text-red-600 mb-4">{error || "تعذر تحميل بيانات الشركة"}</p>
          <button
            type="button"
            onClick={() => router.replace("/login")}
            className="px-4 py-2 bg-slate-900 text-white rounded-lg"
          >
            العودة لتسجيل الدخول
          </button>
        </div>
      </div>
    );
  }

  const iconMap: Record<string, string> = {
    users: "👥",
    briefcase: "💼",
    "trending-up": "📈",
    "check-circle": "✅",
    package: "📦",
  };

  const workspaceHref = (path: string) =>
    `/${encodeURIComponent(tenant)}${path.startsWith("/") ? path : `/${path}`}`;

  return (
    <div className="min-h-screen bg-slate-50" dir="rtl">
      <div className="flex">
        <aside className="w-64 bg-white border-l border-slate-200 min-h-screen p-6 hidden lg:block">
          <div className="text-2xl font-bold text-emerald-600 mb-2">Dealix</div>
          <p className="text-xs text-slate-400 mb-8">Saudi B2B AI Company OS</p>
          <nav className="space-y-2">
            {[
              { label: "الرئيسية", href: workspaceHref("/dashboard") },
              { label: "العملاء والفرص", href: workspaceHref("/crm") },
              { label: "المشاريع", href: workspaceHref("/projects") },
              { label: "الدعم", href: workspaceHref("/support") },
              { label: "المستندات", href: workspaceHref("/documents") },
              { label: "الإعدادات", href: workspaceHref("/settings/billing") },
            ].map((item) => (
              <a
                key={item.label}
                href={item.href}
                className="block px-4 py-2 rounded-lg text-slate-600 hover:bg-slate-100 hover:text-emerald-600 transition"
              >
                {item.label}
              </a>
            ))}
          </nav>
        </aside>

        <main className="flex-1 p-4 md:p-8">
          <header className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-2xl font-bold text-slate-900">
                مرحباً، {data.tenant_name}
              </h1>
              <p className="text-slate-500 text-sm">
                الخطة: {data.plan_name} —{" "}
                <span
                  className={`px-2 py-0.5 rounded text-xs font-medium ${
                    data.subscription_status === "active"
                      ? "bg-emerald-100 text-emerald-700"
                      : data.subscription_status === "trialing"
                        ? "bg-amber-100 text-amber-700"
                        : "bg-red-100 text-red-700"
                  }`}
                >
                  {data.subscription_status === "active"
                    ? "نشط"
                    : data.subscription_status === "trialing"
                      ? "تجريبي"
                      : data.subscription_status}
                </span>
              </p>
            </div>
          </header>

          {data.notifications.length > 0 && (
            <div className="mb-6 space-y-3">
              {data.notifications.map((notification, index) => (
                <div
                  key={`${notification.type}-${index}`}
                  className={`p-4 rounded-xl border-r-4 ${
                    notification.type === "warning"
                      ? "bg-amber-50 border-amber-500"
                      : "bg-red-50 border-red-500"
                  }`}
                >
                  <p className="font-semibold text-slate-800">
                    {notification.title_ar || notification.title}
                  </p>
                  {notification.action && (
                    <a
                      href={workspaceHref(notification.action.href)}
                      className="text-emerald-600 text-sm font-medium mt-1 inline-block hover:underline"
                    >
                      {notification.action.label_ar || notification.action.label} →
                    </a>
                  )}
                </div>
              ))}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-8">
            {data.kpi_cards.map((kpi, index) => (
              <div
                key={`${kpi.label}-${index}`}
                className="bg-white p-6 rounded-xl shadow-sm border border-slate-100"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-2xl" aria-hidden="true">{iconMap[kpi.icon] || "📊"}</span>
                </div>
                <p className="text-slate-500 text-sm">{kpi.label_ar}</p>
                <p className="text-2xl font-bold text-slate-900">{kpi.value}</p>
              </div>
            ))}
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 mb-8">
            <h2 className="text-lg font-bold text-slate-900 mb-4">إجراءات سريعة</h2>
            <div className="flex flex-wrap gap-3">
              {data.quick_actions.map((action) => (
                <a
                  key={action.id}
                  href={workspaceHref(action.href)}
                  className="px-4 py-2 bg-emerald-50 text-emerald-700 rounded-lg font-medium hover:bg-emerald-100 transition"
                >
                  {action.label_ar || action.label}
                </a>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
            <h2 className="text-lg font-bold text-slate-900 mb-4">آخر النشاطات</h2>
            {data.recent_activity.length === 0 ? (
              <p className="text-slate-400">لا توجد نشاطات حديثة</p>
            ) : (
              <div className="space-y-3">
                {data.recent_activity.map((activity, index) => (
                  <div
                    key={`${activity.title}-${index}`}
                    className="flex items-center justify-between p-3 bg-slate-50 rounded-lg"
                  >
                    <div>
                      <p className="font-medium text-slate-800">
                        {activity.title_ar || activity.title}
                      </p>
                      <p className="text-xs text-slate-400">
                        {activity.timestamp
                          ? new Date(activity.timestamp).toLocaleDateString("ar-SA")
                          : ""}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
